
import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import EmojiCreation2
from datetime import datetime, timedelta
from db.Class.CustomClass import UserInfo
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
from Handling.Economy.Inventory_Shop.ItemClass import Item

class CouplePairView(discord.ui.View):
    def __init__(self, user: discord.Member, user_profile: Profile, target: discord.Member, target_profile: Profile, chosen_gift: Item):
        super().__init__(timeout=60)
        self.old_message: discord.Message = None
        self.user = user
        self.user_profile = user_profile
        self.target = target
        self.target_profile = target_profile
        self.chosen_gift = chosen_gift
    
    async def on_timeout(self):
        await self.old_message.edit(view=None, content=f"Rất tiếc, {self.target.mention} đã không trả lời bạn, có lẽ người ấy không thích bạn rồi!")
        return
        
    @discord.ui.button(label="❤️ Chấp nhận", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target.id: return
        await interaction.response.defer(ephemeral=True)
        CoupleMongoManager.create_couple(guild_id=interaction.guild_id, guild_name=interaction.guild.name, first_user_id=self.user.id, first_user_name=self.user.name, first_user_display_name=self.user.display_name, second_user_id=self.target.id, second_user_name=self.target.name, second_user_display_name=self.target.display_name)
        #Chuyển item từ người này sang người kia
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item= self.chosen_gift, amount= -1)
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, item= self.chosen_gift, amount= 1)
        await interaction.followup.send(content=f"Bạn đã chấp nhận lời bày tỏ của {self.user.mention}!", ephemeral=True)
        text = f"Chúc mừng {self.user.mention}! {self.target.mention} đã đồng ý lời bày tỏ và vật phẩm [{self.chosen_gift.emoji} - **{self.chosen_gift.item_name}**]  của bạn, và cả hai đã kết thành đôi!"
        await self.old_message.edit(content=text, view=None, embed= None)
        return
    
    @discord.ui.button(label="💔 Từ chối", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.target.id: return
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f"Bạn đã từ chối lời bày tỏ của {self.user.mention}!", ephemeral=True)
        text = f"Rất tiếc, {self.user.mention}! {self.target.mention} chỉ xem bạn là bạn bè mà thôi!"
        await self.old_message.edit(content=text, view=None, embed= None)
        return
        