import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from Handling.Economy.GA.GuardianAngelAttackClass import GuardianAngelAttackClass
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import random
import asyncio
from datetime import datetime, timedelta
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Economy.GA.GaBattleView import GaBattleView

class GaChallengeView(discord.ui.View):
    def __init__(self, guild_id: int, user: discord.Member, target: discord.Member, user_profile: Profile, target_profile: Profile, so_tien:int = None, battle_type:str = "A", loai_tien:str = None, title = "", footer = "", max_players:int = 3, channel_name = "Không rõ", timeout = 200):
        super().__init__(timeout=timeout)
        self.message : discord.Message = None
        self.battle_button = discord.ui.Button(label="⚔️ Chấp Nhận Thách Đấu", style=discord.ButtonStyle.primary)
        self.battle_button.callback = self.battle_button_event
        self.add_item(self.battle_button)
        self.guild_id = guild_id
        self.user = user
        self.target = target
        self.user_profile = user_profile
        self.target_profile = target_profile
        self.so_tien = so_tien
        self.loai_tien = loai_tien
        self.max_players = max_players
        self.is_accepted = False
        self.title = title
        self.footer = footer
        self.battle_type = battle_type
        self.channel_name = channel_name

    async def on_timeout(self):
        #Delete
        if self.message != None and self.is_accepted == False: 
            await self.message.edit(content="Rất tiếc, đối thủ đã không chấp nhận thách đấu!", view=None)
            return

    async def battle_button_event(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != self.target.id:
            await interaction.followup.send("Bạn không phải là người được thách đấu!", ephemeral=True)
            return
        self.is_accepted = True
        await interaction.followup.send(f"Bạn đã chấp nhận thách đấu với {self.user.mention}!", ephemeral=True)
        view = GaBattleView(user_profile=self.user_profile, user=self.user, is_players_versus_players=True, enemy_ga=self.target_profile.guardian, guild_id=self.guild_id, target=self.target, target_profile=self.target_profile, max_players=self.max_players, embed_title=self.title, gold_reward=0, silver_reward=0, dignity_point=0, bonus_all_reward_percent=0, footer_text=self.footer, channel_name=self.channel_name)
        view.is_challenge = True
        view.so_tien = self.so_tien
        view.loai_tien = self.loai_tien
        view.battle_type = self.battle_type
        mess = await self.message.edit(view=view)
        view.message = mess
        print(f"Username {interaction.user.name} has started guardian challenge in guild {interaction.guild.name} at channel {interaction.channel.name}!")
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=self.user.id, data_type="last_joined_battle", date_value=datetime.now())
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=self.target.id, data_type="last_joined_battle", date_value=datetime.now())
        ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=self.user.id, count_type="count_battle_pvp")
        ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=self.target.id, count_type="count_battle_pvp")
        await view.commence_battle()
        return