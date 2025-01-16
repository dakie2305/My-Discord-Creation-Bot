from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.HelpPageView import HelpPageView
from typing import List, Optional, Dict
import random

async def setup(bot: commands.Bot):
    await bot.add_cog(Donation(bot=bot))
    print("Donation command is ready!")

class Donation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def donation(self, ctx):
        message: discord.Message = ctx.message
        if message:
            embed = discord.Embed(title=f"**Donate Darkie**", description=f"Cảm ơn mạnh thường quân đã ủng hộ!", color=0xc379e0)
            embed.set_image(url="https://i.imgur.com/Zsoel4d.png")
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name="", value=f"- Nếu mọi người có chút lòng thành để ủng hộ và tạo động lực cho Darkie làm thêm chức năng mới, mini-game hoặc cải thiện bot, hoặc đẩy nhanh tiến độ dịch truyện, đăng truyện thì có thể donate một ít cafe nhé! Darkie **xin chân thành cảm ơn** rất rất nhiều!", inline=False)
            embed.add_field(name="", value=f"> ACB: 9799317", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.set_footer(text=f"Cảm ơn chân thành vì đã đọc, mong tin nhắn này không làm phiền mọi người.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            await message.channel.send(embed=embed)
    
    #region keo_bua_bao command
    @discord.app_commands.command(name="donation", description="Ủng hộ tác giả của bot: Darkie!")
    async def donation_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(title=f"**Donate Darkie**", description=f"Cảm ơn mạnh thường quân đã ủng hộ!", color=0xc379e0)
        embed.set_image(url="https://i.imgur.com/Zsoel4d.png")
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name="", value=f"- Nếu mọi người có chút lòng thành để ủng hộ và tạo động lực cho Darkie làm thêm chức năng mới, mini-game hoặc cải thiện bot, hoặc đẩy nhanh tiến độ dịch truyện, đăng truyện thì có thể donate một ít cafe nhé! Darkie **xin chân thành cảm ơn** rất rất nhiều!", inline=False)
        embed.add_field(name="", value=f"> ACB: 9799317", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Cảm ơn chân thành vì đã đọc, mong tin nhắn này không làm phiền mọi người.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        await interaction.followup.send(embed=embed, ephemeral=False)
    
        