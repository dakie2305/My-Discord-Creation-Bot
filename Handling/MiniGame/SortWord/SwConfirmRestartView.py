import discord
from CustomEnum.EmojiEnum import EmojiCreation1
from Handling.MiniGame.SortWord import SwMongoManager, SwClass
class SwConfirmRestartView(discord.ui.View):
    def __init__(self, user: discord.Member, channel_id: str, lan: str, info: SwClass.SortWordInfo):
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
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Đoán Từ", color=0x03F8FC)
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
        SwMongoManager.delete_data_info(channel_id=self.channel_id, guild_id=interaction.guild_id, lang=self.lan)
        #Tạo mới
        lan_label = "Tiếng Anh" if self.lan == "en" else "Tiếng Việt"
        current_word = "hello" if self.lan == "en" else "trai"
        unsorted = "olehl" if self.lan == "en" else "rtia"
        data = SwClass.SortWordInfo(channel_id=self.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, current_word=current_word, unsorted_word=unsorted, special_case=False)
        SwMongoManager.create_info(data=data, guild_id=interaction.guild_id, lang=self.lan)
        embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Đoán Từ {lan_label}", description=f"",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} {interaction.user.mention} đã chọn kênh này làm kênh đoán từ.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hướng dẫn chơi Tiếng Anh:\n `ih` -> `hi`, `ytr` -> `try`", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hướng dẫn chơi Tiếng Việt:\n `han rtai` -> `anh trai`, `me rait` -> `em trai`", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Đoán từ hiện tại:", inline=False)
        embed.add_field(name=f"{data.unsorted_word}", value=f"", inline=False)
        channel = interaction.channel
        await channel.send(embed=embed)
        return