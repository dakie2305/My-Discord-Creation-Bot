
import discord
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from typing import List, Optional, Dict
from Handling.Economy.GA.GuardianAngelClass import GuardianAngelMemory
from Handling.Economy.Profile.ProfileClass import Profile

class GuardianMemoryView(discord.ui.View):
    def __init__(self, profile: Profile, list_data: list[GuardianAngelMemory] = None):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.page_size = 6
        self.profile = profile
        self.list_data = list_data
        self.pages = [list_data[i:i+self.page_size] for i in range(0, len(list_data), self.page_size)]
        self.current_page = 0
        self.total_pages = len(self.pages) if len(self.pages) > 0 else 1

    def create_embed(self):
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
        page_data = self.pages[self.current_page] if self.pages else []
        if not page_data:
            embed.add_field(name=f"", value="Không có dữ liệu ký ức", inline=False)
        else:
            for idx, data in enumerate(page_data, start=1 + self.current_page * self.page_size):
                # Convert data.date to Discord unix time format if possible
                unix_time = int(data.date.timestamp())
                date_display = f"<t:{unix_time}:f>"
                text = f"{EmojiCreation2.SHINY_POINT.value} {data.description}"
                embed.add_field(name=f"#{idx}. Tại kênh *{data.channel_name}* - Ngày: {date_display}", value=text, inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Trang {self.current_page+1}/{self.total_pages}")
        return embed
    
    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % self.total_pages
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="Đi tới trang khác", style=discord.ButtonStyle.grey)
    async def go_to_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextGoToPageInputModal(owning_view=self, list_data=self.list_data, message=self.message))
        return

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % self.total_pages
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
        
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
    
class TextGoToPageInputModal(discord.ui.Modal):
    def __init__(self, owning_view: GuardianMemoryView, list_data: List[GuardianAngelMemory], message: discord.Message):
        super().__init__(title="Chọn trang mà bạn muốn đi tới")
        self.message: discord.Message = message
        self.list_all_embed = list_data
        self.input_index_page_field = discord.ui.TextInput(
            label="Nhập số trang mà bạn muốn tới",
            placeholder="VD: 1, 2, 3, 4,...",
            required=True,
            default = "1",
            max_length=2
        )
        self.add_item(self.input_index_page_field)
        self.owning_view = owning_view
    
    async def on_submit(self, interaction: discord.Interaction):
        #
        input_value = self.input_index_page_field.value
        try:
            index = int(input_value) - 1
            #Đảm bảo giá trị hợp lệ
            if index < 0:
                index = 0
            elif index >= self.owning_view.total_pages:
                index = self.owning_view.total_pages - 1
            #Chuyển page đến trang người dùng muốn
            self.owning_view.current_page = index
            await interaction.response.edit_message(embed=self.owning_view.create_embed(), view=self.owning_view)
        except Exception:
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
            return
        return