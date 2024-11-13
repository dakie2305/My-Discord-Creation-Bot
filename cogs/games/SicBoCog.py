import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from enum import Enum
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomEnum.UserEnum as UserEnum
import CustomFunctions
import asyncio
import random
from discord.app_commands import Choice
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from datetime import datetime, timedelta

async def setup(bot: commands.Bot):
    await bot.add_cog(SicboCog(bot=bot))
    print("Sic Bo game is ready!")

class SicboCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    sb_group = discord.app_commands.Group(name="sb", description="Các lệnh liên quan đến Minigame tài xỉu!")
    
    #region tài xỉu normal
    @sb_group.command(name="normal", description="Tài xỉu phiên bản đơn giản hoá")
    @discord.app_commands.checks.cooldown(1, 5)
    @discord.app_commands.describe(tai_xiu="Chọn tài/xỉu.")
    @discord.app_commands.describe(so_tien="Chọn số tiền muốn cá cược.")
    @discord.app_commands.describe(loai_tien="Chọn loại tiền muốn cược.")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    @discord.app_commands.choices(tai_xiu=[
        Choice(name="Tài", value="tài"),
        Choice(name="Xỉu", value="xỉu"),
    ])
    async def sb_normal_slash_command(self, interaction: discord.Interaction, tai_xiu: str, so_tien:int = None, loai_tien:str = None):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if (so_tien != None and loai_tien == None):
            loai_tien = "C"
            
        if (so_tien == None and loai_tien != None):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Đã chọn loại tiền thì vui lòng chọn giá tiền cần cá cược!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
            
        profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if so_tien != None and profile == None:
            await interaction.followup.send(f"Để cá cược thì bạn phải thực hiện lệnh {SlashCommand.PROFILE.value} trước đã!")
            return
        elif so_tien != None and profile != None:
            if loai_tien == "C" and profile.copper < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.COPPER.value} để cá cược!")
                return
            elif loai_tien == "S" and profile.silver < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.SILVER.value} để cá cược!")
                return
            elif loai_tien == "G" and profile.gold < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.GOLD.value} để cá cược!")
                return
        if so_tien != None and so_tien <= 0:
            await interaction.followup.send(f"Số tiền nhập không hợp lệ!")
            return
        
        gambling_text = ""
        if so_tien != None and loai_tien != None:
            emoji = self.get_emoji_from_loai_tien(loai_tien=loai_tien)
            gambling_text = f" với tiền cược là **{so_tien}**{emoji}"
            
        embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã chơi tài xỉu và chọn **{tai_xiu}**{gambling_text}.\nNhà cái đã tung xúc xắc {EmojiCreation2.DICE_ROLLING.value} {EmojiCreation2.DICE_ROLLING.value}", color=0x03F8FC)
        mess = await interaction.followup.send(embed=embed)
        if mess:
            await self.edit_embed_sb_normal(message=mess, user=interaction.user, tai_xiu=tai_xiu, so_tien=so_tien, loai_tien=loai_tien, profile=profile)
        return
    
    @sb_normal_slash_command.error
    async def sb_normal_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    
    
    async def edit_embed_sb_normal(self, message: discord.Message, user: discord.Member, tai_xiu: str, so_tien:int = None, loai_tien:str = None, profile: Profile = None):
        first_num, first_dice_emoji = self.get_random_dice()
        second_num, second_dice_emoji = self.get_random_dice()
        third_num, third_dice_emoji = self.get_random_dice()
        count_all = first_num + second_num + third_num
        await asyncio.sleep(4)
        
        l_chance = self.get_chance(5)
        if l_chance:
            await self.police_in(message=message, user=user, so_tien=so_tien, loai_tien=loai_tien, profile=profile)
            return
            
        #Xỉu là 4-10
        #Tài là 11 - 17
        is_player_win = False
        
        if count_all >=4 and count_all<= 10 and tai_xiu == "xỉu":
            is_player_win = True
        elif count_all >= 11 and count_all<= 17 and tai_xiu == "tài":
            is_player_win = True
        
        #Triple là thua
        if first_num == second_num == third_num:
            is_player_win = False
        
        gambling_text = ""
        if so_tien != None:
            gambling_text = f" **{so_tien}** {self.get_emoji_from_loai_tien(loai_tien=loai_tien)}"
        
        chinh_quyen_text = ""
        if profile != None and profile.is_authority == False:
            chinh_quyen_text = "Chính quyền đã lấy một nửa số tiền cá cược để làm thuế!"
        if is_player_win == True:
            result_text = f"\n{user.mention} đã thắng{gambling_text}!"
        else:
            result_text = f"\n{user.mention} đã thua{gambling_text}! {chinh_quyen_text}"
            if first_num == second_num == third_num:
                result_text = f"\n{user.mention} đã thua{gambling_text} vì xúc xắc đều quay ra ba con giống nhau! {chinh_quyen_text}"
        embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã chơi tài xỉu và chọn **{tai_xiu}**{gambling_text}.\nXúc xắc đã quay ra: {first_dice_emoji} | {second_dice_emoji} | {third_dice_emoji} |\n{result_text}", color=0x03F8FC)
        
        if so_tien != None and loai_tien!= None and profile != None:
            if loai_tien == "G": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, gold=so_tien, loai_tien=loai_tien)
            elif loai_tien == "S": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, silver=so_tien, loai_tien=loai_tien)
            elif loai_tien == "C": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, copper=so_tien, loai_tien=loai_tien)

            
        await message.edit(embed=embed_updated)
        check_quest_message = QuestMongoManager.increase_sb_normal_count(guild_id=user.guild.id, user_id=user.id)
        if check_quest_message == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            ms = await message.channel.send(embed=quest_embed, content=f"{user.mention}", view=view)
            view.message = ms
        return
    
    def update_player_money_and_authority_money(self, is_player_win: bool, loai_tien: str, guild_int: int, profile: Profile, copper: int = 0, silver: int = 0, gold: int = 0):
        #Tính cộng trừ tiền cho player
        if is_player_win:
            #Cộng user, trừ authority
            ProfileMongoManager.update_profile_money(guild_id=guild_int, guild_name=profile.guild_name, user_id=profile.user_id, user_name=profile.user_name, user_display_name=profile.user_display_name, gold=gold, silver=silver, copper=copper)
            if profile != None and profile.is_authority == False:
                ProfileMongoManager.update_money_authority(guild_id=guild_int, silver=-silver, copper=-copper, gold=-gold)
            #Cộng exp
            if loai_tien == "C" and copper < 10000: return
            ProfileMongoManager.update_level_progressing(guild_id=guild_int, user_id=profile.user_id)
        else:
            #trừ một điểm dignity point
            ProfileMongoManager.update_dignity_point(guild_id=guild_int, guild_name=profile.guild_name, user_id=profile.user_id,user_name=profile.user_name, user_display_name=profile.user_display_name, dignity_point=-1)
            ProfileMongoManager.update_profile_money(guild_id=guild_int, guild_name=profile.guild_name, user_id=profile.user_id, user_name=profile.user_name, user_display_name=profile.user_display_name, gold=-gold, silver=-silver, copper=-copper)
            #Authority chỉ ăn 50%
            if profile != None and profile.is_authority == False:
                if loai_tien == "G":
                    ProfileMongoManager.update_money_authority(guild_id=guild_int, gold=int(gold/2) if int(gold/2)>0 else 1)
                elif loai_tien == "S":
                    ProfileMongoManager.update_money_authority(guild_id=guild_int, silver=int(silver/2) if int(silver/2)>0 else 1)
                elif loai_tien == "C":
                    ProfileMongoManager.update_money_authority(guild_id=guild_int, copper=int(copper/2) if int(copper/2)>0 else 1)
        
    
    async def police_in(self, message: discord.Message, user: discord.Member, so_tien:int = None, loai_tien:str = None, profile: Profile = None):
        #Công an ập vào
            lost_money_text = ""
            if so_tien != None:
                lost_money_text = f"{user.mention} cũng đã bị Chính Quyền tịch thu số tiền **{so_tien}** {self.get_emoji_from_loai_tien(loai_tien=loai_tien)}!"
            lose_embed = discord.Embed(title=f"", description=f"Công an đã ập vào để bắt quả tang {user.mention} vì tổ chức chơi đánh bạc tài xỉu và bị giam 30 phút!\n{lost_money_text}", color=0x03F8FC)
            await message.edit(embed=lose_embed)
            time_window = timedelta(minutes=30)
            jail_time = datetime.now() + time_window
            ProfileMongoManager.update_jail_time(guild_id=user.guild.id, user_id=user.id, jail_time=jail_time)
            if so_tien != None and loai_tien!= None and profile != None:
                if loai_tien == "G": self.update_player_money_and_authority_money(is_player_win=False, guild_int=user.guild.id, profile=profile, gold=so_tien*2, loai_tien=loai_tien)
                elif loai_tien == "S": self.update_player_money_and_authority_money(is_player_win=False, guild_int=user.guild.id, profile=profile, silver=so_tien*2, loai_tien=loai_tien)
                elif loai_tien == "C": self.update_player_money_and_authority_money(is_player_win=False, guild_int=user.guild.id, profile=profile, copper=so_tien*2, loai_tien=loai_tien)
            return

    
    #region tài xỉu double
    @sb_group.command(name="double", description="Tài xỉu Double!")
    @discord.app_commands.checks.cooldown(1, 5)
    @discord.app_commands.describe(number="Đoán con số xúc xắc sẽ xuất hiện hai lần.")
    @discord.app_commands.describe(so_tien="Chọn số tiền muốn cá cược.")
    @discord.app_commands.describe(loai_tien="Chọn loại tiền muốn cược.")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    async def sb_double_slash_command(self, interaction: discord.Interaction, number: int = None, so_tien:int = None, loai_tien:str = None):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if number != None and (number < 1 or number > 6):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Chỉ được chọn từ 1 đến 6!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if (so_tien != None and loai_tien == None):
            loai_tien = "C"
            
        if (so_tien == None and loai_tien != None):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Đã chọn loại tiền thì vui lòng chọn giá tiền cần cá cược!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
            
        profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if so_tien != None and profile == None:
            await interaction.followup.send(f"Để cá cược thì bạn phải thực hiện lệnh {SlashCommand.PROFILE.value} trước đã!")
            return
        elif so_tien != None and profile != None:
            if loai_tien == "C" and profile.copper < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.COPPER.value} để cá cược!")
                return
            elif loai_tien == "S" and profile.silver < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.SILVER.value} để cá cược!")
                return
            elif loai_tien == "G" and profile.gold < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.GOLD.value} để cá cược!")
                return
        if so_tien != None and so_tien <= 0:
            await interaction.followup.send(f"Số tiền nhập không hợp lệ!")
            return
        
        gambling_number_guess = ""
        if number != None:
            gambling_number_guess = f" và đặt cược vào số **{number}**"
        
        gambling_money_text = ""
        if so_tien != None and loai_tien != None:
            emoji = self.get_emoji_from_loai_tien(loai_tien=loai_tien)
            gambling_money_text = f" với tiền cược là **{so_tien}**{emoji}"
            
        embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã chơi tài xỉu đôi{gambling_number_guess}{gambling_money_text}.\nNhà cái đã tung xúc xắc {EmojiCreation2.DICE_ROLLING.value} {EmojiCreation2.DICE_ROLLING.value}", color=0x03F8FC)
        mess = await interaction.followup.send(embed=embed)
        if mess:
            await self.edit_embed_sb_double(message=mess, user=interaction.user, number=number, so_tien=so_tien, loai_tien=loai_tien, profile=profile)
        
        return
    
    
    @sb_double_slash_command.error
    async def sb_double_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    
    
    async def edit_embed_sb_double(self, message: discord.Message, user: discord.Member, number: int = None, so_tien:int = None, loai_tien:str = None, profile: Profile = None):
        #65% thua ngay
        lose_chance = self.get_chance(45)
        if lose_chance == True:
            first_num, first_dice_emoji, second_num, second_dice_emoji, third_num, third_dice_emoji = self.fixed_roll_dice_double_lose()
        else:
            first_num, first_dice_emoji = self.get_random_dice()
            second_num, second_dice_emoji = self.get_random_dice()
            third_num, third_dice_emoji = self.get_random_dice()
        
        await asyncio.sleep(4)
        l_chance = self.get_chance(5)
        if l_chance:
            await self.police_in(message=message, user=user, so_tien=so_tien, loai_tien=loai_tien, profile=profile)
            return
            
        #Nếu không có ít nhất hai cái trùng thì thua
        is_player_win = False
        if number == None:
            if first_num == second_num or second_num == third_num or first_num == third_num:
                is_player_win= True
        else:
            count = sum(1 for x in (first_num, second_num, third_num) if x == number)
            if count >= 2:
                is_player_win = True
        
        #Triple là thua
        if first_num == second_num == third_num:
            is_player_win = False
        print(f"At guild: {user.guild.name}, user {user.name} played Sic Bo Double and is_player_win = {is_player_win}, lose_chance: {lose_chance}")
        gambling_number_guess = ""
        if number != None:
            gambling_number_guess = f" và đặt cược vào số **{number}**"
        gambling_text = ""
        if so_tien != None:
            #Nếu thắng thì tỉ lệ ăn 1:2
            #Nếu thắng cả đoán số thì tỉ lệ ăn 1:4
            if number == None and so_tien != None and is_player_win == True:
                so_tien = so_tien*2
            elif number != None and so_tien != None and is_player_win == True:
                so_tien = so_tien*4
            gambling_text = f" **{so_tien}** {self.get_emoji_from_loai_tien(loai_tien=loai_tien)}"
        
        chinh_quyen_text = ""
        if profile!= None and profile.is_authority == False and so_tien != None:
            chinh_quyen_text = "Chính quyền đã lấy một nửa số tiền cá cược để làm thuế!"
        
        if is_player_win == True:
            result_text = f"\n{user.mention} đã thắng{gambling_text}!"
        else:
            result_text = f"\n{user.mention} đã thua{gambling_text}! {chinh_quyen_text}"
            if first_num == second_num == third_num:
                result_text = f"\n{user.mention} đã thua{gambling_text} vì xúc xắc đều quay ra ba con giống nhau! {chinh_quyen_text}"
            
        embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã chơi tài xỉu đôi{gambling_number_guess}.\nXúc xắc đã quay ra: {first_dice_emoji} | {second_dice_emoji} | {third_dice_emoji} |\n{result_text}", color=0x03F8FC)
        
        if so_tien != None and loai_tien!= None and profile != None:
            if loai_tien == "G": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, gold=so_tien, loai_tien=loai_tien)
            elif loai_tien == "S": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, silver=so_tien, loai_tien=loai_tien)
            elif loai_tien == "C": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, copper=so_tien, loai_tien=loai_tien)
        await message.edit(embed=embed_updated)

        check_quest_message = QuestMongoManager.increase_sb_double_count(guild_id=user.guild.id, user_id=user.id)
        if check_quest_message == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            ms = await message.channel.send(embed=quest_embed, content=f"{user.mention}", view=view)
            view.message = ms
        
        return
    
        #region tài xỉu triple
    @sb_group.command(name="triple", description="Tài xỉu Triple!")
    @discord.app_commands.checks.cooldown(1, 5)
    @discord.app_commands.describe(number="Đoán con số xúc xắc sẽ xuất hiện ba lần.")
    @discord.app_commands.describe(so_tien="Chọn số tiền muốn cá cược.")
    @discord.app_commands.describe(loai_tien="Chọn loại tiền muốn cược.")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    async def sb_triple_slash_command(self, interaction: discord.Interaction, number: int = None, so_tien:int = None, loai_tien:str = None):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if number != None and (number < 1 or number > 6):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Chỉ được chọn từ 1 đến 6!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if (so_tien != None and loai_tien == None):
            loai_tien = "C"
            
        if (so_tien == None and loai_tien != None):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Đã chọn loại tiền thì vui lòng chọn giá tiền cần cá cược!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
            
        profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if so_tien != None and profile == None:
            await interaction.followup.send(f"Để cá cược thì bạn phải thực hiện lệnh {SlashCommand.PROFILE.value} trước đã!")
            return
        elif so_tien != None and profile != None:
            if loai_tien == "C" and profile.copper < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.COPPER.value} để cá cược!")
                return
            elif loai_tien == "S" and profile.silver < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.SILVER.value} để cá cược!")
                return
            elif loai_tien == "G" and profile.gold < so_tien:
                await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.GOLD.value} để cá cược!")
                return
        if so_tien != None and so_tien <= 0:
            await interaction.followup.send(f"Số tiền nhập không hợp lệ!")
            return
        
        gambling_number_guess = ""
        if number != None:
            gambling_number_guess = f" và đặt cược vào số **{number}**"
        
        gambling_money_text = ""
        if so_tien != None and loai_tien != None:
            emoji = self.get_emoji_from_loai_tien(loai_tien=loai_tien)
            gambling_money_text = f" với tiền cược là **{so_tien}**{emoji}"
            
        embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã chơi tài xỉu ba{gambling_number_guess}{gambling_money_text}.\nNhà cái đã tung xúc xắc {EmojiCreation2.DICE_ROLLING.value} {EmojiCreation2.DICE_ROLLING.value}", color=0x03F8FC)
        mess = await interaction.followup.send(embed=embed)
        if mess:
            await self.edit_embed_sb_triple(message=mess, user=interaction.user, number=number, so_tien=so_tien, loai_tien=loai_tien, profile=profile)
        return
    
    @sb_triple_slash_command.error
    async def sb_triple_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    
    async def edit_embed_sb_triple(self, message: discord.Message, user: discord.Member, number: int = None, so_tien:int = None, loai_tien:str = None, profile: Profile = None):
        first_num, first_dice_emoji = self.get_random_dice()
        second_num, second_dice_emoji = self.get_random_dice()
        third_num, third_dice_emoji = self.get_random_dice()
        await asyncio.sleep(4)
        l_chance = self.get_chance(5)
        if l_chance:
            await self.police_in(message=message, user=user, so_tien=so_tien, loai_tien=loai_tien, profile=profile)
            return
            
        #Nếu không có ít nhất ba cái trùng thì thua
        is_player_win = False
        if number == None:
            if first_num == second_num and second_num == third_num and first_num == third_num:
                is_player_win= True
        else:
            if first_num == number and second_num == number and first_num == number:
                is_player_win = True
            
        gambling_number_guess = ""
        if number != None:
            gambling_number_guess = f" và đặt cược vào số **{number}**"
        gambling_text = ""
        if so_tien != None:
            #Nếu thắng thì tỉ lệ ăn 1:6
            #Nếu thắng cả đoán số thì tỉ lệ ăn 1:8
            if number == None and so_tien != None and is_player_win == True:
                so_tien = so_tien*6
            elif number != None and so_tien != None and is_player_win == True:
                so_tien = so_tien*8
            gambling_text = f" **{so_tien}** {self.get_emoji_from_loai_tien(loai_tien=loai_tien)}"
        
        chinh_quyen_text = ""
        if profile != None and profile.is_authority == False and so_tien != None:
            chinh_quyen_text = "Chính quyền đã lấy một nửa số tiền cá cược để làm thuế!"
        
        if is_player_win == True:
            result_text = f"\n{user.mention} đã thắng{gambling_text}!"
        else:
            result_text = f"\n{user.mention} đã thua{gambling_text}! {chinh_quyen_text}"
            
        embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã chơi tài xỉu ba{gambling_number_guess}.\nXúc xắc đã quay ra: {first_dice_emoji} | {second_dice_emoji} | {third_dice_emoji} |\n{result_text}", color=0x03F8FC)
        
        if so_tien != None and loai_tien!= None and profile != None:
            if loai_tien == "G": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, gold=so_tien, loai_tien=loai_tien)
            elif loai_tien == "S": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, silver=so_tien, loai_tien=loai_tien)
            elif loai_tien == "C": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, copper=so_tien, loai_tien=loai_tien)
        await message.edit(embed=embed_updated)

        check_quest_message = QuestMongoManager.increase_sb_triple_count(guild_id=user.guild.id, user_id=user.id)
        if check_quest_message == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            ms = await message.channel.send(embed=quest_embed, content=f"{user.mention}", view=view)
            view.message = ms
        
        return
    
    
    def get_random_dice(self):
        list_dice= [
            EmojiCreation2.DICE_1.value, 
            EmojiCreation2.DICE_2.value, 
            EmojiCreation2.DICE_3.value, 
            EmojiCreation2.DICE_4.value, 
            EmojiCreation2.DICE_5.value, 
            EmojiCreation2.DICE_6.value]
        list_dice_number = [1,2,3,4,5,6]
        
        index = random.randint(0, 5)
        return list_dice_number[index], list_dice[index]
    
    def fixed_roll_dice_double_lose(self):
        list_dice= [
            EmojiCreation2.DICE_1.value, 
            EmojiCreation2.DICE_2.value, 
            EmojiCreation2.DICE_3.value, 
            EmojiCreation2.DICE_4.value, 
            EmojiCreation2.DICE_5.value, 
            EmojiCreation2.DICE_6.value]
        list_dice_number = [1,2,3,4,5,6]
        
        if random.random() < 0.5:
            # 50% 3 dice bằng nhau
                chosen_index = random.randint(0, 5)
                chosen_value = list_dice_number[chosen_index]
                chosen_emoji = list_dice[chosen_index]
                rolls = [
                    (chosen_value, chosen_emoji),
                    (chosen_value, chosen_emoji),
                    (chosen_value, chosen_emoji)
                ]
                (first_num, first_dice_emoji), (second_num, second_dice_emoji), (third_num, third_dice_emoji) = rolls
                return first_num, first_dice_emoji, second_num, second_dice_emoji, third_num, third_dice_emoji
        else:
            # 50% ba dice khác nhau
                chosen_indices = random.sample(range(6), 3)
                rolls = [
                    (list_dice_number[i], list_dice[i]) for i in chosen_indices
                ]
                (first_num, first_dice_emoji), (second_num, second_dice_emoji), (third_num, third_dice_emoji) = rolls
                return first_num, first_dice_emoji, second_num, second_dice_emoji, third_num, third_dice_emoji

        
        
    def get_emoji_from_loai_tien(self, loai_tien):
        if loai_tien == "G": return EmojiCreation2.GOLD.value
        if loai_tien == "S": return EmojiCreation2.SILVER.value
        return EmojiCreation2.COPPER.value
        
    def get_chance(self, chance: int):
        rand_num = random.randint(0, 100)
        if rand_num < chance:
            return True
        else:
            return False