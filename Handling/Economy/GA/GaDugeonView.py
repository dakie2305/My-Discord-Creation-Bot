
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
import CustomFunctions
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_small_copper_fish,list_gold_fish, list_silver_fish, list_gift_items, list_trash, list_plant, list_legend_weapon_1, list_legend_weapon_2, list_support_ga_items, list_protection_items,list_attack_items,list_support_items
from Handling.Economy.GA.GaBattleView import GaBattleView

class GaDugeonView(discord.ui.View):
    def __init__(self, guild_id: int, enemy_ga: GuardianAngel, enemy_ga_2: GuardianAngel = None, title: str = "", bonus_percent: int = None, difficulty: int = 1):
        super().__init__(timeout=300)
        self.message : discord.Message = None
        
        self.is_attacked = False
        self.title = title
        self.guild_id = guild_id
        self.enemy_ga = enemy_ga
        self.enemy_ga_2 = enemy_ga_2
        self.bonus_percent = bonus_percent
        self.difficulty = difficulty
        self.battle_button = discord.ui.Button(label="⚔️ Chiến Đấu", style=discord.ButtonStyle.primary)
        self.battle_button.callback = self.battle_button_event
        self.add_item(self.battle_button)

    async def on_timeout(self):
        #Delete
        if self.message != None and self.is_attacked == False: 
            await self.message.delete()
            return

    async def battle_button_event(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.is_attacked:
            await interaction.followup.send(f'Đã có người đánh, vui lòng gia nhập họ', ephemeral=True)
            return
        
        #Lấy dữ liệu profile của người dùng và add vào attack_class
        new_player_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if new_player_profile == None:
            await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        elif new_player_profile.guardian == None or new_player_profile.guardian.is_dead:
            await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True)
            return
        
        if new_player_profile.guardian.last_joined_battle != None:
            time_window = timedelta(minutes=1)
            check = UtilitiesFunctions.check_if_within_time_delta(input=new_player_profile.guardian.last_joined_battle, time_window=time_window)
            if check:
                next_time = new_player_profile.guardian.last_joined_battle + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 {interaction.user.mention} Bạn vừa tham chiến xong. Vui lòng đợi một phút rồi thực hiện lại lệnh!", color=0xc379e0)
                view = SelfDestructView(timeout=60)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
        
        if new_player_profile.guardian.time_to_recover!= None:
            if new_player_profile.guardian.time_to_recover > datetime.now():
                next_time = new_player_profile.guardian.time_to_recover
                unix_time = int(next_time.timestamp())
                await interaction.followup.send(content=f"Hộ Vệ Thần của bạn đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True)
                return
            else:
                #Hồi phục 50% máu, 50% thể lực
                health = int(new_player_profile.guardian.max_health*50/100)
                stamina = int(new_player_profile.guardian.max_stamina*50/100)
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
                new_player_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        
        await interaction.followup.send(content=f"Bạn đã tham chiến!", ephemeral=True)
        self.is_attacked = True
        
        
        if self.difficulty >= 3:
            #Nếu self.difficulty trên 3 thì roll lại kẻ địch theo stats của player ga nếu player ga trên cấp 80 hoặc enemy thấp cấp hơn
            #Thì scale theo level của player
            if new_player_profile.guardian.level >= 80 or self.enemy_ga.level < new_player_profile.guardian.level:
                text_name = self.enemy_ga.ga_name
                text_emoji = self.enemy_ga.ga_emoji
                self.enemy_ga = ListGAAndSkills.get_random_ga_enemy_generic(level=new_player_profile.guardian.level+10)
                self.enemy_ga.ga_name = text_name
                self.enemy_ga.ga_emoji = text_emoji
                
                if self.enemy_ga_2 != None:
                    text_name = self.enemy_ga_2.ga_name
                    text_emoji = self.enemy_ga_2.ga_emoji
                    self.enemy_ga_2 = ListGAAndSkills.get_random_ga_enemy_generic(level=new_player_profile.guardian.level+10)
                    self.enemy_ga_2.ga_name = text_name
                    self.enemy_ga_2.ga_emoji = text_emoji
        
        gold_reward = 50
        silver_reward = 100
        exp_reward = 80
        dignity_point_reward = 10
        
        #Tính lại theo enemy_ga
        gold_reward = int(gold_reward + gold_reward*self.enemy_ga.level*0.2)
        silver_reward = int(silver_reward + silver_reward*self.enemy_ga.level*0.3)
        exp_reward = int(exp_reward + exp_reward*self.enemy_ga.level*0.1)
        
        embed = discord.Embed(title=f"", description=self.title, color=0x0ce7f2)
        
        embed.add_field(name=f"", value=f"Hộ Vệ Thần {new_player_profile.guardian.ga_emoji} - **{new_player_profile.guardian.ga_name}** (Cấp {new_player_profile.guardian.level}) của {interaction.user.mention}", inline=False)
        embed.add_field(name=f"", value=f"🦾: **{new_player_profile.guardian.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=new_player_profile.guardian.health, max_value=new_player_profile.guardian.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=new_player_profile.guardian.stamina, max_value=new_player_profile.guardian.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=new_player_profile.guardian.mana, max_value=new_player_profile.guardian.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        
        text = f"Kẻ thù {self.enemy_ga.ga_emoji} - **{self.enemy_ga.ga_name}** (Cấp {self.enemy_ga.level})"
        embed.add_field(name=f"", value=text, inline=False)
        embed.add_field(name=f"", value="", inline=False)
        embed.add_field(name=f"", value=f"🦾: **{self.enemy_ga.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=self.enemy_ga.health, max_value=self.enemy_ga.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self.enemy_ga.stamina, max_value=self.enemy_ga.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self.enemy_ga.mana, max_value=self.enemy_ga.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        if self.enemy_ga_2 != None:
            text = f"Kẻ thù {self.enemy_ga_2.ga_emoji} - **{self.enemy_ga_2.ga_name}** (Cấp {self.enemy_ga_2.level})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value="", inline=False)
            embed.add_field(name=f"", value=f"🦾: **{self.enemy_ga_2.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=self.enemy_ga_2.health, max_value=self.enemy_ga_2.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self.enemy_ga_2.stamina, max_value=self.enemy_ga_2.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self.enemy_ga_2.mana, max_value=self.enemy_ga_2.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        
        view = GaBattleView(user=interaction.user, user_profile=new_player_profile, is_players_versus_players=False, max_players=3, enemy_ga=self.enemy_ga, enemy_ga_2=self.enemy_ga_2, guild_id=interaction.guild_id, gold_reward=gold_reward, silver_reward=silver_reward, bonus_exp=exp_reward, dignity_point=dignity_point_reward, embed_title=self.title, bonus_all_reward_percent=self.bonus_percent)
        mess = await self.message.edit(embed=embed, view=view)
        view.message = mess
        print(f"Username {interaction.user.name} has started guardian battle in guild {interaction.guild.name} at channel {interaction.channel.name}!")
        await view.commence_battle()