import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from datetime import datetime, timedelta
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from Handling.MiniGame.SortWord import SwClass, SwHandling, SwMongoManager, SwView

async def setup(bot: commands.Bot):
    await bot.add_cog(MatchWordCog(bot=bot))
    print("Matching Word game is ready!")

class MatchWordCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    