import discord
from discord.ext import commands
from discord import app_commands
from typing import List, Optional
import random

class ProfileView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.message: discord.Message = None