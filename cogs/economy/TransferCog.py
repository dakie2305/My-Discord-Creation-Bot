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
    
    
    @commands.command()
    async def um(self, ctx, amount: int = None, user: discord.Member = None, loai_tien: str = None):
        #Chỉ dành owner hoặc Darkie
        message: discord.Message = ctx.message
        if message:
            view = SelfDestructView(timeout=5)
            text = ""
            if message.author.id != message.guild.owner_id and message.author.id != UserEnum.UserId.DARKIE.value:
                text = "Lệnh dành riêng cho Owner server để cập nhật tiền cho một user bất kỳ!"
            elif amount == None or user == None or loai_tien == None:
                text = f"Sai cú pháp lệnh! Vui lòng nhập đúng như bên dưới để chuyển {EmojiCreation2.COPPER.value}\n !um 100 @user C"
            elif loai_tien != "C" and loai_tien != "D" and loai_tien != "G" and loai_tien != "S":
                text = f"Sai loại tiền! Loại tiền chỉ được nhập một trong những giá trị sau: C, S, G, D"
            else:
                emoji = ""
                if loai_tien == "S" or loai_tien == "s":
                    emoji = f"{EmojiCreation2.SILVER.value}"
                    ProfileMongoManager.update_profile_money(guild_id=user.guild.id,guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, silver= amount)
                elif loai_tien == "G" or loai_tien == "g":
                    emoji = f"{EmojiCreation2.GOLD.value}"
                    ProfileMongoManager.update_profile_money(guild_id=user.guild.id,guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, gold= amount)
                elif loai_tien == "D" or loai_tien == "d":
                    emoji = f"{EmojiCreation2.DARKIUM.value}"
                    ProfileMongoManager.update_profile_money(guild_id=user.guild.id,guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, darkium= amount)
                else:
                    emoji = f"{EmojiCreation2.COPPER.value}"
                    ProfileMongoManager.update_profile_money(guild_id=user.guild.id,guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper= amount)
                text = f"Owner đã chuyển **{amount}** {emoji} cho {user.display_name}"
            embed = discord.Embed(title=f"", description=f"{text}", color=0xc379e0)
            mess = await message.reply(embed=embed, view=view)
            view.message = mess
            return  

    #region transfer
    @discord.app_commands.command(name="transfer", description="Chuyển tiền đến user trong server!")
    @discord.app_commands.describe(amount="Chọn số lượng tiền cần chuyển.")
    @discord.app_commands.describe(user="Chọn user để chuyển tiền.")
    @discord.app_commands.describe(message="Lời nhắn khi chuyển tiền.")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    async def transfer_slash_command(self, interaction: discord.Interaction, amount: int,  user: discord.Member, loai_tien: str, message: str = None):
        await interaction.response.defer()
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if user.id == interaction.user.id:
            await interaction.followup.send(f"Chuyển tiền cho bản thân chi vậy?", ephemeral=True)
            return
        #Kiểm tra xem người dùng lệnh đã tồn tại chưa
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", color=0xc379e0)
            await interaction.followup.send(embed=embed)
            return
        #Kiểm tra xem người nhận có tồn tại profile chưa
        receive_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=user.id)
        if receive_user == None:
            embed = discord.Embed(title=f"", description=f"Người nhận tiền {user.mention} vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", color=0xc379e0)
            await interaction.followup.send(embed=embed)
            return
        #Kiểm tra xem amount có âm không
        if amount <= 0:
            embed = discord.Embed(title=f"", description=f"Khỏi test bug! Vì gây lãng phí tài nguyên, {interaction.user.mention} đã bị trừ **500**{EmojiCreation2.COPPER.value}!", color=0xc379e0)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id,guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper= -500)
            await interaction.followup.send(embed=embed)
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
        
        tax = 150
        #Cộng tiền tax Copper cho chính quyền nếu user_profile không phải là chính quyền
        tax_text = ""
        extra_mess = ""
        if message != None:
            extra_mess = f" với lời nhắn: *{message}*"
        if user_profile.is_authority == False:
            tax_text = f"Đương nhiên là bị trừ {tax} {EmojiCreation2.COPPER.value} để đóng thuế cho Chính Quyền!"
            authority_profile = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
            if authority_profile:
                authority_profile.copper += int(tax * authority_profile.dignity_point/100)
                ProfileMongoManager.update_profile_money_fast(guild_id=interaction.guild_id, data=authority_profile)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper= -tax)
        #Cập nhập level progressing, transfer chỉ được cộng 1 ít
        ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id= user.id, bonus_exp= -10)
        ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id= interaction.user.id, bonus_exp= -10)
        await interaction.followup.send(f"{interaction.user.mention} đã chuyển **{amount}** {self.get_emoji_from_type(loai_tien)} cho {user.mention}{extra_mess}. {tax_text}", ephemeral=False)
    
    
    
    def get_emoji_from_type(self, input: str):
        if input == "D" or input == "D":
            return EmojiCreation2.DARKIUM.value
        if input == "G" or input == "G":
            return EmojiCreation2.GOLD.value
        if input == "S" or input == "S":
            return EmojiCreation2.SILVER.value
        if input == "C" or input == "C":
            return EmojiCreation2.COPPER.value
    
        