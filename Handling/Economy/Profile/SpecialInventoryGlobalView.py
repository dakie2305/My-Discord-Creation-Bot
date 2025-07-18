import discord
from Handling.Economy.Global.GlobalInventoryClass import GlobalItem
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List
from Handling.Economy.Inventory_Shop.ItemClass import Item
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from datetime import datetime, timedelta
import random


class SpecialInventoryGlobalView(discord.ui.View):
    def __init__(self, profile: Profile, global_inventory: GlobalItem, profile_embed: discord.Embed = None):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
        self.profile_embed = profile_embed
        self.global_inventory = global_inventory
    
    async def on_timeout(self):
        #Delete
        if self.message != None: 
            #Disable
            for item in self.children:
                if isinstance(item, discord.ui.Button):
                    item.disabled = True
                if isinstance(item, discord.ui.Select):
                    item.disabled = True
            try:
                await self.message.edit(view=None)
            except Exception:
                return
    
    @discord.ui.button(label="Profile", style=discord.ButtonStyle.primary)
    async def profile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.profile_embed != None:
            #Chuyển về embed cũ
            await self.message.edit(embed=self.profile_embed, view = None)
            return

    @discord.ui.button(label="Kho Đồ Liên Thông", style=discord.ButtonStyle.blurple)
    async def global_inventory_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        unix_time = int(self.global_inventory.enable_until.timestamp())
        date_display = f"<t:{unix_time}:d>"
        embed_color = 0xffffff
        if isinstance(self.profile.profile_color, int) and 0x000000 <= self.profile.profile_color <= 0xFFFFFF:
            embed_color = self.profile.profile_color
        embed = discord.Embed(title="", description=f"**Kho Đồ Liên Thông của <@{self.profile.user_id}>**", color=embed_color)
        embed.add_field(name=f"Số lượng vật phẩm: {len(self.global_inventory.list_items)}", value=f"", inline=True)
        embed.add_field(name=f"Hết hạn truy cập vào: {date_display}", value=f"", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        for item in self.global_inventory.list_items:
            embed.add_field(name=f"", value=f"{item.emoji} - {item.item_name} (x{item.quantity})", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Đừng quên, bạn chỉ được giữ tối đa 10 vật phẩm trong Kho Đồ Liên Thông, mỗi loại vật phẩm chỉ tối đa 99 cái thôi nhé!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        await self.message.edit(embed=embed, view=None)
        await interaction.followup.send(f"Bạn đã chuyển sang Kho Đồ Liên Thông!", ephemeral=True)
        return