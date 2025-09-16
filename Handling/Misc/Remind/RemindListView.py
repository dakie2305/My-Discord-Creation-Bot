import discord
from CustomEnum.SlashEnum import SlashCommand
from typing import List, Optional, Dict
from Handling.Misc.Remind import RemindMongoManager
from Handling.Misc.Remind.RemindClass import Remind

class RemindListView(discord.ui.View):
    def __init__(self, user: discord.Member, list_reminds: List[Remind]):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.list_reminds = list_reminds
        self.current_page = 0
        self.total_pages = len(self.list_reminds) if list_reminds else 1
        self.user = user
        
    def create_embed(self):
        # Tạo embed
        embed = discord.Embed(title=f"", description=f"**Lời nhắc của {self.user.mention}**", color=discord.Color.blue())
        embed.add_field(name=f"", value=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬",inline=False)
        if self.list_reminds:
            remind = self.list_reminds[self.current_page]
            unix_time = int(remind.date_remind.timestamp())
            embed.add_field(name=f"Nội Dung", value=f"{remind.message_content}",inline=False)
            embed.add_field(name=f"Thời Gian Nhắc", value=f"<t:{unix_time}:f>",inline=False)
            embed.add_field(name=f"Kênh", value=f"Kênh **{remind.channel_name}** của Server **{remind.guild_name}**",inline=False)
            embed.set_footer(text=f"Trang {self.current_page + 1}/{self.total_pages}")
        else:
            embed.add_field(name="Không có lời nhắc nào cả", value="Vui lòng tạo lời nhắc mới bằng lệnh\n`/remind create`.", inline=False)
        return embed
    
    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % self.total_pages
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="Xóa", style=discord.ButtonStyle.red)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.list_reminds:
            await interaction.response.send_message("❌ Không còn lời nhắc nào để xóa.", ephemeral=True)
            return
        remind = self.list_reminds[self.current_page]
        RemindMongoManager.delete_remind_by_id(remind_id=remind.remind_id)
        # Remove from local list
        self.list_reminds.pop(self.current_page)
        self.total_pages = max(len(self.list_reminds), 1)
        self.current_page = min(self.current_page, self.total_pages - 1)
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % self.total_pages
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
        
    async def on_timeout(self):
        # Disable all buttons khi hết hạn
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass
