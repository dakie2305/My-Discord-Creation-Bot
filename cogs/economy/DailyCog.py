from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
        
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
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            
            embed = await self.embed_daily_command(user=message.author)
            await message.reply(embed=embed)
            return
    
    #region daily
    @discord.app_commands.command(name="daily", description="Điểm danh hằng ngày trong server!")
    async def daily_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
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
        
        if user_profile == None:
            user_profile = ProfileMongoManager.create_profile(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name)
        
        if user_profile != None:
            if user_profile.last_attendance != None and user_profile.last_attendance.date() == today:
                unix_time = int(tommorow.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã điểm danh xong hôm nay rồi, vui lòng đợi đến ngày mai <t:{unix_time}:D> !", color=0xc379e0)
                return embed
            
            #Không cho thực hiện nếu còn jail_time
            if user_profile.jail_time != None:
                if user_profile.jail_time > datetime.now():
                    unix_time = int(user_profile.jail_time.timestamp())
                    embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                    return embed
                else:
                    ProfileMongoManager.update_jail_time(guild_id=user.guild.id, user_id=user.id, jail_time=None)
            dignity_point = user_profile.dignity_point
            if user_profile.last_attendance != None and user_profile.last_attendance.date() == yesterday:
                consecutive_date = True
        
        #Cập nhật last_attendance
        ProfileMongoManager.update_last_attendance_now(guild_id=user.guild.id, user_id=user.id)
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        
        embed = discord.Embed(title=f"", description=f"**Điểm danh ngày thành công!**", color=0xc379e0)
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        #Tuỳ vào điểm nhân phẩm để cộng tiền, base là 500 * +- dignity point, và +5 nhân phẩm, nhân với level
        level_bonus = int(user_profile.level/20*500) if user_profile.level != None else 0
        base_money = 500 + level_bonus
        embed.add_field(name=f"", value=f"- Tiền điểm danh: +**{base_money}** {EmojiCreation2.COPPER.value}", inline=False)
        actual_money = 0
        if dignity_point >= 50:
            actual_money = base_money + int(base_money*dignity_point/100)
            embed.add_field(name=f"", value=f"- Điểm nhân phẩm {dignity_point}: +**{int(base_money*dignity_point/100)}** {EmojiCreation2.COPPER.value}", inline=False)
        else:
            rate = int(base_money*dignity_point/100)
            if rate == 0: rate = 400
            actual_money = base_money - rate
            embed.add_field(name=f"", value=f"- Điểm nhân phẩm {dignity_point}: -**{rate}** {EmojiCreation2.COPPER.value}", inline=False)
        if consecutive_date == True:
            actual_money += 200
            embed.add_field(name=f"", value=f"- Điểm danh hằng ngày: +**200** {EmojiCreation2.COPPER.value}", inline=False)
        if user_profile != None and user_profile.is_authority:
            actual_money += 3000
            embed.add_field(name=f"", value=f"- Là chính quyền tối cao: +**3000** {EmojiCreation2.COPPER.value}", inline=False)
        if user_profile != None and user_profile.daily_streak_count != None and user_profile.daily_streak_count > 0:
            #Mỗi một ngày daily là cộng 1000
            bonus_streak = 1000 * user_profile.daily_streak_count
            if bonus_streak > 60000: bonus_streak = 60000
            actual_money += bonus_streak
            embed.add_field(name=f"", value=f"- Đã điểm danh liên tiếp **{user_profile.daily_streak_count}** ngày liền: **{bonus_streak}** {EmojiCreation2.COPPER.value}", inline=False)
        
        #Đặc quyền server tổng
        if user.guild.id == 1256987900277690470:
            for role in user.roles:
                if role.id == TrueHeavenEnum.MODERATOR.value:
                    actual_money += 2000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.MODERATOR.value}> : +**2000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.CHOSEN_ONE.value:
                    actual_money += 1000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.CHOSEN_ONE.value}> : +**1000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.TOP_1_WORD_MATCHING.value or role.id == TrueHeavenEnum.TOP_1_WORD_SORT.value:
                    actual_money += 1500
                    embed.add_field(name=f"", value=f"- Là <@&{role.id}> : +**1500** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.TOP_1_WEALTH.value:
                    actual_money += 60000
                    embed.add_field(name=f"", value=f"- Là <@&{role.id}> : +**60000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.TOP_1_GUARDIAN.value:
                    actual_money += 60000
                    embed.add_field(name=f"", value=f"- Là <@&{role.id}> : +**60000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.TOP_2_WORD_MATCHING.value or role.id == TrueHeavenEnum.TOP_2_WORD_SORT.value:
                    actual_money += 1200
                    embed.add_field(name=f"", value=f"- Là <@&{role.id}> : +**1200** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.TOP_3_WORD_MATCHING.value or role.id == TrueHeavenEnum.TOP_3_WORD_SORT.value:
                    actual_money += 1000
                    embed.add_field(name=f"", value=f"- Là <@&{role.id}> : +**1000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_20.value:
                    actual_money += 500
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_20.value}> : +**500** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_30.value:
                    actual_money += 1000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_30.value}> : +**1000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_40.value:
                    actual_money += 2000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_40.value}> : +**2000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_50.value:
                    actual_money += 5000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_50.value}> : +**5000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_60.value:
                    actual_money += 10000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_60.value}> : +**10000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_70.value:
                    actual_money += 20000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_70.value}> : +**20000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_80.value:
                    actual_money += 40000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_80.value}> : +**40000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_90.value:
                    actual_money += 50000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_90.value}> : +**50000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_99.value:
                    actual_money += 65000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_99.value}> : +**65000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.RANK_100.value:
                    actual_money += 75000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.RANK_100.value}> : +**75000** {EmojiCreation2.COPPER.value}", inline=False)
                if role.id == TrueHeavenEnum.BOOSTER.value:
                    actual_money += 100000
                    embed.add_field(name=f"", value=f"- Là <@&{TrueHeavenEnum.BOOSTER.value}> : +**100000** {EmojiCreation2.COPPER.value}", inline=False)
        
        if actual_money == 0: actual_money = 200
        embed.add_field(name=f"", value=f"▬▬▬▬ι═════════>\n> Tổng tiền nhận từ điểm danh {SlashCommand.DAILY.value} hôm nay:   **+{int(actual_money)} {EmojiCreation2.COPPER.value} **", inline=False)
        embed.set_footer(text=f"{user.name} điểm danh.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        #Cộng tiền cho user
        ProfileMongoManager.update_profile_money(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name= user.display_name, copper=actual_money)
        
        #Nếu không phải chính quyền thì trừ tiền của chính quyền
        if user_profile!= None and user_profile.is_authority == False:
            ProfileMongoManager.update_money_authority(guild_id=user.guild.id, copper= -actual_money)
        
        #cộng 5 điểm dignity point
        ProfileMongoManager.update_dignity_point(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name= user.display_name, dignity_point=5)
        #Cập nhập level progressing
        ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id= user.id, bonus_exp=50)
        
        return embed
    
    def check_if_within_time_delta(self, input: datetime, time_window: timedelta):
        now = datetime.now()
        if now - time_window <= input <= now + time_window:
            return True
        else:
            return False