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

async def setup(bot: commands.Bot):
    await bot.add_cog(SicboCog(bot=bot))
    print("Sic Bo game is ready!")

class SicboCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    sb_group = discord.app_commands.Group(name="sb", description="Các lệnh liên quan đến Minigame tài xỉu!")
    
    #region tài xỉu normal
    @sb_group.command(name="normal", description="Tài xỉu phiên bản đơn giản hoá")
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
    
    
    async def edit_embed_sb_normal(self, message: discord.Message, user: discord.Member, tai_xiu: str, so_tien:int = None, loai_tien:str = None, profile: Profile = None):
        first_num, first_dice_emoji = self.get_random_dice()
        second_num, second_dice_emoji = self.get_random_dice()
        third_num, third_dice_emoji = self.get_random_dice()
        count_all = first_num + second_num + third_num
        await asyncio.sleep(4)
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
        
        if is_player_win == True:
            result_text = f"> {user.mention} đã thắng{gambling_text}!"
        else:
            result_text = f"> {user.mention} đã thua{gambling_text}! Chính quyền đã lấy một nửa số tiền cá cược để làm thuế!"
            if first_num == second_num == third_num:
                result_text = f"\n{user.mention} đã thua{gambling_text} vì xúc xắc đều quay ra ba con giống nhau! Chính quyền đã lấy một nửa số tiền cá cược để làm thuế!"
        embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã chơi tài xỉu và chọn **{tai_xiu}**.\nXúc xắc đã quay ra: {first_dice_emoji} | {second_dice_emoji} | {third_dice_emoji}!\n{result_text}", color=0x03F8FC)
        
        if so_tien != None and loai_tien!= None and profile != None:
            if loai_tien == "G": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, gold=so_tien)
            elif loai_tien == "S": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, silver=so_tien)
            elif loai_tien == "C": self.update_player_money_and_authority_money(is_player_win=is_player_win, guild_int=user.guild.id, profile=profile, copper=so_tien)

            
        await message.edit(embed=embed_updated)
        return
    
    def update_player_money_and_authority_money(self, is_player_win: bool, guild_int: int, profile: Profile, copper: int = 0, silver: int = 0, gold: int = 0):
        #Tính cộng trừ tiền cho player
        if is_player_win:
            #Cộng user, trừ authority
            ProfileMongoManager.update_profile_money(guild_id=guild_int, guild_name=profile.guild_name, user_id=profile.user_id, user_name=profile.user_name, user_display_name=profile.user_display_name, gold=gold, silver=silver, copper=copper)
            ProfileMongoManager.update_money_authority(guild_id=guild_int, silver=-silver, copper=-copper, gold=-gold)
        else:
            ProfileMongoManager.update_profile_money(guild_id=guild_int, guild_name=profile.guild_name, user_id=profile.user_id, user_name=profile.user_name, user_display_name=profile.user_display_name, gold=-gold, silver=-silver, copper=-copper)
            #Authority chỉ ăn 50%
            ProfileMongoManager.update_money_authority(guild_id=guild_int, silver=int(silver/2), copper=int(copper/2), gold=int(gold/2))
        
        
        
    
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
        
    def get_emoji_from_loai_tien(self, loai_tien):
        if loai_tien == "G": return EmojiCreation2.GOLD.value
        if loai_tien == "S": return EmojiCreation2.SILVER.value
        return EmojiCreation2.COPPER.value
        
    