from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from CustomEnum.RoleEnum import TrueHeavenRoleId
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
from typing import List, Optional, Dict
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items
from Handling.Economy.Inventory_Shop.ShopGlobalView import ShopGlobalView


async def setup(bot: commands.Bot):
    await bot.add_cog(ShopEconomy(bot=bot))
    print("Shop Economy is ready!")

class ShopEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.list_all_shops: Dict[str, List[Item]] = {}
    
    shop_group = discord.app_commands.Group(name="shop", description="Các lệnh liên quan đến Shop Item!")
    #region shop slash
    @shop_group.command(name="global", description="Hiển thị các mặt hàng trong thị trường toàn cầu")
    @discord.app_commands.checks.cooldown(1, 10)
    async def shop_global_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        #View đầu tiên luôn là gift shop
        self.list_all_shops["Shop Quà Tặng Cuộc Sống"] = list_gift_items
        
        keys = list(self.list_all_shops.keys())  # Shop names
        
        # Tạo embed cho shop
        embed = discord.Embed(title=f"**Shop Quà Tặng Cuộc Sống**", description=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬", color=discord.Color.blue())
        count = 1
        for item in self.list_all_shops["Shop Quà Tặng Cuộc Sống"]:
            embed.add_field(name=f"`{count}` {item.emoji} - {item.item_name}", value=f"{EmojiCreation2.SHINY_POINT.value} Giá: **{item.item_worth_amount}**{self.get_emoji_money_from_type(type=item.item_worth_type)}\n{EmojiCreation2.SHINY_POINT.value} {item.item_description}",inline=False)
            embed.add_field(name=f"", value=f"\n",inline=False)
            count+=1
        embed.set_footer(text=f"Trang 1/{len(keys)}")
        view = ShopGlobalView(list_all_shops= self.list_all_shops)
        view.current_list_item = self.list_all_shops["Shop Quà Tặng Cuộc Sống"]
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
        view.message = mess
        
    @shop_global_slash_command.error
    async def shop_global_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
        
    def get_emoji_money_from_type(self, type: str):
        if type == "C": return EmojiCreation2.COPPER.value
        if type == "S": return EmojiCreation2.SILVER.value
        if type == "G": return EmojiCreation2.GOLD.value
        if type == "D": return EmojiCreation2.DARKIUM.value
