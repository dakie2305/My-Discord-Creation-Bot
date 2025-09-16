import discord
from discord.ext import commands
from discord.app_commands import Choice
from Handling.Misc.Remind import RemindMongoManager
from Handling.Misc.Remind.RemindListView import RemindListView
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
from datetime import datetime, timedelta

async def setup(bot: commands.Bot):
    await bot.add_cog(RemindCog(bot=bot))
    print("Remind Class is ready!")

class RemindCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    remind_group = discord.app_commands.Group(name="remind", description="Các lệnh liên quan đến nhắc nhở!")
    #region remind list
    @remind_group.command(name="list", description="Xem và chỉnh sửa các lời nhắc của bản thân liên server.")
    @discord.app_commands.checks.cooldown(1, 60)
    async def remind_list_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        #Hiển thị danh sách remind
        list_reminds = RemindMongoManager.find_all_reminds_by_user(user_id=interaction.user.id)
        if not list_reminds:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không có lời nhắc nào cả", description=f"", color=discord.Color.blue())
            embed.add_field(name="", value="Vui lòng tạo lời nhắc mới bằng lệnh\n`/remind create`.", inline=False)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        remind = list_reminds[0]
        embed = discord.Embed(title=f"", description=f"**Lời nhắc của {interaction.user.mention}**", color=discord.Color.blue())
        unix_time = int(remind.date_remind.timestamp())
        embed.add_field(name=f"Nội Dung", value=f"{remind.message_content}",inline=False)
        embed.add_field(name=f"Thời Gian Nhắc", value=f"<t:{unix_time}:f>",inline=False)
        embed.add_field(name=f"Kênh", value=f"Kênh **{remind.channel_name}** của Server **{remind.guild_name}**",inline=False)
        embed.set_footer(text=f"Trang 1/{len(list_reminds)}")
        view = RemindListView(user=interaction.user, list_reminds=list_reminds)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        return
            
    @remind_list_slash_command.error
    async def remind_list_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    #region remind ne
    @remind_group.command(name="create", description="Tạo các lời nhắc cho bản thân. Khi đến lúc, bot sẽ nhắc bạn ngay tại kênh này!")
    @discord.app_commands.checks.cooldown(1, 30)
    @discord.app_commands.choices(time_format=[
        Choice(name="Giây", value="second"),
        Choice(name="Phút", value="minute"),
        Choice(name="Giờ", value="hour"),
        Choice(name="Ngày", value="day"),
        Choice(name="Tuần", value="week"),
    ])
    @discord.app_commands.describe(time_format="Loại thời gian", time_number="Lượng thời gian", content="Nội dung lời nhắc")
    async def remind_create_slash_command(self, interaction: discord.Interaction, time_number: int, time_format: str, content: str):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Mỗi user chỉ được phép có tối đa 5 lời nhắc trong bất kỳ server nào
        #Trừ Darkie
        if interaction.user.id != UserEnum.UserId.DARKIE.value:
            count_remind = RemindMongoManager.count_reminds_by_user(user_id=interaction.user.id)
            if count_remind >= 5:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Bạn đã đạt giới hạn!", description="Mỗi người dùng chỉ được phép có tối đa **5** lời nhắc!", color=discord.Color.red())
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
        
        date_remind = self.get_remind_datetime(time_number=time_number, time_format=time_format)
        limit_date = datetime.now() + timedelta(weeks=38)
        if date_remind > limit_date:
            view = SelfDestructView(timeout=30)
            unix_time = int(limit_date.timestamp())
            embed = discord.Embed(title=f"Thời gian không hợp lệ!", description=f"Lời nhắc không được phép vượt quá ngày <t:{unix_time}:d>!", color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        remind = RemindMongoManager.create_or_update_remind(remind_id=None, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, guild_id=interaction.guild.id, guild_name=interaction.guild.name, channel_id=interaction.channel.id, channel_name=interaction.channel.name, message_content=content, date_remind=date_remind)
        unix_time = int(date_remind.timestamp())
        embed = discord.Embed(title=f"Tạo lời nhắc thành công!", description=f"", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"Vào lúc <t:{unix_time}:f> Creation bot sẽ nhắc bạn với nội dung sau:", inline=False)
        embed.add_field(name=f"", value=f"- **{content}**", inline=False)
        embed.add_field(name=f"", value=f"Tại Server {interaction.guild.name} tại kênh <#{interaction.channel.id}>", inline=False)
        await interaction.followup.send(content= f"{interaction.user.mention}",embed=embed, ephemeral=False)
        
    
    @remind_create_slash_command.error
    async def remind_create_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    
    def get_remind_datetime(self, time_number: int, time_format: str) -> datetime:
        now = datetime.now()
        if time_format == "second":
            return now + timedelta(seconds=time_number)
        elif time_format == "minute":
            return now + timedelta(minutes=time_number)
        elif time_format == "hour":
            return now + timedelta(hours=time_number)
        elif time_format == "day":
            return now + timedelta(days=time_number)
        elif time_format == "week":
            return now + timedelta(weeks=time_number)
        else:
            raise ValueError(f"Unknown time_format: {time_format}")
