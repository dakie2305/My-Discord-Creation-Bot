from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import CurrencyEmoji
from CustomEnum.RoleEnum import TrueHeavenRoleId
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import random
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
import CustomFunctions

async def setup(bot: commands.Bot):
    await bot.add_cog(WorkEconomy(bot=bot))
    print("Work Economy is ready!")

class WorkEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.random_title_at_work = ["sếp", "đồng nghiệp", "nhân viên cùng chỗ làm", "thanh niên", "công đoàn"]
        self.random_user = ["Rui", "Darkie", "Leila", "Duck", "LunLun", "ẩn danh", "bí ẩn", "mới", "cũ", "nào đó", "HuyGold", "Kyo", "Tuz"]
        self.random_praise = [
            "Vì thành tích công việc tốt, nên {title} {person} đã có chút khen thưởng về thành quả mà {user_name} đạt được. ", 
            "Trong lúc làm việc, {title} {person} rất hài lòng khi thấy {user_name} đã làm việc chăm chỉ. ",
            "Trong lúc test lệnh trong server {server_name}, {title} {person} gửi lời cảm ơn đến {user_name} vì đã dùng lệnh thường xuyên. ",
            "Vì hoàn thành KPI, {title} {person} không ngớt lời khen ngợi {user_name} về thành quả đạt được. ",
            "Vì hoàn thành KPI đăng content trong server {server_name}, {title} {person} quyết định thưởng cho {user_name} một chút để làm động lực. ",
            "Vì đã lo rất tốt cho {server_name}, {title} {person} đã biểu dương thành tích của {user_name} và đánh giá cao thành quả đạt được. ",
            "Vì không để nơi này thành dead server, {title} {person} nhiệt liệt tán thưởng {user_name} vì đã nói nhiều. ",
            "Là thành viên ưu tú của server {server_name}, {user_name} được thưởng thêm một chút. ",
            "Nhờ việc lảm nhảm nhiều nên server {server_name} không dead, nên {title} {person} gửi chút cà phê cho {user_name}. ",
                              ]
        self.random_critizie = [
                "Vì thành tích công việc quá dở tệ, nên {title} {person} đã kêu {user_name} vào phòng riêng để làm việc lại về thái độ. ", 
                "Trong lúc làm việc, {title} {person} đã thấy {user_name} chểnh mảng và làm hư đồ tùm lum, gây hại cho nhân loại. ",
                "Trong lúc test lệnh trong server {server_name}, {user_name} đã spam quá nhiều và bị {title} {person} phát hiện và báo cáo admin. ",
                "Để gáng hoàn thành KPI, {user_name} đã không từ thủ đoạn bỉ ổi nào, và đã bị chính quyền server {server_name} phát giác. ",
                "Vì không hoàn thành KPI đăng content trong server {server_name}, {title} {person} quyết định phạt {user_name} một chút để làm gương. ",
                "Vì chuyên gia quậy phá và spam trong {server_name}, {title} {person} đã quyết định giam thưởng và trừ lương {user_name}. ",
                "Vì liên tục spam không ngừng trong {server_name}, {user_name} đã bị chính quyền tiễn vong lương thưởng. ",
                "Là thành viên đáy xã hội trong server {server_name}, {user_name} đã vi phạm luật và bị admin trừng phạt. ",
                "Nhờ việc lảm nhảm trong server {server_name}, nên {title} {person} quyết định giam lương và trừ tiền {user_name}. ",
                                ]
    
    @commands.command()
    async def work(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            
            embed, view = await self.embed_work_command(user=message.author)
            mes = await message.reply(embed=embed, view=view)
            if view != None:
                view.message = mes
            return
    
    #region work
    @discord.app_commands.command(name="work", description="Lệnh lao động trong server!")
    async def work_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        embed, view = await self.embed_work_command(user=interaction.user)
        mess = await interaction.followup.send(embed=embed)
        if view != None:
            view.message = mess
        return
        
    async def embed_work_command(self, user: discord.Member):
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        
        if user_profile != None and user_profile.last_work != None:
            time_window = timedelta(hours=1, minutes=30)
            check = self.check_if_within_time_delta(input=user_profile.last_work, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào 1h30 xem chừng nào mới làm việc được tiếp
                work_next_time = user_profile.last_work + time_window
                unix_time = int(work_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã làm việc rồi. Vui lòng thực hiện lại lệnh {SlashCommand.WORK.value} vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                return embed, view
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                return embed, None
            else:
                ProfileMongoManager.update_jail_time(guild_id=user.guild.id, user_id=user.id, jail_time=None)
        
        authority_user = ProfileMongoManager.is_authority(guild_id=user.guild.id, user_id= user.id)
        dignity_point = 50
        tax = 80
        pay_tax = True
        bonus = False
        
        if user_profile != None and user_profile.dignity_point != None:
            dignity_point = user_profile.dignity_point
            if user_profile.dignity_point == 0: 
                #Gian Thượng Đại Đạo không cần trả thuế, nhưng cũng không được bonus
                pay_tax = False
                bonus = False
            else:
                dignity_rate = int(user_profile.dignity_point/10)
                if dignity_rate == 0:
                    #Không thể trốn thuế, nhưng chắc chắn bonus
                    pay_tax = True
                    bonus = True
                else:
                    #Roll tỉ lệ trốn thuế dựa trên rate và tỉ lệ bonus dựa trên dignity_rate
                    dice_tax_evade = random.randint(0, 10)
                    if dignity_rate <= dice_tax_evade:
                        #Có thể trốn thuế
                        pay_tax = False
                    #Roll tỉ lệ bonus dựa trên rate và tỉ lệ bonus dựa trên dignity_rate
                    dice_bonus = random.randint(0, 10)
                    if dignity_rate >= dice_bonus:
                        bonus = True
        base_money = 600
        base_authority_money = 2
        text_authority = ""
        if authority_user!=None:
            text_authority = f" và **{2}** {CurrencyEmoji.SILVER.value}"
        base_text = f"Hôm nay bạn đã làm việc chăm chỉ, và nhận được **{base_money}** {CurrencyEmoji.COPPER.value}{text_authority}! "
        #random thêm để xem có được cộng trừ bonus không
        chance = random.randint(0, 10)
        if chance >= 5:
            #Dựa vào bonus để cộng hoặc trừ
            if bonus:
                text = self.get_bonus_message(True, user.guild.name, user.mention)
                base_text += text
                #Cộng thêm tiền dựa trên phần trăm của điểm dignity point
                bonus_money = int(base_money/dignity_point*10)
                base_money += bonus_money
                base_text += f"Bạn được cộng thêm {bonus_money} {CurrencyEmoji.COPPER.value}! "
            else:
                text = self.get_bonus_message(False, user.guild.name, user.mention)
                base_text += text
                #Trừ tiền dựa trên phần trăm của điểm dignity point
                bonus_money = int(base_money/dignity_point*10)
                base_money -= bonus_money
                base_text += f"Bạn bị trừ {bonus_money} {CurrencyEmoji.COPPER.value}! "
        
        #dựa vào Pay_tax để xác định trốn thuế hay đóng thuế
        text_tax = f"Là công dân gương mẫu nên bạn đã đóng thêm thuế {tax} {CurrencyEmoji.COPPER.value}."
        if pay_tax:
            base_money -= tax
            text_tax = f"\nLà công dân gương mẫu nên bạn đã đóng thêm thuế {tax} {CurrencyEmoji.COPPER.value}."
        else:
            text_tax = f"\nVới chút tài mọn, bạn đã trốn đóng thuế thành công."
        
        
        
        if base_money == 0: base_money = 300
        base_text += text_tax
        base_text += f"\n\n> Tổng tiền nhận từ {SlashCommand.WORK.value} hôm nay: **{base_money}** {CurrencyEmoji.COPPER.value}{text_authority}."
        
        #Cộng tiền, cộng 2 điểm nhân phẩm
        ProfileMongoManager.update_profile_money(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper=base_money)
        ProfileMongoManager.update_dignity_point(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point=2)
        #Cộng thuế cho chính quyền
        if pay_tax:
            ProfileMongoManager.update_money_authority(guild_id=user.guild.id, copper= tax)
        ProfileMongoManager.update_last_work_now(guild_id=user.guild.id, user_id=user.id)
        
        #Cộng thêm cho chính quyền
        if authority_user != None:
            ProfileMongoManager.update_money_authority(guild_id=user.guild.id, silver=base_authority_money)
        
        #Cập nhập level progressing
        ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id= user.id)
        
        embed = discord.Embed(title=f"", description=f"{base_text}", color=0x1ae8e8)
        return embed, None
        
        
    def check_if_within_time_delta(self, input: datetime, time_window: timedelta):
        now = datetime.now()
        if now - time_window <= input <= now + time_window:
            return True
        else:
            return False
    
    def get_bonus_message(self, is_add_bonus, server_name: str, user_name: str):
        title = random.choice(self.random_title_at_work)
        person = random.choice(self.random_user)
        if is_add_bonus:
            text = random.choice(self.random_praise)
        else:
            text = random.choice(self.random_critizie)
        text = text.replace("{title}", title)
        text = text.replace("{person}", person)
        text = text.replace("{server_name}", server_name)
        text = text.replace("{user_name}", user_name)
        return text
        