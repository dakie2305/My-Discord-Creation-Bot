
import discord
from typing import List, Optional
import string
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from discord.ext import commands
from CustomEnum.SlashEnum import SlashCommand 

class QuestHandling():
    def __init__ (self, bot: commands.Bot):
        self.bot = bot
        
    async def handling_quest_progress(self, message: discord.Message):
        if message.author.bot: return
        
        #Kiểm tra attachments
        if message.attachments and len(message.attachments)> 0:
            check_attachment_count = QuestMongoManager.increase_attachment_count(guild_id=message.guild.id, user_id=message.author.id, channel_id=message.channel.id, count=len(message.attachments))
            if check_attachment_count == True:
                quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
                await message.channel.send(embed=quest_embed, content=f"{message.author.mention}")
        
        if str.isspace(message.content): return
        if message.content and message.content[0] in string.punctuation and len(message.content) < 5: return
        if message.content and message.content[0] == ":" and len(message.content) < 3: return
        check_quest_message = QuestMongoManager.increase_message_count(guild_id=message.guild.id, user_id=message.author.id, channel_id=message.channel.id)
        if check_quest_message == True:
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            await message.channel.send(embed=quest_embed, content=f"{message.author.mention}")
        

        
        return