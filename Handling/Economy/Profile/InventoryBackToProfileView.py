import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class ProfileToInventoryView(discord.ui.View):
    def __init__(self, profile: Profile):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
        
    @discord.ui.button(label="Kho Đồ", style=discord.ButtonStyle.primary)
    async def inventory_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        embed = discord.Embed(title=f"", description=f"**Kho đồ của <@{self.profile.user_id}>**", color=0xddede7)
        embed.add_field(name=f"Số lượng vật phẩm: {len(self.profile.list_items)}", value=f"", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        for item in self.profile.list_items:
            embed.add_field(name=f"", value=f"{item.emoji} - {item.item_name} (x{item.quantity})", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Đừng quên, bạn chỉ được giữ tối đa 20 vật phẩm, mỗi loại vật phẩm chỉ tối đa 99 cái thôi nhé!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/9e8749a5a47cae53211484d7aee42040.webp?size=100&quot")
        view = InventoryBackToProfileView(profile=self.profile)
        m = await self.message.edit(embed=embed, view = view)
        view.message = m
        await interaction.followup.send(f"Bạn đã chuyển sang chế độ Kho Đồ!", ephemeral=True)

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
                await self.message.edit(view=self)
            except Exception:
                return
        
class InventoryBackToProfileView(discord.ui.View):
    def __init__(self, profile: Profile):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
    
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
                await self.message.edit(view=self)
            except Exception:
                return
    
    @discord.ui.button(label="Profile", style=discord.ButtonStyle.primary)
    async def profile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        if self.profile.is_authority and ProfileMongoManager.is_in_debt(data = self.profile, copper_threshold=100000):
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            self.profile.copper = -10000
            self.profile.silver = 0
            self.profile.gold = 0
            self.profile.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= interaction.guild_id, data=self.profile)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild_id)
            ProfileMongoManager.update_last_authority(guild_id=interaction.guild_id, user_id=self.profile)
            await self.message.edit(embed=embed)
            await interaction.followup.send(f"Bạn đã chuyển sang chế độ Profile!", ephemeral=True)
            return
        cq = ""
        if self.profile.is_authority:
            cq = "Chính Quyền Tối Cao"
        embed = discord.Embed(title=cq, description=f"**Profile <@{self.profile.user_id}>**", color=0xddede7)
        if self.profile.protection_item != None:
            embed.add_field(name=f"", value=f"Bảo Hộ Vật: [{self.profile.protection_item.emoji} - **{self.profile.protection_item.item_name}**]", inline=False)
        if self.profile.attack_item != None:
            embed.add_field(name=f"", value=f"Vũ Khí: [{self.profile.attack_item.emoji} - **{self.profile.attack_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value=f"Nhân phẩm: **{UtilitiesFunctions.get_nhan_pham(self.profile.dignity_point)}** ({self.profile.dignity_point})", inline=True)
        embed.add_field(name=f"", value=f"Địa Vị: **{UtilitiesFunctions.get_dia_vi(self.profile)}**", inline=True)
        embed.add_field(name=f"", value=f"Rank: **{self.profile.level}**", inline=False)
        bar_progress = self.progress_bar(input_value= self.profile.level_progressing)
        embed.add_field(name=f"", value=f"{bar_progress}\n", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"**Tổng tài sản**:", inline=False)
        show_darkium = f"{EmojiCreation2.DARKIUM.value}: **{UtilitiesFunctions.shortened_currency(self.profile.darkium)}**\n"
        if self.profile.darkium == 0:
            show_darkium = ""
        embed.add_field(name=f"", value=f">>> {show_darkium}{EmojiCreation2.GOLD.value}: **{UtilitiesFunctions.shortened_currency(self.profile.gold)}**\n{EmojiCreation2.SILVER.value}: **{UtilitiesFunctions.shortened_currency(self.profile.silver)}**\n{EmojiCreation2.COPPER.value}: **{UtilitiesFunctions.shortened_currency(self.profile.copper)}**", inline=False)
        #Quote
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"**Quote**: \"{self.profile.quote}\"", inline=False)
        embed.set_footer(text=f"Profile của {self.profile.user_name}.", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/9e8749a5a47cae53211484d7aee42040.webp?size=100&quot")
        await self.message.edit(embed=embed, view = None)
        await interaction.followup.send(f"Bạn đã chuyển sang chế độ Profile!", ephemeral=True)
        
    
    def progress_bar(self, input_value: int, total_progress: int = 1000, bar_length=15):
        # Calculate the percentage of progress
        percentage = (input_value / total_progress) * 100
        # Determine the number of filled (█) characters
        filled_length = int(bar_length * input_value // total_progress)
        # Create the progress bar string
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        # Format the output with percentage
        return f'{bar} **{int(percentage)}%**'
