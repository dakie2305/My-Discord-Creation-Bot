from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord.app_commands import Choice
from CustomEnum import UserEnum
from CustomEnum.EmojiEnum import EmojiCreation1
import CustomFunctions
import random
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from Handling.MiniGame.MatchWord.MwConfirmHintView import MwConfirmHintView
from Handling.MiniGame.SortWord import SwClass, SwHandling, SwMongoManager
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
from Handling.MiniGame.SortWord.SwConfirmDeleteView import SwConfirmDeleteView
from Handling.MiniGame.SortWord.SwConfirmHintView import SwConfirmHintView
from Handling.MiniGame.SortWord.SwConfirmRestartView import SwConfirmRestartView
from Handling.Misc.SelfDestructView import SelfDestructView

async def setup(bot: commands.Bot):
    await bot.add_cog(HintWordMiniGame(bot=bot))
    print("Hint Word Mini Game is ready!")

class HintWordMiniGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.english_words_dictionary = CustomFunctions.get_english_dict()
        self.vietnamese_words_dictionary = CustomFunctions.get_vietnamese_dict()
    
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
    @discord.app_commands.command(name="hint", description="Gợi ý từ hợp lệ trong Đoán Từ, Nối Từ.")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def hint(self, interaction: discord.Interaction):
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
            view = MwConfirmHintView(user=interaction.user, info=info, lan=lan, english_words_dictionary=self.english_words_dictionary, vietnamese_dict=self.vietnamese_words_dictionary)
            embed = self.get_hint_embed(interaction=interaction, lan= lan, mw_info=info)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            #Đoán từ
            view = SwConfirmHintView(user=interaction.user, info=info, lan=lan)
            embed = self.get_hint_embed(interaction=interaction, lan= lan, sw_info=info)
            mess = await interaction.followup.send(embed=embed)
            view.message = mess
            return
        #Không có
        view = SelfDestructView(timeout=30)
        embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Chỉ dùng lệnh này trong kênh chơi Đoán Từ hoặc Nối Từ!",color=discord.Color.red())
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
        view.message = mess
        return
    
    @hint.error
    async def hint_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    def get_hint_embed(self, interaction: discord.Interaction,lan: str, sw_info: SwClass.SortWordInfo = None, mw_info: MwClass.MatchWordInfo = None):
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
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=30)  # 30 seconds from now
        unix_time = int(end_time.timestamp())
        embed = discord.Embed(title=f"{EmojiCreation1.QUESTION_MARK.value} Gợi Ý Từ Hợp Lệ {EmojiCreation1.QUESTION_MARK.value}", description=f"Trò Chơi {title} {lan}", color=0x03F8FC)
        embed.add_field(name=f"", value=f"{interaction.user.mention} bạn có muốn đổi 3 điểm để gợi ý từ tiếp theo không?", inline=False)
        embed.add_field(name="______________", value= f"Thời gian còn lại: <t:{unix_time}:R>", inline=False)
        return embed