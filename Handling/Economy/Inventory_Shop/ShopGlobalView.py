import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
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
        if(self.total_pages == 1):
            self.next_button.disabled = True
            self.prev_button.disabled = True
        elif self.current_page + 1 == self.total_pages:
            #Trang cuối, ẩn nút next
            self.next_button.disabled = True
            self.prev_button.disabled = False
        elif self.current_page == 0:
            #Trang đầu, ẩn nút prev
            self.next_button.disabled = False
            self.prev_button.disabled = True
        else:
            self.next_button.disabled = False
            self.prev_button.disabled = False
    
    def create_embed(self):
        shop_name = self.keys[self.current_page]
        items = self.list_all_shops[shop_name]
        self.current_list_item = items
        # Tạo embed cho shop
        embed = discord.Embed(title=f"**{shop_name}**", description=f"Tỷ giá hiện tại: **{self.rate}**", color=discord.Color.blue())
        embed.add_field(name=f"", value=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬",inline=False)
        count = 1
        for item in items:
            embed.add_field(name=f"`{count}` {item.emoji} - {item.item_name}", value=f"{EmojiCreation2.SHINY_POINT.value} Giá: **{int(item.item_worth_amount*self.rate)}**{self.get_emoji_money_from_type(type=item.item_worth_type)}\n{EmojiCreation2.SHINY_POINT.value} Rank tối thiểu: **{item.rank_required}**\n{EmojiCreation2.SHINY_POINT.value} {item.item_description}",inline=False)
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
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="Mua", style=discord.ButtonStyle.green)
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextShopInputModal(rate=self.rate, message=self.message, current_list_item=self.current_list_item))
        return

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        
    async def on_timeout(self):
        if self.message != None:
            try:
                await self.message.delete()
            except Exception:
                return

# Create a custom modal for text input
class TextShopInputModal(discord.ui.Modal):
    def __init__(self, current_list_item: List[Item],message: discord.Message, rate: float = 1.0):
        super().__init__(title="Chọn mã vật phẩm mà bạn muốn mua")
        self.rate = rate
        self.message: discord.Message = message
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
            if item.item_id == "cuff" and profile_user.is_authority == False:
                await interaction.followup.send(f"Chỉ có Chính Quyền mới được mua còng tay!", ephemeral=True)
                return
            
            #rank phải đủ như tối thiểu
            if profile_user.level < item.rank_required:
                await interaction.followup.send(f"Bạn phải nâng rank mình lên trên **{item.rank_required}** để mua vật phẩm {item.emoji}!", ephemeral=True)
                return
            #Kiểm tra phải vũ khí huyền thoại không
            legend_check = False
            if "legend_" in item.item_id:
                legend_check = True
                amount = 1
                
            cost_money = amount * int(item.item_worth_amount*self.rate)
            
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
            
            money_for_authority = int(cost_money/2)
            if money_for_authority == 0: money_for_authority = 1
            
            if item.item_worth_type == "C":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, copper=money_for_authority)
            elif item.item_worth_type == "S":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, silver=money_for_authority)
            elif item.item_worth_type == "G":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=money_for_authority)
            elif item.item_worth_type == "D":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, darkium=money_for_authority)
            
            if "legend_" in item.item_id:
                new_worth_amount = int(item.item_worth_amount/2)
                item.item_worth_amount = new_worth_amount
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, item=item, amount=amount)

            maintenance_text = ""
            maintenance_money = 3500
            maintenance_emoji = EmojiCreation2.COPPER.value

            if item.item_worth_type == "D" and profile_user.darkium > 30:
                maintenance_money = 1
                maintenance_emoji = EmojiCreation2.DARKIUM.value
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium=-maintenance_money)
            elif item.item_worth_type == "D" and profile_user.darkium < 30:
                #Sẽ lấy 500 gold
                maintenance_money = 500
                maintenance_emoji = EmojiCreation2.GOLD.value
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=-maintenance_money)
            elif item.item_worth_type == "G":
                #mặc định 5% giá trị của item
                maintenance_money = int(cost_money * 5 / 100)
                maintenance_emoji = EmojiCreation2.GOLD.value
                if maintenance_money <= 0: maintenance_money = 1
                if maintenance_money > 10000: maintenance_money = 10000
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=-maintenance_money)
            elif item.item_worth_type == "S":
                #mặc định 10% giá trị của item
                maintenance_money = int(cost_money * 10 / 100)
                maintenance_emoji = EmojiCreation2.SILVER.value
                if maintenance_money <= 0: maintenance_money = 100
                if maintenance_money > 80000: maintenance_money = 80000
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=-maintenance_money)
            else:
                #mặc định copper
                #mặc định 20% giá trị của item
                maintenance_money = int(cost_money * 20 / 100)
                if maintenance_money < 3500: maintenance_money = 3500
                if maintenance_money > 200000: maintenance_money = 200000
                maintenance_emoji = EmojiCreation2.COPPER.value
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper=-maintenance_money)
                
            maintenance_text = f"\nNgoài ra, {interaction.user.mention} phải đóng thuế VAT là **{maintenance_money}** {maintenance_emoji}!"
            authority_text = f"Chính Quyền đã nhận được **{money_for_authority}** {self.get_emoji_money_from_type(item.item_worth_type)}!"
            if profile_user.is_authority == True:
                authority_text = ""
            await interaction.followup.send(f"{interaction.user.mention} đã chọn mua **{amount}** [{item.emoji}- **{item.item_name}**] với giá {cost_money} {self.get_emoji_money_from_type(item.item_worth_type)}! {authority_text}{maintenance_text}", ephemeral=False)
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
            if legend_check:
                if self.message != None: await self.message.delete()
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