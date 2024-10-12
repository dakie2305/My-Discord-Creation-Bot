import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView

async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot=bot))
    print("Profile Economy is ready!")

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #region profile
    @discord.app_commands.command(name="profile", description="Hiển thị profile của user trong server")
    @discord.app_commands.describe(user="Chọn user để xem profile của người đó.")
    async def show_profile(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        await interaction.response.defer(ephemeral=False)
        if user == None:
            embed = await self.procress_profile_embed(user=interaction.user)
        else:
            embed = await self.procress_profile_embed(user=user)
        await interaction.followup.send(embed=embed)
        return
    
    
    @commands.command()
    async def profile(self, ctx, user: Optional[discord.Member] = None):
        message: discord.Message = ctx.message
        if message:
            if user == None:
                embed = await self.procress_profile_embed(user=message.author)
            else:
                embed = await self.procress_profile_embed(user=user)
            await message.reply(embed=embed)
    #Quote
    @commands.command()
    async def quote(self, ctx, *, quote: str = None):
        message: discord.Message = ctx.message
        if message:
            if quote == None:
                quote = "None"
            embed = discord.Embed(title=f"", description=f"Đã cập nhật quote thành công. Vui lòng dùng lệnh </profile:1294699979058970656> để xem profile.", color=0xddede7)
            ProfileMongoManager.update_profile_quote(guild_name=message.guild.name,guild_id=message.guild.id, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, quote=quote)
            view = SelfDestructView(timeout=30)
            message_sent = await message.reply(embed=embed, view=view)
            view.message = message_sent
    
    async def procress_profile_embed(self, user: discord.Member):
        data = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        print(f"data: {data}")
        if data == None:
            data = ProfileMongoManager.create_profile(guild_id=user.guild.id, user_id=user.id, guild_name=user.guild.name, user_name=user.name, user_display_name=user.display_name)
        
        embed = discord.Embed(title=f"", description=f"Rank: **{data.level}**", color=0xddede7)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value=f"Nhân phẩm: **{self.get_nhan_pham(data.dignity_point)}** ({data.dignity_point})", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═════════════>", inline=False)
        embed.add_field(name=f"", value=f"**Tổng tài sản**:", inline=False)
        show_darkium = f"<a:darkium:1294615481701105734>: **{self.shortened_currency(data.darkium)}**\n"
        if data.darkium == 0:
            show_darkium = ""
        embed.add_field(name=f"", value=f">>> {show_darkium}<a:gold:1294615502588608563>: **{self.shortened_currency(data.gold)}**\n<a:silver:1294615512919048224>: **{self.shortened_currency(data.silver)}**\n<a:copper:1294615524918956052>: **{self.shortened_currency(data.copper)}**", inline=False)
        #Quote
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═════════════>", inline=False)
        embed.add_field(name=f"", value=f"**Quote**: \"{data.quote}\"", inline=False)
        embed.set_footer(text=f"Profile của {user.name}.", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
        return embed
    
    def shortened_currency(self, number: int):
        if number >= 1000000000:
            suffix =number % 1000000000 // 1000000
            if suffix == 0: suffix = "" 
            return f"{number // 1000000000}B{suffix}"
        elif number >= 1000000:
            suffix = number % 1000000 // 1000
            if suffix == 0: suffix = "" 
            return f"{number // 1000000}M{suffix}"
        elif number >= 10000:
            suffix = number % 1000 // 100
            if suffix == 0: suffix = ""
            return f"{number // 1000}K{suffix}"  
        else:
            return str(number)
    
    def get_nhan_pham(self, number):
        text = "Người Thường"
        if number >= 100:
            text = "Thánh Nhân"
        elif number >= 75:
            text = "Người Tốt"
        elif number >= 60:
            text = "Lành tính"
        elif number >= 50:
            text = "Người Thường"
        elif number >= 40:
            text = "Tiểu Nhân"
        elif number >= 30:
            text = "Quỷ Quyệt"
        elif number >= 20:
            text = "Tội Phạm"
        else:
            text = "Gian Thương Tà Đạo"
        return text