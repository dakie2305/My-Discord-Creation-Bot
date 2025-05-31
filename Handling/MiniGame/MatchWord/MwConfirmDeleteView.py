import discord
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
class MwConfirmDeleteView(discord.ui.View):
    def __init__(self, user: discord.Member, channel_id: str, lan: str):
        super().__init__(timeout=30)
        self.user = user
        self.lan = lan
        self.channel_id = channel_id
        self.message: discord.Message = None
        
    async def on_timeout(self):
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
        
    @discord.ui.button(label="Xác Nhận", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        MwMongoManager.delete_data_info(channel_id=self.channel_id, guild_id=interaction.guild_id, lang=self.lan)
        await interaction.followup.send(content=f"{interaction.user.mention} đã xoá trò chơi Nối Từ trong kênh này!")
        return
        