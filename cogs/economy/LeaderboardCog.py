from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import discord
from discord.ext import commands
from Handling.Economy.Global import GlobalMongoManager
from Handling.Misc import DonatorMongoManager
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
from discord.app_commands import Choice
from typing import Optional

async def setup(bot: commands.Bot):
    await bot.add_cog(LeaderboardEconomy(bot=bot))
    print("Leaderboard Economy is ready!")

class LeaderboardEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    @commands.command()
    async def leaderboard(self, ctx, user: Optional[discord.Member] = None):
        message: discord.Message = ctx.message
        if message:
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            view = SelfDestructView(120)
            embed = await self.embed_leaderboard_command(type="all", called_user=message.author, user=user)
            n = await message.reply(embed=embed, view=view)
            view.message = n
    
    #region leader slash
    @discord.app_commands.choices(type=[
        Choice(name="Tổng toàn bộ tài sản", value="all"),
        Choice(name="Xếp hạng theo tổng số Gold", value="gold_only"),
        Choice(name="Xếp hạng theo rank", value="rank"),
        Choice(name="Xếp hạng Quest hoàn thành", value="quest"),
        Choice(name="Xếp hạng cấp bậc Hộ Vệ Thần", value="guardian"),
        Choice(name="Xếp hạng lực chiến Hộ Vệ Thần", value="guardian_power"),
        Choice(name="Xếp hạng Hộ Vệ Thần Liên Server", value="guardian_power_global"),
        Choice(name="Xếp hạng Mạnh Thường Quân Donator", value="donator"),
    ])
    @discord.app_commands.checks.cooldown(1, 10)
    @discord.app_commands.command(name="leaderboard", description="Bảng xếp hạng người dùng theo nhiều tiêu chí!")
    async def leaderboard_slash_command(self, interaction: discord.Interaction, type: str = None, user: discord.Member = None):
        await interaction.response.defer(ephemeral=False)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        if type == None: type = "all"
        view = SelfDestructView(120)
        embed = await self.embed_leaderboard_command(type=type, called_user=interaction.user, user=user)
        m = await interaction.followup.send(embed=embed, view=view)
        view.message = m
    
    @leaderboard_slash_command.error
    async def leaderboard_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    
    async def embed_leaderboard_command(self, type: str, called_user: discord.Member, user: discord.Member = None):
        if type == "guardian_power_global" or type == "donator":
            return await self.embed_leaderboard_special(type=type, user=user)
        if user != None:
            user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
            if user_profile  == None:
                embed = discord.Embed(title=f"", description=f"User {user.display_name} phải dùng lệnh {SlashCommand.PROFILE.value} trước thì mới có dữ liệu để tạo bảng xếp hạng!", color=0x03F8FC)
                return embed
        
        list_profile_guild = ProfileMongoManager.find_all_profiles(guild_id=called_user.guild.id)
        if list_profile_guild == None or len(list_profile_guild) == 0:
            embed = discord.Embed(title=f"", description=f"Cần phải có người dùng lệnh {SlashCommand.PROFILE.value} trước thì mới có dữ liệu để tạo bảng xếp hạng!", color=0x03F8FC)
            return embed
        embed = discord.Embed(color=0x0ce7f2)
        embed.add_field(name="", value="▬▬▬▬ι══════════>", inline=False)
        title = "Bảng Xếp Hạng"
        #region leaderboard all
        if type == "all":
            #Lọc theo tổng tài sản
            title = "Bảng Xếp Hạng Tổng Tài Sản"
            list_profile_guild.sort(key=lambda x: (x.copper + x.silver * 5000 + x.gold * 5000 * 5000 + x.darkium * 5000 * 5000 * 10000), reverse=True)
            embed.description = title
            if user == None:
                count = 1
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    text_money = ""
                    if profile.darkium >0:
                        text_money += f"**{self.shortened_currency(profile.darkium)}** {EmojiCreation2.DARKIUM.value}  "
                    if profile.gold >0:
                        text_money += f"**{self.shortened_currency(profile.gold)}** {EmojiCreation2.GOLD.value}  "
                    if profile.silver > 0:
                        text_money += f"**{self.shortened_currency(profile.silver)}** {EmojiCreation2.SILVER.value}  "
                    if profile.copper > 0:
                        text_money += f"**{self.shortened_currency(profile.copper)}** {EmojiCreation2.COPPER.value}  "
                    if (index+1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: <@{profile.user_id}>", inline=False)
                        embed.add_field(name=f"", value=f"{text_money}", inline=False)
                    elif (index+1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: <@{profile.user_id}>", inline=False)
                        embed.add_field(name=f"", value=f"{text_money}", inline=False)
                    elif (index+1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: <@{profile.user_id}>", inline=False)
                        embed.add_field(name=f"", value=f"{text_money}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}**: <@{profile.user_id}>", inline=False)
                        embed.add_field(name=f"", value=f"{text_money}", inline=False)
                    count+=1
                    if count > 10: break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.user_id == user.id:
                        text_money = ""
                        if profile.darkium >0:
                            text_money += f"**{self.shortened_currency(profile.darkium)}** {EmojiCreation2.DARKIUM.value}  "
                        if profile.gold >0:
                            text_money += f"**{self.shortened_currency(profile.gold)}** {EmojiCreation2.GOLD.value}  "
                        if profile.silver > 0:
                            text_money += f"**{self.shortened_currency(profile.silver)}** {EmojiCreation2.SILVER.value}  "
                        if profile.copper > 0:
                            text_money += f"**{self.shortened_currency(profile.copper)}** {EmojiCreation2.COPPER.value}  "
                        if (index+1) == 1:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: <@{profile.user_id}>", inline=False)
                            embed.add_field(name=f"", value=f"{text_money}", inline=False)
                        elif (index+1) == 2:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: <@{profile.user_id}>", inline=False)
                            embed.add_field(name=f"", value=f"{text_money}", inline=False)
                        elif (index+1) == 3:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: <@{profile.user_id}>", inline=False)
                            embed.add_field(name=f"", value=f"{text_money}", inline=False)
                        else:
                            embed.add_field(name=f"", value=f"**Hạng {index+1}**: <@{profile.user_id}>", inline=False)
                            embed.add_field(name=f"", value=f"{text_money}", inline=False)
                        break
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            return embed
        #region leaderboard each
        elif type == "gold_only" or type == "silver_only" or type == "copper_only":
            emoji = EmojiCreation2.GOLD.value
            if type == "silver_only": 
                emoji = EmojiCreation2.SILVER.value
                list_profile_guild.sort(key=lambda x: x.silver, reverse=True)
            if type == "copper_only": 
                emoji = EmojiCreation2.COPPER.value
                list_profile_guild.sort(key=lambda x: x.copper, reverse=True)
            if type == "gold_only": 
                emoji = EmojiCreation2.GOLD.value
                list_profile_guild.sort(key=lambda x: x.gold, reverse=True)
            
            title = f"Bảng Xếp Hạng Tổng {emoji}"
            embed.description = title
            if user == None:
                count = 1
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if type == "gold_only" and profile.gold <= 0: continue
                    if type == "silver_only" and profile.silver <= 0: continue
                    if type == "copper_only" and profile.copper <= 0: continue
                    
                    short_text = self.shortened_currency(profile.gold)
                    if type == "silver_only": short_text = self.shortened_currency(profile.silver)
                    if type == "copper_only": short_text = self.shortened_currency(profile.copper)
                    
                    if (index+1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: <@{profile.user_id}> với tận **{short_text}** {emoji}", inline=False)
                    elif (index+1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: <@{profile.user_id}> với khoảng **{short_text}** {emoji}", inline=False)
                    elif (index+1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: <@{profile.user_id}> với tầm **{short_text}** {emoji}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}**: <@{profile.user_id}> với **{short_text}** {emoji}", inline=False)
                    count+=1
                    if count >= 20: break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.user_id == user.id:
                        short_text = self.shortened_currency(profile.gold)
                        if type == "silver_only": short_text = self.shortened_currency(profile.silver)
                        if type == "copper_only": short_text = self.shortened_currency(profile.copper)
                        
                        if (index+1) == 1:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}.**: <@{profile.user_id}> với tận **{short_text}** {emoji}", inline=False)
                        elif (index+1) == 2:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}.**: <@{profile.user_id}> với khoảng **{short_text}** {emoji}", inline=False)
                        elif (index+1) == 3:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}.**: <@{profile.user_id}> với tầm **{short_text}** {emoji}", inline=False)
                        else:
                            embed.add_field(name=f"", value=f"**Hạng {index+1}.**: <@{profile.user_id}> với **{short_text}** {emoji}", inline=False)
                        break
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            return embed
        #region leaderboard rank
        elif type == "rank":
            #Lọc theo rank
            title = "Bảng Xếp Hạng Rank"
            embed.description = title
            list_profile_guild.sort(key=lambda x: x.level, reverse=True)
            if user == None:
                count = 1
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if (index+1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                    elif (index+1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                    elif (index+1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                    count+=1
                    if count >= 20: break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.user_id == user.id:
                        if (index+1) == 1:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                        elif (index+1) == 2:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                        elif (index+1) == 3:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                        else:
                            embed.add_field(name=f"", value=f"**Hạng {index+1}**: <@{profile.user_id}> Rank **{profile.level}**", inline=False)
                        break
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            return embed
        #region leaderboard quest
        elif type == "quest":
            #Lọc theo rank
            title = "Bảng Xếp Hạng Nhiệm Vụ Hoàn Thành"
            list_profile_guild.sort(key=lambda x: x.quest_finished, reverse=True)
            embed.description = title
            if user == None:
                count = 1
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.quest_finished <= 0: continue
                    text = f"hoàn thành **{profile.quest_finished}** nhiệm vụ"
                    if (index+1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: <@{profile.user_id}> {text}", inline=False)
                    elif (index+1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: <@{profile.user_id}> {text}", inline=False)
                    elif (index+1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: <@{profile.user_id}> {text}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}**: <@{profile.user_id}> {text}", inline=False)
                    count+=1
                    if count >= 20: break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    text = f"hoàn thành **{profile.quest_finished}** nhiệm vụ"
                    if profile.user_id == user.id:
                        if (index+1) == 1:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: <@{profile.user_id}> {text}", inline=False)
                        elif (index+1) == 2:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: <@{profile.user_id}> {text}", inline=False)
                        elif (index+1) == 3:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: <@{profile.user_id}> {text}", inline=False)
                        else:
                            embed.add_field(name=f"", value=f"**Hạng {index+1}**: <@{profile.user_id}> {text}", inline=False)
                        break
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            return embed
        #region leaderboard guardian
        elif type == "guardian":
            #Lọc theo rank
            title = "Bảng Xếp Hạng Cấp Bậc Vệ Thần"
            list_profile_guild = sorted(
                [profile for profile in list_profile_guild if profile.guardian], 
                key=lambda profile: profile.guardian.level, reverse=True
            )
            # list_profile_guild.sort(key=lambda x: x.guardian.level, reverse=True)
            embed.description = title
            if user == None:
                count = 1
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.guardian == None: continue
                    if (index+1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                    elif (index+1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                    elif (index+1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                    count+=1
                    if count >= 20: break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.guardian == None: continue
                    if profile.user_id == user.id:
                        if (index+1) == 1:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                        elif (index+1) == 2:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                        elif (index+1) == 3:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                        else:
                            embed.add_field(name=f"", value=f"**Hạng {index+1}**: {profile.guardian.ga_emoji} - {profile.guardian.ga_name}, cấp **{profile.guardian.level}** (<@{profile.user_id}>)", inline=False)
                        break
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            return embed
        
        #region leaderboard guardian_power
        elif type == "guardian_power":
            #Lọc theo rank
            title = "Bảng Xếp Hạng Lực Chiến Vệ Thần"
            list_profile_guild = sorted(
                [profile for profile in list_profile_guild if profile.guardian],
                key=lambda p: (p.guardian.max_stamina + p.guardian.max_health + p.guardian.max_mana + p.guardian.attack_power + p.guardian.stats_point * 5 + p.guardian.max_skills
                ),
                reverse=True
            )
            embed.description = title
            if user == None:
                count = 1
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.guardian == None: continue
                    total_stats = profile.guardian.max_stamina + profile.guardian.max_health + profile.guardian.max_mana + profile.guardian.attack_power + profile.guardian.stats_point * 5 + profile.guardian.max_skills
                    text = f"{profile.guardian.ga_emoji} - {profile.guardian.ga_name} (<@{profile.user_id}>) với lực chiến **{total_stats}**"
                    if (index+1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {text}", inline=False)
                    elif (index+1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {text}", inline=False)
                    elif (index+1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {text}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}**: {text}", inline=False)
                    count+=1
                    if count >= 20: break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                for index, profile in enumerate(list_profile_guild):
                    if profile == None or profile.user_id == None: continue
                    if profile.guardian == None: continue
                    if profile.user_id == user.id:
                        total_stats = profile.guardian.max_stamina + profile.guardian.max_health + profile.guardian.max_mana + profile.guardian.attack_power + profile.guardian.stats_point * 5 + profile.guardian.max_skills
                        text = f"{profile.guardian.ga_emoji} - {profile.guardian.ga_name} (<@{profile.user_id}>) với lực chiến **{total_stats}**"
                        if (index+1) == 1:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {text}", inline=False)
                        elif (index+1) == 2:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {text}", inline=False)
                        elif (index+1) == 3:
                            embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {text}", inline=False)
                        else:
                            embed.add_field(name=f"", value=f"**Hạng {index+1}**: {text}", inline=False)
                        break
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            return embed
        else:
            embed = discord.Embed(title=f"", description=f"Loại bảng xếp hạng này vẫn chưa được code xong!", color=0x03F8FC)
            return embed
        
    async def embed_leaderboard_special(self, type: str, user: discord.Member = None):
        embed = discord.Embed(color=0x0ce7f2)
        embed.add_field(name="", value="▬▬▬▬ι══════════>", inline=False)
        #region Leaderboard global guardian
        if type == "guardian_power_global":
            #Lọc theo rank
            title = "Bảng Xếp Hạng Hộ Vệ Thần Liên Server"
            embed.description = title
            if user == None:
                list_profile = GlobalMongoManager.get_top_guardian_profiles()
                count = 1
                for index, profile in enumerate(list_profile):
                    if profile == None or profile.user_id == None: continue
                    if profile.guardian == None: continue
                    total_stats = profile.guardian.max_stamina + profile.guardian.max_health + profile.guardian.max_mana + profile.guardian.attack_power + profile.guardian.stats_point * 5 + profile.guardian.max_skills
                    text = f"{profile.guardian.ga_emoji} - {profile.guardian.ga_name} cấp {profile.guardian.level} (**{profile.user_name} - {profile.user_display_name}**) với lực chiến **{total_stats}**"
                    if (index+1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {text}", inline=False)
                    elif (index+1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {text}", inline=False)
                    elif (index+1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {text}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}**: {text}", inline=False)
                    count+=1
                    if count >= 20: break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                global_profile = GlobalMongoManager.get_guardian_rank_and_profile(user_id=user.id)
                if not global_profile: 
                    embed.add_field(name=f"", value=f"Không tìm thấy dữ liệu Hộ Vệ Thần Liên Thông Server của {user.mention}", inline=False)
                else:
                    rank, profile = global_profile
                    total_stats = profile.guardian.max_stamina + profile.guardian.max_health + profile.guardian.max_mana + profile.guardian.attack_power + profile.guardian.stats_point * 5 + profile.guardian.max_skills
                    text = f"{profile.guardian.ga_emoji} - {profile.guardian.ga_name} cấp {profile.guardian.level} (**{profile.user_name} - {profile.user_display_name}**) với lực chiến **{total_stats}**"
                    if rank == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {text}", inline=False)
                    elif rank == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {text}", inline=False)
                    elif rank == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {text}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {rank}**: {text}", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        elif type == "donator":
            title = "Bảng Xếp Hạng Mạnh Thường Quân Donator"
            embed.description = title
            if user is None:
                list_donators = DonatorMongoManager.get_top_donators()
                count = 1
                for index, profile in enumerate(list_donators):
                    if profile is None or profile.user_id is None:
                        continue
                    text = f"**{profile.user_name} - {profile.user_display_name}** đã ủng hộ tổng cộng **{profile.total_time_donate}** lần, tổng lên đến **{self.format_dot_separator(profile.total_amount_donate)} VND**"
                    if (index + 1) == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {text}", inline=False)
                    elif (index + 1) == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {text}", inline=False)
                    elif (index + 1) == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {text}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {index + 1}**: {text}", inline=False)
                    count += 1
                    if count >= 20:
                        break
            else:
                embed.add_field(name=f"", value=f"Xếp hạng của {user.mention}", inline=True)
                embed.add_field(name=f"", value=f"_____________", inline=False)
                result = DonatorMongoManager.get_donator_rank_and_profile(user_id=user.id)
                if not result:
                    embed.add_field(name=f"", value=f"Không tìm thấy dữ liệu donate của {user.mention}", inline=False)
                else:
                    rank, profile = result
                    text = f"**{profile.user_name} - {profile.user_display_name}** đã ủng hộ tổng cộng **{profile.total_time_donate}** lần, tổng lên đến **{self.format_dot_separator(profile.total_amount_donate)} VND**"
                    if rank == 1:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.FIRST_CUP.value}**: {text}", inline=False)
                    elif rank == 2:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.SECOND_CUP.value}**: {text}", inline=False)
                    elif rank == 3:
                        embed.add_field(name=f"", value=f"**Hạng {EmojiCreation2.THIRD_CUP.value}**: {text}", inline=False)
                    else:
                        embed.add_field(name=f"", value=f"**Hạng {rank}**: {text}", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        return embed
        
    def shortened_currency(self, number: int):
        if number >= 1000000000:
            suffix = int(number % 1000000000 // 1000000)
            if suffix == 0: suffix = "" 
            return f"{int(number // 1000000000)}B{suffix}"
        elif number >= 1000000:
            suffix = int(number % 1000000 // 1000)
            if suffix == 0: suffix = "" 
            return f"{int(number // 1000000)}M{suffix}"
        elif number >= 10000:
            suffix = int(number % 1000 // 100)
            if suffix == 0: suffix = ""
            return f"{int(number // 1000)}K{suffix}"  
        else:
            return str(int(number))

    def format_dot_separator(self, number: int) -> str:
        return f"{number:,}".replace(",", ".")