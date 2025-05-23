
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