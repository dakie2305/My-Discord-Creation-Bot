import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView

async def setup(bot: commands.Bot):
    await bot.add_cog(BankEconomy(bot=bot))
    print("Bank Economy is ready!")

class BankEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
