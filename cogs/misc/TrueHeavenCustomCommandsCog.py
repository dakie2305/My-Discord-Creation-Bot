import discord
from discord import Object
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from CustomEnum import UserEnum
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from CustomEnum.UserEnum import UserId
import CustomFunctions
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Misc import DonatorMongoManager
from Handling.Misc.AppealJailView import AppealJailView
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import db.DbMongoManager as db
from db.Class.CustomClass import UserInfo
import db.DbMongoManager as db
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from discord.app_commands import Choice
import re

async def setup(bot: commands.Bot):
    await bot.add_cog(TrueHeavenCustomCommands(bot=bot))
    print("True Heaven Rule Embed is ready!")

class TrueHeavenCustomCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    #region rule
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def rule_true_heaven(self, ctx):
        message: discord.Message = ctx.message
        if message:
            if message.author.id != 315835396305059840:
                mess = await message.channel.send(f"Đây là lệnh đặc biệt, vui lòng không dùng.")
                await asyncio.sleep(3)
                await mess.delete()
                return
            embed = discord.Embed(title=f"", description=f"**TRUE HEAVENS RULES**", color=0x03F8FC)
            embed.add_field(name="", value="-----------------------------------------------------------------------------------")
            count = 1
            embed.add_field(name=f"**{count}. Không spam tin nhắn rác, invite link, scam link**\n**   (Do not spam, post invite link, scam link,...)**", value=f"\n- Spammer là cút server, không nói nhiều. Để nhắn invite link tuyệt đối phải xin phép trước để tránh bay mà vô cớ.\n- *(Invite link, scam link will result in immediate ban with no unban, spamming will resulted in jail or kicked)*", inline=False)
            embed.add_field(name="\n", value="\n")
            
            count+=1
            embed.add_field(name=f"**{count}. Nhắn đúng chỗ, đúng nơi, đúng người**\n**   (Find right place, right channel, suitable channel for your message)**", value=f"\n- Server cực kỳ thoáng, nhưng không phải bạ đâu nhắn đấy. Hãy nhắn đúng chỗ, đúng nơi, đúng channel. Chat thường ra chất thường, chat NSFW ra đúng chỗ NSFW.\n- *(We do not restrict your freedom of speech, but please only chat at suitable channel. Normal chat in lobbly channel, NSFW chat in NSFW channel, bot spam at bot channel)*", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Không gạ gẫm dưới bất kỳ hình thức**\n**   (Do not ever sexting, asking for private pictures of members in this server without their consent)**", value=f"\n- Còn cần phải giải thích à?\n- *(For fuck sake do I have to explain this to you?)*", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Không chửi nhau, hay toxic vô cớ**\n**   (Do not randomly insulting or being toxic to eachother)**", value=f"\n- Chúng ta đều là con người, và ai cũng có cảm xúc, đừng có đổ hết cảm xúc tiêu cực lên đầu đối phương.\n- *(We are all human, decent being, so don't just dump all your problems on others)*", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Admin, moderator là luật**\n**   (Admins, moderators represent the rule)**", value=f"\n- Muốn khiếu nại vui lòng liên hệ thẳng Server Master nếu cảm thấy oan ức hoặc bức xúc vì hành vi, hành động của bất kỳ admin, mod nào. Nếu khiếu nại hợp lý sẽ được phép thay thế vị trí của admin/mod vi phạm nếu đủ trình độ.\n- *(Contact Server Master if encounter any abusing Moderator or Admin, or if you feel unjust with their judgements)*", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Không gây hấn về chủ đề chính trị, vùng miền, hay phân biệt vùng miền, quốc gia, giới tính...**\n**   (Do not being aggressive, hostile, radical, discriminate about politic, regions, countries, genders...)**", value=f"\n- Những chủ đề này cực kỳ nhạy cảm, luôn có chừng mực, luôn luôn để ý miệng mồm. Cảm thấy gây hấn thì nên ngậm mồm luôn đừng nói cho đỡ gây chuyện.\n- *(Those topics are really sensitive and could offense many people. It is best avoided if situation escalating quickly and immediately contact Moderators or Admins and just shut it)*", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Biết chừng mực**\n**   (Behave)**", value=f"\n- Người khôn nên biết chừng mực.\n- *(Wise people know when to shut it)*", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Cấm nội dung phảm cảm với BOT Creation 1, Creation 2**\n**   (Inappropriate behavior with bot Creation 1 and bot Creation 2)**", value=f"\n- Riêng hai BOT Creation 1, Creation 2 vì là BOT chạy Gemini nên tốt nhất đừng nhắn phản cảm, sẽ gây ảnh hưởng đến Server Master. Còn những bot khác sẽ không áp dụng luật này..\n- *(BOT Creation 1, Creation 2 is Bot AI using Gemini, so do not try anything inappropriate or there will costly consequences. The rule does not applied to other bots)*", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Nghiêm cấm tuyệt đối những nội dung sau**\n**   (Forbidden topic, content)**", value=f"🚫 Bất kỳ hình ảnh, video, nội dung có liên quan đến trẻ em và truyền tải thông điệp xấu dưới bất kỳ hình thức nào.\n(Do not ever post anything bad related to minors. Do not even mentions them) \n\n🚫 Gay lọ đời thật (đừng có giở giọng gay quyền ở đây).\n  (Do not ever post anything bad related to gay. And no, I don't care about your opinions)\n\n🚫 Những nội dung tởm lợm, máu me, nghi ngờ tam quan khác.*\n  (Do not ever post gore or questionable contents)", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Nghiêm cấm tuyệt đối những nội dung NSFW, có khuynh hướng phản cảm hoặc 18+**\n**   (NSFW or 18+ content is forbidden)**", value=f"🚫 Không được phép đăng tải bất kỳ nội dung đồi truỵ, phản cảm hoặc 18+ dù có lộ ít hay nhiều. Nếu cảm thấy hình ảnh nhạy cảm, vui lòng dùng lệnh `/report` để admin và moderator giải quyết", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Nghiêm cấm tài khoản để tên, hoặc hình ảnh phản cảm, hoặc 18+**\n**   (Accounts showing inappropriate content are forbidden)**", value=f"🚫 Tài khoản không được phép để tên hoặc hình ảnh nhạy cảm hoặc vi phạm tiêu chuẩn cộng đồng", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)

            unix_time = int(datetime.now().timestamp())
            embed.add_field(name="", value=f"Update: <t:{unix_time}:D>", inline=False)
            embed.set_footer(text=f"{message.author.name}", icon_url=message.author.avatar.url)
            
            embed_2 = discord.Embed(title=f"XỬ LÝ VI PHẠM", description=f"BÁO CÁO NGƯỜI DÙNG VI PHẠM BẰNG LỆNH `/report` của Creation 1!", color=0xfc0703)
            embed_2.add_field(name="", value="-----------------------------------------------------------------------------------")
            embed_2.add_field(name=f"\n", value=f"\n- **Vi phạm lần một:** cảnh cáo / phạt tù 30 phút.\n- **Vi phạm lần hai:** phạt tù / mute theo ngày.\n- **Vi phạm lần ba:** CÚT.", inline=False)
            embed_2.add_field(name="\n", value="\n",inline=False)
            embed_2.add_field(name="-----------------------------------------------------------------------------------", value="**Các Admin và Moderator sẽ xử lý theo đúng điều luật bên trên, và thậm chí có thể Kick/Ban nếu vi phạm nặng mà không cần cảnh báo trước!**\n*(Admins and Moderators can enforce their rule according to the rules, even KICK/BAN without forewarning!)*", inline=False)
            
            
            await message.channel.send(embed=embed)
            await message.channel.send(embed=embed_2)

    #region sd_th
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def sd_th(self, ctx, user: discord.Member, *, text: str):
        message: discord.Message = ctx.message
        if message:
            if message.author.id != UserId.DARKIE.value:
                return
            channel = message.channel
            await message.delete()
            today = datetime.now()
            two_week = today + timedelta(weeks=2)
            unix_time = int(today.timestamp())
            unix_time_two_weeks_later = int(two_week.timestamp())
            embed = discord.Embed(title=f"", description=f"**NHIỆT LIỆT VINH DANH {user.mention}**", color=0x69f5ee)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"<t:{unix_time}:F>", inline=False)
            embed.add_field(name=f"", value=f"- Darkie xin chân thành cảm ơn mạnh thường quân {user.mention} ({user.display_name}), username: {user.name} đã donate Darkie nhằm giúp ủng hộ phát triển server và cả bot! Một số tiền dù có ra sao thì cũng rất hoan nghênh!", inline=False)
            embed.add_field(name=f"", value=f"- Sự ủng hộ của bạn chính là niềm vui, và cũng là niềm động lực để Darkie tiếp tục phát triển thêm nhiều thứ hay ho cho bot lẫn server!", inline=False)
            embed.add_field(name=f"", value=f"- Bạn đã nhận được role <@&{TrueHeavenEnum.DONATOR.value}> cho đến ngày <t:{unix_time_two_weeks_later}:D>!", inline=False)
            embed.add_field(name=f"", value=f"- Số tiền nhận được:", inline=False)
            embed.add_field(name=f"", value=f"> 🔥** {text} VNĐ** 🔥", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            await channel.send(embed=embed, content=user.mention)
            donation_amount = UtilitiesFunctions.extract_number(text=text)
            if donation_amount == None: donation_amount = 0
            DonatorMongoManager.create_or_update_profile(user_id=user.id, user_name= user.name, user_display_name= user.display_name, donation_amount=donation_amount)
            if message.guild.id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
                #Give role
                donator_role = message.guild.get_role(TrueHeavenEnum.DONATOR.value)
                if donator_role:
                    await user.add_roles(donator_role, reason="Donated to support Darkie.")
            return
            
    #region sticky partner posting
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def sticky_partner_rule(self, ctx):
        message: discord.Message = ctx.message
        if message:
            if message.author.id != 315835396305059840 or message.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
                return
            channel = message.channel
            
            await message.delete()
            count= 0
            embed = discord.Embed(title=f"", description=f"**QUY ĐỊNH PARTNER SERVER**", color=0x69f5ee)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**Server đối tác phải ít nhất trên 500 người tham gia thật, không tính bot**\n   (Partner servers will need to have at least 500 real members, not including bot)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**Server đối tác phải là server cộng đồng, công khai cho mọi người**\n   (Partner servers will have to be public Community Server)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**Server đối tác phải có khu dành cho Partner**\n   (Partner servers need to have Partnership's place to PR server)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**Đại diện server out coi như huỷ partner**\n   (If partner server's representative leaves, that means partnership will be dissolved)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**Chỉ được phép đăng tối đa hai lần một ngày để quảng bá server**\n   (Partner's representatives are only allowed PR servers twice per day)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**Đọc kỹ luật của True Heavens trước khi nhắn tin**\n   (At least read True Heavens' rule first before doing anything)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**🚫 Không gửi link invite server ra kênh khác ngoài kênh này để tránh bị ban**\n   (Posting server's invite link to any other channels will result in ban)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**🚫 Không chấp nhận server để ảnh bìa là NSFW**\n   (Servers with NSFW background are not allowed to be partner)**", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**🚫 Không chấp nhận server phân biệt đối xử hoặc để ảnh nhạy cảm, phân biệt**\n   (Discrimination, hate spreading servers are not allowed to be partner)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**🚫 Không chấp nhận server ba que, có member hoặc dấu hiện phản động**\n  (Fuck off, stupid ass)", inline=False)
            
            count+=1
            embed.add_field(name=f"Điều thứ {count}:", value=f"**🚫 Nghiêm cấp các server trade, buôn bán có dấu hiệu scam. True Heavens không chịu bất kỳ trách nhiệm cho hành vi mất mát**\n(Beware of scamming server)\n{EmojiCreation1.SHINY_POINT.value} Partner không có nghĩa là True Heavens sử dụng dịch vụ do Server Partner cung cấp, và không chịu trách nhiệm nếu Server Partner là scam. Hãy là người dùng thông minh, và đồ ngon không bao giờ rẻ", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            mess = await channel.send(embed=embed)
            
            guild_extra_info = db.find_guild_extra_info_by_id(guild_id=message.guild.id)
            if guild_extra_info != None:
                data_updated = {"custom_parameter_1": mess.id, "custom_parameter_2": mess.channel.id}
                db.update_guild_extra_info(guild_id=message.guild.id, update_data= data_updated)
            
    
    #region khang_tu
    @discord.app_commands.guilds(Object(id=TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value))
    @discord.app_commands.command(name="khang_tu", description="Bỏ tiền để nhờ luật sư kháng án tù!")
    async def khang_tu_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            embed = discord.Embed(title=f"", description=f"Bắt buộc phải dùng lệnh `/profile` trước.", color=0xddede7)
            embed.add_field(name=f"", value=f"Ngoài ra, bạn cần phải kiếm tiền mới đủ tiền kháng án tù!", inline=False)
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Trừ 5% số tiền lớn nhất, tối thiểu 100000 gold
        money_cost = 100000
        money_type = "G"
        flag_not_enough_money = False
        if user_profile.darkium > 100:
            money_cost = int(user_profile.darkium * 5 / 100)
            if money_cost > 10000000: money_cost = 10000000
            money_type = "D"
        elif user_profile.gold > 100000:
            money_cost = int(user_profile.gold * 5 / 100)
            money_type = "G"
        else:
            flag_not_enough_money = True
        if money_type == EmojiCreation2.GOLD.value and money_cost < 100000:
            flag_not_enough_money = True
        if flag_not_enough_money:
            embed = discord.Embed(title=f"", description=f"Không đủ tiền kháng án tù.", color=0xddede7)
            embed.add_field(name=f"", value=f"Bạn cần phải có ít nhất 100.000 Gold để bắt đầu kháng án tù!", inline=False)
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        #Hiện view xác nhận
        view = AppealJailView(user=interaction.user, guild_id=interaction.guild_id, money=money_cost, money_type=money_type)
        embed = discord.Embed(title=f"Kháng Án Tù", description=f"", color=0xddede7)
        embed.add_field(name=f"", value=f"Bạn có chấp nhận bỏ ra **{UtilitiesFunctions.shortened_currency(money_cost)}** {money_type} để bắt đầu kháng án tù?", inline=False)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess

    #region khang_tu prefix
    @commands.command()
    @commands.cooldown(rate=1, per=120.0, type=commands.BucketType.user)
    async def khang_tu(self, ctx):
        message: discord.Message = ctx.message
        if not message or message.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            return

        user: discord.Member = ctx.author
        guild_id: int = ctx.guild.id

        if CustomFunctions.check_if_dev_mode() and user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(
                title="Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",
                color=discord.Color.blue()
            )
            mess = await ctx.send(embed=embed, view=view)
            view.message = mess
            return

        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=guild_id, user_id=user.id)
        if user_profile is None:
            embed = discord.Embed(description="Bắt buộc phải dùng lệnh `/profile` trước.", color=0xddede7)
            embed.add_field(name="", value="Ngoài ra, bạn cần phải kiếm tiền mới đủ tiền kháng án tù!", inline=False)
            view = SelfDestructView(timeout=30)
            mess = await ctx.send(embed=embed, view=view)
            view.message = mess
            return
        # Tính tiền kháng án
        money_cost = 100000
        money_type = "G"
        flag_not_enough_money = False

        if user_profile.darkium > 100:
            money_cost = int(user_profile.darkium * 5 / 100)
            if money_cost > 10000000:
                money_cost = 10000000
            money_type = "D"
        elif user_profile.gold > 100000:
            money_cost = int(user_profile.gold * 5 / 100)
            money_type = "G"
        else:
            flag_not_enough_money = True
        if money_type == EmojiCreation2.GOLD.value and money_cost < 100000:
            flag_not_enough_money = True
        if flag_not_enough_money:
            embed = discord.Embed(description="Không đủ tiền kháng án tù.", color=0xddede7)
            embed.add_field(name="", value="Bạn cần phải có ít nhất 100.000 Gold để bắt đầu kháng án tù!", inline=False)
            view = SelfDestructView(timeout=30)
            mess = await ctx.send(embed=embed, view=view)
            view.message = mess
            return
        # Gửi view xác nhận
        view = AppealJailView(user=user, guild_id=guild_id, money=money_cost, money_type=money_type)
        embed = discord.Embed(title="Kháng Án Tù", color=0xddede7)
        embed.add_field(
            name="",
            value=f"Bạn có chấp nhận bỏ ra **{UtilitiesFunctions.shortened_currency(money_cost)}** {money_type} để bắt đầu kháng án tù?",
            inline=False
        )
        mess = await ctx.send(embed=embed, view=view)
        view.message = mess
        
    @khang_tu.error
    async def khang_tu_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(
                title="❗ Lỗi: Lệnh đang trong thời gian hồi",
                description=f"Hãy thử lại sau {round(error.retry_after, 1)} giây nữa.",
                color=discord.Color.red()
            )
            mess = await ctx.send(embed=embed, view=view)
            view.message = mess

    #region jail
    @discord.app_commands.guilds(Object(id=TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value))
    @discord.app_commands.command(name="jail", description="Tống ai đó vào đại lao trong khoảng thời gian nhất định!")
    @discord.app_commands.choices(time_format=[
        Choice(name="Giây", value="second"),
        Choice(name="Phút", value="minute"),
        Choice(name="Giờ", value="hour"),
        Choice(name="Ngày", value="day"),
        Choice(name="Tuần", value="week"),
        Choice(name="Tháng", value="month"),
    ])
    @discord.app_commands.describe(user= "Người cần tống giam", duration= "Thời gian tống giam (nhập số)", time_format = "Thời gian tống giam (second, minute, hour, day, week, month)", reason="Lý do tống giam")
    async def jail_slash_command(self, interaction: discord.Interaction, user : discord.Member, duration: int, time_format : str, reason : str):
        await interaction.response.defer(ephemeral=True)  # Defer the interaction early
        req_roles = ['Cai Ngục', 'Supervisor', 'Server Master', 'Moderator', 'Ultimate Admins']
        jail_db = "jailed_user"
        has_required_role = any(role.name in req_roles for role in interaction.user.roles)
        if not has_required_role:
            await interaction.followup.send("Không đủ thẩm quyền để tống giam.")
            return
        
        await interaction.followup.send(f"Bạn đã tống giam {user.mention} vào đại lao thành công!", ephemeral=True)
        channel = interaction.channel
        await self.jail_user(channel=channel, jailer=interaction.user, user=user, reason=reason, duration=duration, time_format=time_format, jail_db=jail_db)
        return
        
    async def jail_user(self, channel: discord.TextChannel, jailer:discord.Member, user: discord.Member, reason: str, duration: int, time_format: str, jail_db = 'jailed_user'):
        #Nếu là Bot thì lật ngược vị thế:
        temp_author = jailer 
        if user.bot:
            user = user
            user = temp_author
        
        # Calculate the end time
        end_time = datetime.now() + CustomFunctions.get_timedelta(duration, time_format)
        mordern_date_time_format = end_time.strftime(f"%d/%m/%Y %H:%M")

        
        #Tìm xem user này đã có chưa, chưa có thì insert
        search_user = db.find_user_by_id(user.id, jail_db)
        if search_user == None:
            # Save user's roles
            original_roles = [role for role in user.roles if not role.is_default() and not role.is_premium_subscriber()]
            stored_original_roles = []
            for role in original_roles:
                old_role = {
                                "role_id": role.id,
                                "role_name": role.name
                            }
                stored_original_roles.append(old_role)
            # Remove all roles and add jail role
            jail_role = discord.utils.get(user.guild.roles, name="Đáy Xã Hội")
            
            user_info = UserInfo(
                user_id=user.id,
                user_name=user.name,
                user_display_name=user.display_name,
                jailer_id = jailer.id,
                jailer_display_name= jailer.display_name,
                jailer_user_name= jailer.name,
                channel_id=channel.id,
                channel_name=channel.name,
                reason= reason,
                jail_until= end_time,
                roles=stored_original_roles
            )
            db.create_user(user_info= user_info, chosen_collection= jail_db)
        else:
            #Update lại jail_until và reason
            db.update_user_jail_time(user_id=user.id, jail_until=end_time, reason=reason, jailer_id= jailer.id, jailer_display_name= jailer.display_name, jailer_user_name= jailer.name)
        
        try:
            for ori_role in original_roles:
                try:
                    await user.remove_roles(ori_role)
                except Exception:
                    continue
            await user.add_roles(jail_role)
        except Exception as e:
            print(e)

        await channel.send(f"Kẻ tội độ {user.mention} đã bị {jailer.mention} bắt giữ và sẽ bị tống vào đại lao. Kẻ tội đồ này chỉ được thả ra xã hội sau {duration} {time_format}. Lý do tống giam: {reason}")
        embed = discord.Embed(title="Đại Lao Thẳng Tiến", description=f"Kẻ tội đồ {user.mention} đã bị {jailer.mention} bắt giữ và tống vào đại lao!", color=0x00FF00)  # Green color
        embed.add_field(name="Lý do bị tù đày:", value=reason, inline=False)  # Single-line field
        embed.add_field(name="Sẽ được ân xoá sau khoảng thời gian:", value=f"{duration} {time_format}", inline=False)
        embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
        embed.add_field(name="Ghi chú", value="Nếu quá thời hạn phạt tù mà chưa được ra tù thì hãy la làng lên nhé!", inline=False) 
        embed.add_field(name="Kháng tù", value="Dùng lệnh `!khang_tu` để kháng án tù! Lệnh này sẽ tốn nhiều tiền!", inline=False) 
        embed.set_footer(text=f"Đã bị tống giam bởi: {jailer.name}")  # Footer text

        channel = self.bot.get_channel(1257012036718563380)
        if channel:
            await channel.send(content=f"{user.mention}",embed=embed)
        print(f"Username {jailer.name}, Display user name {jailer.display_name} jailed {user.display_name} for {duration} {time_format}. Reason: {reason}")

    #region unjail
    @discord.app_commands.guilds(Object(id=TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value))
    @discord.app_commands.command(name="unjail", description="Ân xá tội đồ ra khỏi đại lao ngay lập tức!")
    @discord.app_commands.describe(user= "Người cần ân xá", reason = "Lý do tại sao ân xá")
    async def unjail_slash_command(self, interaction: discord.Interaction, user : discord.Member, reason : str):
        await interaction.response.defer()
        req_roles = ['Cai Ngục', 'Supervisor', 'Server Master', 'Moderator', 'Ultimate Admins']
        jail_db = "jailed_user"
        has_required_role = any(role.name in req_roles for role in interaction.user.roles)
        if not has_required_role:
            await interaction.followup.send("Không đủ thẩm quyền để ân xá tội đồ.")
            return
        
        #Xoá role Đáy Xã Hội
        jail_role = discord.utils.get(user.guild.roles, name="Đáy Xã Hội")
        if jail_role:
            await user.remove_roles(jail_role)
        
        #Tìm xem user này đã có chưa, có thì xoá khỏi db jail_user
        search_user = db.find_user_by_id(user.id, jail_db)
        if search_user:
            #Restore lại roles cũ của user
            for role in search_user.roles:
                get_role_from_server = discord.utils.get(user.guild.roles, id = role["role_id"])
                if get_role_from_server:
                    try:
                        await user.add_roles(get_role_from_server)
                    except Exception:
                        continue
            #Xoá row khỏi database
            db.delete_user_by_id(user_id= user.id, chosen_collection= jail_db)
            # Create embed object
            mordern_date_time_format = datetime.now().strftime(f"%d/%m/%Y %H:%M")
            embed = discord.Embed(title="Ân Xá Khỏi Đại Lao", description=f"Kẻ tội đồ {user.mention} đã được {interaction.user.mention} ân xoá khỏi đại lao!", color=0x00FF00)  # Green color
            embed.add_field(name="Lý do được ân xá:", value=reason, inline=False)  # Single-line field
            embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
            embed.add_field(name="Ghi chú", value="Nhớ đừng vi phạm để bị tống vài đại lao nữa nhé!", inline=False) 
            embed.set_footer(text=f"Đã được ân xoá bởi: {interaction.user.name}")  # Footer text

            await interaction.followup.send(f"Kẻ tội độ {user.mention} đã được {interaction.user.mention} ân xá đại lao. Mong thần dân đừng vi phạm để thành kẻ tội đồ nữa. Lý do ân xá: {reason}")
            channel = self.bot.get_channel(1257012036718563380)
            if channel:
                await channel.send(embed=embed)
        else:
            await interaction.followup.send(f"Người này không ở trong tù.", ephemeral=True)
        print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} unjailed {user.display_name}. Reason: {reason}")