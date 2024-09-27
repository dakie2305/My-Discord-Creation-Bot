import discord
from discord.ext import commands
from typing import Optional
from collections import deque
import asyncio
from datetime import datetime, timedelta
from mini_game.RockPaperScissor import RpsClass, RpsMongoManager, RpsView

async def setup(bot: commands.Bot):
    await bot.add_cog(RockPaperScissors(bot=bot))
    print("Rock Paper Scissor is ready!")

class RockPaperScissors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.games = {}

    #region say command
    @discord.app_commands.command(name="keo_bua_bao", description="Bắt đầu chơi game Kéo - Búa - Bao")
    @discord.app_commands.describe(user="Chọn user để chơi cùng. Không chọn tức là sẽ chơi với bot")
    async def create_rps(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        await interaction.response.defer()
        if interaction.user.id != 315835396305059840:
            interaction.followup.send("Game đang hoàn thiện sau!")
            return
        if user is None:
            user = self.bot.user
        elif user.id == interaction.id:
            interaction.followup.send("Bạn không thể chơi với chính bạn được!")
            return
        # Get the current epoch time (in seconds)
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=30)  # 30 seconds from now
        unix_time = int(end_time.timestamp())
        # Tạo embed thông báo
        embed = discord.Embed(title=f"", description= f"{interaction.user.mention} đã mời {user.mention} chơi Kéo Búa Bao!", color=0xC3A757)  # Yellowish color
        embed.add_field(name="______________", value= f"Cả hai vui lòng chọn lượt chơi của mình. Thời gian còn lại: <t:{unix_time}:R>", inline=False)
        view = RpsView.RPSView(player_1= interaction.user, player_2=user, embed=embed)
        message = await interaction.followup.send(embed=embed, view= view, content= f"{user.mention}")
        view.message_id = message.id
        view.channel_id = interaction.channel_id
        view.message = message
        