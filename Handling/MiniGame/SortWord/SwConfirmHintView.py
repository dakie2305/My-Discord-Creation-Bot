import discord
from Handling.MiniGame.SortWord import SwClass, SwMongoManager

class SwConfirmHintView(discord.ui.View):
    def __init__(self, user: discord.Member, info: SwClass.SortWordInfo, lan: str):
        super().__init__(timeout=30)
        self.user = user
        self.info = info
        self.message: discord.Message = None
        self.is_confirmed = False
        self.lan = lan
        
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
        message = f"{interaction.user.mention} Bạn đã chấp nhận đổi 3 điểm!"
        await interaction.followup.send(content=f"{message}")
        try:
            await self.message.edit(content=f"{interaction.user.mention} đã chấp nhận đánh đổi 3 điểm.\nGợi ý từ hợp lệ: **`{self.info.current_word}**`", view=None, embed= None)
        except Exception as e:
            print(f"Exception at hint SW: {e}")
        SwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name= interaction.user.display_name, point=-3)
        self.is_confirmed = True