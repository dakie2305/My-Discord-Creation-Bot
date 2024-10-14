from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import CurrencyEmoji
import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
        
async def setup(bot: commands.Bot):
    await bot.add_cog(DailyEconomy(bot=bot))
    print("Daily Economy is ready!")

class DailyEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def daily(self, ctx):
        message: discord.Message = ctx.message
        if message:
            embed = await self.embed_daily_command(user=message.author)
            await message.reply(embed=embed)
            return
    
    #region transfer
    @discord.app_commands.command(name="daily", description="Điểm danh hằng ngày trong server!")
    async def transfer_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        embed = await self.embed_daily_command(user=interaction.user)
        await interaction.followup.send(embed=embed)
        
    
    async def embed_daily_command(self, user: discord.Member):
        dignity_point = 50
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        consecutive_date = False
        consecutive_date_text = ""
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)
        tommorow = datetime.today() + timedelta(days=1)
        
        if user_profile != None:
            if user_profile.last_attendance != None and user_profile.last_attendance.date() == today:
                unix_time = int(tommorow.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã điểm danh xong hôm nay rồi, vui lòng đợi đến ngày mai <t:{unix_time}:D> !", color=0xc379e0)
                return embed
            
            dignity_point = user_profile.dignity_point
            if user_profile.last_attendance != None and user_profile.last_attendance.date() == yesterday:
                consecutive_date = True
        
        embed = discord.Embed(title=f"", description=f"**Điểm danh ngày thành công!**", color=0xc379e0)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        #Tuỳ vào điểm nhân phẩm để cộng tiền, base là 500 * +- dignity point, và +5 nhân phẩm
        base_money = 500
        embed.add_field(name=f"", value=f"- Tiền điểm danh: +**{base_money}** {CurrencyEmoji.COPPER.value}", inline=False)
        actual_money = 0
        if dignity_point >= 50:
            actual_money = base_money + int(base_money*dignity_point/100)
            embed.add_field(name=f"", value=f"- Điểm nhân phẩm {dignity_point}: +**{int(base_money*dignity_point/100)}** {CurrencyEmoji.COPPER.value}", inline=False)
        else:
            rate = base_money*dignity_point/100
            if rate == 0: rate = 400
            actual_money = base_money - rate
            embed.add_field(name=f"", value=f"- Điểm nhân phẩm {dignity_point}: -**{rate}** {CurrencyEmoji.COPPER.value}", inline=False)
        if consecutive_date == True:
            actual_money += 200
            embed.add_field(name=f"", value=f"- Điểm danh hằng ngày: +**200** {CurrencyEmoji.COPPER.value}", inline=False)
        if user_profile != None and user_profile.is_authority:
            actual_money += 600
            embed.add_field(name=f"", value=f"- Là chính quyền tối cao: +**600** {CurrencyEmoji.COPPER.value}", inline=False)
        if actual_money == 0: actual_money = 200
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"> Tổng tiền nhận từ điểm danh {SlashCommand.DAILY.value} hôm nay:   **+{int(actual_money)} {CurrencyEmoji.COPPER.value} **", inline=False)
        embed.set_footer(text=f"{user.name} điểm danh.", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
        #Cộng tiền cho user
        ProfileMongoManager.update_profile_money(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name= user.display_name, copper=actual_money)
        
        #Nếu không phải chính quyền thì trừ tiền của chính quyền
        if user_profile!= None and user_profile.is_authority == False:
            ProfileMongoManager.update_money_authority(guild_id=user.guild.id, copper= -actual_money)
        #Cập nhật last_attendance
        ProfileMongoManager.update_last_attendance_now(guild_id=user.guild.id, user_id=user.id)
        return embed