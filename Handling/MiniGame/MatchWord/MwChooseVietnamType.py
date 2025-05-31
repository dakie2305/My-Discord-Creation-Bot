import discord
from CustomEnum.EmojiEnum import EmojiCreation1
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
class MwChooseVietnamType(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__(timeout=30)
        self.user = user
        self.message: discord.Message = None
        
    async def on_timeout(self):
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
        
    @discord.ui.button(label="Nối Theo Từ Cuối", style=discord.ButtonStyle.green)
    async def type_a_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        current_type = "A"
        await self.handling_create_match_word_vietnamese(interaction=interaction, type=current_type)
    
    @discord.ui.button(label="Nối Theo Âm Cuối", style=discord.ButtonStyle.blurple)
    async def type_b_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        current_type = "B"
        await self.handling_create_match_word_vietnamese(interaction=interaction, type=current_type)
    
    async def handling_create_match_word_vietnamese(self, interaction: discord.Interaction, type: str):
        type_label = "Nối Theo Từ Cuối" if type == "A" else "Nối Theo Âm Cuối"
        is_special = False if type == "A" else True
        data = MwClass.MatchWordInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, current_word="anh", special_case=is_special, type=type)
        MwMongoManager.create_info(data=data, guild_id=interaction.guild_id, lang="vn")
        embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Nối Từ Tiếng Việt", description=f"Thể Loại: **{type_label}**",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đã chọn kênh này làm kênh nối từ.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Từ hiện tại:", inline=False)
        embed.add_field(name=f"{data.current_word}", value=f"", inline=False)
        await interaction.followup.send(embed=embed)
        return