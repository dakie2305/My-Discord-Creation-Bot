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
from CustomEnum.EmojiEnum import CurrencyEmoji
import CustomEnum.UserEnum as UserEnum

import CustomFunctions

async def setup(bot: commands.Bot):
    await bot.add_cog(AuthorityEconomy(bot=bot))
    print("Authority Economy is ready!")

class AuthorityEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # Define the parent command group for 'authority'
    authority_group = discord.app_commands.Group(name="authority", description="Các lệnh liên quan đến Chính Quyền của server!")
    
    #region Authority view
    @authority_group.command(name="view", description="Xem chính quyền đương nhiệm hiện tại của server")
    async def view_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Kiểm tra xem server đã tồn tại ai là chính quyền chưa
        existed_authority = ProfileMongoManager.is_authority_existed(guild_id=interaction.guild_id)
        if existed_authority!= None:
            #Get thử xem còn tồn tại trong server không
            member = interaction.guild.get_member(existed_authority.user_id)
            if member:
                await interaction.followup.send(content=f"Server này đã có Chính Quyền là {member.mention} rồi! Vui lòng lật đổ hoặc ép Chính Quyền từ bỏ địa vị để tranh chức Chính Quyền!", ephemeral=True)
            else:
                await interaction.followup.send(f"Chính Quyền đã lưu vong khỏi server. Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!")
                ProfileMongoManager.delete_profile(guild_id=interaction.guild_id, user_id= existed_authority.user_id)
        else:
            await interaction.followup.send(f"Server không tồn tại Chính Quyền! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!")
        
    #region Authority vote
    @authority_group.command(name="vote", description="Bầu chọn bản thân làm Chính Quyền, sẽ tốn 500 C mỗi lần làm")
    async def vote_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer()
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        #Kiểm tra xem đây có phải là chính quyền không
        if ProfileMongoManager.is_authority(guild_id=interaction.guild_id, user_id=interaction.user.id) != None:
            await interaction.followup.send(content=f"Bạn đã là Chính Quyền rồi. Vì gây lãng phí tài nguyên, bạn đã bị trừ 500 {CurrencyEmoji.COPPER.value}!")
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper=-500, guild_name= interaction.guild.name)
            return
        #Kiểm tra xem server đã tồn tại ai là chính quyền chưa
        existed_authority = ProfileMongoManager.is_authority_existed(guild_id=interaction.guild_id)
        if existed_authority!= None:
            #Get thử xem còn tồn tại trong server không
            member = interaction.guild.get_member(existed_authority.user_id)
            if member:
                await interaction.followup.send(content=f"Server này đã có Chính Quyền là {member.mention} rồi! Vui lòng lật đổ hoặc ép Chính Quyền từ bỏ địa vị để tranh chức Chính Quyền!", ephemeral=True)
                return
        data = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if data == None:
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã! Vì gây lãng phí tài nguyên, bạn đã bị trừ 500 {CurrencyEmoji.COPPER.value}!", color=0xc379e0)
            await interaction.followup.send(embed=embed)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper=-500, guild_name= interaction.guild.name)
            return
        #Phải đủ tiền mới được vote
        elif data.copper<500:
            embed = discord.Embed(title=f"", description=f"Bạn phải có đủ **500** {CurrencyEmoji.COPPER.value} trước đã!", color=0xc379e0)
            await interaction.followup.send(embed=embed)
            return
        
        embed = discord.Embed(title=f"Chính Quyền Đương Cử",description=f"Bầu chọn cho **{interaction.user.mention}** làm Chính Quyền của server {interaction.guild.name}.",color=discord.Color.blue())
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value=f"> Rank: **{data.level}**", inline=False)
        embed.add_field(name=f"", value=f"> Nhân phẩm: **{self.get_nhan_pham(data.dignity_point)}** ({data.dignity_point})", inline=False)
        view = AuthorityView(user=interaction.user, data=data)
        me = await interaction.followup.send(embed=embed, view=view)
        view.message = me
        view.embed = embed
        return

    #region Authority view
    @authority_group.command(name="riot", description="Bạo động để phá chính quyền đương nhiệm của server!")
    async def riot_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Kiểm tra xem đây có phải là chính quyền không
        if ProfileMongoManager.is_authority(guild_id=interaction.guild_id, user_id=interaction.user.id) != None:
            await interaction.followup.send(content=f"Bạn đã là Chính Quyền thì không thể tự bạo động. Vì gây lãng phí tài nguyên, bạn đã bị trừ 500 {CurrencyEmoji.COPPER.value}!")
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper=-500, guild_name= interaction.guild.name)
            return
        #Kiểm tra xem server đã tồn tại ai là chính quyền chưa
        existed_authority = ProfileMongoManager.is_authority_existed(guild_id=interaction.guild_id)
        if existed_authority == None:
            await interaction.followup.send(content=f"Server không tồn tại Chính Quyền! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", ephemeral=True)
            return
        
        
        


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