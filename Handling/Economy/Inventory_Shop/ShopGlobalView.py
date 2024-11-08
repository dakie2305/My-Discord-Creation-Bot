import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from  Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items

class ShopGlobalView(discord.ui.View):
    def __init__(self, rate: float = 1.0, list_all_shops: Dict[str, List[Item]] = {}):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.list_all_shops = list_all_shops
        self.keys = list(list_all_shops.keys())  # Shop names
        self.current_page = 0
        self.total_pages = len(self.keys)
        self.current_list_item: List[Item] = None
        self.rate = rate
        self.update_buttons()

    def update_buttons(self):
        self.next_button.disabled = self.current_page == self.total_pages - 1
        self.prev_button.disabled = self.current_page == 0
    
    def create_embed(self):
        shop_name = self.keys[self.current_page]
        items = self.list_all_shops[shop_name]
        self.current_list_item = items
        # Tạo embed cho shop
        embed = discord.Embed(title=f"**{shop_name}**", description=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬", color=discord.Color.blue())
        count = 1
        for item in items:
            embed.add_field(name=f"`{count}` {item.emoji} - {item.item_name}", value=f"{EmojiCreation2.SHINY_POINT.value} Giá: **{item.item_worth_amount}**{self.get_emoji_money_from_type(type=item.item_worth_type)}\n{EmojiCreation2.SHINY_POINT.value} {item.item_description}",inline=False)
            embed.add_field(name=f"", value=f"\n",inline=False)
            count+=1
        embed.set_footer(text=f"Trang {self.current_page + 1}/{self.total_pages}")
        return embed
    
    def get_emoji_money_from_type(self, type: str):
        if type == "C": return EmojiCreation2.COPPER.value
        if type == "S": return EmojiCreation2.SILVER.value
        if type == "G": return EmojiCreation2.GOLD.value
        if type == "D": return EmojiCreation2.DARKIUM.value
        
    
    
    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
            self.update_buttons()
    
    @discord.ui.button(label="Mua", style=discord.ButtonStyle.green)
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextShopInputModal(rate=self.rate, current_list_item=self.current_list_item))
        return

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
            self.update_buttons()
        
    async def on_timeout(self):
        if self.message != None: 
            await self.message.delete()
            return

# Create a custom modal for text input
class TextShopInputModal(discord.ui.Modal):
    def __init__(self, current_list_item: List[Item], rate: float = 1.0):
        super().__init__(title="Chọn mã vật phẩm mà bạn muốn mua")
        self.rate = rate
        self.current_list_item = current_list_item
        self.input_id_field = discord.ui.TextInput(
            label="Nhập số thứ tự của vật phẩm muốn mua",
            placeholder="VD: 1, 2, 3, 4,...",
            required=True,
            default = "1",
            max_length=2
        )
        self.input_amount_field = discord.ui.TextInput(
            label="Nhập số lượng",
            placeholder="VD: 1, 2, 3, 4,...",
            required=True,
            default = "1",
            max_length=2
        )
        self.add_item(self.input_id_field)
        self.add_item(self.input_amount_field)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        profile_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if profile_user == None:
            await interaction.followup.send(f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        input_id_field = self.input_id_field.value
        input_amount_field = self.input_amount_field.value
        try:
            item_id = int(input_id_field) - 1
            amount = int(input_amount_field)
            if item_id < 0 or amount <= 0:
                await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
                return
            if self.is_valid_index(item_id, self.current_list_item) == False:
                await interaction.followup.send(f"Id sản phẩm nhập vào không hợp lệ!", ephemeral=True)
                return
            item = self.current_list_item[item_id]
            
            cost_money = int(amount * self.rate * item.item_worth_amount)
            
            if item.item_worth_type == "C" and profile_user.copper < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.COPPER.value}!", ephemeral=True)
                return
            elif item.item_worth_type == "S" and profile_user.silver < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.SILVER.value}!", ephemeral=True)
                return
            elif item.item_worth_type == "G" and profile_user.gold < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.GOLD.value}!", ephemeral=True)
                return
            elif item.item_worth_type == "D" and profile_user.darkium < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.DARKIUM.value}!", ephemeral=True)
                return
            
            if item.item_worth_type == "C":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, copper=cost_money)
            elif item.item_worth_type == "S":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, silver=cost_money)
            elif item.item_worth_type == "G":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=cost_money)
            elif item.item_worth_type == "D":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, darkium=cost_money)
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, item=item, amount=amount)

            authority_text = f"Chính Quyền đã nhận toàn bộ số tiền trên!"
            if profile_user.is_authority == True:
                authority_text = ""
            await interaction.followup.send(f"{interaction.user.mention} đã chọn mua **{amount}** {item.emoji} với giá {cost_money} {self.get_emoji_money_from_type(item.item_worth_type)}! {authority_text}", ephemeral=False)
        except ValueError:
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
            return
        
    def is_valid_index(self, value: int, lst: list) -> bool:
        return 0 <= value < len(lst)
    def get_emoji_money_from_type(self, type: str):
        if type == "C": return EmojiCreation2.COPPER.value
        if type == "S": return EmojiCreation2.SILVER.value
        if type == "G": return EmojiCreation2.GOLD.value
        if type == "D": return EmojiCreation2.DARKIUM.value