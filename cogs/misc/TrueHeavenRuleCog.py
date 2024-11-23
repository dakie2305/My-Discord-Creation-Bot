import discord
from discord.ext import commands
import asyncio
from datetime import datetime

async def setup(bot: commands.Bot):
    await bot.add_cog(TrueHeavenRuleEmbed(bot=bot))
    print("True Heaven Rule Embed is ready!")

class TrueHeavenRuleEmbed(commands.Cog):
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
            

            unix_time = int(datetime.now().timestamp())
            embed.add_field(name="", value=f"Update: <t:{unix_time}:D>", inline=False)
            embed.set_footer(text=f"{message.author.name}", icon_url=message.author.avatar.url)
            
            embed_2 = discord.Embed(title=f"", description=f"**XỬ LÝ VI PHẠM**", color=0xfc0703)
            embed_2.add_field(name="", value="-----------------------------------------------------------------------------------")
            embed_2.add_field(name=f"\n", value=f"\n- **Vi phạm lần một:** cảnh cáo / phạt tù 30 phút.\n- **Vi phạm lần hai:** phạt tù / mute theo ngày.\n- **Vi phạm lần ba:** CÚT.", inline=False)
            embed_2.add_field(name="\n", value="\n",inline=False)
            embed_2.add_field(name="-----------------------------------------------------------------------------------", value="**Các Admin và Moderator sẽ xử lý theo đúng điều luật bên trên, và thậm chí có thể Kick/Ban nếu vi phạm nặng mà không cần cảnh báo trước!**\n*(Admins and Moderators can enforce their rule according to the rules, even KICK/BAN without forewarning!)*", inline=False)
            
            
            await message.channel.send(embed=embed)
            await message.channel.send(embed=embed_2)

    #region rule
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def sd_th(self, ctx, user: discord.Member, text: str):
        message: discord.Message = ctx.message
        if message:
            if message.author.id != 315835396305059840 or message.guild.id != 1256987900277690470:
                return
            channel = message.channel
            await message.delete()
            today = datetime.now()
            unix_time = int(today.timestamp())
            embed = discord.Embed(title=f"", description=f"**NHIỆT LIỆT VINH DANH {user.mention}**", color=0x69f5ee)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"<t:{unix_time}:F>", inline=False)
            embed.add_field(name=f"", value=f"- Darkie xin chân thành cảm ơn mạnh thường quân {user.mention} ({user.display_name}), username: {user.name} đã donate Darkie nhằm giúp ủng hộ phát triển server và cả bot! Một số tiền dù có ra sao thì cũng rất hoan nghênh!", inline=False)
            embed.add_field(name=f"", value=f"- Sự ủng hộ của bạn chính là niềm vui, và cũng là niềm động lực để Darkie tiếp tục phát triển thêm nhiều thứ hay ho cho bot lẫn server!", inline=False)
            embed.add_field(name=f"", value=f"- Số tiền nhận được:", inline=False)
            embed.add_field(name=f"", value=f"> 🔥** {text} VNĐ** 🔥", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            await channel.send(embed=embed, content=user.mention)