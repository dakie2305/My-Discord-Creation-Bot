import discord
from discord.ext import commands
import CustomFunctions
import asyncio
import random
from Handling.Misc.SelfDestructView import SelfDestructView
from enum import Enum
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from CustomEnum.EmojiEnum import EmojiCreation2 

class AutoLevelupProfileHandling():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def handling_auto_level_up(self, message: discord.Message):
        #Không áp dụng cho bot
        if message.author.bot: return
        #Không áp dụng cho message quá ngắn
        if len(message.content.split()) < 4: return
        ProfileMongoManager.update_auto_level_progressing(guild_id=message.guild.id, user_id=message.author.id)
        return