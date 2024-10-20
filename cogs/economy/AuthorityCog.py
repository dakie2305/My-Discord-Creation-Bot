import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Economy.Authority.AuthorityView import AuthorityView
from Handling.Economy.Authority.AuthorityRiotView import AuthorityRiotView
from enum import Enum
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomEnum.UserEnum as UserEnum
from datetime import datetime, timedelta
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
                #Kiểm xem chính quyền có mặc nợ không, có thì từ chức và phạt authority
                if ProfileMongoManager.is_in_debt(data= existed_authority, copper_threshold=50000):
                    embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {self.CurrencySlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
                    existed_authority.copper = -10000
                    existed_authority.silver = 0
                    existed_authority.gold = 0
                    existed_authority.darkium = 0
                    ProfileMongoManager.update_profile_money_fast(guild_id= interaction.guild.id, data=existed_authority)
                    ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild.id)
                    return embed, None
                else:
                    await interaction.followup.send(content=f"Server này đã có Chính Quyền là {member.mention} rồi! Vui lòng bào tiền Chính Quyền, hoặc ép Chính Quyền từ bỏ địa vị để tranh chức Chính Quyền!", ephemeral=True)
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
            await interaction.followup.send(content=f"Bạn đã là Chính Quyền rồi. Vì gây lãng phí tài nguyên, bạn đã bị trừ 500 {EmojiCreation2.COPPER.value}!")
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
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã! Vì gây lãng phí tài nguyên, bạn đã bị trừ 500 {EmojiCreation2.COPPER.value}!", color=0xc379e0)
            await interaction.followup.send(embed=embed)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper=-500, guild_name= interaction.guild.name)
            return
        #Phải đủ tiền mới được vote
        elif data.copper<500:
            embed = discord.Embed(title=f"", description=f"Bạn phải có đủ **500** {EmojiCreation2.COPPER.value} trước đã!", color=0xc379e0)
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

    #region Authority riot
    @authority_group.command(name="riot", description="Bạo động để phá chính quyền đương nhiệm của server!")
    async def riot_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        # #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Kiểm tra xem đây có phải là chính quyền không
        if ProfileMongoManager.is_authority(guild_id=interaction.guild_id, user_id=interaction.user.id) != None:
            await interaction.followup.send(content=f"Bạn đã là Chính Quyền thì không thể tự bạo động. Vì gây lãng phí tài nguyên, bạn đã bị trừ 500 {EmojiCreation2.COPPER.value}!")
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper=-500, guild_name= interaction.guild.name)
            return
        #Kiểm tra xem server đã tồn tại ai là chính quyền chưa
        existed_authority = ProfileMongoManager.is_authority_existed(guild_id=interaction.guild_id)
        if existed_authority == None:
            await interaction.followup.send(content=f"Server không tồn tại Chính Quyền! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", ephemeral=True)
            return
        else:
            authority_user = self.bot.get_guild(interaction.guild_id).get_member(existed_authority.user_id)
            if authority_user == None:
                await interaction.followup.send(content=f"Chính Quyền đã lưu vong khỏi Server! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", ephemeral=True)
                return
            
        #Kiểm tra xem user có /profile chưa
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id= interaction.user.id)
        if user_profile == None:
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", color=0xc379e0)
            view = SelfDestructView(15)
            mes = await interaction.followup.send(embed=embed, view=view)
            view.message = mes
            return
        
        #Mỗi lần bạo động cần tốn base 100 Silver * 0.dignity_point  để phát động, và chính quyền sẽ cần tốn 500 Silver để dẹp loạn
        #Kiểm xem user có đủ 100 Silver không
        money_base_riot = 120
        money_for_riot = money_base_riot
        if existed_authority.dignity_point != None:
            money_for_riot = int(money_base_riot * existed_authority.dignity_point / 100)
            if money_for_riot == 0: money_for_riot = 50
        
        if user_profile.silver < money_for_riot:
            embed = discord.Embed(title=f"", description=f"Để kêu gọi bạo động chính quyền thì bạn cần **{money_for_riot}**{EmojiCreation2.SILVER.value}!", color=0xc379e0)
            mes = await interaction.followup.send(embed=embed)
            return
        #Trừ silver
        ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=-money_for_riot)
        timeout = 70 #Cho timeout giây để kết thúc
        endtime = datetime.now() + timedelta(seconds=timeout)
        #Đưa ra embed bạo động
        embed = discord.Embed(title=f"Lời Kêu Gọi Bạo Động",description=f"{interaction.user.mention} đã kêu gọi mọi người đứng lên khởi nghĩa chống lại Chính Quyền Server <@{existed_authority.user_id}>!",color=discord.Color.red())
        embed.add_field(name=f"", value="▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"Thời gian kết thúc: <t:{int(endtime.timestamp())}:r>", inline=False)
        embed.add_field(name=f"", value=f"- Nếu kêu gọi thành công nhiều **người bạo động** chính quyền thì {interaction.user.mention} sẽ nhận được **500**{EmojiCreation2.SILVER.value} và Chính Quyền <@{existed_authority.user_id}> sẽ mất **1000**{EmojiCreation2.SILVER.value}!", inline=False)
        embed.add_field(name=f"", value=f"- Chính Quyền <@{existed_authority.user_id}> có thể bỏ ra **500**{EmojiCreation2.SILVER.value} để lập tức điều động bắt giữ những kẻ bạo động, hoặc huy động **người phản đối** bạo động để tránh mất tiền!", inline=False)
        embed.set_image(url="https://kustomsignals.com/wp-content/uploads/2022/09/shutterstock_56579431-1024x680.jpg")
        
        view = AuthorityRiotView(user=interaction.user, user_authority=existed_authority, timeout=timeout)
        view.embed = embed
        await interaction.followup.send(f"Bạn đã bị trừ **{money_base_riot}** {EmojiCreation2.SILVER.value} để tạo bạo động!",ephemeral=True)
        called_channel = interaction.channel
        mes = await called_channel.send(embed=embed, view=view, content= authority_user.mention if authority_user != None else "", allowed_mentions=discord.AllowedMentions(users=True))
        view.message = mes
    
    #region Authority riot
    @authority_group.command(name="overthrow", description="Lật đổ chính quyền đương nhiệm trong server!")
    async def riot_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != interaction.guild.owner_id and interaction.user.id != UserEnum.UserId.DARKIE.value:
            text = "Lệnh hiện tại chỉ mới dành cho Owner server!"
            await interaction.followup.send(f"{text}",ephemeral=True)
            return
        #Nếu là server owner thì chỉ việc remove như bình thường 
        else:
            authority = ProfileMongoManager.is_authority_existed(guild_id=interaction.guild.id)
            if authority == None:
                await interaction.followup.send(f"Server không có chính quyền để lật đổ!",ephemeral=True)
                return
            authority.silver = 0
            authority.gold = 0
            authority.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= interaction.guild.id, data=authority)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild.id)
            await interaction.followup.send(f"Bạn đã lật đổ chính quyền của Server!",ephemeral=True)
            channel = interaction.channel
            embed = discord.Embed(title=f"", description=f"Chính Quyền của server đã bị lật đổ! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            await channel.send(embed=embed)            

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