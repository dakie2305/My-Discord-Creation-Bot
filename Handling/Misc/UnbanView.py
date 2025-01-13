import discord
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from typing import List, Optional, Dict

class UnbanView(discord.ui.View):
    def __init__(self, user: discord.Member, guild: discord.Guild):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.user = user
        self.guild = guild
        
        self.unban_button = discord.ui.Button(label="🚨 Huỷ Ban 🚨", style=discord.ButtonStyle.red)
        self.unban_button.callback = self.unban_button_callback
        self.add_item(self.unban_button)
        self.is_unbanned = False
    
    async def unban_button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TextInputModal(unban_view=self, message=self.message, guild=self.guild, user=self.user))
    
    async def on_timeout(self):
        #Delete
        if self.message != None and self.is_unbanned == False: 
            try:
                await self.message.edit(view=None)
            except Exception:
                return

# Create a custom modal for text input
class TextInputModal(discord.ui.Modal):
    def __init__(self, user: discord.Member, guild:discord.Guild,message: discord.Message,  unban_view: "UnbanView"):
        super().__init__(title="Lý do unban")
        self.user = user
        self.guild = guild
        self.unban_view = unban_view
        self.message = message
        self.input_reason_field = discord.ui.TextInput(
            label="Nhập lý do unban",
            placeholder="Lý do: chơi ngu bị ban",
            required=True,
            default = "",
            max_length=100
        )
        self.add_item(self.input_reason_field)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        self.unban_view.is_unbanned = True
        reason_input = self.input_reason_field.value
        try:
            await self.guild.unban(user=self.user, reason=reason_input)
            await interaction.followup.send(f"{interaction.user.mention} đã unban cho {self.user.mention} với lý do: **{reason_input}**")
            if self.message: await self.message.edit(view=None)
        except Exception as e:
            await interaction.channel.send(f"Bot gặp lỗi exception trong lúc unban user: {e}")