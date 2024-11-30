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
        
        #Phải tồn tại chính quyền server thì mới được crime
        authority = ProfileMongoManager.get_authority(guild_id=interaction.guild.id)
        if authority == None:
            embed = discord.Embed(title=f"", description=f"Server vẫn chưa tồn tại Chính Quyền. Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            await interaction.followup.send(embed=embed)
            return
        
        authority_user = self.bot.get_guild(interaction.guild.id).get_member(authority.user_id)
        # Nếu không get được tức là authority không trong server
        if authority_user == None:
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã lưu vong khỏi server. Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=interaction.user.guild.id, user_id=authority.user_id)
            await interaction.followup.send(embed=embed)
            return
        
        #Kiểm xem chính quyền có mặc nợ không, có thì từ chức và phạt authority
        if ProfileMongoManager.is_in_debt(data= authority, copper_threshold=100000):
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            authority.copper = -10000
            authority.silver = 0
            authority.gold = 0
            authority.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= interaction.user.guild.id, data=authority)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.user.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=interaction.user.guild.id, user_id=authority.user_id)
            await interaction.followup.send(embed=embed)
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
        
        target_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=target_user.id)
        if target_profile == None:
            target_profile = ProfileMongoManager.create_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target_user.id, user_name=target_user.name, user_display_name=target_user.display_name)
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> để thực hiện lại lệnh!", color=0xc379e0)
                view = SelfDestructView(60)
                m = await interaction.followup.send(embed=embed, view=view)
                view.message = m
                return
        
        #Nếu quá nghèo thì bỏ
        if action == "rob" and target_profile.copper < 10000 and target_profile.silver <= 0 and target_profile.gold <= 0:
            print(f"target_profile.copper: {target_profile.copper} target_profile.silver {target_profile.silver} target_profile.gold {target_profile.gold}")
            view = SelfDestructView(60)
            embed = discord.Embed(title=f"", description=f"{target_user.mention} quá nghèo, bạn không thể cướp của người có địa vị Hạ Đẳng!", color=0xe82517)
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
        elif user_profile.dignity_point <= 10:
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
        elif action == "rob":
            await self.process_rob_command(interaction=interaction, user=interaction.user, target_user=target_user, user_profile=user_profile, target_profile=target_profile)
        elif action == "laundry":
            await self.process_laundry_command(interaction=interaction, user=interaction.user, target_user=target_user, user_profile=user_profile, target_profile=target_profile)
        elif action == "smuggler":
            await self.process_smuggler_command(interaction=interaction, user=interaction.user, target_user=target_user, user_profile=user_profile, target_profile=target_profile)
        else:
            view = SelfDestructView(30)
            embed = discord.Embed(title=f"", description=f"Chức năng này vẫn chưa hoàn thiện, Darkie vẫn đang code!", color=0xe82517)
            m = await interaction.followup.send(embed=embed, view=view)
            view.message = m
            return
        
    #region Rob
    async def process_rob_command(self, interaction: discord.Interaction, user: discord.Member, target_user: discord.Member, user_profile: Profile, target_profile: Profile):    
        authority_user = ProfileMongoManager.get_authority(guild_id=user.guild.id)
        #Rob sẽ dựa vào level để xác định tỉ lệ thắng của user và target_user
        user_win = False
        if user_profile.is_authority == False:
            if user_profile.level + 5 < target_profile.level:
                user_win = self.get_chance(25)
            else:
                if target_profile.is_authority == True:
                    user_win = self.get_chance(40)
                else: user_win = self.get_chance(75)
        else:
            user_win = self.get_chance(40)
        
        preloading_text = f"{user.mention} đang chuẩn bị cướp tiền của {target_user.mention}!"
        if user_profile.is_authority == False:
            preloading_text += "\nCó thể gọi Chính Quyền vào cuộc để ngăn chặn cướp giật!"
        embed = discord.Embed(title=f"", description=f"{preloading_text}", color=0xc379e0)
        view = AuthorityInterceptView(user=user, user_profile=user_profile, crime_type="rob", target_profile=target_profile, target_user=target_user, authority_user=authority_user)
        await interaction.followup.send(f"Bạn đã cướp giật!", ephemeral=True)
        #Update last_crime
        ProfileMongoManager.update_last_crime(guild_id=interaction.guild_id, user_id=user.id)
        channel = interaction.channel
        if user_profile.is_authority == False:
            me = await channel.send(embed=embed, view=view, content=f"{target_user.mention}")
        else:
            me = await channel.send(embed=embed, view=None, content=f"{target_user.mention}")
        view.old_message = me
        #Đợi để xác định người thắng
        await asyncio.sleep(20)
        if view.interrupted == True: return
        
        #Kiểm tra, có item bảo hộ thì kết quả sẽ khác
        if target_profile.protection_item != None:
            if target_profile.protection_item.item_id == "armor_rob_1":
                embed = discord.Embed(title=f"", description=f"{user.mention} đang chuẩn bị cướp tiền của {target_user.mention}!", color=0xc379e0)
                embed.add_field(name=f"", value=f"{target_user.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên đã thoát thân kịp thời!", inline=False)
                #Gỡ phòng hộ bản thân
                ProfileMongoManager.remove_current_protection_item_profile(guild_id=interaction.guild_id, user_id=target_user.id)
                await me.edit(embed=embed, view=None, content=f"{target_user.mention}")
                return
            elif target_profile.protection_item.item_id == "armor_rob_2":
                #Random chọn giữa silver và copper
                silver_chance = self.get_chance(10)
                money = 0
                emoji = EmojiCreation2.COPPER.value
                if silver_chance and target_profile != None and target_profile.silver >= 5:
                    #Trừ 10% silver
                    money = int(user_profile.silver*0.1)
                    if money <= 0: money = 1000
                    if money > 10000: money = 10000
                    emoji = EmojiCreation2.SILVER.value
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, silver=-money)
                else:
                    #Trừ 30% copper
                    money = int(user_profile.copper*0.3)
                    if money <= 0: money = 10000
                    if money > 100000: money = 100000
                    emoji = EmojiCreation2.COPPER.value
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper=- money)
                embed = discord.Embed(title=f"", description=f"{user.mention} đang chuẩn bị cướp tiền của {target_user.mention}!", color=0xc379e0)
                embed.add_field(name=f"", value=f"{target_user.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**]!", inline=False)
                embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} {user.mention} đã mất **{money}** {emoji}!", inline=False)
                #Gỡ phòng hộ bản thân
                ProfileMongoManager.remove_current_protection_item_profile(guild_id=interaction.guild_id, user_id=target_user.id)
                await me.edit(embed=embed, view=None, content=f"{target_user.mention}")
                return
        
        result_text =f""
        if user_win:
            dignity_point = 10
            #Random chọn giữa silver và copper
            silver_chance = self.get_chance(10)
            money = 0
            emoji = EmojiCreation2.COPPER.value
            if silver_chance and target_profile != None and target_profile.silver >= 5:
                #Trừ 10% silver
                money = int(target_profile.silver*0.1)
                if money == 0: money = 1000
                if money > 50000: money = 50000
                emoji = EmojiCreation2.SILVER.value
            else:
                #Trừ 30% copper
                money = int(target_profile.copper*0.3)
                emoji = EmojiCreation2.COPPER.value
                if money == 0: money = 20000
                if money > 1500000: money = 1500000
            if user_profile.is_authority == True: money = money *2
            result_text = f"{user.mention} đã thành công cướp được **{money}** {emoji} của {target_user.mention}!\nVì hành vi trộm cắp nên {user.mention} đã mất **{dignity_point} nhân phẩm**!"
            #Trừ tiền target_profile, cộng cho user_profile
            if emoji == EmojiCreation2.SILVER.value:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, silver=money)
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=target_user.id, user_name=target_user.name, user_display_name=target_user.display_name, silver=-money)
            else:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper=money)
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=target_user.id, user_name=target_user.name, user_display_name=target_user.display_name, copper=-money)
            #Cộng kinh nghiệm cho người thắng
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=user.id, bonus_exp=10)
            #Trừ nhân phẩm vì cướp giật
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        else:
            dignity_point = 15
            result_text += f"{user.mention} đã không đủ trình để cướp tiền của {target_user.mention}!\nVì hành vi trộm cắp nên {user.mention} đã mất **{dignity_point} nhân phẩm**!"
            #Trừ nhân phẩm người đánh
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        new_embed = discord.Embed(title=f"", description=f"{result_text}", color=0xc379e0)
        try:
            await me.edit(embed=new_embed, view=None, content=f"{target_user.mention}")
        except Exception:
            return
    
    #region Fight
    async def process_fight_command(self, interaction: discord.Interaction, user: discord.Member, target_user: discord.Member, user_profile: Profile, target_profile: Profile):
        authority_user = ProfileMongoManager.get_authority(guild_id=user.guild.id)
        win_lines = [
                    "{user_name} đã chọc vào mắt {target_name} và đã thắng!",
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
        if user_profile.is_authority == False:
            if user_profile.level < target_profile.level:
                user_win_fight = self.get_chance(25)
            else:
                if target_profile.is_authority == True:
                    user_win_fight = self.get_chance(35)
                else: user_win_fight = self.get_chance(75)
        else:
            user_win_fight = self.get_chance(40)
        
        preloading_text = f"{user.mention} đã lao đến đánh lộn với {target_user.mention}!"
        if user_profile.is_authority == False:
            preloading_text += "\nCó thể gọi Chính Quyền vào cuộc để ngăn chặn ẩu đả này!"
        embed = discord.Embed(title=f"", description=f"{preloading_text}", color=0xc379e0)
        fight_gif = random.choice(fighting_gif_link)
        embed.set_image(url=fight_gif)
        view = AuthorityInterceptView(user=user, user_profile=user_profile, crime_type="fight", target_profile=target_profile, target_user=target_user, authority_user=authority_user)
        await interaction.followup.send(f"Bạn đã gây gỗ!", ephemeral=True)
        #Update last_crime
        ProfileMongoManager.update_last_crime(guild_id=interaction.guild_id, user_id=user.id)
        channel = interaction.channel
        if user_profile.is_authority == False:
            me = await channel.send(embed=embed, view=view, content=f"{target_user.mention}")
        else:
            me = await channel.send(embed=embed, view=None, content=f"{target_user.mention}")
        view.old_message = me
        #Đợi để xác định người thắng
        await asyncio.sleep(20)
        if view.interrupted == True: return
        
        #Kiểm tra, có item bảo hộ thì kết quả sẽ khác
        if target_profile.protection_item != None:
            if target_profile.protection_item.item_id == "hat_fight_1":
                embed = discord.Embed(title=f"", description=f"{user.mention} đã lao đến đánh lộn với {target_user.mention}!", color=0xc379e0)
                embed.add_field(name=f"", value=f"{target_user.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên đã thoát thân kịp thời!", inline=False)
                #Gỡ phòng hộ bản thân
                ProfileMongoManager.remove_current_protection_item_profile(guild_id=interaction.guild_id, user_id=target_user.id)
                await me.edit(embed=embed, view=None, content=f"{target_user.mention}")
                return
            elif target_profile.protection_item.item_id == "hat_fight_2":
                embed = discord.Embed(title=f"", description=f"{user.mention} đã lao đến đánh lộn với {target_user.mention}!", color=0xc379e0)
                embed.add_field(name=f"", value=f"{target_user.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**]!", inline=False)
                embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} {user.mention} đã bị đấm ngược lại, và mất **20** nhân phẩm!", inline=False)
                #Trừ nhân phẩm user 
                ProfileMongoManager.update_dignity_point(guild_id=interaction.guild.id, guild_name=interaction.guild.name, user_id= user.id, user_name=user.name, user_display_name=user.display_name, dignity_point=-20)
                #Gỡ phòng hộ bản thân
                ProfileMongoManager.remove_current_protection_item_profile(guild_id=interaction.guild_id, user_id=target_user.id)
                await me.edit(embed=embed, view=None, content=f"{target_user.mention}")
                return
        
        result_text =f""
        if user_win_fight:
            result_text = random.choice(win_lines)
            result_text = result_text.replace("{user_name}", user.mention)
            result_text = result_text.replace("{target_name}", target_user.mention)
            dignity_point = 15
            result_text += f"\n{user.mention} đã đánh thắng {target_user.mention} nên {target_user.mention} đã mất **{dignity_point} nhân phẩm**!"
            #Trừ nhân phẩm người thua
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target_user.id, user_name=target_user.name, user_display_name=target_user.display_name, dignity_point= -dignity_point)
            #Cộng kinh nghiệm cho người thắng
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=user.id, bonus_exp=10)
            
        else:
            result_text = random.choice(lose_lines)
            result_text = result_text.replace("{user_name}", user.mention)
            result_text = result_text.replace("{target_name}", target_user.mention)
            dignity_point = 10
            result_text += f"\n{user.mention} đã đánh thua {target_user.mention}, nên {user.display_name} đã bị trừ  **{dignity_point} nhân phẩm**!"
            #Trừ nhân phẩm người đánh
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        new_embed = discord.Embed(title=f"", description=f"{result_text}", color=0xc379e0)
        new_embed.set_image(url=fight_gif)
        try:
            await me.edit(embed=new_embed, view=None, content=f"{target_user.mention}")
        except Exception:
            return
    
    
    #region Laundry
    async def process_laundry_command(self, interaction: discord.Interaction, user: discord.Member, target_user: discord.Member, user_profile: Profile, target_profile: Profile):
        authority_user = ProfileMongoManager.get_authority(guild_id=user.guild.id)
        #Rửa tiền thì tuỳ vào xem có phải chính quyền không
        if user_profile.is_authority == False:
            user_win = self.get_chance(75)
        else:
            user_win = self.get_chance(40)
        
        preloading_text = f"{user.mention} đang chuẩn bị rửa tiền và trốn thuế!"
        if user_profile.is_authority == False:
            preloading_text += "\nCó thể gọi Chính Quyền vào cuộc để ngăn chặn hành vi rửa tiền trốn thuế!"
        embed = discord.Embed(title=f"", description=f"{preloading_text}", color=0xc379e0)
        view = AuthorityInterceptView(user=user, user_profile=user_profile, crime_type="laundry", target_profile=target_profile, target_user=target_user, authority_user=authority_user)
        await interaction.followup.send(f"Bạn đã rửa tiền và trốn thuế!", ephemeral=True)
        #Update last_crime
        ProfileMongoManager.update_last_crime(guild_id=interaction.guild_id, user_id=user.id)
        channel = interaction.channel
        if user_profile.is_authority == False:
            me = await channel.send(embed=embed, view=view, content=f"")
        else:
            me = await channel.send(embed=embed, view=None, content=f"")
        view.old_message = me
        #Đợi để xác định người thắng
        await asyncio.sleep(20)
        if view.interrupted == True: return
        result_text =f""
        if user_win:
            dignity_point = 15
            #Random chọn giữa silver và copper
            silver_chance = self.get_chance(10)
            money = 0
            emoji = EmojiCreation2.COPPER.value
            if silver_chance:
                #random 3 silver nhân với level của user
                money = 2 * user_profile.level
                if money > 100: money = 100 #Cap lại
                emoji = EmojiCreation2.SILVER.value
            else:
                #random 3000 copper nhân với level của user
                money = 3000 * user_profile.level
                if money > 85000: money = 85000 #Cap lại
                emoji = EmojiCreation2.COPPER.value
            if user_profile.is_authority == True: money = money *2
            result_text = f"{user.mention} đã làm thất thoát **{money}** {emoji} của Chính Quyền và bỏ vào túi cá nhân!\nVì hành vi rửa tiền trốn thuế nên {user.mention} đã mất **{dignity_point} nhân phẩm**!"
            #Trừ tiền chính quyền nếu có, cộng cho user_profile
            if emoji == EmojiCreation2.SILVER.value:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, silver=money)
                if authority_user != None:
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=authority_user.user_id, user_name=authority_user.user_name, user_display_name=authority_user.user_display_name, silver=-money)
            else:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper=money)
                if authority_user != None:
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=authority_user.user_id, user_name=authority_user.user_name, user_display_name=authority_user.user_display_name, copper=-money)
            #Cộng kinh nghiệm cho người thắng
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=user.id, bonus_exp=10)
            #Trừ nhân phẩm
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        else:
            dignity_point = 15
            result_text += f"{user.mention} đã không đủ trình để rửa tiền và trốn thuế!\nVì hành vi tội đồ nên {user.mention} đã mất **{dignity_point} nhân phẩm**!"
            #Trừ nhân phẩm
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        new_embed = discord.Embed(title=f"", description=f"{result_text}", color=0xc379e0)
        try:
            await me.edit(embed=new_embed, view=None, content=f"")
        except Exception:
            return
    
    #region smuggler
    async def process_smuggler_command(self, interaction: discord.Interaction, user: discord.Member, target_user: discord.Member, user_profile: Profile, target_profile: Profile):
        authority_user = ProfileMongoManager.get_authority(guild_id=user.guild.id)
        #Rửa tiền thì tuỳ vào xem có phải chính quyền không
        if user_profile.is_authority == False:
            user_win = self.get_chance(75)
        else:user_win = self.get_chance(50)
        
        preloading_text = f"{user.mention} đang chuẩn bị buôn lậu hàng cấm!"
        if user_profile.is_authority == False:
            preloading_text += "\nCó thể gọi Chính Quyền vào cuộc để ngăn chặn hành vi buôn lậu!"
        embed = discord.Embed(title=f"", description=f"{preloading_text}", color=0xc379e0)
        view = AuthorityInterceptView(user=user, user_profile=user_profile, crime_type="smuggler", target_profile=target_profile, target_user=target_user, authority_user=authority_user)
        await interaction.followup.send(f"Bạn đã buôn lậu!", ephemeral=True)
        #Update last_crime
        ProfileMongoManager.update_last_crime(guild_id=interaction.guild_id, user_id=user.id)
        channel = interaction.channel
        if user_profile.is_authority == False:
            me = await channel.send(embed=embed, view=view, content=f"")
        else:
            me = await channel.send(embed=embed, view=None, content=f"")
        view.old_message = me
        #Đợi để xác định người thắng
        await asyncio.sleep(20)
        if view.interrupted == True: return
        result_text =f""
        if user_win:
            dignity_point = 10
            money = 3000 * user_profile.level - int(2000*user_profile.dignity_point/100)
            if money > 150000: money = 150000 #Cap lại
            if user_profile.is_authority == True: money = money *2
            result_text = f"{user.mention} đã tuồn lậu hàng cấm về bán, và kiếm lời được **{money}** {EmojiCreation2.COPPER.value}!\nVì hành vi buôn lậu nên {user.mention} đã mất **{dignity_point} nhân phẩm**!"
            #Cộng cho user_profile
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper=money)
            #Cộng kinh nghiệm cho người thắng
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=user.id, bonus_exp=10)
            #Trừ nhân phẩm
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        else:
            dignity_point = 5
            result_text += f"{user.mention} đã không thể buôn lậu nên mất luôn tiền vốn **2000** {EmojiCreation2.COPPER.value}!\nVì hành vi tội đồ nên {user.mention} đã mất thêm **{dignity_point} nhân phẩm**!"
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper=-2000)
            #Trừ nhân phẩm
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point= -dignity_point)
        new_embed = discord.Embed(title=f"", description=f"{result_text}", color=0xc379e0)
        try:
            await me.edit(embed=new_embed, view=None, content=f"")
        except Exception:
            return
    
    
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
    
        