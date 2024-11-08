import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Economy.Authority.AuthorityView import AuthorityView
from Handling.Economy.Authority.AuthorityRiotView import AuthorityRiotView
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from enum import Enum
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomEnum.UserEnum as UserEnum
from datetime import datetime, timedelta
import CustomFunctions
import db.DbMongoManager as db
import random
from Handling.Misc.RandomDropboxEconomyView import RandomDropboxEconomyView

async def setup(bot: commands.Bot):
    await bot.add_cog(AuthorityEconomy(bot=bot))
    print("Authority Economy is ready!")

class AuthorityEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_used_per_guild = {}
    
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
        existed_authority = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
        if existed_authority!= None:
            #Get thử xem còn tồn tại trong server không
            member = interaction.guild.get_member(existed_authority.user_id)
            if member:
                #Kiểm xem chính quyền có mặc nợ không, có thì từ chức và phạt authority
                if ProfileMongoManager.is_in_debt(data= existed_authority, copper_threshold=100000):
                    embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {self.CurrencySlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
                    existed_authority.copper = -10000
                    existed_authority.silver = 0
                    existed_authority.gold = 0
                    existed_authority.darkium = 0
                    ProfileMongoManager.update_profile_money_fast(guild_id= interaction.guild.id, data=existed_authority)
                    ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild.id)
                    ProfileMongoManager.update_last_authority(guild_id=interaction.guild.id, user_id=existed_authority.user_id)
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
        existed_authority = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
        if existed_authority!= None:
            #Get thử xem còn tồn tại trong server không
            member = interaction.guild.get_member(existed_authority.user_id)
            if member:
                await interaction.followup.send(content=f"Server này đã có Chính Quyền là {member.mention} rồi! Vui lòng lật đổ hoặc ép Chính Quyền từ bỏ địa vị để tranh chức Chính Quyền!", ephemeral=True)
                return
        conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=interaction.guild_id)
        if conversion_rate != None and conversion_rate.last_authority == interaction.user.id:
            await interaction.followup.send(content=f"Bạn đã từng là chính quyền rồi! Vui lòng nhường chức Chính Quyền cho người khác!", ephemeral=True)
            return
            
        data = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if data == None:
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã! Vì gây lãng phí tài nguyên, bạn đã bị trừ 500 {EmojiCreation2.COPPER.value}!", color=0xc379e0)
            await interaction.followup.send(embed=embed)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper=-500, guild_name= interaction.guild.name)
            return
        #Phải đủ tiền mới được vote
        elif data.silver<= 0 and data.gold<= 0 and data.darkium<= 0 and data.copper<500:
            embed = discord.Embed(title=f"", description=f"Bạn phải có đủ ít nhất **500** {EmojiCreation2.COPPER.value} trước đã!", color=0xc379e0)
            await interaction.followup.send(embed=embed)
            return
        
        # Kiểm tra xem command có nằm trong giới hạn 15 phút không
        now = datetime.now()
        if interaction.guild_id in self.last_used_per_guild and (now - self.last_used_per_guild[interaction.guild_id]) < timedelta(minutes=5):
            time_remaining = (self.last_used_per_guild[interaction.guild_id] + timedelta(minutes=5) - now).seconds
            minutes, seconds = divmod(time_remaining, 60)
            await interaction.followup.send(f"Đã có người tiến hành bầu cử. Vui lòng thử lại lệnh sau {minutes} phút {seconds} giây.", ephemeral=True)
            return
        # Set the last used time to now
        self.last_used_per_guild[interaction.guild_id] = now
        
        #Trừ 10% số tiền lớn nhất để tiến hành bầu cử
        money_to_vote = 0
        emoji = EmojiCreation2.COPPER.value
        if data.darkium > 0:
            money_to_vote = int(data.darkium * 10 / 100)
            emoji = EmojiCreation2.DARKIUM.value
        elif data.gold > 0:
            money_to_vote = int(data.gold * 10 / 100)
            emoji = EmojiCreation2.GOLD.value
        elif data.silver > 0:
            money_to_vote = int(data.silver * 10 / 100)
            emoji = EmojiCreation2.SILVER.value
        else:
            money_to_vote = int(data.copper * 10 / 100)
            emoji = EmojiCreation2.COPPER.value
        if money_to_vote == 0: money_to_vote = 1
        if emoji == EmojiCreation2.COPPER.value and money_to_vote < 500: money_to_vote = 500

        await interaction.followup.send(content=f"{interaction.user.mention} đã bỏ **{money_to_vote}** {emoji} để vận động tranh cử chức Chính Quyền server!")
        channel = interaction.channel
        embed = discord.Embed(title=f"Chính Quyền Đương Cử",description=f"Bầu chọn cho **{interaction.user.mention}** làm Chính Quyền của server {interaction.guild.name}.",color=discord.Color.blue())
        if interaction.user.avatar != None:
            embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value=f"> Rank: **{data.level}**", inline=False)
        embed.add_field(name=f"", value=f"> Nhân phẩm: **{self.get_nhan_pham(data.dignity_point)}** ({data.dignity_point})", inline=False)
        view = AuthorityView(user=interaction.user, data=data)
        me = await channel.send(embed=embed, view=view)
        view.message = me
        view.embed = embed
        return

    #region Authority riot
    @authority_group.command(name="riot", description="Bạo động để phá chính quyền đương nhiệm của server!")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
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
        existed_authority = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
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
        
        #Không cho riot trong vòng cùng 1 ngày
        if user_profile != None and user_profile.last_riot != None:
            if user_profile.last_riot.date() == datetime.now().date():
                tommorow = datetime.today() + timedelta(days=1)
                unix_time = int(tommorow.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã bạo động trong hôm nay rồi, vui lòng đợi đến <t:{unix_time}:D> để thực hiện lại lệnh!", color=0xc379e0)
                view = SelfDestructView(60)
                m = await interaction.followup.send(embed=embed, view=view)
                view.message = m
                return
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> để thực hiện lại lệnh!", color=0xc379e0)
                view = SelfDestructView(60)
                m = await interaction.followup.send(embed=embed, view=view)
                view.message = m
                return
        
        #Mỗi lần bạo động cần tốn base 100 Silver * 0.dignity_point  để phát động, và chính quyền sẽ cần tốn 500 Silver để dẹp loạn
        #Kiểm xem user có đủ 100 Silver không
        money_base_riot = 180
        money_for_riot = money_base_riot
        if existed_authority.dignity_point != None:
            money_for_riot = int(money_base_riot * existed_authority.dignity_point / 100)
            if money_for_riot == 0: money_for_riot = 50
        
        if user_profile.silver < money_for_riot:
            embed = discord.Embed(title=f"", description=f"Để kêu gọi bạo động chính quyền thì bạn cần **{money_for_riot}**{EmojiCreation2.SILVER.value}!", color=0xc379e0)
            mes = await interaction.followup.send(embed=embed)
            return
        
        #Cập nhật last riot
        ProfileMongoManager.update_last_riot_now(guild_id=interaction.guild_id, user_id=interaction.user.id)
        #Trừ silver
        ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=-money_for_riot)
        timeout = 20 #Cho timeout giây để kết thúc
        endtime = datetime.now() + timedelta(seconds=timeout)
        #Đưa ra embed bạo động
        embed = discord.Embed(title=f"Lời Kêu Gọi Bạo Động",description=f"{interaction.user.mention} đã kêu gọi mọi người đứng lên khởi nghĩa chống lại Chính Quyền Server <@{existed_authority.user_id}>!",color=discord.Color.red())
        embed.add_field(name=f"", value="▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"Thời gian kết thúc: <t:{int(endtime.timestamp())}:R>", inline=False)
        embed.add_field(name=f"", value=f"- Nếu kêu gọi thành công nhiều **người bạo động** chính quyền thì {interaction.user.mention} sẽ nhận được **300**{EmojiCreation2.SILVER.value} và Chính Quyền <@{existed_authority.user_id}> sẽ mất **1000**{EmojiCreation2.SILVER.value}!", inline=False)
        embed.add_field(name=f"", value=f"- Chính Quyền <@{existed_authority.user_id}> có thể bỏ ra **500**{EmojiCreation2.SILVER.value} để lập tức điều động bắt giữ những kẻ bạo động, hoặc huy động **người phản đối** bạo động để tránh mất tiền!", inline=False)
        embed.set_image(url="https://kustomsignals.com/wp-content/uploads/2022/09/shutterstock_56579431-1024x680.jpg")
        
        view = AuthorityRiotView(user=interaction.user, user_authority=existed_authority, timeout=timeout)
        view.embed = embed
        await interaction.followup.send(f"Bạn đã bị trừ **{money_for_riot}** {EmojiCreation2.SILVER.value} để tạo bạo động!",ephemeral=True)
        called_channel = interaction.channel
        mes = await called_channel.send(embed=embed, view=view, content= authority_user.mention if authority_user != None else "", allowed_mentions=discord.AllowedMentions(users=True))
        view.message = mes
    
    #region Authority overthrow
    @authority_group.command(name="overthrow", description="Lật đổ chính quyền đương nhiệm trong server!")
    async def riot_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != interaction.guild.owner_id and interaction.user.id != UserEnum.UserId.DARKIE.value:
            text = "Lệnh hiện tại chỉ mới dành cho Owner server!"
            await interaction.followup.send(f"{text}",ephemeral=True)
            return
        #Nếu là server owner thì chỉ việc remove như bình thường 
        else:
            authority = ProfileMongoManager.get_authority(guild_id=interaction.guild.id)
            if authority == None:
                await interaction.followup.send(f"Server không có chính quyền để lật đổ!",ephemeral=True)
                return
            authority.silver = 0
            authority.gold = 0
            authority.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= interaction.guild.id, data=authority)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=interaction.guild.id, user_id=authority.user_id)
            await interaction.followup.send(f"Bạn đã lật đổ chính quyền của Server!",ephemeral=True)
            channel = interaction.channel
            embed = discord.Embed(title=f"", description=f"Chính Quyền của server đã bị lật đổ! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            await channel.send(embed=embed)            

    #region unjail
    @discord.app_commands.describe(user="Chọn user cần thả tù treo.")
    @authority_group.command(name="unjail", description="Thả cầm tù dành cho những ai bị phạt tù!")
    async def unjail_authority_slash(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=False)
        #Kiểm tra xem server đã tồn tại ai là chính quyền chưa
        existed_authority = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
        if existed_authority == None:
            await interaction.followup.send(content=f"Server không tồn tại Chính Quyền! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", ephemeral=True)
            return
        if interaction.user.id != existed_authority.user_id and interaction.user.id != interaction.guild.owner_id:
            await interaction.followup.send(content=f"Chỉ chính quyền mới được quyền dùng lệnh này để thả giam những người bị tù!", ephemeral=True)
            return
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=user.id)
        if user_profile == None:
            await interaction.followup.send(content=f"Người này chưa dùng lệnh {SlashCommand.PROFILE.value}!", ephemeral=True)
            return
        ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=user.id, jail_time=None)
        await interaction.followup.send(content=f"Đã thả giam lệnh cho {user.display_name}!", ephemeral=False)
    
    #region Authority dropbox
    @discord.app_commands.checks.cooldown(1, 1800)
    @authority_group.command(name="dropbox", description="Kích hoạt thả hộp quà ngẫu nhiên!")
    async def dropbox_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Kiểm tra xem server đã tồn tại ai là chính quyền chưa
        existed_authority = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
        if existed_authority == None:
            await interaction.followup.send(content=f"Server không tồn tại Chính Quyền! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", ephemeral=True)
            return
        if interaction.user.id != existed_authority.user_id and interaction.user.id != interaction.guild.owner_id:
            await interaction.followup.send(content=f"Chỉ chính quyền mới được quyền dùng lệnh này để kích hoạt hộp quà ngẫu nhiên!", ephemeral=True)
            return
        if existed_authority != None and existed_authority.gold <100:
            await interaction.followup.send(content=f"Chính quyền cần 100 {EmojiCreation2.GOLD.value} thì mới tạo hộp quà ngẫu nhiên được!", ephemeral=True)
            return
        
        #Kiểm tra quest channel của server, nếu có thì mới chọn
        guild_info = db.find_guild_extra_info_by_id(guild_id=interaction.guild.id)
        if guild_info == None:
            await interaction.followup.send(content=f"Server chưa có channel dành cho thực hiện quest. Vui lòng dùng lệnh {SlashCommand.QUEST_CHANNELS.value} trước!", ephemeral=True)
            return
        if guild_info.list_channels_quests == None or len(guild_info.list_channels_quests) <= 0: 
            await interaction.followup.send(content=f"Server chưa có channel dành cho thực hiện quest. Vui lòng dùng lệnh {SlashCommand.QUEST_CHANNELS.value} trước!", ephemeral=True)
            return
        list_channels_quests = guild_info.list_channels_quests
        random_quest_channel_id = random.choice(list_channels_quests)
        quest_channel = interaction.guild.get_channel(random_quest_channel_id)
        if quest_channel == None:
            #Xoá channel_id lỗi
            list_channels_quests.remove(random_quest_channel_id)
            data_updated = {"list_channels_quests": list_channels_quests}
            db.update_guild_extra_info(guild_id=interaction.guild.id, update_data= data_updated)
            #Chọn channel khác không bị lỗi
            while quest_channel == None:
                random_quest_channel_id = random.choice(list_channels_quests)
                quest_channel = interaction.guild.get_channel(random_quest_channel_id)
        if quest_channel != None:
            endtime = datetime.now() + timedelta(seconds=60)
            embed = discord.Embed(title=f"", description=f"{EmojiCreation2.GOLDEN_GIFT_BOX.value} **Hộp Quà Thần Bí** {EmojiCreation2.GOLDEN_GIFT_BOX.value}", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Một hộp quà thần bí đã xuất hiện tại đúng channel này!", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Ai nhanh tay thì được nhé, vì hộp quà sẽ biến mất đúng sau: <t:{int(endtime.timestamp())}:R>", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.set_footer(text=f"Hộp quà sẽ xuất hiện ngẫu nhiên, và khi thấy thì nhớ nhanh tay nhé!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
            print(f"Created random dropbox at channel {quest_channel.name} in guild {interaction.guild.name}.")
            await interaction.followup.send(content=f"Đã trừ **100** {EmojiCreation2.GOLD.value} của Chính Quyền để tạo hộp quà may mắn!", ephemeral=True)
            ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=-100)
            view = RandomDropboxEconomyView()
            m = await quest_channel.send(embed=embed, view=view)
            view.old_message = m
        else:
            await interaction.followup.send(content=f"Server chưa có channel dành cho thực hiện quest. Vui lòng dùng lệnh {SlashCommand.QUEST_CHANNELS.value} trước!", ephemeral=True)
            return
    
    @dropbox_authority_slash.error
    async def dropbox_authority_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    #region Authority reset_rate
    @discord.app_commands.checks.cooldown(1, 1800)
    @authority_group.command(name="reset_rate", description="Reset tỷ lệ quy đổi của bank!")
    async def reset_rate_authority_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Kiểm tra xem server đã tồn tại ai là chính quyền chưa
        existed_authority = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
        if existed_authority == None:
            await interaction.followup.send(content=f"Server không tồn tại Chính Quyền! Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", ephemeral=True)
            return
        if interaction.user.id != existed_authority.user_id and interaction.user.id != interaction.guild.owner_id:
            await interaction.followup.send(content=f"Chỉ chính quyền mới được quyền dùng lệnh này để kích hoạt hộp quà ngẫu nhiên!", ephemeral=True)
            return
        if existed_authority != None and existed_authority.gold < 2000:
            await interaction.followup.send(content=f"Chính quyền cần 2000 {EmojiCreation2.GOLD.value} thì mới reset rate của bank được!", ephemeral=True)
            return
        rate_conver = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=interaction.guild_id)
        if rate_conver == None:
            await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.BANK.value} trước rồi thử lại sau!", ephemeral=True)
            return
        ConversionRateMongoManager.create_update_conversion_rate(guild_id=interaction.guild.id, rate=1.0)
        ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=-2000)
        await interaction.followup.send(content=f"Đã trừ **2000** {EmojiCreation2.GOLD.value} của Chính Quyền để reset lại rate của bank!", ephemeral=True)
    
    @reset_rate_authority_slash.error
    async def reset_rate_authority_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
        
        
        
    
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