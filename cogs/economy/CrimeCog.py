from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from CustomEnum.RoleEnum import TrueHeavenRoleId
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import random
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
import CustomFunctions
from discord.app_commands import Choice
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from Handling.Economy.Profile.ProfileClass import Profile

async def setup(bot: commands.Bot):
    await bot.add_cog(CrimeEconomy(bot=bot))
    print("Crime Economy is ready!")

class CrimeEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def crime(self, ctx):
        message: discord.Message = ctx.message
        if message:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không hỗ trợ prefix command. Vui lòng dùng lệnh /crime !",color=discord.Color.blue())
            mes = await message.reply(embed=embed, view=view)
            if view != None:
                view.message = mes
            return
    
    #region crime
    @discord.app_commands.choices(action=[
        Choice(name="Đánh nhau, gây gỗ người khác", value="fight"),
        Choice(name="Cướp bóc người khác", value="rob"),
        Choice(name="Xúc phạm nhân phẩm người khác", value="insult"),
        Choice(name="Rửa tiền, trốn thuế", value="laundry"),
        Choice(name="Buôn lậu, tuồn hàng cấm", value="smuggler"),
    ])
    @discord.app_commands.describe(action="Chọn loại hành vi phạm tội.")
    @discord.app_commands.command(name="crime", description="Lệnh thực hiện các hành vi phạm tội!")
    async def crime_slash_command(self, interaction: discord.Interaction, action: str, target_user: discord.Member):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang làm lệnh này! Vui lòng đợi nhé!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if target_user.bot:
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"Không được chọn Bot!", color=0xe82517)
            await interaction.followup.send(embed=embed, view=view)
            return
        
        #Nếu cướp, đánh, chửi thì interaction user khác target
        if action == "rob" or action == "fight" or action == "insult":
            if interaction.user.id == target_user.id:
                view = SelfDestructView(30)
                embed = discord.Embed(title=f"", description=f"Bạn không thể chọn bản thân!", color=0xe82517)
                await interaction.followup.send(embed=embed, view=view)
                return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            user_profile = ProfileMongoManager.create_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name)
        
        target_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if target_profile == None:
            target_profile = ProfileMongoManager.create_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target_user.id, user_name=target_user.name, user_display_name=target_user.display_name)
        
        
        #Nếu quá nghèo thì bỏ
        if action == "rob" and target_profile.copper < 10000 and target_profile.silver <= 0 and target_profile.gold <= 0 and target_profile.darkium <= 0:
            view = SelfDestructView(60)
            embed = discord.Embed(title=f"", description=f"{target_user.mention} quá nghèo, bạn không thể cướp của người quá nghèo!", color=0xe82517)
            await interaction.followup.send(embed=embed, view=view)
            return
        #Nếu hơn người ta 10 level thì không cho cướp nữa
        elif action == "rob" and (user_profile.level -10 > target_profile.level):
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"{target_user.mention} cấp quá thấp, bạn không thể cướp của người thấp hơn mình 10 cấp!", color=0xe82517)
            await interaction.followup.send(embed=embed, view=view)
            return
        
        #Nếu buôn lậu thì cần ít nhất 2000 Copper trong profile
        elif action == "smuggler" and user_profile.copper < 2000:
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"{interaction.user.mention} cần ít nhất 2000 {EmojiCreation2.COPPER.value} để thực hiện buôn lậu!", color=0xe82517)
            await interaction.followup.send(embed=embed, view=view)
            return

        await interaction.followup.send("Lệnh đang hoàn thiện sau!")
        return
        view = SelfDestructView(60)
        embed, view = await self.embed_crime_command(user=interaction.user)
        mess = await interaction.followup.send(embed=embed)
        
        return
        
    async def embed_crime_command(self, user: discord.Member, target_user: discord.Member, action: str):
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        
        if user_profile != None and user_profile.last_crime != None:
            time_window = timedelta(hours=1, minutes=30)
            check = self.check_if_within_time_delta(input=user_profile.last_crime, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào 1h30 xem chừng nào mới làm việc được tiếp
                crime_next_time = user_profile.last_crime + time_window
                unix_time = int(crime_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã làm việc rồi. Vui lòng thực hiện lại lệnh {SlashCommand.WORK.value} vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                return embed, view
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                return embed, None
            else:
                ProfileMongoManager.update_jail_time(guild_id=user.guild.id, user_id=user.id, jail_time=None)
        
        authority_user = ProfileMongoManager.is_authority(guild_id=user.guild.id, user_id= user.id)
        dignity_point = 50
        tax = 80
        pay_tax = True
        bonus = False
        
        
        
        
    def check_if_within_time_delta(self, input: datetime, time_window: timedelta):
        now = datetime.now()
        if now - time_window <= input <= now + time_window:
            return True
        else:
            return False
    
        