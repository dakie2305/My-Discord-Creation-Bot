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
import asyncio
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.Crime.AuthorityInterceptView import AuthorityInterceptView

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
        await interaction.response.defer(ephemeral=True)
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
                m = await interaction.followup.send(embed=embed, view=view)
                view.message = m
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
            m = await interaction.followup.send(embed=embed, view=view)
            view.message = m
            return
        #Nếu hơn người ta 10 level thì không cho cướp nữa
        elif action == "rob" and (user_profile.level -10 > target_profile.level):
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"{target_user.mention} cấp quá thấp, bạn không thể cướp của người thấp hơn mình 10 cấp!", color=0xe82517)
            m = await interaction.followup.send(embed=embed, view=view)
            view.message = m
            return
        #Đánh nhau mà không còn điểm nhân phẩm thì không cho đánh nhau
        elif action == "fight" and user_profile.dignity_point <= 10:
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"Điểm nhân phẩm bạn quá thấp, hãy tăng nhân phẩm bằng cách dùng lệnh {SlashCommand.WORK.value} hoặc {SlashCommand.DAILY.value} trước đi!", color=0xe82517)
            m = await interaction.followup.send(embed=embed, view=view)
            view.message = m
            return
        
        #Nếu buôn lậu thì cần ít nhất 2000 Copper trong profile
        elif action == "smuggler" and user_profile.copper < 2000:
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"{interaction.user.mention} cần ít nhất 2000 {EmojiCreation2.COPPER.value} để thực hiện buôn lậu!", color=0xe82517)
            m = await interaction.followup.send(embed=embed, view=view)
            view.message = m
            return
        
        elif user_profile != None and user_profile.last_crime != None:
            time_window = timedelta(hours=1)
            check = self.check_if_within_time_delta(input=user_profile.last_crime, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào 1h xem chừng nào mới crime được tiếp
                crime_next_time = user_profile.last_crime + time_window
                unix_time = int(crime_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã làm việc xấu rồi. Vui lòng thực hiện lại lệnh {SlashCommand.CRIME.value} vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=30)
                m = await interaction.followup.send(embed=embed, view=view)
                view.message = m
                return

        if action == "fight":
            await self.process_fight_command(interaction=interaction, user=interaction.user, target_user=target_user, user_profile=user_profile, target_profile=target_profile)
        else:
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"Chức năng này vẫn chưa hoàn thiện, Darkie vẫn đang code!", color=0xe82517)
            m = await interaction.followup.send(embed=embed, view=view)
            view.message = m
            return
        
        
    async def process_fight_command(self, interaction: discord.Interaction, user: discord.Member, target_user: discord.Member, user_profile: Profile, target_profile: Profile):
        authority_user = ProfileMongoManager.get_authority(guild_id=user.guild.id)
        win_lines = [
                    "{user_name} đã chọc vào móc {target_name} và đã thắng!",
                     "{user_name} đã móc súng ra, và {target_name} đã chấp nhận hoà giải!",
                     "{user_name} đã nhanh chóng khống chế được {target_name}!",
                     "{user_name} đã ra đòn chí mạng, hạ con mẹ nó gục {target_name}!",
                     "{user_name} đã đánh bại {target_name} bằng kỹ năng thượng thừa!",
                     "{user_name} đã khoá mồm {target_name} thành công!",
                     "{user_name} đã áp đảo {target_name} đến mức Mike Tyson phải gọi bằng mồm!",
                     "{target_name} không hề đủ tuổi so với {user_name}!",
                     "{target_name} tuổi con tôm với {user_name}!",
                     "{target_name} cố gắng chống trả, nhưng {user_name} đã ra tay chấm dứt trận đấu!",
                     ]
        lose_lines = [
            "{user_name} không hề đủ tuổi so với {target_name}!",
            "{user_name} tuổi con tôm với {target_name}!",
            "{target_name} đã gọi anh em hội động ngược lại {user_name}!",
            "{user_name} tưởng mình ngon, nhưng tuổi l với {target_name}!",
            "{user_name} đã đi sai nước, và bị {target_name} đánh lại cho bầm dập!",
            "{user_name} đã chọn sai đối thủ, và bị {target_name} đánh cho lên bờ xuống ruộng!",
            "{user_name} đã bị {target_name} vả cho lệch mồm!",
            "{user_name} định lao đến thì {target_name} đã móc súng ra nên {user_name} chỉ có thể xin giảng hoà!",
            ]
        
        fighting_gif_link = [
            "https://i.pinimg.com/originals/bf/d4/7c/bfd47c06b2f98db0877b56d990e73662.gif",
            "https://i.pinimg.com/originals/bc/e4/b9/bce4b931cb3e21bedf6e9384fa19b6a3.gif",
            "https://i.pinimg.com/originals/41/bc/1a/41bc1ad4b1477371329a30b9e06466dd.gif",
            "https://i.pinimg.com/originals/36/c8/99/36c899aab751ae2e8d397592b1ea89a1.gif",
            "https://i.pinimg.com/originals/09/6a/2b/096a2b76d0b8c00c40a69547933ab7c8.gif",
        ]
        
        #Fight sẽ dựa vào level để xác định tỉ lệ thắng của user và target_user
        user_win_fight = False
        if user_profile.level < target_profile.level:
            user_win_fight = self.get_chance(25)
        else:
            user_win_fight = self.get_chance(75)
        
        preloading_text = f"{user.mention} đã lao đến đánh lộn với {target_user.mention}!\nCó thể gọi Chính Quyền vào cuộc để ngăn chặn ẩu đả này!"
        embed = discord.Embed(title=f"", description=f"{preloading_text}", color=0xc379e0)
        embed.set_image(url=random.choice(fighting_gif_link))
        view = AuthorityInterceptView(user=user, user_profile=user_profile, crime_type="fight", target_profile=target_profile, target_user=target_user, authority_user=authority_user)
        await interaction.followup.send(f"Bạn đã gây gỗ!", ephemeral=True)
        channel = interaction.channel
        m = await channel.send(embed=embed, view=view, content=f"{target_user.mention}")
        view.old_message = m
        #Đợi 30s để xác định người thắng
        await asyncio.sleep(30)
        result_text =f""
        if user_win_fight:
            result_text = random.choice(win_lines)
            result_text = result_text.replace("{user_name}", user.mention)
            result_text = result_text.replace("{target_name}", target_user.mention)
            dignity_point = 10
            result_text += f"\n{user.mention} đã đánh thắng {target_user.mention} nên cả hai đều mất **{dignity_point} nhân phẩm** như nhau!"
            #Trừ nhân phẩm cả hai
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target_user.id, user_name=target_user.name, user_display_name=target_user.display_name, dignity_point= -dignity_point)
            #Cộng kinh nghiệm cho người thắng
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=user.id)
            
        else:
            result_text = random.choice(lose_lines)
            result_text = result_text.replace("{user_name}", user.mention)
            result_text = result_text.replace("{target_name}", target_user.mention)
            dignity_point = 15
            result_text += f"\n{user.mention} đã đánh thua {target_user.mention}, nên {user.display_name} đã bị trừ  **{dignity_point} nhân phẩm**!"
            #Trừ nhân phẩm người đánh
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        #Update last_crime
        ProfileMongoManager.update_last_crime_now(guild_id=interaction.guild_id, user_id=user.id)
        
        new_embed = discord.Embed(title=f"", description=f"{result_text}", color=0xc379e0)
        await channel.send(embed=new_embed)
        await m.delete()
    
    def get_chance(self, chance: int):
        rand_num = random.randint(0, 100)
        if rand_num < chance:
            return True
        else:
            return False

        
        
        
    def check_if_within_time_delta(self, input: datetime, time_window: timedelta):
        now = datetime.now()
        if now - time_window <= input <= now + time_window:
            return True
        else:
            return False
    
        