import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from  Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items

class InventorySellView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member, rate: float = 1.0):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.rate = rate
        self.user_profile = user_profile
        self.user = user
        self.add_item(ItemSelect(user, user_profile.list_items, self))
        self.selected_item: Item = None
        self.sell_button = discord.ui.Button(label="💵 Bán Vật Phẩm", style=discord.ButtonStyle.green)
        self.sell_button.callback = self.sell_button_callback
        self.add_item(self.sell_button)
        
    async def on_timeout(self):
        if self.message != None: 
            try:
                await self.message.delete()
            except Exception: return
            return
    
    async def sell_button_callback(self, interaction: discord.Interaction):
        if self.selected_item == None: return
        if interaction.user.id != self.user.id: return
        await interaction.response.send_modal(TextSellInventoryInputModal(rate=self.rate, current_item=self.selected_item, user=self.user))        
        return

class ItemSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_item: List[Item], view: "InventorySellView"):
        options = [
            discord.SelectOption(label=f"{item.item_name} (x{item.quantity})", description=item.item_description[:97] + '...', value=item.item_id)
            for item in list_item
        ]
        super().__init__(placeholder="Chọn vật phẩm muốn bán", options=options)
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

# Create a custom modal for text input
class TextSellInventoryInputModal(discord.ui.Modal):
    def __init__(self, user: discord.Member, current_item: Item, rate: float = 1.0):
        super().__init__(title="Chọn số lượng vật phẩm mà bạn muốn bán đi")
        self.rate = rate
        self.user = user
        self.current_item = current_item
        self.input_amount_field = discord.ui.TextInput(
            label="Nhập số lượng muốn bán",
            placeholder="VD: 1, 2, 3, 4,...",
            required=True,
            default = "1",
            max_length=2
        )
        self.add_item(self.input_amount_field)
    
    async def on_submit(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        profile_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if profile_user == None:
            await interaction.followup.send(f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        
        #Kiểm tra xem item đó còn không
        check_fail = True
        item_remaining_quantity = 1
        for player_item in profile_user.list_items:
            if player_item.item_id == self.current_item.item_id and player_item.quantity > 0:
                check_fail = False
                item_remaining_quantity = player_item.quantity
                break
        if check_fail:
            await interaction.followup.send(f'Vật phẩm {self.current_item.emoji} - **{self.current_item.item_name}** đã không còn trong túi đồ của bạn!')
            return
        
        #Nhận 50% giá trị * rate hiện tại của shop
        input_amount_field = self.input_amount_field.value
        try:
            amount = int(input_amount_field)
            if amount <= 0:
                await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=False)
                return
            #Nếu số quá cao thì bán hết
            if amount > item_remaining_quantity: amount = item_remaining_quantity
            sell_money = int(amount * (self.current_item.item_worth_amount * self.rate / 2))
            if sell_money == 0: sell_money = 1
            
            if self.current_item.item_worth_type == "C":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper=sell_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, copper=-sell_money)
            elif self.current_item.item_worth_type == "S":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=sell_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, silver=-sell_money)
            elif self.current_item.item_worth_type == "G":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=sell_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=-sell_money)
            elif self.current_item.item_worth_type == "D":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium=sell_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, darkium=-sell_money)
            #Xoá khỏi inventory
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, item=self.current_item, amount=-amount)
            
            await interaction.followup.send(f"{interaction.user.mention} đã bán x{amount} [{self.current_item.emoji} - **{self.current_item.item_name}**] và nhận được **{sell_money}** {self.get_emoji_money_from_type(self.current_item.item_worth_type)}", ephemeral=False)
            return
            
            
        except ValueError:
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=False)
            return
        
    def get_emoji_money_from_type(self, type: str):
        if type == "C": return EmojiCreation2.COPPER.value
        if type == "S": return EmojiCreation2.SILVER.value
        if type == "G": return EmojiCreation2.GOLD.value
        if type == "D": return EmojiCreation2.DARKIUM.value