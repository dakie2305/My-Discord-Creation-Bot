import discord
from discord.ext import commands
import PIL
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import db.DbMongoManager as db
import CustomFunctions
import os
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1


class StickyMessageHandling():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def handling_sticky_message(self, message: discord.Message):
        if message.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
        if message.author.bot: return
        #Hiện tại chỉ cho True Heaven thôi
        #Xoá cũ và send lại cái mới
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
        mess = await message.channel.send(embed=embed)
        
        guild_extra_info = db.find_guild_extra_info_by_id(guild_id=message.guild.id)
        if guild_extra_info != None:
            if guild_extra_info.custom_parameter_1 != None:
                #Kiểm tra và xoá message cũ
                try:
                    old_mess = await message.channel.fetch_message(guild_extra_info.custom_parameter_1)
                    if old_mess != None: await old_mess.delete()
                except Exception: print()
            data_updated = {"custom_parameter_1": mess.id, "custom_parameter_2": mess.channel.id}
            db.update_guild_extra_info(guild_id=message.guild.id, update_data= data_updated)
        return