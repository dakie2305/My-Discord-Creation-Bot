import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import EmojiCreation2
from datetime import datetime, timedelta
from db.Class.CustomClass import UserInfo
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
from Handling.Economy.Couple.CoupleClass import Couple
from Handling.Economy.Inventory_Shop.ItemClass import Item

class CoupleBreakupView(discord.ui.View):
    def __init__(self, user: discord.Member, couple: Couple, target_id: int):
        super().__init__(timeout=60)
        self.old_message: discord.Message = None
        self.user = user
        self.couple = couple
        self.target_id = target_id
    
    async def on_timeout(self):
        await self.old_message.edit(view=None, content=f"Rất tiếc, <@{self.couple.second_user_id}> đã không trả lời bạn, có lẽ người ấy vẫn chưa sẵn sàng!")
        return
        
    @discord.ui.button(label="💔 Chấp nhận rời xa", style=discord.ButtonStyle.red)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.couple.first_user_id and interaction.user.id != self.couple.second_user_id: return
        if interaction.user.id != self.target_id: return
        
        await interaction.response.defer(ephemeral=True)
        CoupleMongoManager.delete_couple_by_id(guild_id=interaction.guild_id, user_id=self.user.id)
        ProfileMongoManager.update_last_breakup_now(guild_id=interaction.guild_id, user_id=self.user.id)
        ProfileMongoManager.update_last_breakup_now(guild_id=interaction.guild_id, user_id=self.target_id)
        await interaction.followup.send(content=f"Bạn đã chấp nhận chia tay với {self.user.mention}!", ephemeral=True)
        text = f"💔 Cặp đôi <@{self.couple.first_user_id}> - <@{self.couple.second_user_id}> đã tan rã và không còn muốn bên nhau nữa!"
        await self.old_message.edit(content=text, view=None, embed=None)
        return
    