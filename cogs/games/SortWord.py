import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from datetime import datetime, timedelta
from mini_game.SortWord import SwClass, SwHandling, SwMongoManager

async def setup(bot: commands.Bot):
    await bot.add_cog(SortWords(bot=bot))
    print("Sort Word game is ready!")

class SortWords(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def check_if_message_inside_game(self, source: discord.Message):
        if source == None: return None, None
        langs = ['en', 'vn']
        for lan in langs:
            check = SwMongoManager.find_sort_word_info_by_id(lang=lan, guild_id=source.guild.id, channel_id= source.channel.id)
            if check!=None:
                return check, lan
        return None, None
    
    #region start sort word Commands
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def start_sw_en(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Kiểm tra xem đã tồn tại game trong channel này chưa
            if SwMongoManager.find_sort_word_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, lang='en'):
                #Xoá game
                SwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang='en')
                await ctx.send(f"Đã xoá trò chơi đoán chữ trong channel này.")
            #Không tạo trong channel đoán từ tiếng việt
            elif SwMongoManager.find_sort_word_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, lang='vn'):
                await ctx.send(f"Channel này đã dành cho game đoán từ Tiếng Việt rồi!")
            else:
                #Tạo mới
                data = SwClass.SortWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="hi", unsorted_word="ih")
                result = SwMongoManager.create_info(data=data, guild_id=message.guild.id, lang='en')
                message_tu_hien_tai = f"\nTừ hiện tại: `'{data.unsorted_word}'`."
                await ctx.send(f"Đã tạo trò chơi đoán chữ tiếng Anh cho channel này. Hãy bắt đầu đoán đi. {message_tu_hien_tai}")
            return
        
    #region reset
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def reset_sw(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Kiểm xem có game Sort Word ở đây không
            sw_info, lan = await self.check_if_message_inside_game(source=message)
            if sw_info == None:
                await message.channel.send(f"Không tìm được trò chơi sắp xếp từ để xoá trong channel này")
                return
            await self.process_reset(message=message, sw_info=sw_info, language=lan)
            return
        
    async def process_reset(self, message: discord.Message, sw_info: SwClass.SortWordInfo, language: str):
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Sắp Xếp Từ", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 0
        if sw_info.player_profiles:
            sw_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for index, profile in enumerate(sw_info.player_profiles):
                user = message.guild.get_member(profile.user_id)
                if user != None and (profile.point!= 0 or len(profile.special_items)> 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 25: break
        await message.channel.send(content=f"Chúc mừng các player top đầu! <@315835396305059840> sẽ trao role đặc biệt cho những Player thuộc top 3 nhé!", embed=embed)
        #Xoá đi tạo lại
        SwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang=language)
        
        #Tạo lại
        data = SwClass.SortWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="hi", unsorted_word="ih")
        result = SwMongoManager.create_info(data=data, guild_id=message.guild.id, lang='en')
        message_tu_hien_tai = f"\nTừ hiện tại: `'{data.unsorted_word}'`."
        await message.channel.send(f"Đã reset trò chơi trong channel này. {message_tu_hien_tai}")