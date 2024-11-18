import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
import db.DbMongoManager as DbMongoManager
import CustomFunctions
import random
from Handling.MiniGame.TruthDare.TruthDareView import TruthDareView
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from Handling.Misc.SelfDestructView import SelfDestructView

async def setup(bot: commands.Bot):
    await bot.add_cog(TruthDare(bot=bot))
    print("Truth Dare game is ready!")

class TruthDare(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    #region Truth Dare
    @discord.app_commands.command(name="truth_dare", description="Tạo mới trò chơi Truth Or Dare.")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def truth_dare(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        channel = interaction.channel
        #Random true false, true là Truth, false là Dare
        ran = random.choice([True, False])
        user_count = DbMongoManager.find_user_count_by_id(guild_id=interaction.guild_id, user_id= interaction.user.id)
        content = ""
        question_type = "Sự Thật"
        if ran == True:
            #Truth
            index_excluded = user_count.truth_game_count if user_count and len(user_count.truth_game_count) > 0 else None
            index, content = CustomFunctions.get_random_truth_dare(True, index_excluded)
            question_type = "Sự Thật"
            DbMongoManager.update_or_insert_user_count(guild_id=interaction.guild_id, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name=interaction.user.display_name, truth_game_index=index)
        else:
            index_excluded = user_count.dare_game_count if user_count and len(user_count.dare_game_count) > 0 else None
            question_type = "Thách Thức"
            index, content = CustomFunctions.get_random_truth_dare(False, index_excluded)
            DbMongoManager.update_or_insert_user_count(guild_id=interaction.guild_id, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name=interaction.user.display_name, dare_game_index=index)
        # Create embed object
        embed = discord.Embed(title=f"", description=f"*Loại trò chơi: {question_type}*", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        embed.add_field(name=f"", value=content, inline=False)
        if interaction.user.avatar != None:
            embed.set_footer(text=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
        view = TruthDareView()
        await interaction.followup.send(f"Bạn đã chọn {question_type}.", ephemeral=True)
        message= await channel.send(embed=embed, view= view)
        view.message = message
        
        #Kiểm tra quest
        quest_progress = QuestMongoManager.increase_truth_dare_count(guild_id=interaction.guild_id, user_id=interaction.user.id, is_truth=ran)
        if quest_progress != None and quest_progress == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            m = await channel.send(embed=quest_embed, content=f"{interaction.user.mention}", view= view)
            view.message = m