import discord
from discord.ext import commands
from discord.app_commands import Choice
from CustomEnum import UserEnum
from CustomEnum.EmojiEnum import EmojiCreation1
import CustomFunctions
import random
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from Handling.MiniGame.SortWord import SwClass, SwHandling, SwMongoManager
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
from Handling.MiniGame.SortWord.SwConfirmDeleteView import SwConfirmDeleteView
from Handling.MiniGame.SortWord.SwConfirmRestartView import SwConfirmRestartView
from Handling.Misc.SelfDestructView import SelfDestructView

async def setup(bot: commands.Bot):
    await bot.add_cog(LeaderboardWordMiniGame(bot=bot))
    print("Leaderboard Word Mini Game is ready!")

class LeaderboardWordMiniGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def check_if_message_inside_sw_game(self, guild_id: int = None, channel_id: int = None):
        langs = ['en', 'vn']
        for lan in langs:
            check = SwMongoManager.find_sort_word_info_by_id(lang=lan, guild_id=guild_id, channel_id= channel_id)
            if check is not None:
                return check, lan
        return None, None
    
    def check_if_message_inside_mw_game(self, guild_id: int = None, channel_id: int = None):
        langs = ['en', 'vn']
        for lan in langs:
            check = MwMongoManager.find_match_word_info_by_id(lang=lan, guild_id=guild_id, channel_id= channel_id)
            if check is not None:
                return check, lan
        return None, None

    #region Truth Dare
    @discord.app_commands.command(name="bxh", description="Kiểm tra bảng xếp hạng Nối Từ/Đoán Từ trong kênh này.")
    @discord.app_commands.describe(user="Chọn user cần muốn xem cụ thể xếp hạng")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def bxh(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Kiểm tra xem tồn tại mini game nối từ hay đoán từ chưa
        info, lan = self.check_if_message_inside_mw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            #Nối từ
            embed = self.get_leaderboard_embed(interaction=interaction, lan= lan, mw_info=info, user_mention = user)
            await interaction.followup.send(embed=embed)
            return
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            #Đoán từ
            embed = self.get_leaderboard_embed(interaction=interaction, lan= lan, sw_info=info, user_mention = user)
            await interaction.followup.send(embed=embed)
            return
        #Không có
        view = SelfDestructView(timeout=30)
        embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Chỉ dùng lệnh này trong kênh chơi Đoán Từ hoặc Nối Từ!",color=discord.Color.red())
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
        view.message = mess
        return
    
    @bxh.error
    async def bxh_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    def get_leaderboard_embed(self, interaction: discord.Interaction,lan: str, sw_info: SwClass.SortWordInfo = None, mw_info: MwClass.MatchWordInfo = None, user_mention: discord.Member = None):
        if lan == 'en' or lan == 'eng':
            lan = "Tiếng Anh"
        elif lan == 'vn':
            lan = "Tiếng Việt"
        
        title = "Đoán Từ"
        game_info = None
        if sw_info is not None:
            game_info = sw_info
        elif mw_info is not None:
            game_info = mw_info
            title = "Nối Từ"
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Trò Chơi {title} {lan}", color=0x03F8FC)
        embed.add_field(name=f"", value=f"Lượt chơi thứ: {game_info.current_round}/500", inline=False)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 0
        if game_info.player_profiles:
            game_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            if user_mention == None:
                for index, profile in enumerate(game_info.player_profiles):
                    user = interaction.guild.get_member(profile.user_id)
                    if user != None and (profile.point!= 0):
                        embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                        count+=1
                    if count >= 15: break
            else:
                matched = False
                for index, profile in enumerate(game_info.player_profiles):
                    if profile.user_id == user_mention.id:
                        user = interaction.guild.get_member(profile.user_id)
                        embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                        #Show kỹ năng luôn
                        if profile.special_items:
                            embed.add_field(name=f"________________", value= f"")
                            for index_item, item in enumerate(profile.special_items):
                                instruction = f"!sws {item.item_id}"
                                if item.required_target:
                                    instruction = f"!sws {item.item_id} <@315835396305059840>"
                                embed.add_field(name=f"Kỹ năng {index_item+1}", value= f"Tên kỹ năng: *{item.item_name}*\n\nMô tả kỹ năng: {item.item_description}\n\nCách dùng:**/skills**", inline=False)
                                embed.add_field(name=f"________________", value= f"")
                        matched = True
                        break
                if matched == False:
                    embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi này*", inline=False)     
        else:
            embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi*", inline=False)       
        embed.add_field(name=f"", value="___________________", inline=False)
        return embed