from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
import random
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from db.DbMongoManager import GuildExtraInfo
import db.DbMongoManager as db

async def setup(bot: commands.Bot):
    await bot.add_cog(LiXiCog(bot=bot))
    print("Li Xi is ready!")

class LiXiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.random_wish = [
            "Chúc {user_name} Vạn sự như ý - An khang thịnh vượng!", 
            "Chúc {user_name} một năm mới phát đạt, niềm vui tràn đầy, tình duyên nồng ấm, thành công mỗi ngày!",
            "Chúc {user_name} một năm mới tiền đầy túi, tim đầy tình, xăng đầy bình, gạo đầy lu, muối đầy hũ, vàng đầy tủ, sức khỏe đầy đủ!",
            "Chúc {user_name} một năm mới vạn sự như ý, tỷ sự như mơ, làm việc như thơ, đời vui như nhạc, chung thủy với cơm và sắc son với phở!",
            "Năm mới xin chúc {user_name} tiền tiêu thoải mái, hạnh phúc dài dài!",
            "Năm mới xin chúc {user_name} mọi điều tốt đẹp lên. Chúc nhà thêm hạnh phúc, phú quý mãi kề bên. An khang luôn rực rỡ, vui sống trọn niềm tin!",
            "Xuân về vạn lộc, xin chúc {user_name} công việc hanh thông, tình yêu rực rỡ, phú quý thành công!",
            "Năm mới phú quý, xin chúc {user_name} tài lộc tràn tay, công việc thăng tiến, hạnh phúc đủ đầy, tình yêu rực rỡ, phú quý đại lộc!",
            "Cầu chúc {user_name} tết này may mắn, tài lộc ngập tràn, phúc về muôn ngả, xuân sang bình an!",
            "Cầu chúc {user_name} trẻ mãi không già, vui tươi như Tết, dịu dàng như xuân!",
            "Mong {user_name} tiền vào như nước sông Đà, tiền ra nhỏ giọt như cà phê phin!",
            "Mong {user_name} năm mới ăn sung mặc sướng, tiền rủng rỉnh túi, tình rủng rỉnh tim!",
            "Mong {user_name} năm mới sức khỏe dồi dào. Gia đình luôn được ấm no, yên vui!",
            "Năm cũ qua đi, năm mới đã tới. Chúc {user_name} bầu trời sức khỏe, biển cả tình thương, đại dương tình bạn, sự nghiệp sáng ngời, gia đình thịnh vượng!",
            "Năm mới chúc {user_name} thực hiện được những dự định còn dang dở, quen thêm những người bạn mới, đến những vùng đất mới!",
            "Năm mới chúc {user_name} đau đầu vì nhà giàu. Mệt mỏi vì học giỏi. Buồn phiền vì nhiều tiền. Ngang trái vì xinh gái. Mệt mỏi vì đẹp trai. Và mất ngủ vì không có đối thủ!",
            "Năm mới chúc {user_name} 12 tháng phú quý, 365 ngày phát tài, 8.760 giờ sung túc, 525.600 phút thành công và 31.536.000 giây mã đáo!",
            "Tết này chúc {user_name} tiền vào mạnh như voi, tiền ra nhẹ như kiến, sức khỏe dai như đỉa!",
            "Tết này chúc {user_name} tiền vào cửa trước, tiền ra cửa sau. Hai cái gặp nhau chui vào két sắt, một phần mua đất, một phần mua vàng, vẫn còn rủng rỉnh!",
            "Tết này chúc {user_name} xuân đến rạng ngọc ngà, tết đến thêm thịnh vượng, an khang khắp mọi nhà. Tài lộc đầy tay tới, hạnh phúc mãi thiết tha!",
                              ]
    
    @commands.command()
    async def li_xi(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            
            today = datetime.today()
            start_date = datetime(today.year, 1, 29)  # Mùng 1
            end_date = datetime(today.year, 1, 31)    # Mùng 3
            if not (start_date <= today <= end_date):
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Chưa đến lúc!", description=f"Lệnh `!li_xi` chỉ có thể dùng được trong Mùng 1 Tết Âm Lịch đến Mùng 3 Tết Âm Lịch, nhằm ngày 29/01 - 31/01",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
                
            check_exist = db.find_guild_extra_info_by_id(int(ctx.guild.id))
            if check_exist == None: 
                data = GuildExtraInfo(guild_id=ctx.guild.id, guild_name= ctx.guild.name, allowed_ai_bot=False)
                db.insert_guild_extra_info(data)
            check_exist = db.find_guild_extra_info_by_id(int(ctx.guild.id))
            if check_exist == None:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Gặp vấn đề trong lúc tạo Guild Extra Info. Vui lòng liên hệ Darkie để được hỗ trợ!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            list_li_xi = []
            if check_exist!= None and check_exist.list_li_xi != None and len(check_exist.list_li_xi)>0:
                #Kiểm tra xem có user_id trong đây chưa
                if message.author.id in check_exist.list_li_xi:
                    view = SelfDestructView(timeout=30)
                    embed = discord.Embed(title=f"Bạn đã nhận được lì xì rồi, mỗi người chỉ được nhận duy nhất một lần!",color=discord.Color.blue())
                    mess = await message.reply(embed=embed, view=view)
                    view.message = mess
                    return
            
            user_profile = ProfileMongoManager.find_profile_by_id(guild_id=message.guild.id, user_id=message.author.id)
            if user_profile == None:
                user_profile = ProfileMongoManager.create_profile(guild_id=message.author.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name)
            if user_profile == None:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Vui lòng tạo profile của bản thân trong server bằng lệnh {SlashCommand.PROFILE.value} trước đi đã!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            #Dựa vào điểm nhân phẩm để xác định là nhận darkium hay gold
            #Điểm nhân phẩm càng thấp thì càng có cơ hội cao nhận darkium
            caculated_chance = user_profile.dignity_point - 100
            if caculated_chance < 0: caculated_chance = caculated_chance * (-1)
            if caculated_chance > 85: caculated_chance = 85
            if caculated_chance < 45: caculated_chance = 15
            
            emoji = EmojiCreation2.GOLD.value
            dice_darkium = UtilitiesFunctions.get_chance(caculated_chance)
            if dice_darkium:
                #random trong khoảng
                allowed_values = [1, 2, 5, 10, 20, 30, 40, 50, 60, 70,80,90,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
                amount = random.choice(allowed_values)
                ProfileMongoManager.update_profile_money(guild_id=message.author.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, darkium=amount)
                emoji = EmojiCreation2.DARKIUM.value
            else:
                #random trong khoảng
                allowed_values = [1000, 2000, 3000, 4000, 5000, 7500, 8000, 9000, 10000, 15000, 12000, 13000, 17000, 18000, 19000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 60000, 70000, 80000, 90000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 55000, 600000, 650000, 700000, 800000, 900000, 1000000]
                amount = random.choice(allowed_values)
                ProfileMongoManager.update_profile_money(guild_id=message.author.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, gold=amount)
            list_li_xi = check_exist.list_li_xi
            list_li_xi.append(message.author.id)
            data_updated = {"list_li_xi": list_li_xi}
            db.update_guild_extra_info(guild_id=message.guild.id, update_data= data_updated)
            embed = discord.Embed(title=f"", description=f"**{EmojiCreation2.LIXI.value} Lì Xì Tài Lộc {EmojiCreation2.LIXI.value}**", color=0x69f5ee)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"- Với **{user_profile.dignity_point}** điểm nhân phẩm, {message.author.mention} đã bốc lì xì!", inline=False)
            embed.add_field(name=f"", value=f"- Số tiền bốc lì xì nhận được:", inline=False)
            embed.add_field(name=f"", value=f"> 🔥 ||**{amount} {emoji}**|| 🔥", inline=False)
            random_text = random.choice(self.random_wish)
            random_text = random_text.replace("{user_name}", message.author.mention)
            embed.add_field(name=f"", value=f"- {random_text}", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.set_footer(text=f"Nhận lì xì bằng lệnh\n!li_xi", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            await message.channel.send(embed=embed, content=message.author.mention)
            
            
            
            