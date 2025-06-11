import discord

from Handling.MiniGame.GuessNumber import GnMongoManager
from Handling.MiniGame.GuessNumber.GuessNumberClass import GuessNumberInfo
class GnConfirmHintView(discord.ui.View):
    def __init__(self, user: discord.Member, info: GuessNumberInfo, point = 10):
        super().__init__(timeout=30)
        self.user = user
        self.info = info
        self.message: discord.Message = None
        self.is_confirmed = False
        self.point = point
        
    async def on_timeout(self):
        if self.is_confirmed: return
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
        
    @discord.ui.button(label="Xác Nhận", style=discord.ButtonStyle.blurple)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        message = f"{interaction.user.mention} Bạn đã chấp nhận đổi {self.point} điểm!"
        await interaction.followup.send(content=f"{message}", ephemeral=True)
        try:
            await self.message.edit(content=f"{interaction.user.mention} đã chấp nhận đánh đổi {self.point} điểm.\nĐáp án chính xác là **`{self.info.correct_number}`**", view=None, embed= None)
        except Exception as e:
            print(f"Exception at hint GN: {e}")
        GnMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name= interaction.user.display_name, point=-self.point)
        self.is_confirmed = True