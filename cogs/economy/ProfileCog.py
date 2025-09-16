import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Economy.Authority.AuthorityView import AuthorityView
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Economy.Profile.InventoryBackToProfileView import ProfileAdditionalView, BackToProfileView
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
from datetime import datetime, timedelta
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum

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
            embed, data = await self.procress_profile_embed(user=interaction.user, guild_id=interaction.guild_id)
        else:
            embed, data = await self.procress_profile_embed(user=user, guild_id=interaction.guild_id)
        if data != None:
            view = ProfileAdditionalView(profile=data, profile_embed=embed)
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
            if user!= None and user.id == 315835396305059840:
                user_profile = ProfileMongoManager.find_profile_by_id(guild_id=message.guild.id, user_id=message.author.id)
                if user_profile == None:
                    user_profile = ProfileMongoManager.create_profile(guild_id=message.author.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name)
                #Trừ 50% số tiền lớn nhất
                money_cost = 1000
                emoji = EmojiCreation2.COPPER.value
                if user_profile.darkium > 0:
                    money_cost = int(user_profile.darkium * 50 / 100)
                    emoji = EmojiCreation2.DARKIUM.value
                elif user_profile.gold > 0:
                    money_cost = int(user_profile.gold * 50 / 100)
                    emoji = EmojiCreation2.GOLD.value
                elif user_profile.silver > 0:
                    money_cost = int(user_profile.silver * 50 / 100)
                    emoji = EmojiCreation2.SILVER.value
                else:
                    money_cost = int(user_profile.copper * 50 / 100)
                    emoji = EmojiCreation2.COPPER.value
                if money_cost == 0: money_cost = 1000
                if emoji == EmojiCreation2.COPPER.value and money_cost < 500: money_cost = 500
                if emoji == EmojiCreation2.COPPER.value:
                    ProfileMongoManager.update_profile_money(guild_id=message.guild.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, copper=-money_cost)
                elif emoji == EmojiCreation2.SILVER.value:
                    ProfileMongoManager.update_profile_money(guild_id=message.guild.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, silver=-money_cost)
                elif emoji == EmojiCreation2.GOLD.value:
                    ProfileMongoManager.update_profile_money(guild_id=message.guild.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, gold=-money_cost)
                else:
                    ProfileMongoManager.update_profile_money(guild_id=message.guild.id, guild_name=message.author.guild.name, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, darkium=-money_cost)
                embed = discord.Embed(title=f"Đã bảo là không tag t nữa!", description=f"Vì đã quay vào ô mất lượt nên {message.author.mention} đã mất **{money_cost}** {emoji}!",color=discord.Color.blue())
                mess = await message.reply(embed=embed)
                return
            data = None
            view = None
            if user == None:
                embed, data = await self.procress_profile_embed(user=message.author, guild_id=message.guild.id)
            else:
                embed, data = await self.procress_profile_embed(user=user, guild_id=message.guild.id)
            if data != None:
                view = ProfileAdditionalView(profile=data)
                m = await message.reply(embed=embed, view= view)
                view.message = m
            else:
                await message.reply(embed=embed)
    #Quote
    @commands.command()
    async def quote(self, ctx, *, quote: str = None):
        message: discord.Message = ctx.message
        if message:
            if not quote or quote.strip() == "":
                await message.reply(
                    content="👉 Dùng lệnh như sau: `!quote tôi bị khùng`"
                )
                return
            if len(quote.split()) > 50:
                await message.reply(content="Độ dài quá ký tự cho phép")
                return
            if len(quote) > 800:
                await message.reply(content="Độ dài quá ký tự cho phép")
                return
            embed = discord.Embed(title=f"", description=f"Đã cập nhật quote thành công. Vui lòng dùng lệnh {SlashCommand.PROFILE.value} để xem profile.", color=0xffffff)
            ProfileMongoManager.update_profile_quote(guild_name=message.guild.name, guild_id=message.guild.id, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, quote=quote)
            view = SelfDestructView(timeout=30)
            message_sent = await message.reply(embed=embed, view=view)
            view.message = message_sent
    
    async def procress_profile_embed(self, user: discord.Member, guild_id: int):
        data = ProfileMongoManager.find_profile_by_id(guild_id=guild_id, user_id=user.id)
        if data == None:
            data = ProfileMongoManager.create_profile(guild_id=guild_id, user_id=user.id, guild_name=user.guild.name, user_name=user.name, user_display_name=user.display_name)
            if data == None:
                embed = discord.Embed(title=f"", description=f"Không thể tạo profile! Vui lòng thử lại!", color=0xffffff)
                return embed, None
        
        if data.guardian!= None and data.guardian.time_to_recover!= None:
            if data.guardian.time_to_recover < datetime.now():
                #Hồi phục 50% máu, 50% thể lực
                health = int(data.guardian.max_health*50/100)
                stamina = int(data.guardian.max_stamina*50/100)
                ProfileMongoManager.update_guardian_stats(guild_id=guild_id,user_id=user.id, health=health, stamina=stamina)
                data = ProfileMongoManager.find_profile_by_id(guild_id=guild_id, user_id=user.id)
        
        if data.is_authority and ProfileMongoManager.is_in_debt(data= data, copper_threshold=100000):
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xffffff)
            data.copper = -10000
            data.silver = 0
            data.gold = 0
            data.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= guild_id, data=data)
            ProfileMongoManager.remove_authority_from_server(guild_id=guild_id)
            ProfileMongoManager.update_last_authority(guild_id=guild_id, user_id=data.user_id)
            return embed, None
        
        couple_info = CoupleMongoManager.find_couple_by_id(guild_id=guild_id, user_id=user.id)
        if couple_info!= None and couple_info.first_user_id == couple_info.second_user_id:
            #Nếu ai tạo trùng thì xoá
            couple_info = None
            CoupleMongoManager.delete_couple_by_id(guild_id=guild_id, user_id=user.id)
        
        cq = ""
        #Đặc quyền server tổng
        if user.guild.id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            for role in user.roles:
                if role.id == TrueHeavenEnum.TOP_1_QUEST.value:
                    cq = "Huyền Thoại Thợ Săn Tiền Thưởng"
                elif role.id == TrueHeavenEnum.TOP_1_WEALTH.value:
                    cq = "Tài Sản Giàu Nứt Vách Đổ Tường"
                elif role.id == TrueHeavenEnum.TOP_1_GUARDIAN.value:
                    cq = "Huyển Thoại Hộ Vệ Thần Đỉnh Cấp"
                elif role.id == TrueHeavenEnum.TOP_1_WORD_MATCHING.value:
                    cq = "Kẻ Nối Từ Đỉnh Cấp Nhất"
                elif role.id == TrueHeavenEnum.TOP_1_WORD_SORT.value:
                    cq = "Kẻ Đoán Từ Đỉnh Cấp Nhất"
                elif role.id == TrueHeavenEnum.TOP_1_WORD_SORT.value:
                    cq = "Kẻ Đoán Từ Đỉnh Cấp Nhất"
                elif role.id == TrueHeavenEnum.DRAGON_WARRIOR_DONATOR.value:
                    cq = "Thần Long Đại Hiệp"
                elif role.id == TrueHeavenEnum.LONG.value:
                    cq = "Long Đại Thần"
                elif role.id == TrueHeavenEnum.ULTIMATE_SUGAR_DADDY.value:
                    cq = "Bố Đường Tối Thượng"
                elif role.id == TrueHeavenEnum.DONATOR.value:
                    cq = "Mạnh Thường Quân Huyền Thoại"
        if data.is_authority:
            cq = "Chính Quyền Tối Cao"

        embed_color = 0xffffff
        if isinstance(data.profile_color, int) and 0x000000 <= data.profile_color <= 0xFFFFFF:
            embed_color = data.profile_color
        embed = discord.Embed(title=cq, description=f"**Profile {user.mention}**", color=embed_color)
        if user.avatar != None:
            embed.set_thumbnail(url=user.avatar.url)
        if data.protection_item != None:
            embed.add_field(name=f"", value=f"Bảo Hộ Vật: [{data.protection_item.emoji} - **{data.protection_item.item_name}**]", inline=False)
        if data.attack_item != None:
            embed.add_field(name=f"", value=f"Vũ Khí: [{data.attack_item.emoji} - **{data.attack_item.item_name}**]", inline=False)
        embed.add_field(name=f"", value=f"Nhân phẩm: **{UtilitiesFunctions.get_nhan_pham(data.dignity_point)}** ({data.dignity_point})", inline=True)
        embed.add_field(name=f"", value=f"Địa Vị: **{UtilitiesFunctions.get_dia_vi(data)}**", inline=True)
        if data.level > 100:
            embed.add_field(name=f"", value=f"Rank: **{data.level} (Vô Hư Phá)**", inline=False)
        else:
            embed.add_field(name=f"", value=f"Rank: **{data.level}**", inline=False)
        bar_progress = self.progress_bar(input_value= data.level_progressing)
        embed.add_field(name=f"", value=f"{bar_progress}\n", inline=False)
        if couple_info!= None:
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"Tình trạng cặp đôi: **{UtilitiesFunctions.get_text_on_love_rank(couple_info.love_rank)}** (**{couple_info.love_rank}**)", inline=False)
            embed.add_field(name=f"", value=f"<@{couple_info.first_user_id}> -`{UtilitiesFunctions.get_heart_emoji_on_rank(couple_info.love_rank)}´- <@{couple_info.second_user_id}>", inline=False)
            embed.add_field(name=f"", value=f"Điểm thân mật: **{couple_info.love_point}**", inline=False)
            embed.add_field(name=f"", value=f"Tỉ lệ thăng hoa cảm xúc: **{int(couple_info.love_progressing/1000*100)}%**", inline=False)
            date_created = couple_info.date_created
            unix_time = int(date_created.timestamp())
            embed.add_field(name=f"", value=f"Ngày đầu quen nhau: <t:{unix_time}:D>", inline=False)
            if couple_info.date_married != None:
                date_married = couple_info.date_married
                unix_time_m = int(date_married.timestamp())
                embed.add_field(name=f"", value=f"Ngày cưới nhau: <t:{unix_time_m}:D>", inline=False)
        
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
        embed.set_footer(text=f"Profile của {user.name}.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        
        if user.guild.id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            #Của true heaven
            await self.update_rank_role(user= user, profile= data)
        return embed, data
    
    async def update_rank_role(self, user: discord.Member, profile: Profile):
        if user.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
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

    