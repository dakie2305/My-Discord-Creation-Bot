import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from datetime import datetime, timedelta
from CustomEnum import UserEnum
from CustomEnum.EmojiEnum import EmojiCreation1
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import CustomFunctions
from Handling.MiniGame.MatchWord.MwChooseVietnamType import MwChooseVietnamType
from Handling.MiniGame.MatchWord.MwConfirmDeleteView import MwConfirmDeleteView
from Handling.MiniGame.MatchWord.MwConfirmRestartView import MwConfirmRestartView
from Handling.MiniGame.SortWord import SwClass, SwHandling, SwMongoManager, SwView
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
from Handling.MiniGame.SortWord.SwConfirmDeleteView import SwConfirmDeleteView
from Handling.MiniGame.SortWord.SwConfirmRestartView import SwConfirmRestartView
from Handling.Misc.SelfDestructView import SelfDestructView

async def setup(bot: commands.Bot):
    await bot.add_cog(WordMiniGameCog(bot=bot))
    print("Words Mini Game is ready!")

class WordMiniGameCog(commands.Cog):
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
    
    start = discord.app_commands.Group(name="start", description="Các lệnh liên quan đến Mini Game Từ Vựng!")
    #region start match_word slash
    @start.command(name="match_word", description="Bắt đầu/kết thúc Nối Từ trong channel hiện tại!")
    @discord.app_commands.describe(language="Chọn ngôn ngữ của game Nối Từ.")
    @discord.app_commands.choices(language=[
        Choice(name="Tiếng Anh", value="en"),
        Choice(name="Tiếng Việt", value="vn"),
    ])
    @discord.app_commands.checks.cooldown(1, 30)
    async def start_match_word_slash_command(self, interaction: discord.Interaction, language: str):
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
            lan_label = "Tiếng Anh" if lan == "en" else "Tiếng Việt"
            #Đã tồn tại thì xoá đi
            embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Xoá Nối Từ {lan_label} {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.red())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đây đang là kênh để chơi Nối Từ.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} Bạn sắp sửa xoá trò chơi Nối Từ {lan_label} của channel <#{interaction.channel.id}>.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bạn có chắc không? Nếu thực sự chắc chắn thì ấn vào nút bên dưới.", inline=False)
            view = MwConfirmDeleteView(user=interaction.user, channel_id=interaction.channel_id, lan=lan)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        #Kiểm tra đoán từ
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là kênh dùng để chơi Đoán Từ, không thể bắt đầu chơi Nối Từ được!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        #Tạo mới nối từ
        lan_label = "Tiếng Anh" if language == "en" else "Tiếng Việt"
        #Nếu là tiếng anh thì cứ tạo bình thường
        if language == "en":
            data = MwClass.MatchWordInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, current_word="hello", special_case=False)
            MwMongoManager.create_info(data=data, guild_id=interaction.guild_id, lang=language)
            embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Nối Từ {lan_label}", description=f"",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đã chọn kênh này làm kênh nối từ.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Từ hiện tại:", inline=False)
            embed.add_field(name=f"{data.current_word}", value=f"", inline=False)
            mess = await interaction.followup.send(embed=embed)
        else:
            #Tiếng Việt thì có hai loại đặc biệt, nối theo âm cuối, hoặc nối theo nguyên từ cuối
            embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Nối Từ {lan_label}", description=f"",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Nối Từ Tiếng Việt có hai loại đặc biệt: **Nối Theo Từ Cuối** hoặc **Nối Theo Âm Cuối**.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Ví dụ khi chọn **Nối Theo Từ Cuối**:\n `anh trai`  ->  `trai làng`  ->   `làng quê`", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Ví dụ khi chọn **Nối Theo Âm Cuối**:\n `anh trai`  ->  `im lặng`  ->   `gay cấn`", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Vui lòng chọn thể loại hình thức bạn muốn.", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            view = MwChooseVietnamType(user=interaction.user)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
    @start_match_word_slash_command.error
    async def start_match_word_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    #region start sort_word slash
    @start.command(name="sort_word", description="Bắt đầu/kết thúc Đoán Từ trong channel hiện tại!")
    @discord.app_commands.describe(language="Chọn ngôn ngữ của game Đoán Từ.")
    @discord.app_commands.choices(language=[
        Choice(name="Tiếng Anh", value="en"),
        Choice(name="Tiếng Việt", value="vn"),
    ])
    @discord.app_commands.checks.cooldown(1, 30)
    async def start_sort_word_slash_command(self, interaction: discord.Interaction, language: str):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        #Kiểm tra xem tồn tại mini game nối từ hay đoán từ chưa
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            lan_label = "Tiếng Anh" if lan == "en" else "Tiếng Việt"
            #Đã tồn tại thì xoá đi
            embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Xoá Đoán Từ {lan_label} {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.red())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đây đang là kênh để chơi Đoán Từ {lan_label}.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} Bạn sắp sửa xoá trò chơi Đoán Từ {lan_label} của channel <#{interaction.channel.id}>.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bạn có chắc không? Nếu thực sự chắc chắn thì ấn vào nút bên dưới.", inline=False)
            view = SwConfirmDeleteView(user=interaction.user, channel_id=interaction.channel_id, lan=lan)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        #Kiểm tra đoán từ
        info, lan = self.check_if_message_inside_mw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là kênh dùng để chơi Nối Từ, không thể bắt đầu chơi Đoán Từ được!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        #Tạo mới đoán từ
        lan_label = "Tiếng Anh" if language == "en" else "Tiếng Việt"
        current_word = "hello" if language == "en" else "trai"
        unsorted = "olehl" if language == "en" else "rtia"
        data = SwClass.SortWordInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, current_word=current_word, unsorted_word=unsorted, special_case=False)
        SwMongoManager.create_info(data=data, guild_id=interaction.guild_id, lang=language)
        embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Đoán Từ {lan_label}", description=f"",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đã chọn kênh này làm kênh đoán từ.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hướng dẫn chơi Tiếng Anh:\n `ih` -> `hi`, `ytr` -> `try`", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hướng dẫn chơi Tiếng Việt:\n `han rtai` -> `anh trai`, `me rait` -> `em trai`", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Đoán từ hiện tại:", inline=False)
        embed.add_field(name=f"{data.unsorted_word}", value=f"", inline=False)
        mess = await interaction.followup.send(embed=embed)
        return

        
    @start_sort_word_slash_command.error
    async def start_sort_word_slash_command(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    

    restart = discord.app_commands.Group(name="restart", description="Các lệnh liên quan đến Mini Game Từ Vựng!")
    #region start match_word slash
    @restart.command(name="match_word", description="Restart trò chơi Nối Từ trong channel hiện tại!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def restart_match_word_slash_command(self, interaction: discord.Interaction):
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
        if info is None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là lệnh dùng để restart Nối Từ, chỉ dùng trong kênh Nối Từ!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        lan_label = "Tiếng Anh" if lan == "en" else "Tiếng Việt"
        #Đã tồn tại thì xoá đi
        embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Restart Nối Từ {lan_label} {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.red())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đây đang là kênh để chơi Nối Từ.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} Bạn sắp sửa restart lại Nối Từ {lan_label} của channel <#{interaction.channel.id}>.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bạn có chắc không? Nếu thực sự chắc chắn thì ấn vào nút bên dưới.", inline=False)
        view = MwConfirmRestartView(user=interaction.user, channel_id=interaction.channel_id, lan=lan, info = info)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        return

        
    @restart_match_word_slash_command.error
    async def restart_match_word_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    #region start match_word slash
    @restart.command(name="sort_word", description="Restart trò chơi Đoán Từ trong channel hiện tại!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def restart_sort_word_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Kiểm tra xem tồn tại mini game nối từ hay đoán từ chưa
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là lệnh dùng để restart Đoán Từ, chỉ dùng trong kênh Đoán Từ!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        lan_label = "Tiếng Anh" if lan == "en" else "Tiếng Việt"
        #Đã tồn tại thì xoá đi
        embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Restart Đoán Từ {lan_label} {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.red())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đây đang là kênh để chơi Đoán Từ.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} Bạn sắp sửa restart lại Đoán Từ {lan_label} của channel <#{interaction.channel.id}>.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bạn có chắc không? Nếu thực sự chắc chắn thì ấn vào nút bên dưới.", inline=False)
        view = SwConfirmRestartView(user=interaction.user, channel_id=interaction.channel_id, lan=lan, info = info)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        return

    @restart_sort_word_slash_command.error
    async def restart_sort_word_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)