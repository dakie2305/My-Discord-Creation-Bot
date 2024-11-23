import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from  Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from Handling.Economy.Bank.BankView import BankView
from Handling.Misc.SelfDestructView import SelfDestructView
from datetime import datetime, time
import random
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2

async def setup(bot: commands.Bot):
    await bot.add_cog(BankEconomy(bot=bot))
    print("Bank Economy is ready!")

class BankEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #region Bank
    @discord.app_commands.command(name="bank", description="Gọi ngân hàng chính quyền để đổi tiền")
    async def show_bank_info(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if self.is_within_time_range():
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Hệ thống bank đang trong giai đoạn bổ sung tiền! Vui lòng đợi 10' nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        self_delete_view = SelfDestructView(timeout=120)
        embed, bank_view = await self.get_bank_embed(user=interaction.user)
        if bank_view == None:
            mess = await interaction.followup.send(embed=embed, view=self_delete_view)
            self_delete_view.message = mess
        else:
            mess = await interaction.followup.send(embed=embed, view=bank_view)
            bank_view.message = mess
        return

    @commands.command()
    async def bank(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            
            if self.is_within_time_range():
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Hệ thống bank đang trong giai đoạn bổ sung tiền! Vui lòng đợi 10' nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            
            self_delete_view = SelfDestructView(timeout=120)
            embed, bank_view = await self.get_bank_embed(user=message.author)
            if bank_view == None:
                mess = await message.reply(embed=embed, view=self_delete_view)
                self_delete_view.message = mess
            else:
                me = await message.reply(embed=embed, view=bank_view)
                bank_view.message = me
    
    
    async def get_bank_embed(self, user: discord.Member):
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        if user_profile == None:
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", color=0xddede7)
            return embed, None
        
        authority = ProfileMongoManager.get_authority(guild_id=user.guild.id)
        if authority == None:
            embed = discord.Embed(title=f"", description=f"Server vẫn chưa tồn tại Chính Quyền. Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            return embed, None
        authority_user = self.bot.get_guild(user.guild.id).get_member(authority.user_id)
        # Nếu không get được tức là authority không trong server
        if authority_user == None:
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã lưu vong khỏi server. Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            ProfileMongoManager.remove_authority_from_server(guild_id=user.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=user.guild.id, user_id=authority.user_id)
            return embed, None
        
        #Kiểm xem chính quyền có mặc nợ không, có thì từ chức và phạt authority
        if ProfileMongoManager.is_in_debt(data= authority, copper_threshold=100000):
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            authority.copper = -10000
            authority.silver = 0
            authority.gold = 0
            authority.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= user.guild.id, data=authority)
            ProfileMongoManager.remove_authority_from_server(guild_id=user.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=user.guild.id, user_id=authority.user_id)
            return embed, None
        
        conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=user.guild.id)
        if conversion_rate == None:
            ConversionRateMongoManager.create_update_conversion_rate(guild_id=user.guild.id, rate=1)
            conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=user.guild.id)
        elif conversion_rate != None and conversion_rate.last_reset != None and conversion_rate.last_reset.date() != datetime.now().date():
            #Random tỷ lệ rate
            allowed_values = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
            new_rate = random.choice(allowed_values)
            ConversionRateMongoManager.create_update_conversion_rate(guild_id=user.guild.id, rate=new_rate)
            conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=user.guild.id)
        
        
        embed = discord.Embed(title=f"**Ngân Hàng Chính Quyền Tối Cao**", description=f"{authority_user.mention} hiện đang là Chính Quyền", color=0xddede7)
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value=f"Tỷ lệ quy đổi tiền hôm nay: **{conversion_rate.rate}**", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        
        embed.add_field(name="", value=f">>> 1 {EmojiCreation2.DARKIUM.value} = **{int(10000 * conversion_rate.rate)}** {EmojiCreation2.GOLD.value}", inline=False)
        embed.add_field(name="", value=f">>> 1 {EmojiCreation2.GOLD.value} = **{int(5000 * conversion_rate.rate)}** {EmojiCreation2.SILVER.value}", inline=False)
        embed.add_field(name="", value=f">>> 1 {EmojiCreation2.SILVER.value} = **{int(5000 * conversion_rate.rate)}** {EmojiCreation2.COPPER.value}", inline=False)
        
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Để hiểu rõ hơn về cách ngân hàng hoạt động hãy dùng nhắn câu:\nbank help", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/9e8749a5a47cae53211484d7aee42040.webp?size=100&quot")
        
        bank_view = BankView(authority=authority, rate=conversion_rate.rate)
        
        return embed, bank_view
        
        
    def is_within_time_range(self):
        now = datetime.now().time()
        start_time = time(23, 55)
        end_time = time(0, 5)
        # midnight
        if start_time <= now or now <= end_time:
            return True
        return False
    