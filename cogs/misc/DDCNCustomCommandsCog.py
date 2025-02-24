import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import db.DbMongoManager as db
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1

async def setup(bot: commands.Bot):
    await bot.add_cog(DDCNCustomCommandsCog(bot=bot))
    print("DDCN Custom Commands Cog is ready!")

class DDCNCustomCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    #region rule
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def rule_ddcn(self, ctx):
        message: discord.Message = ctx.message
        if message:
            if message.author.id != 315835396305059840:
                mess = await message.channel.send(f"Đây là lệnh đặc biệt, vui lòng không dùng.")
                await asyncio.sleep(3)
                await mess.delete()
                return
            embed = discord.Embed(title=f"", description=f"**ĐẠO LUẬT SERVER ĐẠI ĐẠO CHI NGUYÊN**", color=0x03F8FC)
            embed.add_field(name="", value="-----------------------------------------------------------------------------------")
            count = 1
            embed.add_field(name=f"**{count}. Không spam tin nhắn rác, invite link, scam link**\n**   (Do not spam, post invite link, scam link,...)**", value=f"\n- Spammer là cút server, không nói nhiều. Để nhắn invite link tuyệt đối phải xin phép trước để tránh bay mà vô cớ.\n- *(Invite link, scam link will result in immediate ban with no unban, spamming will resulted in jail or kicked)*", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Nhắn đúng chỗ, đúng nơi, đúng người**\n**   (Find right place, right channel, suitable channel for your message)**", value=f"\n- Server cực kỳ thoáng, nhưng không phải bạ đâu nhắn đấy. Hãy nhắn đúng chỗ, đúng nơi, đúng channel. Chat thường ra chất thường, chat NSFW ra đúng chỗ NSFW.\n- *(We do not restrict your freedom of speech, but please only chat at suitable channel. Normal chat in lobbly channel, NSFW chat in NSFW channel, bot spam at bot channel)*", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Không gạ gẫm dưới bất kỳ hình thức**\n**   (Do not ever sexting, asking for private pictures of members in this server without their consent)**", value=f"\n- Tuyệt đối nghiêm cấm các hành vi gạ gẫm, dâm dê và hạ nhục user khác dưới bất kỳ hình thức nào. Ai cảm thấy người nào đang làm phiền thì lập tức gọi Admin để giải quyết!\n- *(Immediately contact Admins of the server if there is someone tried to pester you for private, sensitive information without consent)*", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Không chửi nhau, hay toxic vô cớ**\n**   (Do not randomly insulting or being toxic to eachother)**", value=f"\n- Chúng ta đều là con người, và ai cũng có cảm xúc, đừng có đổ hết cảm xúc tiêu cực lên đầu đối phương.\n- *(We are all human, decent being, so don't just dump all your problems on others)*", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Admin, moderator là luật**\n**   (Admins, moderators represent the rule)**", value=f"\n- Muốn khiếu nại vui lòng liên hệ thẳng lên chủ server nếu cảm thấy oan ức hoặc bức xúc vì hành vi, hành động của bất kỳ admin hoặc mod nào.\n- *(Contact Server Master if encounter any abusing Moderator or Admin, or if you feel unjust with their judgements)*", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Không gây hấn về chủ đề chính trị, vùng miền, hay phân biệt vùng miền, quốc gia, giới tính...**\n**   (Do not being aggressive, hostile, radical, discriminate about politic, regions, countries, genders...)**", value=f"\n- Những chủ đề này cực kỳ nhạy cảm, luôn có chừng mực, luôn luôn để ý miệng mồm. Cảm thấy gây hấn thì nên ngậm mồm luôn đừng nói cho đỡ gây chuyện.\n- *(Those topics are really sensitive and could offense many people. It is best avoided if situation escalating quickly and immediately contact Moderators or Admins and just shut it)*", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Nghiêm cấm tuyệt đối những nội dung sau**\n**   (Forbidden topic, content)**", value=f"🚫 Bất kỳ hình ảnh, video, nội dung có liên quan đến trẻ em và truyền tải thông điệp xấu dưới bất kỳ hình thức nào.\n(Do not ever post anything bad related to minors. Do not even mentions them) \n\n🚫 Gay lọ đời thật (đừng có giở giọng gay quyền ở đây).\n  (Do not ever post anything bad related to gay. And no, I don't care about your opinions)\n\n🚫 Những nội dung tởm lợm, máu me, nghi ngờ tam quan khác.*\n  (Do not ever post gore or questionable contents)", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Nghiêm cấm tuyệt đối những nội dung NSFW, có khuynh hướng phản cảm hoặc 18+**\n**   (NSFW or 18+ content is forbidden)**", value=f"🚫 Không được phép đăng tải bất kỳ nội dung đồi truỵ, phản cảm hoặc 18+ dù có lộ ít hay nhiều.", inline=False)
            
            count+=1
            embed.add_field(name=f"**{count}. Nghiêm cấm tài khoản để tên, hoặc hình ảnh phản cảm, hoặc 18+**\n**   (Accounts showing inappropriate content are forbidden)**", value=f"🚫 Tài khoản không được phép để tên hoặc hình ảnh nhạy cảm hoặc vi phạm tiêu chuẩn cộng đồng", inline=False)
            embed.add_field(name="\n", value="\n",inline=False)

            unix_time = int(datetime.now().timestamp())
            embed.add_field(name="", value=f"Update: <t:{unix_time}:D>", inline=False)
            embed.set_footer(text=f"{message.author.name}", icon_url=message.author.avatar.url)
            
            embed_2 = discord.Embed(title=f"KHÁNG CÁO", description=f"Nếu đã bị ban từ trước thì làm cách nào để được xin unban?", color=0xfc0703)
            embed_2.add_field(name="", value="-----------------------------------------------------------------------------------")
            embed_2.add_field(name=f"\n", value=f"\n- Bạn có thể nhắn tin các Admin hoặc Mod (Bắt buộc phải kết bạn với bạn từ trước, hoặc dùng acc khác để nhắn vào server) để xin unban. \n*(You need to send friend request to Admin/Mod in advance, or just different account to ask for unban)*", inline=False)
            embed_2.add_field(name=f"\n", value=f"\n- Tùy vào trường hợp, hành vi, mức độ nặng nhẹ của vi phạm, sự trung thực và hối lỗi của bạn thì dàn Admin hoặc Mod có thể xem xét ân xá cho bạn, hoặc không. \n*(Whether you are to be unbanned or not depend on your attitude, and the severity of the ban case)*", inline=False)
            embed_2.add_field(name=f"\n", value=f"\n- Quyết định của các Admin và Mod là quyết định cuối cùng, và Chủ Server hoàn toàn có thể thay đổi quyết định và mức độ xử phạt khi member vi phạm các luật đã nói trên. \n*(Server Owner has every rights to change ultimate decision, and everything falls into their hands)*", inline=False)
            embed_2.add_field(name="-----------------------------------------------------------------------------------", value="**Các Admin và Moderator sẽ xử lý theo đúng điều luật bên trên, và thậm chí có thể Kick/Ban nếu vi phạm nặng mà không cần cảnh báo trước!**\n*(Admins and Moderators can enforce their rule according to the rules, even KICK/BAN without forewarning!)*", inline=False)
            
            await message.channel.send(embed=embed)
            await message.channel.send(embed=embed_2)