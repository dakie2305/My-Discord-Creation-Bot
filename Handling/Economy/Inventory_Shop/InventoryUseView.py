import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from  Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items

class InventoryUseView(discord.ui.View):
    def __init__(self, user_profile: Profile, target_profile: Profile, user: discord.Member, target_user: discord.Member):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.user_profile = user_profile
        self.target_profile = target_profile
        self.user = user
        self.target_user = target_user
        self.add_item(ItemSelect(user, user_profile.list_items, self))
        self.selected_item: Item = None
        self.use_button = discord.ui.Button(label="🖲️ Sử Dụng Vật Phẩm", style=discord.ButtonStyle.green)
        self.use_button.callback = self.use_button_callback
        self.add_item(self.use_button)

    async def on_timeout(self):
        if self.message != None: 
            try:
                await self.message.delete()
            except Exception: return
            return
    
    async def use_button_callback(self, interaction: discord.Interaction):
        if self.selected_item == None: return
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f'Bạn đã dùng vật phẩm [{self.selected_item.emoji} - **{self.selected_item.item_name}**]', ephemeral=True)
        if self.message != None: 
            await self.message.delete()
            
        
class ItemSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_item: List[Item], view: "InventoryUseView"):
        options = [
            discord.SelectOption(label=f"{item.item_name} (x{item.quantity})", description=item.item_description[:97] + '...', value=item.item_id)
            for item in list_item if item.item_type != "gift"
        ]
        super().__init__(placeholder="Chọn vật phẩm muốn dùng", options=options)
        self.list_item = list_item
        self.parent_view  = view
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        selected_item_id = self.values[0]
        selected_item = next(item for item in self.list_item if item.item_id == selected_item_id)
        self.parent_view.selected_item = selected_item
        await interaction.followup.send(f'Bạn đã chọn chọn vật phẩm {selected_item.emoji} - **{selected_item.item_name}**', ephemeral=True)