import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items, list_plant, list_fishing_rod, PlantItem
import asyncio
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from datetime import datetime

class WorkPlantView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.user_profile = user_profile
        self.user = user
        self.add_item(ItemSelect(user, user_profile.list_items, self))
        self.selected_item: Item = None
        self.use_button = discord.ui.Button(label="🎋 Trồng Cây", style=discord.ButtonStyle.green)
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
        
        #Kiểm tra xem item đó còn không
        check_fail = True
        for player_item in self.user_profile.list_items:
            if player_item.item_id == self.selected_item.item_id and player_item.quantity > 0:
                check_fail = False
                break
        if check_fail:
            await interaction.followup.send(f'Hạt giống {self.selected_item.emoji} - **{self.selected_item.item_name}** đã không còn trong túi đồ của bạn!', ephemeral=True)
            return
        
        #Tìm id cây
        hour_require = 1
        source_id= self.selected_item.item_id
        des_id = "None"
        if source_id == "seed_wheat":
            des_id = "wheat"
        elif source_id == "seed_potato":
            des_id = "potato"
            hour_require = 2
        elif source_id == "seed_corn":
            des_id = "corn"
            hour_require =2
        elif source_id == "seed_watermelon":
            des_id = "watermelon"
            hour_require =3
        elif source_id == "seed_weed":
            des_id = "weed"
            hour_require =3
        item_source: Item = self.selected_item
        item_des: Item = None
        for item in list_plant:
            if item.item_id == des_id:
                item_des = item
                break
        if item_source == None or item_des == None:
            await interaction.followup.send(f'Có lỗi xảy ra, không thể tìm được thành quả của hạt giống [{self.selected_item.emoji} - **{self.selected_item.item_name}**]. Vui lòng liên hệ Darkie gấp', ephemeral=True)
            return
        data = PlantItem(hour_require=hour_require, plant_date=datetime.now(), source_item=item_source, des_item=item_des)
        ProfileMongoManager.update_plant(guild_id=interaction.guild_id, user_id=interaction.user.id, plant=data)
        #Trừ hạt giống
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=self.selected_item, amount= -1)
        if self.message != None: 
            await self.message.delete()
        await interaction.followup.send(f'Bạn đã gieo trồng hạt giống [{self.selected_item.emoji} - **{self.selected_item.item_name}**]', ephemeral=True)
    

class ItemSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_item: List[Item], view: "WorkPlantView"):
        options = [
            discord.SelectOption(label=f"{item.item_name} (x{item.quantity})", description=item.item_description[:97] + '...', value=item.item_id)
            for item in list_item if item.item_type == "seed"
        ]
        super().__init__(placeholder="Chọn hạt giống muốn trồng", options=options)
        self.list_item = list_item
        self.parent_view  = view
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        selected_item_id = self.values[0]
        selected_item = next(item for item in self.list_item if item.item_id == selected_item_id)
        self.parent_view.selected_item = selected_item
        await interaction.followup.send(f'Bạn đã chọn chọn hạt giống {selected_item.emoji} - **{selected_item.item_name}**', ephemeral=True)