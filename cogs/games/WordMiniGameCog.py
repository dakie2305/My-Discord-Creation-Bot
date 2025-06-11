import random
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
from Handling.MiniGame.GuessNumber import GnMongoManager
from Handling.MiniGame.GuessNumber.GnConfirmDeleteView import GnConfirmDeleteView
from Handling.MiniGame.GuessNumber.GnConfirmRestartView import GnConfirmRestartView
from Handling.MiniGame.MatchWord.MwChooseVietnamType import MwChooseVietnamType
from Handling.MiniGame.MatchWord.MwConfirmDeleteView import MwConfirmDeleteView
from Handling.MiniGame.MatchWord.MwConfirmRestartView import MwConfirmRestartView
from Handling.MiniGame.SortWord import SwClass, SwHandling, SwMongoManager
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
from Handling.MiniGame.GuessNumber import GuessNumberClass, GnMongoManager
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
    
    def check_if_message_inside_gn_game(self, guild_id: int = None, channel_id: int = None):
        check = GnMongoManager.find_guess_number_info_by_id(guild_id=guild_id, channel_id= channel_id)
        if check is not None:
            return check
        return None
    
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
        #Kiểm tra đoán số
        info = self.check_if_message_inside_gn_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là kênh dùng để chơi Đoán Số, không thể bắt đầu chơi Nối Từ được!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Tạo mới nối từ
        lan_label = "Tiếng Anh" if language == "en" else "Tiếng Việt"
        #Nếu là tiếng anh thì cứ tạo bình thường
        if language == "en":
            data = MwClass.MatchWordInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, current_word="hello", correct_start_word="o", remaining_word=10000, special_case=False, type="B")
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
        #Kiểm tra đoán số
        info = self.check_if_message_inside_gn_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là kênh dùng để chơi Đoán Số, không thể bắt đầu chơi Đoán Từ được!",color=discord.Color.red())
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
            
    
    #region start guess_number slash
    @start.command(name="guess_number", description="Bắt đầu/kết thúc Đoán Số May Mắn trong channel hiện tại!")
    @discord.app_commands.describe(difficulty="Chọn độ khó của game.")
    @discord.app_commands.choices(difficulty=[
        Choice(name="Dễ, trong khoảng [0, 1000]", value="1"),
        Choice(name="Vừa, trong khoảng [-1000, 1000]", value="2"),
        Choice(name="Khó, trong khoảng [-1000, 10.000]", value="3"),
        Choice(name="Điên Rồ, trong khoảng [-10.000, 100.000]", value="4"),
        Choice(name="Huyền Thoại, trong khoảng [-999.999.999, 999.999.999]", value="5"),
    ])
    @discord.app_commands.checks.cooldown(1, 30)
    async def start_guess_number_slash_command(self, interaction: discord.Interaction, difficulty: str):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Kiểm tra xem tồn tại đoán số chưa
        info = self.check_if_message_inside_gn_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info:
            #Xóa đi
            embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Xoá Trò Chơi Đoán Số {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.red())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đây đang là kênh để chơi Đoán Số.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} Bạn sắp sửa xoá trò chơi Đoán Số của channel <#{interaction.channel.id}>.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bạn có chắc không? Nếu thực sự chắc chắn thì ấn vào nút bên dưới.", inline=False)
            view = GnConfirmDeleteView(user=interaction.user, channel_id=interaction.channel_id)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Kiểm tra xem tồn tại mini game nối từ hay đoán từ chưa
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là kênh dùng để chơi Đoán Từ, không thể bắt đầu chơi Đoán Số được!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Kiểm tra đoán từ
        info, lan = self.check_if_message_inside_mw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là kênh dùng để chơi Nối Từ, không thể bắt đầu chơi Đoán Số được!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        #Tạo mới đoán số
        range_from, range_to = 0, 1000
        number = random.randint(range_from, range_to)
        if difficulty == "2":
            range_from, range_to = -1000, 1000
            number = random.randint(range_from, range_to)
        elif difficulty == "3":
            range_from, range_to = -1000, 10000
            number = random.randint(range_from, range_to)
        elif difficulty == "4":
            range_from, range_to = -10000, 100000
            number = random.randint(range_from, range_to)
        elif difficulty == "5":
            range_from, range_to = -999_999_999, 999_999_999
            number = random.randint(range_from, range_to)
        else:
            range_from, range_to = 0, 1000
            number = random.randint(range_from, range_to)
        data = GuessNumberClass.GuessNumberInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, correct_number=number, range_from=range_from, range_to=range_to)
        GnMongoManager.create_info(data=data, guild_id=interaction.guild_id)
        embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Đoán Số May Mắn", description=f"",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hãy nhắn vào một con số bất kỳ, bot sẽ gợi ý cho bạn tìm ra con số chính xác!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Đáp án đúng sẽ thuộc khoảng từ **`{data.range_from}`** đến **`{data.range_to}`**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bot sẽ react {EmojiCreation1.HIGHER.value} nếu số của bạn thấp hơn đáp án", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bot sẽ react {EmojiCreation1.LOWER.value} nếu số của bạn cao hơn đáp án", inline=False)
        mess = await interaction.followup.send(embed=embed)
        return
        
    @start_guess_number_slash_command.error
    async def start_guess_number_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    

    restart = discord.app_commands.Group(name="restart", description="Các lệnh liên quan đến Mini Game Từ Vựng!")
    #region restart match_word slash
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
    
    #region restart restart_word slash
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
            
    
    #region restart restart_word slash
    @restart.command(name="guess_number", description="Restart trò chơi Đoán Số trong channel hiện tại!")
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
        
        #Kiểm tra xem tồn tại mini game chưa
        info = self.check_if_message_inside_gn_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là lệnh dùng để restart Đoán Số, chỉ dùng trong kênh Đoán Số!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Đã tồn tại thì xoá đi
        embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Restart Đoán Số {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.red())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đây đang là kênh để chơi Đoán Số.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} Bạn sắp sửa restart lại Đoán Số của channel <#{interaction.channel.id}>.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bạn có chắc không? Nếu thực sự chắc chắn thì ấn vào nút bên dưới.", inline=False)
        view = GnConfirmRestartView(user=interaction.user, channel_id=interaction.channel_id, info = info)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        return

    @restart_sort_word_slash_command.error
    async def restart_sort_word_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)