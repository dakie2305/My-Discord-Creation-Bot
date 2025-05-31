import discord
from CustomEnum.EmojiEnum import EmojiCreation1
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
class MwConfirmRestartView(discord.ui.View):
    def __init__(self, user: discord.Member, channel_id: str, lan: str, info: MwClass.MatchWordInfo):
        super().__init__(timeout=30)
        self.user = user
        self.lan = lan
        self.channel_id = channel_id
        self.info = info
        self.message: discord.Message = None
        
    async def on_timeout(self):
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
        
    @discord.ui.button(label="Xác Nhận", style=discord.ButtonStyle.red)
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Nối Từ", color=0x03F8FC)
        embed.add_field(name=f"", value=f"Lượt chơi thứ: {self.info.current_round}/1200", inline=False)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 0
        if self.info.player_profiles:
            self.info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for index, profile in enumerate(self.info.player_profiles):
                if (profile.point!= 0 or len(profile.special_items)> 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** <@{profile.user_id}>. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 25: break
        await interaction.followup.send(content=f"{interaction.user.mention} đã restart trò chơi Nối Từ trong kênh này!")

        #Xoá đi tạo lại
        MwMongoManager.delete_data_info(channel_id=self.channel_id, guild_id=interaction.guild_id, lang=self.lan)
        #Tạo mới nối từ

        lan_label = "Tiếng Anh" if self.lan == "en" else "Tiếng Việt"
        #Nếu là tiếng anh thì cứ tạo bình thường
        if self.lan == "en":
            data = MwClass.MatchWordInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, current_word="hello", special_case=False)
            MwMongoManager.create_info(data=data, guild_id=interaction.guild_id, lang=self.lan)
            embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Nối Từ {lan_label}", description=f"",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đã restart kênh nối từ.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Từ hiện tại:", inline=False)
            embed.add_field(name=f"{data.current_word}", value=f"", inline=False)
            channel = interaction.channel
            await channel.send(embed=embed)
        else:
            type_label = "Nối Theo Từ Cuối" if self.info.type == "A" else "Nối Theo Âm Cuối"
            is_special = True if self.info.type == "A" else False
            data = MwClass.MatchWordInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, current_word="anh", special_case=is_special, type=self.info.type)
            embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Nối Từ {lan_label}", description=f"Thể Loại: **{type_label}**",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đã resrat kênh nối từ.", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Từ hiện tại:", inline=False)
            embed.add_field(name=f"{data.current_word}", value=f"", inline=False)
            channel = interaction.channel
            await channel.send(embed=embed)
        return