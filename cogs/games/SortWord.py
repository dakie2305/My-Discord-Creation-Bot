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
    
    
    #region sort word Commands
    @discord.bot.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def start_sw_en(ctx):
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
                result = SwMongoManager.create_info(data=data, guild_id=message.guild.id, language='en')
                message_tu_hien_tai = f"\nTừ hiện tại: `'{data.unsorted_word}'`."
                await ctx.send(f"Đã tạo trò chơi đoán chữ tiếng Anh cho channel này. Hãy bắt đầu đoán đi. {message_tu_hien_tai}")
            return
        return