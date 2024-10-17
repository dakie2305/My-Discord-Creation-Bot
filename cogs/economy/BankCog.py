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
from enum import Enum
from datetime import datetime
import random
import CustomFunctions
import CustomEnum.UserEnum as UserEnum

async def setup(bot: commands.Bot):
    await bot.add_cog(BankEconomy(bot=bot))
    print("Bank Economy is ready!")

class BankEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    class CurrencyEmoji(Enum):
        DARKIUM = "<a:darkium:1294615481701105734>"
        GOLD = "<a:gold:1294615502588608563>"
        SILVER = "<a:silver:1294615512919048224>"
        COPPER = "<a:copper:1294615524918956052>"
    
    class CurrencySlashCommand(Enum):
        PROFILE = "</profile:1294699979058970656>"
        VOTE_AUTHORITY = "</vote_authority:1294754901988999240>"
    
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
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {self.CurrencySlashCommand.PROFILE.value} trước đã!", color=0xddede7)
            return embed, None
        
        authority = ProfileMongoManager.is_authority_existed(guild_id=user.guild.id)
        if authority == None:
            embed = discord.Embed(title=f"", description=f"Server vẫn chưa tồn tại Chính Quyền. Vui lòng dùng lệnh {self.CurrencySlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            return embed, None
        authority_user = self.bot.get_guild(user.guild.id).get_member(authority.user_id)
        # Nếu không get được tức là authority không trong server
        if authority_user == None:
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã lưu vong khỏi server. Vui lòng dùng lệnh {self.CurrencySlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            ProfileMongoManager.remove_authority_from_server(guild_id=user.guild.id)
            return embed, None
        
        conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=user.guild.id)
        if conversion_rate == None:
            ConversionRateMongoManager.create_update_conversion_rate(guild_id=user.guild.id, rate=1)
            conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=user.guild.id)
        elif conversion_rate != None and conversion_rate.last_reset != None and conversion_rate.last_reset.date() != datetime.now().date():
            #Random tỷ lệ rate
            allowed_values = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
            new_rate = random.choice(allowed_values)
            ConversionRateMongoManager.create_update_conversion_rate(guild_id=user.guild.id, rate=new_rate)
            conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=user.guild.id)
        
        
        embed = discord.Embed(title=f"**Ngân Hàng Chính Quyền Tối Cao**", description=f"{authority_user.mention} hiện đang là Chính Quyền", color=0xddede7)
        embed.add_field(name=f"", value="\n", inline=False)
        embed.add_field(name=f"", value=f"Tỷ lệ quy đổi tiền hôm nay: **{conversion_rate.rate}**", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        
        embed.add_field(name="", value=f">>> 1 {self.CurrencyEmoji.DARKIUM.value} = **{int(10000 * conversion_rate.rate)}** {self.CurrencyEmoji.GOLD.value}", inline=False)
        embed.add_field(name="", value=f">>> 1 {self.CurrencyEmoji.GOLD.value} = **{int(5000 * conversion_rate.rate)}** {self.CurrencyEmoji.SILVER.value}", inline=False)
        embed.add_field(name="", value=f">>> 1 {self.CurrencyEmoji.SILVER.value} = **{int(5000 * conversion_rate.rate)}** {self.CurrencyEmoji.COPPER.value}", inline=False)
        
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Để hiểu rõ hơn về cách ngân hàng hoạt động hãy dùng nhắn câu:\nbank help", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
        
        bank_view = BankView(authority=authority, rate=conversion_rate.rate)
        
        return embed, bank_view
        
        
    
    