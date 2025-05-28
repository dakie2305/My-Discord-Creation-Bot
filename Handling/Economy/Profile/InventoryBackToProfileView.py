import discord
from Handling.Economy.Profile.GuardianMemoryView import GuardianMemoryView
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
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager

class ProfileAdditionalView(discord.ui.View):
    def __init__(self, profile: Profile, profile_embed: discord.Embed = None):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.profile = profile
        self.profile_embed = profile_embed
        
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
        await interaction.response.defer(ephemeral=True)
        if self.profile.is_authority and ProfileMongoManager.is_in_debt(data = self.profile, copper_threshold=100000):
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            self.profile.copper = -10000
            self.profile.silver = 0
            self.profile.gold = 0
            self.profile.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= interaction.guild_id, data=self.profile)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild_id)
            ProfileMongoManager.update_last_authority(guild_id=interaction.guild_id, user_id=self.profile.user_id)
            await self.message.edit(embed=embed)
            await interaction.followup.send(f"Bạn đã chuyển sang chế độ Profile!", ephemeral=True)
            return
        couple_info = CoupleMongoManager.find_couple_by_id(guild_id=interaction.guild_id, user_id=self.profile.user_id)
        cq = ""
        if self.profile.is_authority:
            cq = "Chính Quyền Tối Cao"
        embed_color = 0xffffff
        if isinstance(self.profile.profile_color, int) and 0x000000 <= self.profile.profile_color <= 0xFFFFFF:
            embed_color = self.profile.profile_color
        embed = discord.Embed(title=cq, description=f"**Profile <@{self.profile.user_id}>**", color=embed_color)
        if self.profile.protection_item != None:
            embed.add_field(name=f"", value=f"Bảo Hộ Vật: [{self.profile.protection_item.emoji} - **{self.profile.protection_item.item_name}**]", inline=False)
        if self.profile.attack_item != None:
            embed.add_field(name=f"", value=f"Vũ Khí: [{self.profile.attack_item.emoji} - **{self.profile.attack_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value=f"Nhân phẩm: **{UtilitiesFunctions.get_nhan_pham(self.profile.dignity_point)}** ({self.profile.dignity_point})", inline=True)
        embed.add_field(name=f"", value=f"Địa Vị: **{UtilitiesFunctions.get_dia_vi(self.profile)}**", inline=True)
        embed.add_field(name=f"", value=f"Rank: **{self.profile.level}**", inline=False)
        bar_progress = self.progress_bar(input_value= self.profile.level_progressing)
        embed.add_field(name=f"", value=f"{bar_progress}\n", inline=False)
        if couple_info!= None:
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"Tình trạng cặp đôi: **{UtilitiesFunctions.get_text_on_love_rank(couple_info.love_rank)}** (**{couple_info.love_rank}**)", inline=False)
            embed.add_field(name=f"", value=f"<@{couple_info.first_user_id}> -`{UtilitiesFunctions.get_heart_emoji_on_rank(couple_info.love_rank)}´- <@{couple_info.second_user_id}>", inline=False)
            embed.add_field(name=f"", value=f"Điểm thân mật: **{couple_info.love_point}**", inline=False)
            embed.add_field(name=f"", value=f"Tỉ lệ thăng hoa cảm xúc: **{int(couple_info.love_progressing/1000*100)}%**", inline=False)
            date_created = couple_info.date_created
            unix_time = int(date_created.timestamp())
            embed.add_field(name=f"", value=f"Ngày đầu quen nhau: <t:{unix_time}:D>", inline=False)
            if couple_info.date_married != None:
                date_married = couple_info.date_married
                unix_time_m = int(date_married.timestamp())
                embed.add_field(name=f"", value=f"Ngày cưới nhau: <t:{unix_time_m}:D>", inline=False)
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
        embed.set_footer(text=f"Profile của {self.profile.user_name}.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
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


class SpecialGuardianView(discord.ui.View):
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

    @discord.ui.button(label="Ký Ức Hộ Vệ Thần", style=discord.ButtonStyle.blurple)
    async def memories_button(self, interaction: discord.Interaction, button: discord.ui.Button):
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
                text = f"{EmojiCreation2.SHINY_POINT.value} {data.description}"
                embed.add_field(name=f"#{idx}. Tại kênh *{data.channel_name}* - Ngày: {date_display}", value=text, inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Trang 1/{total_pages}")
        view = GuardianMemoryView(profile=self.profile, list_data=list_data)
        m = await self.message.edit(embed=embed, view=view)
        view.message = m
        await interaction.followup.send(f"Bạn đã chuyển sang Ký Ức Hộ Vệ Thần!", ephemeral=True)
        return
            