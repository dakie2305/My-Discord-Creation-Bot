import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Economy.Authority.AuthorityView import AuthorityView
from enum import Enum
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Economy.Profile.InventoryBackToProfileView import ProfileToInventoryView, InventoryBackToProfileView

async def setup(bot: commands.Bot):
    await bot.add_cog(ProfileEconomy(bot=bot))
    print("Profile Economy is ready!")

class ProfileEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #region profile
    @discord.app_commands.command(name="profile", description="Hiển thị profile của user trong server")
    @discord.app_commands.describe(user="Chọn user để xem profile của người đó.")
    async def show_profile(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        await interaction.response.defer(ephemeral=False)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if user!= None and user.bot:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không được dùng cho bot!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        data = None
        if user == None:
            embed, data = await self.procress_profile_embed(user=interaction.user)
        else:
            embed, data = await self.procress_profile_embed(user=user)
        if data != None and data.list_items != None and len(data.list_items)>0:
            view = ProfileToInventoryView(profile=data)
            m = await interaction.followup.send(embed=embed, view = view)
            view.message = m
        else:
            await interaction.followup.send(embed=embed)
        return
    
    
    @commands.command()
    async def profile(self, ctx, user: Optional[discord.Member] = None):
        if user != None and user.bot: return
        message: discord.Message = ctx.message
        if message:
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            data = None
            view = None
            if user == None:
                embed, data = await self.procress_profile_embed(user=message.author)
            else:
                embed, data = await self.procress_profile_embed(user=user)
            if data != None and data.list_items != None and len(data.list_items)>0:
                view = ProfileToInventoryView(profile=data)
                m = await message.reply(embed=embed, view= view)
                view.message = m
            else:
                await message.reply(embed=embed)
    #Quote
    @commands.command()
    async def quote(self, ctx, *, quote: str = None):
        message: discord.Message = ctx.message
        if message:
            if quote == None:
                quote = "None"
            if len(quote.split()) > 50:
                await message.reply(content="Độ dài quá ký tự cho phép")
                return
            if len(quote) > 800:
                await message.reply(content="Độ dài quá ký tự cho phép")
                return
            embed = discord.Embed(title=f"", description=f"Đã cập nhật quote thành công. Vui lòng dùng lệnh {SlashCommand.PROFILE.value} để xem profile.", color=0xddede7)
            ProfileMongoManager.update_profile_quote(guild_name=message.guild.name, guild_id=message.guild.id, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, quote=quote)
            view = SelfDestructView(timeout=30)
            message_sent = await message.reply(embed=embed, view=view)
            view.message = message_sent
    
    async def procress_profile_embed(self, user: discord.Member):
        data = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        if data == None:
            data = ProfileMongoManager.create_profile(guild_id=user.guild.id, user_id=user.id, guild_name=user.guild.name, user_name=user.name, user_display_name=user.display_name)
        
        if data.is_authority and ProfileMongoManager.is_in_debt(data= data, copper_threshold=100000):
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            data.copper = -10000
            data.silver = 0
            data.gold = 0
            data.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= user.guild.id, data=data)
            ProfileMongoManager.remove_authority_from_server(guild_id=user.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=user.guild.id, user_id=data.user_id)
            return embed, None
        
        embed = discord.Embed(title=f"", description=f"**Profile {user.mention}**", color=0xddede7)
        if user.avatar != None:
            embed.set_thumbnail(url=user.avatar.url)
        if data.is_authority:
            embed.add_field(name=f"", value="**Chính Quyền Tối Cao**", inline=False)
        if data.protection_item != None:
            embed.add_field(name=f"", value=f"Bảo Hộ Vật: [{data.protection_item.emoji} - **{data.protection_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value=f"Nhân phẩm: **{UtilitiesFunctions.get_nhan_pham(data.dignity_point)}** ({data.dignity_point})", inline=True)
        embed.add_field(name=f"", value=f"Địa Vị: **{UtilitiesFunctions.get_dia_vi(data)}**", inline=True)
        if data.level > 100:
            embed.add_field(name=f"", value=f"Rank: **{data.level} (Vô Hư Phá)**", inline=False)
        else:
            embed.add_field(name=f"", value=f"Rank: **{data.level}**", inline=False)
        bar_progress = self.progress_bar(input_value= data.level_progressing)
        embed.add_field(name=f"", value=f"{bar_progress}\n", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"**Tổng tài sản**:", inline=False)
        show_darkium = f"{EmojiCreation2.DARKIUM.value}: **{UtilitiesFunctions.shortened_currency(data.darkium)}**\n"
        if data.darkium == 0:
            show_darkium = ""
        embed.add_field(name=f"", value=f">>> {show_darkium}{EmojiCreation2.GOLD.value}: **{UtilitiesFunctions.shortened_currency(data.gold)}**\n{EmojiCreation2.SILVER.value}: **{UtilitiesFunctions.shortened_currency(data.silver)}**\n{EmojiCreation2.COPPER.value}: **{UtilitiesFunctions.shortened_currency(data.copper)}**", inline=False)
        #Quote
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"**Quote**: \"{data.quote}\"", inline=False)
        embed.set_footer(text=f"Profile của {user.name}.", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
        
        if user.guild.id == 1256987900277690470:
            #Của true heaven
            await self.update_rank_role(user= user, profile= data)
        return embed, data
    
    async def update_rank_role(self, user: discord.Member, profile: Profile):
        if user.guild.id != 1256987900277690470: return
        role_mappings = {
        "Rank 10": range(10, 20),
        "Rank 20": range(20, 30),
        "Rank 30": range(30, 40),
        "Rank 40": range(40, 50),
        "Rank 50": range(50, 60),
        "Rank 60": range(60, 70),
        "Rank 70": range(70, 80),
        "Rank 80": range(80, 90),
        "Rank 90": range(90, 99),
        "Rank 99": range(99, 100),
        "Rank 100+ (Vô Hư Phá)": range(100, 600)
        }
        
        target_role_name = None
        for role_name, level_range in role_mappings.items():
            if profile.level in level_range:
                target_role_name = role_name
                break
        
        if target_role_name == None: return
        
        current_rank_roles = [role for role in user.roles if role.name in role_mappings]
        has_correct_role = any(role.name == target_role_name for role in current_rank_roles)
        if has_correct_role:
            return

        #Xoá các rank cũ đi
        for role in current_rank_roles:
            if role.name != target_role_name:
                await user.remove_roles(role)
                
        target_role = discord.utils.get(user.guild.roles, name=target_role_name)
        if target_role:
            await user.add_roles(target_role)

    
    def progress_bar(self, input_value: int, total_progress: int = 1000, bar_length=15):
        # Calculate the percentage of progress
        percentage = (input_value / total_progress) * 100
        # Determine the number of filled (█) characters
        filled_length = int(bar_length * input_value // total_progress)
        # Create the progress bar string
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        # Format the output with percentage
        return f'{bar} **{int(percentage)}%**'

    