import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from datetime import datetime, timedelta
import random

class ProfileToInventoryView(discord.ui.View):
    def __init__(self, profile: Profile):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
        
        if profile.list_items != None and len(profile.list_items)>0:
            self.profile_button = discord.ui.Button(label="Kho Đồ", style=discord.ButtonStyle.primary)
            self.profile_button.callback = self.inventory_button_function
            self.add_item(self.profile_button)
        if profile.plant != None:
            self.gard_button = discord.ui.Button(label="Khu Vườn", style=discord.ButtonStyle.primary)
            self.gard_button.callback = self.garden_button_function
            self.add_item(self.gard_button)
        
        if profile.guardian != None:
            self.guardian_button = discord.ui.Button(label="Hộ Vệ Thần", style=discord.ButtonStyle.primary)
            self.guardian_button.callback = self.guardian_button_function
            self.add_item(self.guardian_button)
        
        
    # @discord.ui.button(label="Kho Đồ", style=discord.ButtonStyle.primary)
    async def inventory_button_function(self, interaction: discord.Interaction):
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
    
    async def garden_button_function(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        time_window = timedelta(hours=self.profile.plant.hour_require)
        next_time = self.profile.plant.plant_date + time_window
        unix_time = int(next_time.timestamp())
        embed = discord.Embed(title="", description=f"**Vườn nhà của <@{self.profile.user_id}>**", color=0xddede7)
        embed.add_field(name=f"", value=f"Thông tin cây trồng", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"Hạt giống đang trồng: [{self.profile.plant.source_item.emoji} - **{self.profile.plant.source_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value=f"Tiến trình:", inline=False)
        embed.add_field(name=f"", value=f"{UtilitiesFunctions.progress_bar_plant(start_time=self.profile.plant.plant_date, end_time=next_time)}", inline=False)
        embed.add_field(name=f"", value=f"Thời gian thu hoạch: <t:{unix_time}:t>", inline=False)
        embed.add_field(name=f"", value=f"Sẽ thu hoạch được:", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} [{self.profile.plant.des_item.emoji} - **{self.profile.plant.des_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        view = InventoryBackToProfileView(profile=self.profile)
        m = await self.message.edit(embed=embed, view = view)
        view.message = m
        await interaction.followup.send(f"Bạn đã chuyển sang Khu Vườn!", ephemeral=True)

    async def guardian_button_function(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(title="", description=f"**Thông tin Hộ Vệ Thần của <@{self.profile.user_id}>**", color=0xddede7)
        embed.add_field(name=f"", value=f"{self.profile.guardian.ga_emoji} - **{self.profile.guardian.ga_name}**", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"Cấp bậc: **{UtilitiesFunctions.get_text_on_guardian_level(self.profile.guardian.level)}** [{self.profile.guardian.level}]", inline=False)
        embed.add_field(name=f"", value=f"Máu: \n{EmojiCreation2.HP.value}: {self.profile.guardian.max_health}", inline=True)
        embed.add_field(name=f"", value=f"Mana: \n{EmojiCreation2.MP.value}: {self.profile.guardian.max_mana}", inline=True)
        embed.add_field(name=f"", value=f"Thể lực: \n{EmojiCreation2.STAMINA.value}: {self.profile.guardian.max_stamina}", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        if self.profile.guardian.list_skills != None and len(self.profile.guardian.list_skills)>0:
            count = 0
            embed.add_field(name=f"", value=f"Đang sở hữu **{len(self.profile.guardian.list_skills)}** kỹ năng!", inline=False)
            for skill in self.profile.guardian.list_skills:
                embed.add_field(name=f"", value=f"[{skill.emoji} - **{skill.skill_name}**]", inline=True)
                count += 1
                if count > 6:
                    embed.add_field(name=f"", value=f"\nNgoài ra còn nhiều kỹ năng khác!", inline=False)
                    break
        embed.set_footer(text=f"Đừng quên, mọi Hộ Vệ Thần đều có tỉ lệ chết vĩnh viễn nếu trọng thương nhé!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/9e8749a5a47cae53211484d7aee42040.webp?size=100&quot")
        view = InventoryBackToProfileView(profile=self.profile)
        try:
            #Gắn link background dựa trên id của guardian nếu có
            urls = ListGAAndSkills.get_list_back_ground_on_ga_id(self.profile.guardian.ga_id)
            if urls != None and len(urls)>0:
                url = random.choice(urls)
                embed.set_image(url=url)
            m = await self.message.edit(embed=embed, view = view)
            view.message = m
            await interaction.followup.send(f"Bạn đã chuyển sang Hộ Vệ Thần!", ephemeral=True)
        except Exception:
            embed.set_image(url=None)
            m = await self.message.edit(embed=embed, view=view)
            view.message = m
            await interaction.followup.send(f"Bạn đã chuyển sang Hộ Vệ Thần!", ephemeral=True)
            return

    
    
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
