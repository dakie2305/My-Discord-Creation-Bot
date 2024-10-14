import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Economy.Authority.AuthorityView import AuthorityView
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import CurrencyEmoji

        
async def setup(bot: commands.Bot):
    await bot.add_cog(TransferMoneyEconomy(bot=bot))
    print("Transfer Money Economy is ready!")

class TransferMoneyEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def transfer(self, ctx, user: Optional[discord.Member] = None):
        message: discord.Message = ctx.message
        if message:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"", description=f"Không hỗ trợ lệnh prefix. Vui lòng dùng lệnh {SlashCommand.TRANSFER.value} đi.", color=0xc379e0)
            mess = await message.reply(embed=embed, view=view)
            view.message = mess
    
    
    #region transfer
    @discord.app_commands.command(name="transfer", description="Chuyển tiền đến user trong server!")
    @discord.app_commands.describe(amount="Chọn số lượng tiền cần chuyển.")
    @discord.app_commands.describe(user="Chọn user để chuyển tiền.")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Darkium", value="D"),
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    async def transfer_slash_command(self, interaction: discord.Interaction, amount: int,  user: discord.Member, loai_tien: str):
        await interaction.response.defer(ephemeral=False)
        
        if user.id == interaction.user.id:
            await interaction.followup.send(f"Chuyển tiền cho bản thân chi vậy?", ephemeral=True)
            return
        #Kiểm tra xem người dùng lệnh đã tồn tại chưa
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", color=0xc379e0)
            interaction.followup.send(embed=embed)
            return
        #Kiểm tra xem người dùng lệnh có đủ tiền không
        not_sufficient = False
        if loai_tien == "C" and user_profile.copper < amount:
            not_sufficient = True
        elif loai_tien == "S" and user_profile.silver < amount:
            not_sufficient = True
        elif loai_tien == "G" and user_profile.gold < amount:
            not_sufficient = True
        elif loai_tien == "D" and user_profile.darkium < amount:
            not_sufficient = True
        if not_sufficient:
            await interaction.followup.send(f"Bạn làm gì đủ tiền mà đòi chuyển?", ephemeral=True)
            return
        
        if loai_tien == "C":
            #Trừ người gửi
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper= -amount)
            #Cộng người chuyển
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper= amount)
        elif loai_tien == "G":
            #Trừ người gửi
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, gold= -amount)
            #Cộng người chuyển
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, gold= amount)
        elif loai_tien == "S":
            #Trừ người gửi
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, silver= -amount)
            #Cộng người chuyển
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, silver= amount)
        elif loai_tien == "D":
            #Trừ người gửi
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, darkium= -amount)
            #Cộng người chuyển
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, darkium= amount)
        
        tax = 50
        #Cộng tiền tax Copper cho chính quyền nếu user_profile không phải là chính quyền
        tax_text = ""
        if user_profile.is_authority == False:
            tax_text = f"Đương nhiên là bị trừ {tax} {CurrencyEmoji.COPPER.value} để đóng thuế cho Chính Quyền!"
            authority_profile = ProfileMongoManager.is_authority_existed(guild_id=interaction.guild_id)
            if authority_profile:
                authority_profile.copper += tax
                ProfileMongoManager.update_profile_money_fast(guild_id=interaction.guild_id, data=authority_profile)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper= -tax)
        await interaction.followup.send(f"{interaction.user.mention} đã chuyển **{amount}** {self.get_emoji_from_type(loai_tien)} cho {user.mention}. {tax_text}", ephemeral=False)
    
    
    
    
    
    def get_emoji_from_type(self, input: str):
        if input == "D" or input == "D":
            return CurrencyEmoji.DARKIUM.value
        if input == "G" or input == "G":
            return CurrencyEmoji.GOLD.value
        if input == "S" or input == "S":
            return CurrencyEmoji.SILVER.value
        if input == "C" or input == "C":
            return CurrencyEmoji.COPPER.value
    
        