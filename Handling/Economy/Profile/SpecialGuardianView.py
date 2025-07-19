import discord
from Handling.Economy.GA import ListGAAndSkills
from Handling.Economy.Global import GlobalMongoManager
from Handling.Economy.Profile.GuardianMemoryView import GuardianMemoryView
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from datetime import datetime, timedelta
import random

class SpecialGuardianView(discord.ui.View):
    def __init__(self, profile: Profile, profile_embed: discord.Embed = None):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
        self.profile_embed = profile_embed
        
        self.profile_button = discord.ui.Button(label="Profile", style=discord.ButtonStyle.primary)
        self.profile_button.callback = self.profile_button_function
        self.add_item(self.profile_button)
        
        self.memories_button = discord.ui.Button(label="Ký Ức Hộ Vệ Thần", style=discord.ButtonStyle.blurple)
        self.memories_button.callback = self.memories_button_function
        self.add_item(self.memories_button)
        
        self.global_profile = GlobalMongoManager.find_global_profile_by_id(user_id=profile.user_id)
        
        if self.global_profile != None and self.global_profile.guardian != None:
            self.global_guardian_button = discord.ui.Button(label="Hộ Vệ Thần Liên Thông", style=discord.ButtonStyle.secondary)
            self.global_guardian_button.callback = self.global_guardian_function
            self.add_item(self.global_guardian_button)
    
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
    
    async def profile_button_function(self, interaction: discord.Interaction):
        if self.profile_embed != None:
            #Chuyển về embed cũ
            await self.message.edit(embed=self.profile_embed, view = None)
            return

    async def memories_button_function(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        page_size = 4
        list_data = self.profile.guardian.memories if self.profile.guardian.memories else []
        self.pages = [list_data[i:i+page_size] for i in range(0, len(list_data), page_size)]
        current_page = 0
        total_pages = len(self.pages) if len(self.pages) > 0 else 1
        embed_color = 0xffffff
        if isinstance(self.profile.profile_color, int) and 0x000000 <= self.profile.profile_color <= 0xFFFFFF:
            embed_color = self.profile.profile_color
        embed = discord.Embed(title="", description=f"**Ký ức Hộ Vệ Thần của <@{self.profile.user_id}>**", color=embed_color)
        text_name = f"{self.profile.guardian.ga_emoji} - **{self.profile.guardian.ga_name}**"
        embed.add_field(name=f"", value= text_name, inline=False)
        #Stats count
        text_stats = f"Trọng thương: **{self.profile.guardian.count_injury}** - Tử nạn: **{self.profile.guardian.count_death}**"
        embed.add_field(name=f"", value= text_stats, inline=False)
        text_stats = f"PVE thắng: **{self.profile.guardian.count_battle_pve_won}** - PVE thua: **{self.profile.guardian.count_battle_pve_lose}**"
        embed.add_field(name=f"", value= text_stats, inline=False)
        text_stats = f"PVP thắng: **{self.profile.guardian.count_battle_pvp_won}** - PVP thua: **{self.profile.guardian.count_battle_pvp_lose}**"
        embed.add_field(name=f"", value= text_stats, inline=False)
        text_stats = f"Hầm ngục thắng: **{self.profile.guardian.count_dungeon_fight_won}** - Hầm ngục thua: **{self.profile.guardian.count_dungeon_fight_lose}**"
        embed.add_field(name=f"", value= text_stats, inline=False)
        text_stats = f"Ăn: **{self.profile.guardian.count_feed}** - Thiền định: **{self.profile.guardian.count_meditation}**"
        embed.add_field(name=f"", value= text_stats, inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        page_data = self.pages[current_page] if self.pages else []
        if not page_data:
            embed.add_field(name=f"", value="Không có dữ liệu ký ức", inline=False)
        else:
            for idx, data in enumerate(page_data, start=1 + current_page * page_size):
                # Convert data.date to Discord unix time format if possible
                unix_time = int(data.date.timestamp())
                date_display = f"<t:{unix_time}:f>"
                text = f"{EmojiCreation2.SHINY_POINT.value} {data.description}\n\n"
                embed.add_field(name=f"#*{data.channel_name}* - {date_display}", value=text, inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Trang 1/{total_pages}")
        view = GuardianMemoryView(profile=self.profile, list_data=list_data)
        m = await self.message.edit(embed=embed, view=view)
        view.message = m
        await interaction.followup.send(f"Bạn đã chuyển sang Ký Ức Hộ Vệ Thần!", ephemeral=True)
        return
    
    async def global_guardian_function(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        unix_time = int(self.global_profile.enable_until.timestamp())
        date_display = f"<t:{unix_time}:d>"
        embed_color = 0xffffff
        if isinstance(self.profile.profile_color, int) and 0x000000 <= self.profile.profile_color <= 0xFFFFFF:
            embed_color = self.profile.profile_color
        embed = discord.Embed(title="", description=f"**Thông tin Hộ Vệ Thần Liên Thông của <@{self.global_profile.user_id}>**", color=embed_color)
        text_name = f"{self.global_profile.guardian.ga_emoji} - **{self.global_profile.guardian.ga_name}**"
        embed.add_field(name=f"", value=text_name, inline=False)
        embed.add_field(name=f"Hết hạn truy cập vào: {date_display}", value=f"", inline=True)
        if self.profile.guardian.stats_point > 0:
            embed.add_field(name=f"", value=f"Có **{self.global_profile.guardian.stats_point}** điểm cộng khả dụng", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f">>> **Sức tấn công** \n🦾: **{self.global_profile.guardian.attack_power}**", inline=False)
        embed.add_field(name=f"", value=f">>> **Máu** \n{EmojiCreation2.HP.value}: {self.global_profile.guardian.max_health}", inline=False)
        embed.add_field(name=f"", value=f">>> **Thể lực** \n{EmojiCreation2.STAMINA.value}:{self.global_profile.guardian.max_stamina}", inline=False)
        embed.add_field(name=f"", value=f">>> **Mana** \n{EmojiCreation2.MP.value}: {self.global_profile.guardian.max_mana}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"Cấp bậc: **{UtilitiesFunctions.get_text_on_guardian_level(self.global_profile.guardian.level)}** [{self.global_profile.guardian.level}]", inline=False)
        bar_progress = UtilitiesFunctions.progress_bar(input_value= self.global_profile.guardian.level_progressing)
        embed.add_field(name=f"", value=f"{bar_progress}\n", inline=False)
        if self.global_profile.guardian.list_skills != None and len(self.global_profile.guardian.list_skills)>0:
            count = 0
            embed.add_field(name=f"", value=f"Đang sở hữu **{len(self.global_profile.guardian.list_skills)}** kỹ năng [{len(self.global_profile.guardian.list_skills)}/{self.global_profile.guardian.max_skills}]", inline=False)
            for skill in self.global_profile.guardian.list_skills:
                embed.add_field(name=f"", value=f"[{skill.emoji} - **{skill.skill_name}**]", inline=True)
                count += 1
                if count > 6:
                    embed.add_field(name=f"", value=f"\nNgoài ra còn nhiều kỹ năng khác!", inline=False)
                    break
        embed.set_footer(text=f"Đừng quên, nếu có thắc mắc về Hộ Vệ Thần thì cứ nhắn câu\nga help", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        try:
            #Gắn link background dựa trên id của guardian nếu có
            urls = ListGAAndSkills.get_list_back_ground_on_ga_id(self.global_profile.guardian.ga_id)
            if urls != None and len(urls)>0:
                url = random.choice(urls)
                embed.set_image(url=url)
            await self.message.edit(embed=embed, view = None)
            await interaction.followup.send(f"Bạn đã chuyển sang Hộ Vệ Thần Liên Thông!", ephemeral=True)
        except Exception:
            embed.set_image(url=None)
            await self.message.edit(embed=embed, view = None)
            await interaction.followup.send(f"Bạn đã chuyển sang Hộ Vệ Thần Liên Thông!", ephemeral=True)
            return