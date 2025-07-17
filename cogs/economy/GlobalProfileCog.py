from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
from typing import List, Optional, Dict
from Handling.Economy.GA.GuardianAngelAttackClass import GuardianAngelAttackClass
from Handling.Economy.GA.ConfirmSellGuardianView import ConfirmSellGuardianView
from Handling.Economy.GA.GaSellOptionsMenuView import GaSellOptionsMenuView
from Handling.Economy.GA.RankUpView import RankUpView
from Handling.Economy.GA.GaBattleView import GaBattleView
import random
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from discord.app_commands import Choice
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum


async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalCog(bot=bot))
    print("Global Profile is ready!")

class GlobalCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    global_group = discord.app_commands.Group(name="global", description="Các lệnh liên quan đến Global!")
    #region ga sell slash
    @global_group.command(name="inventory", description="Chuyển giao vật phẩm từ kho đồ cá nhân sang kho đồ liên server!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def global_inventory_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        #Xuất view chọn lấy đồ từ kho liên server hoặc chuyển đồ từ kho cá nhân sang kho liên server
        
    
    @global_inventory_slash_command.error
    async def global_inventory_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    