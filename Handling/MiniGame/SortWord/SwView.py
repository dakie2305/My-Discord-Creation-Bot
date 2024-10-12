import discord
from Handling.MiniGame.SortWord.SwClass import SortWordInfo, SwPlayerBan, SwPlayerEffect, SwPlayerProfile, SwSpecialItem
from Handling.MiniGame.SortWord import SwMongoManager as SwMongoManager

class SwView(discord.ui.View):
    def __init__(self, embed: discord.Embed, user: discord.Member, sw_info: SortWordInfo, lan: str):
        super().__init__(timeout=30)
        self.embed = embed
        self.sw_info = sw_info
        self.user = user
        self.lan = lan
        self.message: discord.Message = None
        
    async def on_timeout(self):
        #Xoá luôn message
        await self.message.delete()
        
    @discord.ui.button(label="Gợi Ý", style=discord.ButtonStyle.green)
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_point(interaction)
        
    async def handle_point(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        #User chấp nhận đánh đổi 3 điểm để gợi ý từ phù hợp
        await self.message.edit(embed=None, view=None, content=f"{interaction.user.mention} đã chấp nhận đánh đổi 3 điểm.\nGợi ý từ hợp lệ: **`{self.sw_info.current_word}**`")
        SwMongoManager.update_player_point_data_info(channel_id=interaction.channel.id, guild_id=interaction.guild.id, language= self.lan, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, point=-3)
        