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
    await bot.add_cog(CoinFlip(bot=bot))
    print("Coin Flip game is ready!")

class CoinFlip(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #region Coin flip
    @discord.app_commands.checks.cooldown(1, 7)
    @discord.app_commands.command(name="cf", description="Tung đồng xu sấp/ngửa cho vui")
    @discord.app_commands.describe(sap_ngua="Chọn sấp ngửa.")
    @discord.app_commands.describe(so_tien="Chọn số tiền muốn cá cược.")
    @discord.app_commands.describe(loai_tien="Chọn loại tiền muốn cược.")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    @discord.app_commands.choices(sap_ngua=[
        Choice(name="Sấp", value="s"),
        Choice(name="Ngửa", value="n"),
    ])
    async def coin_flip_slash_command(self, interaction: discord.Interaction, sap_ngua: str = None, so_tien:int = None, loai_tien:str = None):
        await interaction.response.defer(ephemeral=False)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if (sap_ngua != None and (so_tien != None or loai_tien == None)):
            loai_tien = "C"
            
            
        profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if sap_ngua != None and profile == None:
            await interaction.followup.send(f"Để cá cược thì bạn phải thực hiện lệnh {SlashCommand.PROFILE.value} trước đã!")
            return
        elif sap_ngua != None and profile != None:
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
        
        embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã tung đồng xu. Đồng xu đang quay {EmojiCreation2.DOGE_COIN.value} ...", color=0x03F8FC)
        mess = await interaction.followup.send(embed=embed)
        if mess:
            if sap_ngua != None and sap_ngua == 'n': sap_ngua_true_false = False
            elif sap_ngua != None and sap_ngua == 's': sap_ngua_true_false = True
            else : sap_ngua_true_false = None
            await self.edit_embed_coin_flip(message=mess, user=interaction.user, sap_ngua=sap_ngua_true_false, so_tien=so_tien, loai_tien=loai_tien, profile=profile)
        return
    
    @coin_flip_slash_command.error
    async def coin_flip_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    async def edit_embed_coin_flip(self, message: discord.Message, user: discord.Member, sap_ngua: bool = None, so_tien:int = None, loai_tien:str = None, profile: Profile = None):
        player_choice = 'sấp'
        is_player_win = False
        if sap_ngua != None and sap_ngua == False:
            player_choice = 'ngửa'
        currency_emoji = EmojiCreation2.COPPER.value
        if loai_tien != None and loai_tien == "G":
            currency_emoji = EmojiCreation2.GOLD.value
        elif loai_tien != None and loai_tien == "S":
            currency_emoji = EmojiCreation2.SILVER.value
        
        await asyncio.sleep(3)
        choice = random.randint(0,10)
        emoji_state = EmojiCreation2.COIN_NGUA.value
        state = 'ngửa'
        if choice > 0 and choice <=5:
            state = 'sấp'
            emoji_state = EmojiCreation2.COIN_SAP.value
        elif choice == 10:
            #Troll player
            response = CustomFunctions.get_random_response("OnCoinFlip.txt")
            embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã tung đồng xu. {response}", color=0x03F8FC)
            await message.edit(embed=embed_updated)
            return
        if sap_ngua != None and player_choice == state:
            is_player_win = True
        else:
            is_player_win = False
        gambling_text = ""
        if sap_ngua!= None:
            if is_player_win == True:
                gambling_text = f'\n{user.mention} đã chọn **`{player_choice}`** và thắng được **{so_tien}**{currency_emoji} từ Chính Quyền!'
            else:
                au_money_tax = int(so_tien/2)
                if au_money_tax == 0: au_money_tax = 1
                gambling_text = f'\n{user.mention} đã chọn **`{player_choice}`** và thua mất **{so_tien}**{currency_emoji} và mất 1 điểm nhân phẩm! Chính Quyền đã lấy **{au_money_tax}** {currency_emoji} để làm thuế!'
        embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã tung đồng xu. Đồng xu đã quay ra **`{state}`** {emoji_state}!{gambling_text}", color=0x03F8FC)
        await message.edit(embed=embed_updated)
        if choice == 0:
            await asyncio.sleep(2)
            #Troll tập 2
            if state == 'ngửa':
                state = 'sấp'
                emoji_state = EmojiCreation2.COIN_SAP.value
            else:
                state = 'ngửa'
                emoji_state = EmojiCreation2.COIN_NGUA.value
            if sap_ngua != None and player_choice == state:
                is_player_win = True
            else:
                is_player_win = False
            gambling_text = ""
            if sap_ngua!= None:
                if is_player_win == True:
                    gambling_text = f'\n{user.mention} đã chọn **`{player_choice}`** và thắng **{so_tien}**{currency_emoji} từ Chính Quyền!'
                else:
                    gambling_text = f'\n{user.mention} đã chọn **`{player_choice}`** và thua mất **{so_tien}**{currency_emoji} và mất 1 điểm nhân phẩm! Chính Quyền đã lấy **{int(so_tien/2)}** {currency_emoji} để làm thuế!'
            embed_updated = discord.Embed(title=f"", description=f"Đùa thôi. Đồng xu đã quay ra **`{state}`** {emoji_state}!{gambling_text}", color=0x03F8FC)
            await message.edit(embed=embed_updated)
        
        if sap_ngua != None and profile != None:
            #Lấy profile của authority ra luôn
            authority_profile = ProfileMongoManager.get_authority(guild_id=user.guild.id)
            #Tính cộng trừ tiền cho player
            if loai_tien == "C":
                if is_player_win:
                    profile.copper += so_tien 
                    if authority_profile and profile.is_authority == False: authority_profile.copper -= so_tien
                else:
                    profile.copper -= so_tien 
                    if authority_profile and profile.is_authority == False: 
                        au_money_tax = int(so_tien/2)
                        if au_money_tax == 0: au_money_tax = 1
                        authority_profile.copper += au_money_tax
            if loai_tien == "S":
                if is_player_win:
                    profile.silver += so_tien 
                    if authority_profile and profile.is_authority == False: authority_profile.silver -= so_tien
                else:
                    profile.silver -= so_tien 
                    if authority_profile and profile.is_authority == False: 
                        au_money_tax = int(so_tien/2)
                        if au_money_tax == 0: au_money_tax = 1
                        authority_profile.silver += au_money_tax
            if loai_tien == "G":
                if is_player_win:
                    profile.gold += so_tien 
                    if authority_profile and profile.is_authority == False: authority_profile.gold -= so_tien
                else:
                    profile.gold -= so_tien 
                    if authority_profile and profile.is_authority == False:
                        au_money_tax = int(so_tien/2)
                        if au_money_tax == 0: au_money_tax = 1
                        authority_profile.gold += au_money_tax
            
            if is_player_win == False:
                #Trừ 1 điểm nhân phẩm
                ProfileMongoManager.update_dignity_point(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point=-1)
            #Cộng kinh nghiệm nếu thắng
            elif profile != None and so_tien != None and is_player_win == True:
                if loai_tien == "C" and so_tien > 10000:
                    bonus_exp = self.get_bonus_exp_based_on_amount(so_tien=so_tien, loai_tien=loai_tien, profile=profile)
                    ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id=user.id, bonus_exp=bonus_exp)
                elif loai_tien == "S" or loai_tien == "G":
                    bonus_exp = self.get_bonus_exp_based_on_amount(so_tien=so_tien, loai_tien=loai_tien, profile=profile)
                    ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id=user.id, bonus_exp=bonus_exp)
                
            ProfileMongoManager.update_profile_money_fast(guild_id=user.guild.id, data=profile)
            if authority_profile and profile.is_authority == False: ProfileMongoManager.update_profile_money_fast(guild_id=user.guild.id, data=authority_profile)
        
        check_quest_message = QuestMongoManager.increase_coin_flip_count(guild_id=user.guild.id, user_id=user.id)
        if check_quest_message == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            ms = await message.channel.send(embed=quest_embed, content=f"{message.author.mention}", view=view)
            view.message = ms
        return
    
    def get_bonus_exp_based_on_amount(self, so_tien:int = None, loai_tien:str = None, profile: Profile = None):
        if profile == None or so_tien == None or loai_tien == None: return 0
        if so_tien < 10000 and loai_tien == "C": return 0
        if loai_tien == "C":
            exp = int(so_tien / 5000 * profile.level)
            if exp > 50: exp = 50
            return exp
        elif loai_tien == "S":
            exp = int(so_tien / 100 * profile.level)
            if exp == 0: exp = 20
            if exp > 50: exp = 50
            return exp
        elif loai_tien == "G":
            exp = int(so_tien / 10 * profile.level)
            if exp == 0: exp = 50
            if exp > 80: exp = 80
            return exp