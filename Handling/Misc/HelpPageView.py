
import discord
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from typing import List, Optional, Dict

class HelpPageView(discord.ui.View):
    def __init__(self, list_all_embed: list[discord.Embed]):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.list_all_embed = list_all_embed
        self.current_page = 0
        self.total_pages = len(self.list_all_embed)

    
    def create_embed(self):
        embed = self.list_all_embed[self.current_page]
        embed.set_footer(text=f"Trang {self.current_page + 1}/{self.total_pages}")
        return embed
    
    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % self.total_pages
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="Đi tới trang khác", style=discord.ButtonStyle.grey)
    async def go_to_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextGoToPageInputModal(owning_view=self, list_all_embed=self.list_all_embed, message=self.message))
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
    def __init__(self, owning_view: HelpPageView, list_all_embed: List[discord.Embed], message: discord.Message):
        super().__init__(title="Chọn trang mà bạn muốn đi tới")
        self.message: discord.Message = message
        self.list_all_embed = list_all_embed
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