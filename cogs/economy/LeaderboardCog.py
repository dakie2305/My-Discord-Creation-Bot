from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from CustomEnum.RoleEnum import TrueHeavenRoleId
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
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
        Choice(name="Xếp hạng theo tổng số Silver", value="silver_only"),
        Choice(name="Xếp hạng theo tổng số Copper", value="copper_only"),
        Choice(name="Xếp hạng theo rank", value="rank"),
        Choice(name="Xếp hạng Quest hoàn thành", value="quest"),
    ])
    @discord.app_commands.checks.cooldown(1, 10)
    @discord.app_commands.command(name="leaderboard", description="Bảng xếp hạng tài chính trong server!")
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
        if user != None:
            user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
            if user_profile  == None:
                embed = discord.Embed(title=f"", description=f"User {user.display_name} phải dùng lệnh {SlashCommand.PROFILE.value} trước thì mới có dữ liệu để tạo bảng xếp hạng!", color=0x03F8FC)
                return embed
        
        list_profile_guild = ProfileMongoManager.find_all_profiles(guild_id=called_user.guild.id)
        if list_profile_guild == None or len(list_profile_guild) == 0:
            embed = discord.Embed(title=f"", description=f"Cần phải có người dùng lệnh {SlashCommand.PROFILE.value} trước thì mới có dữ liệu để tạo bảng xếp hạng!", color=0x03F8FC)
            return embed
        
        
        title = "Bảng Xếp Hạng"
        #region leaderboard all
        if type == "all":
            #Lọc theo tổng tài sản
            title = "Bảng Xếp Hạng Tổng Tài Sản"
            list_profile_guild.sort(key=lambda x: (x.copper + x.silver * 5000 + x.gold * 5000 * 5000 + x.darkium * 5000 * 5000 * 10000), reverse=True)
            
            embed = discord.Embed(title=f"", description=f"{title}", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
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
                    if count >= 10: break
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
            embed = discord.Embed(title=f"", description=f"{title}", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
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
            list_profile_guild.sort(key=lambda x: x.level, reverse=True)
            embed = discord.Embed(title=f"", description=f"{title}", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
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
            embed = discord.Embed(title=f"", description=f"{title}", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
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
        else:
            embed = discord.Embed(title=f"", description=f"Loại bảng xếp hạng này vẫn chưa được code xong!", color=0x03F8FC)
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
