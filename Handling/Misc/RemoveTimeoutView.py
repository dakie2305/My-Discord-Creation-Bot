import discord
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from typing import List, Optional, Dict

class RemoveTimeoutView(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.user = user
        
        self.remove_timeout_button = discord.ui.Button(label="🚨 Huỷ Timeout 🚨", style=discord.ButtonStyle.red)
        self.remove_timeout_button.callback = self.remove_timeout_button_callback
        self.add_item(self.remove_timeout_button)
        self.is_remove_timeout = False
    
    async def remove_timeout_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TextInputModal(remove_timeout_view=self, message = self.message, user=self.user))
    
    async def on_timeout(self):
        #Delete
        if self.message != None and self.is_remove_timeout == False: 
            try:
                await self.message.edit(view=None)
            except Exception:
                return

# Create a custom modal for text input
class TextInputModal(discord.ui.Modal):
    def __init__(self, user: discord.Member, message: discord.Message, remove_timeout_view: "RemoveTimeoutView"):
        super().__init__(title="Lý do gỡ Timeout")
        self.user = user
        self.message = message
        self.unban_view = remove_timeout_view
        self.input_reason_field = discord.ui.TextInput(
            label="Nhập lý do",
            placeholder="Lý do: chơi ngu bị mute",
            required=True,
            default = "",
            max_length=100
        )
        self.add_item(self.input_reason_field)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        self.unban_view.is_remove_timeout = True
        reason_input = self.input_reason_field.value
        try:
            await self.user.edit(timed_out_until=None)
            await interaction.followup.send(f"{interaction.user.mention} đã gỡ Timeout cho {self.user.mention} với lý do: **{reason_input}**")
            if self.message: await self.message.edit(view=None)
        except Exception as e:
            await interaction.channel.send(f"Bot gặp lỗi exception trong lúc bỏ Timeout user: {e}")