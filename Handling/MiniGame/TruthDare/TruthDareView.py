from Handling.MiniGame.SortWord import SwMongoManager as SwMongoManager
import CustomFunctions
import db.DbMongoManager as DbMongoManager
import discord
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 

class TruthDareView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.message: discord.Message = None
        
    async def on_timeout(self):
        #Ẩn nút
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        await self.message.edit(view=self)
        
    @discord.ui.button(label="Sự thật", style=discord.ButtonStyle.primary, custom_id="truth_button")
    async def buttonTruth_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        user_count = DbMongoManager.find_user_count_by_id(guild_id=interaction.guild_id, user_id= interaction.user.id)
        index_excluded = user_count.truth_game_count if user_count and len(user_count.truth_game_count) > 0 else None
        index, content = CustomFunctions.get_random_truth_dare(True, index_excluded)
        channel = interaction.channel
        # Create embed object
        embed = discord.Embed(title=f"", description=f"*Loại trò chơi: Sự Thật*", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        embed.add_field(name=f"", value=content, inline=False)
        embed.set_footer(text=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
        view = TruthDareView()
        await interaction.followup.send(f"Bạn đã chọn Sự Thật.", ephemeral=True)
        message = await channel.send(embed=embed, view= view)
        view.message = message
        DbMongoManager.update_or_insert_user_count(guild_id=interaction.guild_id, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name=interaction.user.display_name, truth_game_index=index)
        
        #Kiểm tra quest
        quest_progress = QuestMongoManager.increase_truth_dare_count(guild_id=interaction.guild_id, user_id=interaction.user.id, is_truth=True)
        if quest_progress != None and quest_progress == True:
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            await channel.send(embed=quest_embed, content=f"{interaction.user.mention}")
        
    @discord.ui.button(label="Thách thức", style=discord.ButtonStyle.secondary, custom_id="dare_button")
    async def buttonDare_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        user_count = DbMongoManager.find_user_count_by_id(guild_id=interaction.guild_id, user_id= interaction.user.id)
        index_excluded = user_count.dare_game_count if user_count and len(user_count.dare_game_count) > 0 else None
        index, content = CustomFunctions.get_random_truth_dare(False, index_excluded)
        channel = interaction.channel
        # Create embed object
        embed = discord.Embed(title=f"", description=f"*Loại trò chơi: Thử Thách*", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        embed.add_field(name=f"", value=content, inline=False)
        embed.set_footer(text=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
        view = TruthDareView()
        await interaction.followup.send(f"Bạn đã chọn Thách Thức.", ephemeral=True)
        message= await channel.send(embed=embed, view= view)
        view.message = message
        DbMongoManager.update_or_insert_user_count(guild_id=interaction.guild_id, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name=interaction.user.display_name, dare_game_index=index)
        
        #Kiểm tra quest
        quest_progress = QuestMongoManager.increase_truth_dare_count(guild_id=interaction.guild_id, user_id=interaction.user.id, is_truth=False)
        if quest_progress != None and quest_progress == True:
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để nhận thưởng mới nha!", color=0xc379e0)
            await channel.send(embed=quest_embed, content=f"{interaction.user.mention}")