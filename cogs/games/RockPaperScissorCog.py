import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from collections import deque
from datetime import datetime, timedelta
from Handling.MiniGame.RockPaperScissor import RpsClass, RpsMongoManager, RpsView
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from Handling.Misc.SelfDestructView import SelfDestructView
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
import CustomEnum.UserEnum as UserEnum
import CustomFunctions

async def setup(bot: commands.Bot):
    await bot.add_cog(RockPaperScissors(bot=bot))
    print("Rock Paper Scissor is ready!")

class RockPaperScissors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.games = {}

    #region keo_bua_bao command
    @discord.app_commands.command(name="keo_bua_bao", description="Bắt đầu chơi game Kéo - Búa - Bao")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    @discord.app_commands.describe(user="Chọn user để chơi cùng. Không chọn tức là sẽ chơi với bot")
    @discord.app_commands.describe(so_tien="Chọn số tiền muốn cá cược")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    async def create_rps(self, interaction: discord.Interaction, user: Optional[discord.Member] = None, so_tien: int = None, loai_tien: str = None):
        await interaction.response.defer(ephemeral= True)
        if user is None:
            user = self.bot.user
        if user.id == interaction.user.id:
            await interaction.followup.send("Bạn không thể chơi với chính bạn được!", ephemeral=True)
            return
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        if so_tien != None and loai_tien == None:
            loai_tien == "C"
        elif loai_tien!= None and so_tien == None:
            await interaction.followup.send("Nếu muốn cá cược thì phải nhập số tiền vào!", ephemeral=True)
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if so_tien != None and loai_tien != None and user_profile != None:
            if loai_tien == "C" and user_profile.copper < so_tien:
                    await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.COPPER.value} để cá cược!")
                    return
            elif loai_tien == "S" and user_profile.silver < so_tien:
                    await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.SILVER.value} để cá cược!")
                    return
            elif loai_tien == "G" and user_profile.gold < so_tien:
                    await interaction.followup.send(f"Bạn không có đủ {EmojiCreation2.GOLD.value} để cá cược!")
                    return
            if so_tien != None and so_tien <= 0:
                await interaction.followup.send(f"Số tiền nhập không hợp lệ!")
                return
            
        target_profile = None
        if user != None and user.bot == False and so_tien != None:
            target_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=user.id)
            if target_profile == None:
                await interaction.followup.send(f"Đổi thủ của bạn vẫn chưa dùng lệnh {SlashCommand.PROFILE.value}!")
                return
            if so_tien != None and loai_tien != None and target_profile != None:
                if loai_tien == "C" and target_profile.copper < so_tien:
                    await interaction.followup.send(f"Đổi thủ không có đủ {EmojiCreation2.COPPER.value} để cá cược!")
                    return
                elif loai_tien == "S" and target_profile.silver < so_tien:
                    await interaction.followup.send(f"Đổi thủ không có đủ {EmojiCreation2.SILVER.value} để cá cược!")
                    return
                elif loai_tien == "G" and target_profile.gold < so_tien:
                    await interaction.followup.send(f"Đổi thủ không có đủ {EmojiCreation2.GOLD.value} để cá cược!")
                    return
                if so_tien != None and so_tien <= 0:
                    await interaction.followup.send(f"Số tiền nhập không hợp lệ!")
                    return
                
        if target_profile == None:
            #Tìm chính quyền
            target_profile = ProfileMongoManager.get_authority(guild_id=interaction.guild_id)
            
        # Get the current epoch time (in seconds)
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=30)  # 30 seconds from now
        unix_time = int(end_time.timestamp())
        # Tạo embed thông báo
        text = f"{interaction.user.mention} đã mời {user.mention} chơi Kéo Búa Bao!"
        emoji = None
        if so_tien != None and loai_tien != None:
            if loai_tien == "C": emoji = EmojiCreation2.COPPER.value
            elif loai_tien == "S": emoji = EmojiCreation2.SILVER.value
            else: emoji = EmojiCreation2.GOLD.value
            text = f"{interaction.user.mention} đã mời {user.mention} chơi Kéo Búa Bao với số tiền cược là **{so_tien}**{emoji}!"
        embed = discord.Embed(title=f"", description= f"{text}", color=0xC3A757)  # Yellowish color
        embed.add_field(name="______________", value= f"Cả hai vui lòng chọn lượt chơi của mình. Thời gian còn lại: <t:{unix_time}:R>", inline=False)
        view = RpsView.RPSView(player_1= interaction.user, player_2=user, embed=embed)
        view.user_profile = user_profile
        view.target_profile = target_profile
        view.so_tien = so_tien
        view.loai_tien = loai_tien
        view.emoji = emoji
        
        await interaction.followup.send(content= f"Đã tạo trò chơi Kéo Búa Bao!", ephemeral= True)
        channel = interaction.channel
        message = await channel.send(embed=embed, view= view, content= f"{user.mention}")
        view.message_id = message.id
        view.channel_id = interaction.channel_id
        view.message = message
        
        check_quest_message = QuestMongoManager.increase_rps_count(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if check_quest_message == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            m = await channel.send(embed=quest_embed, content= f"{interaction.user.mention}", view = view)
            view.message = m
        
    
    #region bxh_rps command
    @discord.app_commands.command(name="bxh_rps", description="Xem xếp hạng Kéo - Búa - Bao")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    @discord.app_commands.describe(user="Chọn user để xem thứ hạng thực", loai_xep_hang= "Xem xếp hạng điểm Huyền Thoại hoặc điểm Sỉ Nhục")
    @discord.app_commands.choices(loai_xep_hang=[
        Choice(name="Xếp hạng theo điểm Huyền Thoại", value="legendary"),
        Choice(name="Xếp hạng theo điểm Sỉ Nhục", value="humiliate"),
        Choice(name="Xếp hạng theo điểm Thua", value="lose"),
        Choice(name="Xếp hạng theo điểm Hoà", value="draw"),
    ])
    async def bxh_rps(self, interaction: discord.Interaction, user: Optional[discord.Member] = None, loai_xep_hang: Optional[str] = None):
        await interaction.response.defer()
        #get list player profile của guild này ra
        list_player_profile = RpsMongoManager.find_all_player_profile(interaction.guild_id)
        if list_player_profile == None or len(list_player_profile) == 0:
            await interaction.followup.send(content=f"Chưa có ai chơi trong server này để có xếp hạng")
            return
        embed = self.get_bxh_embed(interaction=interaction, list_player_profile=list_player_profile, user_mention=user, loai_xep_hang=loai_xep_hang)
        await interaction.followup.send(embed= embed)
        return
    
    def get_bxh_embed(self, interaction: discord.Interaction, list_player_profile: list[RpsClass.RpsPlayerProfile], user_mention: Optional[discord.Member] = None, loai_xep_hang: Optional[str] = None):
        text = 'Thắng'
        if loai_xep_hang == 'legendary':
            list_player_profile.sort(key=lambda x: x.legendary_point, reverse=True)
            text = 'Huyền Thoại'
        elif loai_xep_hang == 'humiliate':
            list_player_profile.sort(key=lambda x: x.humiliated_point, reverse=True)
            text = 'Sỉ Nhục'
        elif loai_xep_hang == 'lose':
            list_player_profile.sort(key=lambda x: x.lose_point, reverse=True)
            text = 'Thua'
        elif loai_xep_hang == 'draw':
            list_player_profile.sort(key=lambda x: x.draw_point, reverse=True)
            text = 'Hoà'
        else:
            list_player_profile.sort(key=lambda x: x.win_point, reverse=True)
        
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm **{text}**.", description=f"", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 1
        if user_mention == None:
            for index, profile in enumerate(list_player_profile):
                #Skip qua hai con bot vì điểm rất ảo
                if profile.user_id == 1257713292445618239 or profile.user_id == 1257305865124581416: continue
                user = interaction.guild.get_member(profile.user_id)
                if user != None and (profile.win_point!= 0):
                    embed.add_field(name=f"", value=f"**Hạng {count}.** {user.mention}: Thắng: **{profile.win_point}**. Thua: **{profile.lose_point}**. Hoà: **{profile.draw_point}**. Huyền Thoại: **{profile.legendary_point}**. Sỉ Nhục: **{profile.humiliated_point}**.", inline=False)
                    count+=1
                if count >= 25: break
        else:
            matched = False
            for index, profile in enumerate(list_player_profile):
                if profile.user_id == user_mention.id:
                    user = interaction.guild.get_member(profile.user_id)
                    if user != None:
                        embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Thắng: **{profile.win_point}**. Thua: **{profile.lose_point}**. Hoà: **{profile.draw_point}**. Huyền Thoại: **{profile.legendary_point}**. Sỉ Nhục: **{profile.humiliated_point}**.", inline=False)
                    matched = True
                    break
            if matched == False:
                embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi này*", inline=False)        
        embed.add_field(name=f"", value="___________________", inline=False)
        return embed     

        