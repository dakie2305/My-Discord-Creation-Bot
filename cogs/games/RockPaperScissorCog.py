import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from collections import deque
from datetime import datetime, timedelta
from mini_game.RockPaperScissor import RpsClass, RpsMongoManager, RpsView

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
    async def create_rps(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        await interaction.response.defer()
        if user is None:
            user = self.bot.user
        
        if user.id == interaction.user.id:
            await interaction.followup.send("Bạn không thể chơi với chính bạn được!")
            return
        # Get the current epoch time (in seconds)
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=30)  # 30 seconds from now
        unix_time = int(end_time.timestamp())
        # Tạo embed thông báo
        embed = discord.Embed(title=f"", description= f"{interaction.user.mention} đã mời {user.mention} chơi Kéo Búa Bao!", color=0xC3A757)  # Yellowish color
        embed.add_field(name="______________", value= f"Cả hai vui lòng chọn lượt chơi của mình. Thời gian còn lại: <t:{unix_time}:R>", inline=False)
        view = RpsView.RPSView(player_1= interaction.user, player_2=user, embed=embed)
        message = await interaction.followup.send(embed=embed, view= view, content= f"{user.mention}")
        view.message_id = message.id
        view.channel_id = interaction.channel_id
        view.message = message
    
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

        