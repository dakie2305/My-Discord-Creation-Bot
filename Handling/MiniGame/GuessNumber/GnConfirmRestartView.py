import random
import discord
from CustomEnum.EmojiEnum import EmojiCreation1
from Handling.MiniGame.GuessNumber import GnMongoManager
from Handling.MiniGame.GuessNumber.GuessNumberClass import GuessNumberInfo
class GnConfirmRestartView(discord.ui.View):
    def __init__(self, user: discord.Member, channel_id: str, info: GuessNumberInfo):
        super().__init__(timeout=30)
        self.user = user
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
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Đoán Số", color=0x03F8FC)
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
        await interaction.followup.send(content=f"{interaction.user.mention} đã restart trò chơi Đoán Số trong kênh này!", embed=embed)
        #Xoá đi tạo lại
        GnMongoManager.delete_data_info(channel_id=self.channel_id, guild_id=interaction.guild_id)
        num = random.randint(self.info.range_from, self.info.range_to)
        data = GuessNumberInfo(channel_id=interaction.channel_id, channel_name=interaction.channel.name, guild_name=interaction.guild.name, correct_number=num, range_from=self.info.range_from, range_to=self.info.range_to)
        GnMongoManager.create_info(data=data, guild_id=interaction.guild.id)
        embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Đoán Số May Mắn", description=f"",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hãy nhắn vào một con số bất kỳ, bot sẽ gợi ý cho bạn tìm ra con số chính xác!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Đáp án đúng sẽ thuộc khoảng từ **`{self.info.range_from}`** đến **`{self.info.range_to}`**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bot sẽ react {EmojiCreation1.HIGHER.value} nếu số của bạn thấp hơn đáp án", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bot sẽ react {EmojiCreation1.LOWER.value} nếu số của bạn cao hơn đáp án", inline=False)
        channel = interaction.channel
        await channel.send(embed=embed)
        try:
            await self.message.delete()
        except Exception:
            pass
        return