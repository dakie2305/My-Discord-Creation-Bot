import discord
from Handling.Economy.Global import GlobalMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.Profile.SpecialGuardianView import SpecialGuardianView
from Handling.Economy.Profile.SpecialInventoryGlobalView import SpecialInventoryGlobalView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from datetime import datetime, timedelta
import random

class ProfileAdditionalView(discord.ui.View):
    def __init__(self, profile: Profile, profile_embed: discord.Embed = None):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
        self.profile_embed = profile_embed
        
        if profile.list_items != None and len(profile.list_items)>0:
            self.inventory_button = discord.ui.Button(label="Kho Đồ", style=discord.ButtonStyle.primary)
            self.inventory_button.callback = self.inventory_button_function
            self.add_item(self.inventory_button)
            
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
        embed_color = 0xffffff
        if isinstance(self.profile.profile_color, int) and 0x000000 <= self.profile.profile_color <= 0xFFFFFF:
            embed_color = self.profile.profile_color
        embed = discord.Embed(title=f"", description=f"**Kho đồ của <@{self.profile.user_id}>**", color=embed_color)
        embed.add_field(name=f"Số lượng vật phẩm: {len(self.profile.list_items)}", value=f"", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        for item in self.profile.list_items:
            embed.add_field(name=f"", value=f"{item.emoji} - {item.item_name} (x{item.quantity})", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Đừng quên, bạn chỉ được giữ tối đa 20 vật phẩm, mỗi loại vật phẩm chỉ tối đa 99 cái thôi nhé!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        view = BackToProfileView(profile=self.profile, profile_embed=self.profile_embed)
        
        global_inventory = GlobalMongoManager.find_global_profile_by_id(user_id=interaction.user.id)
        if global_inventory != None and global_inventory.enable_until > datetime.now():
            view = SpecialInventoryGlobalView(profile=self.profile, global_inventory=global_inventory, profile_embed=self.profile_embed)
        m = await self.message.edit(embed=embed, view = view)
        view.message = m
        await interaction.followup.send(f"Bạn đã chuyển sang chế độ Kho Đồ!", ephemeral=True)
    
    async def garden_button_function(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        time_window = timedelta(hours=self.profile.plant.hour_require)
        next_time = self.profile.plant.plant_date + time_window
        unix_time = int(next_time.timestamp())
        embed_color = 0xffffff
        if isinstance(self.profile.profile_color, int) and 0x000000 <= self.profile.profile_color <= 0xFFFFFF:
            embed_color = self.profile.profile_color
        embed = discord.Embed(title="", description=f"**Vườn nhà của <@{self.profile.user_id}>**", color=embed_color)
        embed.add_field(name=f"", value=f"Thông tin cây trồng", inline=True)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"Hạt giống đang trồng: [{self.profile.plant.source_item.emoji} - **{self.profile.plant.source_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value=f"Tiến trình:", inline=False)
        embed.add_field(name=f"", value=f"{UtilitiesFunctions.progress_bar_plant(start_time=self.profile.plant.plant_date, end_time=next_time)}", inline=False)
        embed.add_field(name=f"", value=f"Thời gian thu hoạch: <t:{unix_time}:t>", inline=False)
        embed.add_field(name=f"", value=f"Sẽ thu hoạch được:", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} [{self.profile.plant.des_item.emoji} - **{self.profile.plant.des_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        view = BackToProfileView(profile=self.profile, profile_embed=self.profile_embed)
        m = await self.message.edit(embed=embed, view = view)
        view.message = m
        await interaction.followup.send(f"Bạn đã chuyển sang Khu Vườn!", ephemeral=True)

    async def guardian_button_function(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed_color = 0xffffff
        if isinstance(self.profile.profile_color, int) and 0x000000 <= self.profile.profile_color <= 0xFFFFFF:
            embed_color = self.profile.profile_color
        embed = discord.Embed(title="", description=f"**Thông tin Hộ Vệ Thần của <@{self.profile.user_id}>**", color=embed_color)
        text_name = f"{self.profile.guardian.ga_emoji} - **{self.profile.guardian.ga_name}**"
        if self.profile.guardian.time_to_recover != None and self.profile.guardian.time_to_recover > datetime.now() and self.profile.guardian.is_dead == False:
            next_time = self.profile.guardian.time_to_recover
            unix_time = int(next_time.timestamp())
            text_name += f" (Trọng thương đến <t:{unix_time}:t>)"
        if self.profile.guardian.is_dead == True:
            text_name += f"\n(Đã **tử nạn**. Hồi sinh bằng Phục Sinh Thạch trong {SlashCommand.SHOP_GLOBAL.value} hoặc bán đi để mua Hộ Vệ Thần mới)"
        embed.add_field(name=f"", value=text_name, inline=False)
        if self.profile.guardian.stats_point > 0:
            embed.add_field(name=f"", value=f"Có **{self.profile.guardian.stats_point}** điểm cộng ({SlashCommand.GA_RANKUP.value})", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f">>> **Sức tấn công** \n🦾: **{self.profile.guardian.attack_power}**", inline=False)
        embed.add_field(name=f"", value=f">>> **Máu** \n{EmojiCreation2.HP.value}: {self.profile.guardian.health}/{self.profile.guardian.max_health}", inline=False)
        embed.add_field(name=f"", value=f">>> **Thể lực** \n{EmojiCreation2.STAMINA.value}: {self.profile.guardian.stamina}/{self.profile.guardian.max_stamina}", inline=False)
        embed.add_field(name=f"", value=f">>> **Mana** \n{EmojiCreation2.MP.value}: {self.profile.guardian.mana}/{self.profile.guardian.max_mana}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"Cấp bậc: **{UtilitiesFunctions.get_text_on_guardian_level(self.profile.guardian.level)}** [{self.profile.guardian.level}]", inline=False)
        bar_progress = UtilitiesFunctions.progress_bar(input_value= self.profile.guardian.level_progressing)
        embed.add_field(name=f"", value=f"{bar_progress}\n", inline=False)
        if self.profile.guardian.list_skills != None and len(self.profile.guardian.list_skills)>0:
            count = 0
            embed.add_field(name=f"", value=f"Đang sở hữu **{len(self.profile.guardian.list_skills)}** kỹ năng [{len(self.profile.guardian.list_skills)}/{self.profile.guardian.max_skills}]", inline=False)
            for skill in self.profile.guardian.list_skills:
                embed.add_field(name=f"", value=f"[{skill.emoji} - **{skill.skill_name}**]", inline=True)
                count += 1
                if count > 6:
                    embed.add_field(name=f"", value=f"\nNgoài ra còn nhiều kỹ năng khác!", inline=False)
                    break
        embed.set_footer(text=f"Đừng quên, nếu có thắc mắc về Hộ Vệ Thần thì cứ nhắn câu\nga help", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        view = SpecialGuardianView(profile=self.profile, profile_embed=self.profile_embed)
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
                await self.message.edit(view=None)
            except Exception:
                return
        
class BackToProfileView(discord.ui.View):
    def __init__(self, profile: Profile, profile_embed: discord.Embed = None):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
        self.profile_embed = profile_embed
    
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
