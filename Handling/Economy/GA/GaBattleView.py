import discord
from CustomEnum.GuardianMemoryTag import GuardianMemoryTag
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
import copy


class GaBattleView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member,enemy_ga: GuardianAngel, guild_id: int, is_players_versus_players: bool, target_profile: Profile = None, target: discord.Member = None, allowed_multiple_players: bool = False, max_players:int = 1, embed_title: str = "", gold_reward: int = 0, silver_reward: int= 0, dignity_point: int = 10, bonus_exp: int = 200, enemy_ga_2: GuardianAngel = None, bonus_all_reward_percent: int = None, footer_text: str = "", difficulty: int = 1, is_dungeon = False, is_challenge = False, channel_name: str = "Không rõ"):
        super().__init__(timeout=180)
        self.message : discord.Message = None
        self.user: discord.Member = user
        self.target: discord.Member = target
        self.user_profile = user_profile
        self.target_profile = target_profile
        self.difficulty = difficulty
        self.enemy_ga = enemy_ga
        self.enemy_ga_2 = enemy_ga_2
        self.allowed_multiple_players = allowed_multiple_players
        self.max_players = max_players
        self.is_players_versus_players = is_players_versus_players
        self.is_dungeon = is_dungeon
        self.is_challenge = is_challenge
        self.so_tien = None
        self.loai_tien = None
        self.channel_name = channel_name
        self.battle_type = "A"
        self.battle_type_mapping = {
            "A": "Chiến đấu bình thường (Dùng mọi kỹ năng)",
            "B": "Chiến đấu không dùng bất kỳ kỹ năng nào",
            "C": "Chiến đấu không dùng kỹ năng Tẩy Não",
            "D": "Chiến đấu không dùng kỹ năng Triệu Linh",
            "E": "Chiến đấu không dùng kỹ năng Triệu Linh và Tẩy Não",
        }
        self.upper_attack_class: List['GuardianAngelAttackClass'] = []
        self.lower_attack_class: List['GuardianAngelAttackClass'] = []
        
        #Dùng làm danh sách tạm thời cho thao túng list
        self.upper_temp_list: List['GuardianAngelAttackClass'] = []
        self.lower_temp_list: List['GuardianAngelAttackClass'] = []
        
        self.round_number_text_report = {}
        self.round = 1
        self.embed_title = embed_title
        self.footer_text = footer_text
        self.joined_player_id : List[int]= []
        
        self.upper_attack_won = False
        self.dignity_point = dignity_point
        self.gold_reward = gold_reward
        self.silver_reward = silver_reward
        self.bonus_exp = bonus_exp
        self.minus_all_reward_percent: int = None
        self.bonus_all_reward_percent: int = bonus_all_reward_percent
        
        self.guild_id = guild_id
        
        self.battle_ended = False
        
        first_player_class = GuardianAngelAttackClass(player_profile=user_profile, player_ga=user_profile.guardian)
        self.upper_attack_class.append(first_player_class)
        
        if is_players_versus_players:
            self.joined_allied_button = discord.ui.Button(label="Gia Nhập Phe Trên", style=discord.ButtonStyle.primary)
            self.joined_allied_button.callback = self.joined_allied_button_event
            self.add_item(self.joined_allied_button)
            
            self.joined_target_button = discord.ui.Button(label="Gia Nhập Phe Dưới", style=discord.ButtonStyle.red)
            self.joined_target_button.callback = self.joined_target_button_event
            self.add_item(self.joined_target_button)
            
            second_player_class = GuardianAngelAttackClass(player_profile=target_profile, player_ga=target_profile.guardian)
            self.lower_attack_class.append(second_player_class)
            self.joined_player_id.append(user.id)
            self.joined_player_id.append(target.id)
            
        else:
            self.joined_fight_button = discord.ui.Button(label="⚔️ Chiến Đấu", style=discord.ButtonStyle.green)
            self.joined_fight_button.callback = self.joined_the_fight_button_event
            self.add_item(self.joined_fight_button)
            
            second_player_class = GuardianAngelAttackClass(player_ga=enemy_ga)
            self.lower_attack_class.append(second_player_class)
            self.joined_player_id.append(user.id)
            
            if enemy_ga_2 != None:
                second_player_class = GuardianAngelAttackClass(player_ga=enemy_ga_2)
                self.lower_attack_class.append(second_player_class)
        
        #Đảm bảo đúng side
        for ga in self.upper_attack_class:
            ga.is_upper_side = True
        for ga in self.lower_attack_class:
            ga.is_upper_side = False
            
    async def on_timeout(self):
        #Delete
        if self.message != None and self.battle_ended == False: 
            await self.message.edit(view= None)
            return

    #region button event
    async def joined_allied_button_event(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if len(self.upper_attack_class) >= self.max_players:
            await interaction.followup.send(f'Phe trên đã đủ người!', ephemeral=True)
            return
        if interaction.user.id in self.joined_player_id:
            await interaction.followup.send(f'Bạn đã tham gia trận chiến này rồi!', ephemeral=True)
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
                view = SelfDestructView(timeout=30)
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
        
        #Đánh giao hữu thì 100% hết stats
        new_player_profile.guardian.health = new_player_profile.guardian.max_health
        new_player_profile.guardian.mana = new_player_profile.guardian.max_mana
        new_player_profile.guardian.stamina = new_player_profile.guardian.max_stamina
        
        data = GuardianAngelAttackClass(player_profile=new_player_profile, player_ga=new_player_profile.guardian, starting_at_round=self.round)
        self.upper_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_joined_battle", date_value=datetime.now())
        if self.is_players_versus_players:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_battle_pve")
        else:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_battle_pvp")
        await interaction.followup.send(content=f"Bạn đã gia nhập phe trên vào lượt thứ {self.round}!", ephemeral=True)
        return
    
    async def joined_target_button_event(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if len(self.lower_attack_class) >= self.max_players:
            await interaction.followup.send(f'Phe dưới đã đủ người!', ephemeral=True)
            return
        
        if interaction.user.id in self.joined_player_id:
            await interaction.followup.send(f'Bạn đã tham gia trận chiến này rồi!', ephemeral=True)
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
                view = SelfDestructView(timeout=30)
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
        
        #Đánh giao hữu thì 100% hết stats
        new_player_profile.guardian.health = new_player_profile.guardian.max_health
        new_player_profile.guardian.mana = new_player_profile.guardian.max_mana
        new_player_profile.guardian.stamina = new_player_profile.guardian.max_stamina
        
        data = GuardianAngelAttackClass(player_profile=new_player_profile, player_ga=new_player_profile.guardian, starting_at_round=self.round, is_upper_side=False)
        self.lower_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_joined_battle", date_value=datetime.now())
        if self.is_players_versus_players:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_battle_pve")
        else:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_battle_pvp")
        await interaction.followup.send(content=f"Bạn đã gia nhập phe dưới, vào lượt thứ {self.round}!", ephemeral=True)
        return


    async def joined_the_fight_button_event(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if len(self.upper_attack_class) >= self.max_players:
            await interaction.followup.send(f'Không còn chỗ trống cho bạn tham gia trận chiến này', ephemeral=True)
            return
        
        if interaction.user.id in self.joined_player_id:
            await interaction.followup.send(f'Bạn đã tham gia trận chiến này rồi!', ephemeral=True)
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
        
        data = GuardianAngelAttackClass(player_profile=new_player_profile, player_ga=new_player_profile.guardian, starting_at_round=self.round)
        self.upper_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
        await interaction.followup.send(content=f"Bạn đã gia nhập chiến đấu vào lượt thứ {self.round}!", ephemeral=True)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_joined_battle", date_value=datetime.now())
        if self.is_dungeon:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_dungeon_fight")
        else:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_battle_pve")
        return

    #region battle event
    async def commence_battle(self):
        if len(self.upper_attack_class) == 0 or len(self.lower_attack_class) == 0: return
        #Cập nhập lại danh sách team sau khi cả hai đều đánh xong.
        self.apply_pending_team_changes()
        await asyncio.sleep(4)
        #upper attack sẽ đánh trước
        flag_end_battle = False
        full_text = ""
        for self_player_info in self.upper_attack_class:
            #Skip qua guardian đã chết
            if self_player_info.player_ga.health <= 0: continue
            #Mỗi guardian trong upper sẽ chọn ngẫu nhiên một lower để đánh
            opponent_alive_attack_info = self.get_ga_stil_alive("lower")
            if opponent_alive_attack_info == None:
                #phe dưới đã thua, kết thúc trận chiến
                flag_end_battle = True
                self.upper_attack_won = True
                continue
            base_text = self.execute_attack(self_player_info = self_player_info, opponent_alive_attack_info = opponent_alive_attack_info)
            full_text += base_text + "\n"
            
        #tới lượt của phe lower
        for self_player_info in self.lower_attack_class:
            #Skip qua guardian đã chết
            if self_player_info.player_ga.health <= 0: continue
            #Mỗi guardian trong lower sẽ chọn ngẫu nhiên một upper để đánh
            opponent_alive_attack_info = self.get_ga_stil_alive("upper")
            if opponent_alive_attack_info == None:
                #phe trên đã thua, kết thúc trận chiến
                flag_end_battle = True
                self.upper_attack_won = False
                continue
            base_text = self.execute_attack(self_player_info = self_player_info, opponent_alive_attack_info = opponent_alive_attack_info)
            full_text += base_text + "\n"
        
        check_all_dead_upper = self.all_guardians_dead(self.upper_attack_class)
        if check_all_dead_upper:
            flag_end_battle = True
            self.upper_attack_won = False
            
        check_all_dead_lower = self.all_guardians_dead(self.lower_attack_class)
        if check_all_dead_lower:
            flag_end_battle = True
            self.upper_attack_won = True
        
        
        if not self.is_empty_or_whitespace(full_text):
            self.round_number_text_report.update({self.round: full_text.strip()})
        #Cập nhật embed chiến đấu
        embed = discord.Embed(title=f"", description=self.embed_title, color=0x0ce7f2)
        for self_player_info in self.upper_attack_class:
            text_own_profile_exist = f"{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level})"
            if self_player_info.player_profile != None:
                text_own_profile_exist = f"Hộ Vệ Thần {self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level}) của <@{self_player_info.player_profile.user_id}>"
                if self_player_info.player_ga.is_dead == True:
                    text_own_profile_exist += " (Tử Nạn)"
            embed.add_field(name=f"", value=text_own_profile_exist, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{self_player_info.player_ga.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.health, max_value=self_player_info.player_ga.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.stamina, max_value=self_player_info.player_ga.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.mana, max_value=self_player_info.player_ga.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        
        for self_player_info in self.lower_attack_class:
            text_target_profile_exist = f"Kẻ Thù {self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level})"
            if self_player_info.player_profile != None:
                text_target_profile_exist = f"Hộ Vệ Thần {self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level}) của <@{self_player_info.player_profile.user_id}>"
                if self_player_info.player_ga.is_dead == True:
                    text_target_profile_exist += " (Tử Nạn)" 
            embed.add_field(name=f"", value=text_target_profile_exist, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{self_player_info.player_ga.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.health, max_value=self_player_info.player_ga.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.stamina, max_value=self_player_info.player_ga.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.mana, max_value=self_player_info.player_ga.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        
        embed.set_footer(text=self.footer_text, icon_url=EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value)
        formatted_string = "\n".join(f"Lượt thứ **{key}**.\n{value}\n" for key, value in self.round_number_text_report.items())
        try:
            await self.message.edit(embed=embed, content=formatted_string)
        except Exception as e:
            await self.message.edit(embed=embed, content=f"Lượt thứ **{self.round}**")
        if flag_end_battle: await self.end_battle()
        else:
            max_limit = 2
            if len(self.upper_attack_class) >= 3 or len(self.lower_attack_class) >= 3: max_limit = 1
            if self.round > max_limit:
                #Bỏ đi round đầu để tiếp kiệm chỗ
                if self.round_number_text_report:
                    first_key = list(self.round_number_text_report.keys())[0]
                    del self.round_number_text_report[first_key]
            self.round += 1
            await self.commence_battle()
        return
    
    async def end_battle(self):
        print(f"Username {self.user_profile.user_name} has ended guardian battle in guild {self.user_profile.guild_name}!")
        self.battle_ended = True
        embed = discord.Embed(title="Tổng Kết Chiến Đấu", color=0xFFD700)
        # winner, loser
        winning_class = self.upper_attack_class if self.upper_attack_won else self.lower_attack_class
        losing_class = self.lower_attack_class if self.upper_attack_won else self.upper_attack_class
        winner = self.user if self.upper_attack_won else self.target
        loser = self.target if self.upper_attack_won else self.user
        is_solo_battle = all(
            info.player_profile is None or info.player_profile.user_id == self.user.id
            for info in winning_class + losing_class
        )
        if self.upper_attack_won:
            embed.description = "Phe trên thắng!"
        else:
            embed.description = "Phe dưới thắng!"

        # Nếu là challenge thì không có bất kỳ phần thưởng nào hết
        if not self.is_challenge:
            embed.add_field(name="", value="▬▬▬ι════>", inline=False)
            for info in winning_class:
                additional_stats, reward = self.get_result_addition_stats(info, is_solo_battle)
                if additional_stats.strip() and reward.strip():
                    embed.add_field(name="", value=additional_stats, inline=False)
                    embed.add_field(name="", value=reward, inline=False)

            # Cho phép bên thua một tý EXP
            for lose_info in losing_class:
                if lose_info.player_profile is not None:
                    ProfileMongoManager.update_main_guardian_level_progressing(
                        guild_id=self.guild_id, user_id=lose_info.player_profile.user_id
                    )
        else:
            # Là thách đấu nên sẽ ghi khác
            embed.description = f"{EmojiCreation2.SHINY_POINT.value} Hộ Vệ Thần của {winner.mention} đã đánh thắng Hộ Vệ Thần của {loser.mention}!"

            if self.so_tien is not None and self.loai_tien is not None:
                actual_money = int(self.so_tien * 0.95)
                tax_money = self.so_tien - actual_money

                embed.description = f"{EmojiCreation2.SHINY_POINT.value} {winner.mention} đã nhận được **{actual_money}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)}!"
                embed.add_field(
                    name="",
                    value=f"{EmojiCreation2.SHINY_POINT.value} Còn **{tax_money}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)} đã được Chính Quyền thu làm thuế",
                    inline=False
                )

                ProfileMongoManager.update_profile_money_by_type(
                    guild_id=self.guild_id,
                    user_id=winner.id,
                    guild_name="",
                    user_display_name=winner.display_name,
                    user_name=winner.name,
                    money=actual_money,
                    money_type=self.loai_tien
                )
                ProfileMongoManager.update_profile_money_by_type(
                    guild_id=self.guild_id,
                    user_id=loser.id,
                    guild_name="",
                    user_display_name=loser.display_name,
                    user_name=loser.name,
                    money=-self.so_tien,
                    money_type=self.loai_tien
                )
                ProfileMongoManager.update_money_authority_by_money_type(
                    guild_id=self.guild_id,
                    money_type=self.loai_tien,
                    money=tax_money
                )
        try:
            await self.message.reply(embed=embed)
            await self.message.edit(view=None)
        except Exception as e:
            print(e)

        #Tăng count, tạo memories cho từng người có info
        for info in self.upper_attack_class:
            if not info.player_profile: continue
            result = "won" if self.upper_attack_won else "lose"
            self.increase_count_win_lose_profile(info=info, result=result)
            self.add_memory_win_lose(info=info, result=result)
                
        for info in self.lower_attack_class:
            if not info.player_profile: continue
            result = "lose" if self.upper_attack_won else "won"
            self.increase_count_win_lose_profile(info=info, result=result)
            self.add_memory_win_lose(info=info, result=result)

        # nếu là PVP và KHÔNG PHẢI thách đấu thì không cần cập nhật stats
        if self.is_players_versus_players and not self.is_challenge: return
        # Cập nhật stats cho guardian nếu có profile cho PVE, hoặc challenge
        for info in self.upper_attack_class:
            if info.player_profile != None:
                self.update_stats_in_database(info)
        for info in self.lower_attack_class:
            if info.player_profile != None:
                self.update_stats_in_database(info)
        return
    
    
    def calculate_contribution(self, entry_turn):
        if entry_turn > self.round:
            return 0
        turns_participated = self.round - entry_turn + 1
        contribution_percentage = int(turns_participated / self.round * 100) 
        return contribution_percentage
    
    def increase_count_win_lose_profile(self, info: GuardianAngelAttackClass, result = "won"):
        if info.player_profile == None: return
        if self.is_dungeon:
            ProfileMongoManager.increase_count_guardian(guild_id=self.guild_id, user_id=info.player_profile.user_id, count_type=f"count_dungeon_fight_{result}")
        elif self.is_players_versus_players or self.is_challenge:
            ProfileMongoManager.increase_count_guardian(guild_id=self.guild_id, user_id=info.player_profile.user_id, count_type=f"count_battle_pvp_{result}")
        else:
            ProfileMongoManager.increase_count_guardian(guild_id=self.guild_id, user_id=info.player_profile.user_id, count_type=f"count_battle_pve_{result}")


    def add_memory_win_lose(self, info: GuardianAngelAttackClass, result="won"):
        if info.player_profile is None:
            return
        battle_type = "Chiến Đấu Quái"
        if self.is_dungeon:
            battle_type = "Hầm Ngục Hộ Vệ Thần"
        elif self.is_players_versus_players:
            battle_type = "Thách Đấu Hộ Vệ Thần" if self.is_challenge else "Chiến Đấu Hộ Vệ Thần"
        memories = info.player_ga.memories or []
        memory_description = None
        # Templates
        win_templates = [
            f"{info.player_ga.ga_name} đã xuất sắc đánh bại {self.enemy_ga.ga_name} trong trận {battle_type}.",
            f"{info.player_ga.ga_name} dễ dàng hạ gục {self.enemy_ga.ga_name} trong {battle_type}.",
            f"Trong {battle_type}, {info.player_ga.ga_name} đã bón hành cho {self.enemy_ga.ga_name}.",
            f"{info.player_ga.ga_name} đã thắng áp đảo {self.enemy_ga.ga_name} trong {battle_type}.",
        ]

        lose_templates = [
            f"{info.player_ga.ga_name} đã thất bại trước {self.enemy_ga.ga_name} trong trận {battle_type}.",
            f"Dù đã cố gắng, {info.player_ga.ga_name} không thể vượt qua {self.enemy_ga.ga_name} trong {battle_type}.",
            f"Trong {battle_type}, {info.player_ga.ga_name} đã chịu khuất phục trước sức mạnh của {self.enemy_ga.ga_name}.",
            f"Trận {battle_type} kết thúc với thất bại đầy cay đắng của {info.player_ga.ga_name} trước {self.enemy_ga.ga_name}.",
        ]

        templates = win_templates if result == "won" else lose_templates
        selected_description = random.choice(templates)

        # Chỉ có % khả năng nhớ kết quả, và hai memory mới nhất không phải thuộc tag battle
        chance = 40
        if not memories:
            memory_description = selected_description
        else:
            try:
                first = memories[0]
                if first.tag != GuardianMemoryTag.BATTLE:
                    memory_description = selected_description
                elif chance:
                    memory_description = selected_description
            except Exception:
                memory_description = selected_description

        if memory_description:
            ProfileMongoManager.add_memory_guardian(
                guild_id=self.guild_id,
                user_id=info.player_profile.user_id,
                channel_name=self.channel_name,
                memory_description=memory_description,
                tag=GuardianMemoryTag.BATTLE.value
            )
    
    def is_empty_or_whitespace(self, s: str):
        return not s.strip()
    
    def all_guardians_dead(self, guardians: List['GuardianAngelAttackClass']) -> bool:
        return all(guardian.player_ga.health <= 0 for guardian in guardians)
    
    def get_result_addition_stats(self, info: GuardianAngelAttackClass, is_solo = False):
        if info.player_profile == None: return "", ""
        #Nhân theo lượng người tham gia
        bonus_exp = int(self.bonus_exp * len(self.upper_attack_class) + self.bonus_exp*len(self.lower_attack_class))
        if bonus_exp > 350: 
            bonus_exp = 350
            if is_solo: bonus_exp = 450
        gold_reward = int(self.gold_reward * len(self.upper_attack_class) + self.bonus_exp*len(self.lower_attack_class))
        if self.minus_all_reward_percent != None:
            gold_reward = gold_reward * self.minus_all_reward_percent / 100
        if self.bonus_all_reward_percent != None:
            gold_reward += gold_reward * self.bonus_all_reward_percent / 100
        if gold_reward > 50000: gold_reward = 50000
        
        silver_reward = int(self.silver_reward * len(self.upper_attack_class) + self.bonus_exp*len(self.lower_attack_class))
        if self.minus_all_reward_percent != None:
            silver_reward = silver_reward * self.minus_all_reward_percent / 100
        if self.bonus_all_reward_percent != None:
            silver_reward += silver_reward * self.bonus_all_reward_percent / 100
            
        contribution = self.calculate_contribution(info.starting_at_round)
        text_target_profile_exist = f"{EmojiCreation2.SHINY_POINT.value} <@{info.player_profile.user_id}> [{info.starting_at_round}] cống hiến **{contribution}%**, nhận: "
        text_reward = ""
        flag_no_additional_reward = False
        calculated_exp = int(bonus_exp * (contribution / 100))
        if calculated_exp > 0:
            if self.minus_all_reward_percent != None:
                calculated_exp = int(calculated_exp * self.minus_all_reward_percent / 100)
            if self.is_players_versus_players and calculated_exp > 280: calculated_exp = 280
            
            #Nếu level cao đánh hầm ngục thấp thì giảm tất cả phần thưởng
            if self.difficulty < 3 and info.player_ga.level > self.enemy_ga.level and self.is_dungeon:
                calculated_exp = 100
                silver_reward = silver_reward * 0.5
                gold_reward = gold_reward * 0.5
                #Không cho phép nhận phần thưởng cộng thêm
                flag_no_additional_reward = True
            
            text_reward += f"**{calculated_exp}** EXP. "
            ProfileMongoManager.update_level_progressing(guild_id=self.guild_id, user_id=info.player_profile.user_id, bonus_exp=int(calculated_exp*0.3))
            ProfileMongoManager.update_main_guardian_level_progressing(guild_id=self.guild_id, user_id=info.player_profile.user_id, bonus_exp=calculated_exp)
        
        calculated_gold_reward = int(gold_reward * (contribution / 100))
        if calculated_gold_reward > 0:
            text_reward += f"**{calculated_gold_reward}** {EmojiCreation2.GOLD.value} "
        
        calculated_silver_reward = int(silver_reward * (contribution / 100))
        if calculated_silver_reward > 0:
            text_reward += f"**{calculated_silver_reward}** {EmojiCreation2.SILVER.value} "
        
        ProfileMongoManager.update_profile_money(guild_id=self.guild_id, user_id=info.player_profile.user_id, guild_name="",user_display_name="", user_name="", gold=calculated_gold_reward, silver=calculated_silver_reward)
        
        if self.dignity_point > 0:
            text_reward += f"**{self.dignity_point}** Nhân phẩm. "
            ProfileMongoManager.update_dignity_point(guild_id=self.guild_id, user_id=info.player_profile.user_id, guild_name="",user_display_name="", user_name="", dignity_point=self.dignity_point)
        
        if info.player_profile.user_id == self.user.id and self.is_players_versus_players == False and flag_no_additional_reward == False:
            #Chủ party
            text_reward += f"Thưởng thêm: {self.get_result_additional_reward(info=info, is_solo=is_solo)}"
        
        if info.player_ga.is_dead:
            text_reward+= " Hộ Vệ Thần tử nạn. "
        text_reward += "\n"
        return text_target_profile_exist, text_reward
    
    def get_result_additional_reward(self, info: GuardianAngelAttackClass, is_solo = False):
        if info.player_profile == None: return ""
        reward_text = ""
        amount = 1
        #point
        roll_dice = UtilitiesFunctions.get_chance(15)
        if roll_dice:
            amount = 1
            if is_solo: 
                #roll random 1 2
                amount = random.randint(1, 2)
            ProfileMongoManager.set_guardian_stats_points(guild_id=self.guild_id, user_id=info.player_profile.user_id, stats_point=amount)
            reward_text = f"x{amount} **Điểm Cộng Chỉ Số**"
            return reward_text
        #legendary weapon chance
        roll_dice = UtilitiesFunctions.get_chance(5)
        if self.is_dungeon == True and self.difficulty < 4: roll_dice = False
        if roll_dice:
            dice_check = UtilitiesFunctions.get_chance(50)
            if dice_check:
                item = copy.deepcopy(random.choice(list_legend_weapon_1))
                item.item_worth_amount = 10
                reward_text = f"x1 **[{item.emoji} - {item.item_name}]**"
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", item=item, amount=1)
                return reward_text
            else:
                item = copy.deepcopy(random.choice(list_legend_weapon_2))
                item.item_worth_amount = 10
                reward_text = f"x1 **[{item.emoji} - {item.item_name}]**"
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", item=item, amount=1)
                return reward_text
        
        #darkium
        roll_dice =UtilitiesFunctions.get_chance(10)
        if self.is_dungeon == True and self.difficulty < 4: roll_dice = False
        if roll_dice:
            amount = random.randint(1, 3)
            if is_solo: amount * 3
            reward_text = f"**{amount}** {EmojiCreation2.DARKIUM.value}"
            ProfileMongoManager.update_profile_money(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", darkium=amount)
            return reward_text
        
        #Random gift
        roll_dice =UtilitiesFunctions.get_chance(35)
        if roll_dice:
            amount = random.randint(1, 5)
            item = random.choice(list_gift_items)
            if is_solo: amount * 3
            reward_text = f"x{amount} **[{item.emoji} - {item.item_name}]**"
            ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #random potion
        roll_dice =UtilitiesFunctions.get_chance(35)
        if roll_dice:
            amount = random.randint(1, 3)
            #Roll xem trúng bình nào
            if is_solo: amount * 3
            item = copy.deepcopy(random.choice(list_support_ga_items))
            roll_dice = UtilitiesFunctions.get_chance(70)
            if self.is_dungeon == True and self.difficulty < 3: roll_dice = True
            if roll_dice:
                #Trúng 3 bình bình thường
                filtered_items = [
                    d for d in list_support_ga_items 
                    if d.item_id in ["ga_heal_1", "ga_stamina_1", "ga_mana_1"]
                ]
                item =  copy.deepcopy(random.choice(filtered_items))
                item.item_worth_amount = 1000
            else:
                amount = 1
                if is_solo: amount * 3
                item_id = "ga_all_restored"
                additional_dice = UtilitiesFunctions.get_chance(35)
                if additional_dice: item_id = "ga_resurrection"
                additional_dice = UtilitiesFunctions.get_chance(35)
                if additional_dice: item_id = "ga_boss_summoning"
                for randomitem in list_support_ga_items:
                    if randomitem.item_id == item_id:
                        item = copy.deepcopy(randomitem)
                        break
                if item == None: item = copy.deepcopy(random.choice(list_support_ga_items))
                item.item_worth_amount = 5
            reward_text = f"x{amount} **[{item.emoji} - {item.item_name}]**"
            ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #random weapon
        roll_dice =UtilitiesFunctions.get_chance(35)
        if roll_dice:
            amount = random.randint(1, 3)
            if is_solo: amount * 3
            item = random.choice(list_attack_items)
            reward_text = f"x{amount} **[{item.emoji} - {item.item_name}]**"
            ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #random armour
        roll_dice =UtilitiesFunctions.get_chance(25)
        if roll_dice:
            amount = random.randint(1, 2)
            if is_solo: amount * 3
            item = random.choice(list_protection_items)
            reward_text = f"x{amount} **[{item.emoji} - {item.item_name}]**"
            ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #gold
        amount = random.randint(1000, 30000)
        if is_solo: amount * 3
        reward_text = f"**{amount}** {EmojiCreation2.GOLD.value}"
        ProfileMongoManager.update_profile_money(guild_id=self.guild_id, guild_name="", user_id=info.player_profile.user_id, user_display_name="", user_name="", gold=amount)
        return reward_text
        
    
    def update_stats_in_database(self, info: GuardianAngelAttackClass):
        if info.player_profile != None:
            if CustomFunctions.check_if_dev_mode(): return
            ProfileMongoManager.set_guardian_current_stats(guild_id=self.guild_id, user_id=info.player_profile.user_id,stamina=info.player_ga.stamina, health=info.player_ga.health, mana=info.player_ga.mana, is_dead=info.player_ga.is_dead)
            if info.player_ga.is_dead:
                #Tạo memory death
                ProfileMongoManager.add_memory_guardian(
                    guild_id=self.guild_id,
                    user_id=info.player_profile.user_id,
                    channel_name=self.channel_name,
                    memory_description= f"Đã tử nạn trong lúc giao chiến với {self.enemy_ga.ga_emoji} - {self.enemy_ga.ga_name}",
                    tag=GuardianMemoryTag.DEATH.value
                )
            if info.player_ga.health <= 0:
                #Tạo memory injure
                ProfileMongoManager.add_memory_guardian(
                    guild_id=self.guild_id,
                    user_id=info.player_profile.user_id,
                    channel_name=self.channel_name,
                    memory_description= f"Đã trọng thương trong lúc giao chiến với {self.enemy_ga.ga_emoji} - {self.enemy_ga.ga_name}",
                    tag=GuardianMemoryTag.INJURY.value
                )
    
    def get_ga_stil_alive(self, side: str):
        if side == "upper":
            if self.upper_attack_class == None or len(self.upper_attack_class) == 0: return None
            legit_attack_classes = [attack_class for attack_class in self.upper_attack_class if attack_class.player_ga.health > 0]
            if len(legit_attack_classes) == 0: return None
            attack_classes_without_player_profile = [attack_class for attack_class in legit_attack_classes if attack_class.player_profile is None]
            chance = UtilitiesFunctions.get_chance(55)
            #Ưu tiên chọn attack_class không có profile trước
            if chance and len(attack_classes_without_player_profile)>0: return random.choice(attack_classes_without_player_profile)
            return random.choice(legit_attack_classes)
        else:
            if self.lower_attack_class == None or len(self.lower_attack_class) == 0: return None
            legit_attack_classes = [attack_class for attack_class in self.lower_attack_class if attack_class.player_ga.health > 0]
            if len(legit_attack_classes) == 0: return None
            attack_classes_without_player_profile = [attack_class for attack_class in legit_attack_classes if attack_class.player_profile is None]
            chance = UtilitiesFunctions.get_chance(55)
            if chance and len(attack_classes_without_player_profile)>0: return random.choice(attack_classes_without_player_profile)
            return random.choice(legit_attack_classes)

    def execute_attack(self, self_player_info: GuardianAngelAttackClass, opponent_alive_attack_info: GuardianAngelAttackClass):
        health_potion = None
        stamina_potion = None
        mana_potion = None
        #Chỉ để check xem profile của đối thủ có hay không
        text_target_profile_exist = ""
        if opponent_alive_attack_info.player_profile != None:
            text_target_profile_exist = f"của <@{opponent_alive_attack_info.player_profile.user_id}>"
        #Chỉ để check xem profile của bản thân có hay không
        text_own_profile_exist = ""
        if self_player_info.player_profile != None:
            text_own_profile_exist = f"của <@{self_player_info.player_profile.user_id}>"
        
        #Lọc qua inventory của profile để xem có bình máu không
        if self_player_info.player_profile != None and self_player_info.player_profile.list_items != None and len(self_player_info.player_profile.list_items) > 0:
            for item in self_player_info.player_profile.list_items:
                if item.item_id == "ga_heal_1":
                    health_potion = item
                if item.item_id == "ga_stamina_1":
                    stamina_potion = item
                if item.item_id == "ga_mana_1":
                    mana_potion = item
        
        #Kiểm tra xem có stun không, có thì skip lượt
        if self_player_info.stunned_round != 0:
            self_player_info.stunned_round -= 1
            if self_player_info.stunned_round >= 0:
                base_text = f"- **[{self_player_info.player_ga.ga_emoji} - {self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã quá choáng váng không thể làm được gì!"
                return base_text
        
        #Tính tỉ lệ hồi máu nếu máu ít hơn % và phải có bình máu trong kho đồ
        if self_player_info.player_profile != None and self_player_info.player_ga.health < self_player_info.player_ga.max_health*0.45 and health_potion != None:
            #roll chance 40% dùng bình máu nếu có trong inventory của profile
            use_chance = UtilitiesFunctions.get_chance(40)
            if use_chance:
                #Tuỳ loại bình máu mà hồi theo phần trăm máu, mặc định 30%
                percent_restored= 0.3
                
                heal_amount = int(self_player_info.player_ga.max_health * percent_restored)
                self_player_info.player_ga.health += heal_amount
                if self_player_info.player_ga.health > self_player_info.player_ga.max_health: self_player_info.player_ga.health = self_player_info.player_ga.max_health
                
                base_text = f"- **[{self_player_info.player_ga.ga_emoji} - {self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã sử dụng **{health_potion.item_name}** để hồi **{heal_amount}** Máu!"
                
                self_player_info.recovery_time += 1
                #Xóa item khỏi inventory
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, user_name="", guild_name="",user_display_name="", item = health_potion, amount=-1)
                roll_chance = UtilitiesFunctions.get_chance(20)
                if roll_chance:
                    ProfileMongoManager.add_memory_guardian(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, channel_name=self.channel_name, memory_description=f"Đã sử dụng **{health_potion.item_name}** để hồi phục sức mạnh", tag=GuardianMemoryTag.BATTLE.value)
                try:
                    self_player_info.player_profile.list_items.remove(health_potion)
                except Exception as e: print()
                return base_text
        
        #Tính tỉ lệ hồi thể lực nếu thể lực ít hơn % và phải có bình stamina trong kho đồ
        if self_player_info.player_profile != None and self_player_info.player_ga.stamina < self_player_info.player_ga.max_stamina*0.45 and stamina_potion != None:
            #roll chance 40% dùng bình nếu có trong inventory của profile
            use_chance = UtilitiesFunctions.get_chance(40)
            if use_chance:
                #Tuỳ loại bình mà hồi theo phần trăm, mặc định 50%
                percent_restored= 0.5
                
                heal_amount = int(self_player_info.player_ga.max_stamina * percent_restored)
                self_player_info.player_ga.stamina += heal_amount
                if self_player_info.player_ga.stamina > self_player_info.player_ga.max_stamina: self_player_info.player_ga.stamina = self_player_info.player_ga.max_stamina
                
                base_text = f"- **[{self_player_info.player_ga.ga_emoji} - {self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã sử dụng **{stamina_potion.item_name}** để hồi **{heal_amount}** Thể Lực!"
                
                #Xóa item khỏi inventory
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, user_name="", guild_name="",user_display_name="", item = stamina_potion, amount=-1)
                roll_chance = UtilitiesFunctions.get_chance(20)
                if roll_chance:
                    ProfileMongoManager.add_memory_guardian(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, channel_name=self.channel_name, memory_description=f"Đã sử dụng **{stamina_potion.item_name}** để hồi phục sức mạnh", tag=GuardianMemoryTag.BATTLE.value)
                try:
                    self_player_info.player_profile.list_items.remove(stamina_potion)
                except Exception as e: print()
                return base_text
        
        #Tính tỉ lệ hồi mana nếu mana ít hơn % và phải có bình mana trong kho đồ
        if self_player_info.player_profile != None and self_player_info.player_ga.mana < self_player_info.player_ga.max_mana*0.5 and mana_potion != None:
            #roll chance 30% dùng bình nếu có trong inventory của profile
            use_chance = UtilitiesFunctions.get_chance(30)
            if use_chance:
                #Tuỳ loại bình mà hồi theo phần trăm, mặc định 40%
                percent_restored= 0.4
                heal_amount = int(self_player_info.player_ga.max_mana * percent_restored)
                self_player_info.player_ga.mana += heal_amount
                if self_player_info.player_ga.mana > self_player_info.player_ga.max_mana: self_player_info.player_ga.mana = self_player_info.player_ga.max_mana

                base_text = f"- **[{self_player_info.player_ga.ga_emoji} - {self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã sử dụng **{mana_potion.item_name}** để hồi **{heal_amount}** Mana!"

                #Xóa item khỏi inventory
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, user_name="", guild_name="",user_display_name="", item = mana_potion, amount=-1)
                roll_chance = UtilitiesFunctions.get_chance(20)
                if roll_chance:
                    ProfileMongoManager.add_memory_guardian(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, channel_name=self.channel_name, memory_description=f"Đã sử dụng **{mana_potion.item_name}** để hồi phục sức mạnh", tag=GuardianMemoryTag.BATTLE.value)
                try:
                    self_player_info.player_profile.list_items.remove(mana_potion)
                except Exception as e: print()
                return base_text

        #Đánh flag xem đã dùng action chưa
        flag_action = False
        #Xử lý logic dùng skill nếu có skill trong list
        try:
            if self_player_info.player_ga.list_skills != None and len(self_player_info.player_ga.list_skills) > 0 and self.battle_type != "B": #B là không dùng bất kỳ skill nào hết
                #Ưu tiên skill passive trước
                base_text = self.execute_passive_skill(self_player_info = self_player_info, opponent_alive_attack_info = opponent_alive_attack_info, text_target_profile_exist=text_target_profile_exist, text_own_profile_exist=text_own_profile_exist)
                if base_text != None:
                    flag_action = True
                
                if not flag_action:
                    #Đến skill tấn công
                    attack_skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_types=["attack"])
                    if attack_skill != None:
                        #Thi triển kỹ năng
                        base_text = self.execute_attack_skill(self_player_info = self_player_info, opponent_alive_attack_info = opponent_alive_attack_info, skill=attack_skill, text_target_profile_exist=text_target_profile_exist, text_own_profile_exist=text_own_profile_exist)
                        if base_text != None: 
                            flag_action = True
        except Exception as e:
            print(f"Exception when executing attack skill, {e}")
        
        if not flag_action: 
            #Tính tỉ lệ evasion
            loss_amount = int(self_player_info.player_ga.attack_power * 0.5)
            opponent_evasion_chance = self.calculate_chance_by_stats(current_stat=opponent_alive_attack_info.player_ga.stamina, max_stat=opponent_alive_attack_info.player_ga.max_stamina, level=opponent_alive_attack_info.player_ga.level)
            if opponent_evasion_chance > 85: opponent_evasion_chance = 85
            evasion_dice = UtilitiesFunctions.get_chance(opponent_evasion_chance)
            if evasion_dice and opponent_alive_attack_info.player_ga.stamina >= loss_amount: #Phải có đủ thể lực cần thiết mới né được
                #Chỉ trừ stamina của lower, tỉ lệ thấp hơn, tầm 50% của info.player_ga.attack_power
                loss_amount = int(self_player_info.player_ga.attack_power * 0.4)
                opponent_alive_attack_info.player_ga.stamina -= loss_amount
                if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
                base_text = f"- **[{self_player_info.player_ga.ga_emoji} - {self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã lao đến đánh {opponent_alive_attack_info.player_ga.ga_name} {text_target_profile_exist} nhưng mục tiêu đã kịp né tránh, và chỉ mất **{loss_amount}** thể lực!"
            else:
                #trừ máu của lower
                loss_health = int(self_player_info.player_ga.attack_power + self_player_info.player_ga.attack_power*(self_player_info.player_ga.buff_attack_percent/100))
                opponent_alive_attack_info.player_ga.health -= loss_health
                #trừ stamina của lower, tỉ lệ thấp hơn, tầm 25% của info.player_ga.attack_power
                loss_amount = int(self_player_info.player_ga.attack_power * 0.25)
                opponent_alive_attack_info.player_ga.stamina -= loss_amount
                if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
                base_text = f"- **[{self_player_info.player_ga.ga_emoji} - {self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã đánh trúng [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}! Mục tiêu mất **{loss_health}** Máu và **{loss_amount}** Thể Lực!"
                try:
                    #Sau khi attack thì kiểm tra
                    new_base_text = self.execute_after_attack_skill(self_player_info=self_player_info, opponent_alive_attack_info=opponent_alive_attack_info, text_target_profile_exist=text_target_profile_exist, text_own_profile_exist=text_own_profile_exist)
                    if new_base_text != None:
                        base_text = new_base_text
                except Exception as e:
                    print(f"Exception when executing after attack skill, {e}")
        
        additional_loss_stats_text = ""
        #Để đảm bảo stats không bị âm        
        if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
        if opponent_alive_attack_info.player_ga.mana <= 0: opponent_alive_attack_info.player_ga.mana = 0
        if opponent_alive_attack_info.player_ga.health <= 0: 
            opponent_alive_attack_info.player_ga.health = 0
            additional_loss_stats_text = f" Mục tiêu đã bị hạ gục!"
            #Roll tỷ lệ chết nếu đánh PVE
            if self.is_players_versus_players == False and opponent_alive_attack_info.player_profile != None:
                actual_death_chance = UtilitiesFunctions.guardian_death_chance(level=opponent_alive_attack_info.player_ga.level)
                roll_dice_death = UtilitiesFunctions.get_chance(actual_death_chance)
                if roll_dice_death:
                    #Coi như chết
                    additional_loss_stats_text = f" Hộ Vệ Thần của mục tiêu đã chết vĩnh viễn!"
                    opponent_alive_attack_info.is_dead_ga = True
                    opponent_alive_attack_info.player_ga.is_dead = True

            #Kiểm tra xem phải summoned không, có thì remove hẳn khỏi đội hình
            if opponent_alive_attack_info.is_summoned:
                #Remove khỏi đội hình
                try:
                    if opponent_alive_attack_info in self.upper_attack_class:
                        self.upper_attack_class.remove(opponent_alive_attack_info)
                    elif opponent_alive_attack_info in self.lower_attack_class:
                        self.lower_attack_class.remove(opponent_alive_attack_info)
                except Exception as e:
                    print(f"Exception when checking remove summoned ga from team, {e}")
                #Tìm owner và set lại skill
                for a in self.upper_attack_class:
                    if a.player_profile != None and a.player_profile.user_id == opponent_alive_attack_info.summoner_owner_id:
                        a.has_used_summoning = False
                        break
                for a in self.lower_attack_class:
                    if a.player_profile != None and a.player_profile.user_id == opponent_alive_attack_info.summoner_owner_id:
                        a.has_used_summoning = False
                        break
        
        #Trừ -1 tẩy não khi hết lượt
        if self_player_info.brain_washed_round > 0:
            self_player_info.brain_washed_round -= 1
            #Khi còn 0 thì đổi phe
            if self_player_info.brain_washed_round <= 0:
                self_player_info.brain_washed_round = 0
                try:
                    if self_player_info.is_upper_side == False:
                        self.remove_ga_by_player_ga(lst=self.upper_temp_list, target=self_player_info)
                        self.add_ga_by_player_ga(lst=self.lower_temp_list, target=self_player_info)
                    else:
                        self.remove_ga_by_player_ga(lst=self.lower_temp_list, target=self_player_info)
                        self.add_ga_by_player_ga(lst=self.upper_temp_list, target=self_player_info)
                except Exception as e:
                    print(f"Exception when remove brain washed ga from team, {e}")
        
        base_text+= additional_loss_stats_text
        #Đảm bảo stats không âm
        if self_player_info.player_ga.health < 0: self_player_info.player_ga.health = 0
        if self_player_info.player_ga.mana < 0: self_player_info.player_ga.mana = 0
        if self_player_info.player_ga.stamina < 0: self_player_info.player_ga.stamina = 0
        
        if opponent_alive_attack_info.player_ga.health < 0: opponent_alive_attack_info.player_ga.health = 0
        if opponent_alive_attack_info.player_ga.mana < 0: opponent_alive_attack_info.player_ga.mana = 0
        if opponent_alive_attack_info.player_ga.stamina < 0: opponent_alive_attack_info.player_ga.stamina = 0
        
        #Đảm bảo stats không lố max
        if self_player_info.player_ga.health > self_player_info.player_ga.max_health: self_player_info.player_ga.health = self_player_info.player_ga.max_health
        if self_player_info.player_ga.mana > self_player_info.player_ga.max_mana: self_player_info.player_ga.mana = self_player_info.player_ga.max_mana
        if self_player_info.player_ga.stamina > self_player_info.player_ga.max_stamina: self_player_info.player_ga.stamina = self_player_info.player_ga.max_stamina
        if opponent_alive_attack_info.player_ga.health > opponent_alive_attack_info.player_ga.max_health: opponent_alive_attack_info.player_ga.health = opponent_alive_attack_info.player_ga.max_health
        if opponent_alive_attack_info.player_ga.mana > opponent_alive_attack_info.player_ga.max_mana: opponent_alive_attack_info.player_ga.mana = opponent_alive_attack_info.player_ga.max_mana
        if opponent_alive_attack_info.player_ga.stamina > opponent_alive_attack_info.player_ga.max_stamina: opponent_alive_attack_info.player_ga.stamina = opponent_alive_attack_info.player_ga.max_stamina
        return base_text
        
    def calculate_chance_by_stats(self, current_stat, max_stat, level, max_percent=90, level_bonus=0.8):
        level = min(level, 80)
        evasion_chance = ((current_stat / max_stat) * max_percent) + (level * level_bonus)
        return int(min(evasion_chance, max_percent))

    def get_random_skill(self, list_skills: List["GuardianAngelSkill"], skill_types: List[str] = None, skill_id: str = None):
        #Nếu có skill name thì ưu tiên tìm xem có skill name không
        if skill_id != None:
            legit_skills = [skill for skill in list_skills if skill.skill_id == skill_id]
            if len(legit_skills) == 0: return None
            return legit_skills[0]
        #Nếu không yêu cầu loại skill thì random bình thường
        if skill_types == None:
            return random.choice(list_skills)
        else:
            legit_skills = [skill for skill in list_skills if any(t in skill.skill_type for t in skill_types)]
            if len(legit_skills) == 0: return None
            return random.choice(legit_skills)
        return None

    #region execute_attack_skill
    def execute_attack_skill(self, self_player_info: GuardianAngelAttackClass, opponent_alive_attack_info: GuardianAngelAttackClass, skill: GuardianAngelSkill, text_target_profile_exist: str, text_own_profile_exist: str):
        base_text = None
        mem_chance = UtilitiesFunctions.get_chance(20)
        #Mana của bản thân phải lớn hơn hoặc bằng mana yêu cầu của skill
        current_mana_percent = int(self_player_info.player_ga.mana/self_player_info.player_ga.max_mana*100)
        if current_mana_percent >= skill.percent_min_mana_req:
            #roll chance dùng skill
            use_magic_int = self.calculate_chance_by_stats(current_stat=self_player_info.player_ga.mana, max_stat=self_player_info.player_ga.max_mana, level=opponent_alive_attack_info.player_ga.level)
            first_chance = UtilitiesFunctions.get_chance(use_magic_int)
            second_chance = UtilitiesFunctions.get_chance(use_magic_int)
            if first_chance == False or second_chance == False: return None #Nếu cả 2 lần không trúng thì không dùng skill
            
            if skill.skill_id == "emperor_stare_skill":
                #chiêu này có 45% tỉ lệ ra đòn nếu phe đối thủ trên 2, dưới 2 thì 15% ra đòn
                #không áp dụng với kẻ địch cũng có chiêu y hệt
                check_same_skill = False
                for s in opponent_alive_attack_info.player_ga.list_skills:
                    if s.skill_id == "emperor_stare_skill":
                        check_same_skill = True
                        break
                if check_same_skill: return None
                chance = 15
                if self_player_info.is_upper_side and len(self.lower_attack_class) >= 2:
                    chance = 45
                elif not self_player_info.is_upper_side and len(self.upper_attack_class) >= 2:
                    chance = 45
                dice = UtilitiesFunctions.get_chance(chance)
                if not dice: return None
                #Xóa hoàn toàn đối thủ khỏi trận đấu
                try:
                    if opponent_alive_attack_info in self.upper_attack_class:
                        self.upper_attack_class.remove(opponent_alive_attack_info)
                    if opponent_alive_attack_info in self.lower_attack_class:
                        self.lower_attack_class.remove(opponent_alive_attack_info)
                except Exception as e:
                    print(f"Exception when ga run away from team due to emperor_stare_skill, {e}")
                #Lưu lại stats lúc đó
                if CustomFunctions.check_if_dev_mode() == False and opponent_alive_attack_info.player_profile != None:
                    if not self.is_players_versus_players and self.is_challenge:
                        ProfileMongoManager.set_guardian_current_stats(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id,stamina=opponent_alive_attack_info.player_ga.stamina, health=opponent_alive_attack_info.player_ga.health, mana=opponent_alive_attack_info.player_ga.mana)
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** đã thể hiện {skill.emoji} -{skill.skill_name} khiến cho kẻ địch [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} khiếp sợ và bỏ trốn khỏi trận chiến!"
                return base_text
            
            #Xem đối thủ có khiên không, có khiên thì coi như self player tấn công thất bại
            shield = self.get_random_skill(list_skills=opponent_alive_attack_info.player_ga.list_skills, skill_id="shield_skill")
            if shield != None and opponent_alive_attack_info.max_shield > 0 and int(opponent_alive_attack_info.player_ga.mana/opponent_alive_attack_info.player_ga.max_mana*100) > shield.percent_min_mana_req:
                #Đối thủ có khiên
                #Trừ stats của self player như bình thường
                own_loss_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss)
                self_player_info.player_ga.mana -= own_loss_mana
                
                opponent_loss_mana = self.calculate_mana_loss_for_guardian(max_mana=opponent_alive_attack_info.player_ga.max_mana, skill_mana_loss=shield.mana_loss, reference_mana=opponent_alive_attack_info.player_ga.mana)
                opponent_alive_attack_info.player_ga.mana -= opponent_loss_mana
                
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã tung chiêu {skill.emoji} - {skill.skill_name} nhưng [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} đã có khiên chắn! **[{self_player_info.player_ga.ga_name}]** đã mất **{own_loss_mana}** mana và [{opponent_alive_attack_info.player_ga.ga_name}] đã mất **{opponent_loss_mana}** mana!"
                #Trừ khiên đối thủ
                opponent_alive_attack_info.max_shield -= 1
                if opponent_alive_attack_info.player_profile != None and mem_chance:
                    ProfileMongoManager.add_memory_guardian(
                        guild_id=self.guild_id,
                        user_id=opponent_alive_attack_info.player_profile.user_id,
                        channel_name=self.channel_name,
                        memory_description=f"{opponent_alive_attack_info.player_ga.ga_name} đã kịp thời dựng Khiên Chấn Thủ để chống lại {self_player_info.player_ga.ga_name}!",
                        tag=GuardianMemoryTag.BATTLE.value
                    )
                return base_text
            
            non_evasion_skills = ["skill_black_fire", "skill_mass_damage", "skill_trade_stats", "skill_potion_destroyer", "skill_explosion_spell", "skill_mass_stun"]
            #Mới: đối thủ được phép né phép thuật bằng stamina
            #Tính tỉ lệ evasion cho đối thủ
            opponent_evasion_chance = self.calculate_chance_by_stats(current_stat=opponent_alive_attack_info.player_ga.stamina, max_stat=opponent_alive_attack_info.player_ga.max_stamina, level=opponent_alive_attack_info.player_ga.level)

            if opponent_evasion_chance > 85: opponent_evasion_chance = 85
            evasion_dice = UtilitiesFunctions.get_chance(opponent_evasion_chance)
            loss_amount = self.calculate_mana_loss_for_guardian(max_mana=opponent_alive_attack_info.player_ga.max_stamina, skill_mana_loss=skill.mana_loss + skill.attack_power, reference_mana=opponent_alive_attack_info.player_ga.stamina)
            if evasion_dice and opponent_alive_attack_info.player_ga.stamina >= loss_amount and skill.skill_id not in non_evasion_skills: #Phải có đủ thể lực cần thiết, và skill không thuộc diện né được thì mới vào
                #Tính lại trừ stamina
                #Hiện tại: 20% stamina + tổng mana_loss và attack_power của skill. 
                loss_amount = int(0.2 * opponent_alive_attack_info.player_ga.max_stamina) + skill.mana_loss + skill.attack_power
                opponent_alive_attack_info.player_ga.stamina -= loss_amount
                if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
                
                #Trừ mana của người thi triển một chút
                own_loss_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                if own_loss_mana < 0:
                    own_loss_mana *= (-1)
                own_loss_mana = int(own_loss_mana*0.85) #giảm tý
                self_player_info.player_ga.mana -= own_loss_mana
                
                base_text = f"- **[{self_player_info.player_ga.ga_emoji} - {self_player_info.player_ga.ga_name}]** {text_own_profile_exist} vận **{own_loss_mana}** mana để tung chiêu {skill.emoji} - {skill.skill_name} nhưng {opponent_alive_attack_info.player_ga.ga_name} đã né kịp, và chỉ mất **{loss_amount}** thể lực!"
                return base_text
            
            #Tuỳ skill mà tung kỹ năng, vì một số skill tấn công có cách tính khác
            if skill.skill_id == "skill_black_fire":
                ap = self_player_info.player_ga.attack_power
                scaling_ap = ap if ap <= 400 else 400 + (ap - 400) * 0.6  # Sau 400 thì giảm nhẹ
                loss_health = int(scaling_ap + scaling_ap * 0.3)
                choice = random.choice([20, 40, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 110, 120])
                min_damage = ap + choice
                if loss_health < min_damage:
                    loss_health = min_damage
                opponent_alive_attack_info.player_ga.health -= loss_health
                #dùng hàm mới để tính toán số mana sẽ mất
                # own_loss_mana = int(self_player_info.player_ga.max_mana * 0.45) - skill.mana_loss
                own_loss_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                if own_loss_mana < 0:
                    own_loss_mana *= (-1)
                self_player_info.player_ga.mana -= own_loss_mana
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã khai chiêu {skill.emoji} - {skill.skill_name} và thiêu đốt mất {loss_health} máu của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}!"
                return base_text
            
            elif skill.skill_id == "skill_stun":
                #tăng stunned_round của kẻ địch
                loss_health = int(skill.attack_power + (self_player_info.player_ga.attack_power*skill.buff_attack_percent/100))
                opponent_alive_attack_info.player_ga.health -= loss_health
                opponent_alive_attack_info.stunned_round += 1
                #trừ mana của người dùng theo tỉ lệ skill
                # loss_own_mana = int(self_player_info.player_ga.max_mana * skill.mana_loss/100) - skill.mana_loss #Không hẳn là trừ quá nhiều, vì thường magic sẽ mạnh hơn, nên buff một tý cho chắc. Để balance sau
                loss_own_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                if loss_own_mana <= 10: loss_own_mana = 20
                self_player_info.player_ga.mana -= loss_own_mana
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã tung chiêu {skill.emoji} - {skill.skill_name} khiến [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} mất {loss_health} máu và mất một lượt!"
                return base_text
            
            elif skill.skill_id == "skill_mass_damage":

                if opponent_alive_attack_info in self.upper_attack_class:
                    for e in self.upper_attack_class:
                        loss_health = int(skill.attack_power + (self_player_info.player_ga.attack_power*skill.buff_attack_percent/100))
                        e.player_ga.health -= loss_health
                else:
                    for e in self.lower_attack_class:
                        loss_health = int(skill.attack_power + (self_player_info.player_ga.attack_power*skill.buff_attack_percent/100))
                        e.player_ga.health -= loss_health

                loss_own_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                if loss_own_mana <= 10: loss_own_mana = 20
                self_player_info.player_ga.mana -= loss_own_mana
                if self_player_info.player_ga.mana <= 0: self_player_info.player_ga.mana = 0
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã triệu hồi {skill.emoji} - {skill.skill_name} để thiêu đốt toàn bộ đội hình phe địch!"
                return base_text
            
            elif skill.skill_id == "skill_drain_vitality":
                #trừ máu của đối thủ
                loss_health = int(skill.attack_power + skill.attack_power*(skill.buff_attack_percent/100) + self_player_info.player_ga.attack_power*0.2)
                opponent_alive_attack_info.player_ga.health -= loss_health
                #hồi máu cho bản thân
                self_player_info.player_ga.health += loss_health
                if self_player_info.player_ga.health > self_player_info.player_ga.max_health: self_player_info.player_ga.health = self_player_info.player_ga.max_health

                own_loss_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                if own_loss_mana < 0:
                    own_loss_mana *= (-1)
                self_player_info.player_ga.mana -= own_loss_mana
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã khai triển chiêu {skill.emoji} - {skill.skill_name} và ăn cắp được {loss_health} máu của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} về cho bản thân!"
                return base_text

            elif skill.skill_id == "skill_mass_stun":
                #tăng stunned_round của tất cả kẻ địch
                if opponent_alive_attack_info in self.upper_attack_class:
                    for e in self.upper_attack_class:
                        e.stunned_round += 1
                else:
                    for e in self.lower_attack_class:
                        e.stunned_round += 1
                #trừ mana của người dùng theo tỉ lệ skill
                loss_own_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                if loss_own_mana <= 10: loss_own_mana = 20
                self_player_info.player_ga.mana -= loss_own_mana
                if self_player_info.player_ga.mana <= 0: self_player_info.player_ga.mana = 0
                
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã khai ấn chiêu {skill.emoji} - {skill.skill_name} khiến toàn bộ phe địch choáng váng và mất lượt!"
                return base_text
            
            elif skill.skill_id == "skill_explosion_spell":
                #trừ % mana + thể lực, dồn vào damage trong một cú
                mana_part = int(self_player_info.player_ga.mana * 0.8)
                stamina_part = int(self_player_info.player_ga.stamina * 0.3)
                loss_health = mana_part + stamina_part
                opponent_alive_attack_info.player_ga.health -= loss_health
                #chiêu này tốn % mana và cả stamina của bản thân
                self_player_info.player_ga.mana -= mana_part
                self_player_info.player_ga.stamina -= stamina_part
                # Clamp to zero
                if self_player_info.player_ga.mana < 0: self_player_info.player_ga.mana = 0
                if self_player_info.player_ga.stamina < 0: self_player_info.player_ga.stamina = 0
                #Tự stun bản thân hai round
                self_player_info.stunned_round += 2
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã tung chiêu {skill.emoji} - {skill.skill_name} cực mạnh, làm nổ tung mất {loss_health} máu của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}!"
                return base_text
            
            elif skill.skill_id == "skill_potion_destroyer" and opponent_alive_attack_info.player_profile != None and opponent_alive_attack_info.player_profile.list_items != None and len(opponent_alive_attack_info.player_profile.list_items) > 0:
                #phá random bình hồi phục nếu có
                filtered_items = [
                    d for d in opponent_alive_attack_info.player_profile.list_items 
                    if d.item_id in ["ga_heal_1", "ga_stamina_1", "ga_mana_1", "ga_all_restored"]
                ]
                if filtered_items != None and len(filtered_items)>0:
                    rand_potion_filtered = copy.deepcopy(random.choice(filtered_items))
                    amount_destroy = random.randint(1,4)
                    if rand_potion_filtered.item_id == "ga_all_restored": amount_destroy = 1
                    #Trừ máu kẻ địch dựa trên kỹ năng
                    loss_health = int(skill.attack_power + (skill.attack_power * skill.buff_attack_percent/100))
                    opponent_alive_attack_info.player_ga.health -= loss_health
                    #trừ mana của người dùng theo tỉ lệ skill
                    loss_own_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                    if loss_own_mana <= 10: loss_own_mana = 20
                    self_player_info.player_ga.mana -= loss_own_mana
                    ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, guild_name="", user_id= opponent_alive_attack_info.player_profile.user_id, user_display_name="", user_name="", item=rand_potion_filtered, amount=-amount_destroy)
                    base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} khiến {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} mất {loss_health} máu và mất x{amount_destroy} [{rand_potion_filtered.item_name}]"
                    return base_text
            
            elif skill.skill_id == "skill_trade_stats":
                #Dùng lượng mana hoặc thể lực của bản thân để phá mana hoặc thể lực của đối thủ
                amount_loss = 0
                choose_mana = UtilitiesFunctions.get_chance(50)
                additional_t = "Thể Lực"
                if choose_mana:
                    amount_loss = self_player_info.player_ga.mana
                    if amount_loss > opponent_alive_attack_info.player_ga.mana: amount_loss = opponent_alive_attack_info.player_ga.mana
                    opponent_alive_attack_info.player_ga.mana -= amount_loss
                    self_player_info.player_ga.mana -= amount_loss
                    additional_t = "Mana"
                else:
                    amount_loss = self_player_info.player_ga.stamina
                    if amount_loss > opponent_alive_attack_info.player_ga.stamina: amount_loss = opponent_alive_attack_info.player_ga.stamina
                    opponent_alive_attack_info.player_ga.stamina -= amount_loss
                    self_player_info.player_ga.stamina -= amount_loss

                #Trừ máu kẻ địch dựa trên kỹ năng
                loss_health = int(skill.attack_power + (skill.attack_power * skill.buff_attack_percent/100))
                if loss_health > opponent_alive_attack_info.player_ga.max_health: 
                    loss_health = opponent_alive_attack_info.player_ga.max_health - 50
                opponent_alive_attack_info.player_ga.health -= loss_health
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} làm mất {loss_health} máu và {amount_loss} {additional_t} của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}!"
                return base_text

            else:
                #Những skill còn lại thì sẽ quy hết vào cách tính tổng sát thương bên dưới
                #trừ máu của đối thủ theo tỉ lệ của skill
                loss_health = int(skill.attack_power + skill.attack_power*(skill.buff_attack_percent/100) + self_player_info.player_ga.attack_power*0.2)
                opponent_alive_attack_info.player_ga.health -= loss_health
                #trừ mana của đối thủ, tỉ lệ thấp hơn, tầm 25% của info.player_ga.attack_power
                loss_mana = int(self_player_info.player_ga.attack_power * 0.25)
                opponent_alive_attack_info.player_ga.mana -= loss_mana
                #trừ mana của người dùng theo tỉ lệ skill
                # loss_own_mana = int(self_player_info.player_ga.max_mana * (skill.mana_loss/100)) - skill.attack_power #Không hẳn là trừ quá nhiều, vì thường magic sẽ mạnh hơn, nên buff một tý cho chắc. Để balance sau
                
                loss_own_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss, reference_mana=self_player_info.player_ga.mana)
                
                if loss_own_mana <= 10: loss_own_mana = 20
                self_player_info.player_ga.mana -= loss_own_mana
                base_text = f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.skill_name} và đánh bay {loss_health} máu và {loss_mana} Mana của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}!"
                return base_text
        return base_text
    
    #region execute_passive_skill
    def execute_passive_skill(self, self_player_info: GuardianAngelAttackClass, opponent_alive_attack_info: GuardianAngelAttackClass, text_target_profile_exist: str, text_own_profile_exist: str):
        mem_chance = UtilitiesFunctions.get_chance(35)
        base_text = None
        allow_summoning_skill = True
        allow_brain_wash_skill = True
        if self.battle_type == "C":
            allow_brain_wash_skill = False #Không dùng chiêu này trong battle C
        elif self.battle_type == "D":
            allow_summoning_skill = False
        elif self.battle_type == "E":
            allow_summoning_skill = False
            allow_brain_wash_skill = False

        is_upper = False
        if self_player_info in self.upper_attack_class:
            is_upper = True
            
        current_mana_percent = int(self_player_info.player_ga.mana/self_player_info.player_ga.max_mana*100)
        current_health_percent = int(self_player_info.player_ga.health/self_player_info.player_ga.max_health*100)
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="summoning_skill")
        if skill != None and current_mana_percent >= 65 and self_player_info.has_used_summoning == False and allow_summoning_skill:
            #Skill này sẽ triệu hồi một NPC vào phe của 
            #Dựa vào is_upper để xác định phe nào sẽ triệu hồi NPC
            #Nếu phe đó tổng GuardianAngelAttackClass dưới ba mới được triệu hồi
            if is_upper:
                if len(self.upper_attack_class) < 3:
                    #Tạo NPC
                    calculated_level= int(self_player_info.player_ga.level/2)
                    roll_chance_legendary = UtilitiesFunctions.get_chance(5)
                    up = random.randint(2, 3)
                    if roll_chance_legendary: calculated_level = self_player_info.player_ga.level*up
                    if calculated_level < 1: calculated_level = 1
                    enemy: GuardianAngel = ListGAAndSkills.get_random_ga_enemy_generic(level=calculated_level)
                    new_enemy = GuardianAngelAttackClass(player_profile=None, player_ga=enemy, starting_at_round=self.round, is_summoned=True)
                    if self_player_info.player_profile != None:
                        new_enemy.summoner_owner_id = self_player_info.player_profile.user_id
                    if is_upper:
                        #Add vào phe attack upper
                        self.upper_attack_class.append(new_enemy)
                    else:
                        #Add vào phe attack lower
                        self.lower_attack_class.append(new_enemy)
                    #Trừ % mana của bản thân
                    own_loss_mana = int(self_player_info.player_ga.max_mana * 0.45) + skill.mana_loss
                    self_player_info.player_ga.mana -= own_loss_mana
                    base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} để triệu hồi **{enemy.ga_emoji} - {enemy.ga_name}** lên gia nhập đội!"
                    self_player_info.has_used_summoning = True
                    #Tạo memory
                    if self_player_info.player_profile != None and roll_chance_legendary:
                        ProfileMongoManager.add_memory_guardian(
                            guild_id=self.guild_id,
                            user_id=self_player_info.player_profile.user_id,
                            channel_name=self.channel_name,
                            memory_description=f"{self_player_info.player_ga.ga_name} đã thực sự triệu hồi được {enemy.ga_name} huyền thoại gia nhập phe",
                            tag=GuardianMemoryTag.BATTLE.value
                        )
                    return base_text
            else:
                if len(self.lower_attack_class) < 3:
                    #Tạo NPC
                    calculated_level= int(self_player_info.player_ga.level/2)
                    roll_chance_legendary = UtilitiesFunctions.get_chance(5)
                    up = random.randint(2, 3)
                    if roll_chance_legendary: calculated_level = self_player_info.player_ga.level*up
                    if calculated_level < 1: calculated_level = 1
                    enemy: GuardianAngel = ListGAAndSkills.get_random_ga_enemy_generic(level=calculated_level)
                    new_enemy = GuardianAngelAttackClass(player_profile=None, player_ga=enemy, starting_at_round=self.round, is_summoned=True)
                    if self_player_info.player_profile != None:
                        new_enemy.summoner_owner_id = self_player_info.player_profile.user_id

                    if is_upper:
                        #Add vào phe attack upper
                        self.upper_attack_class.append(new_enemy)
                    else:
                        #Add vào phe attack lower
                        self.lower_attack_class.append(new_enemy)
                    #Trừ % mana của bản thân
                    own_loss_mana = int(self_player_info.player_ga.max_mana * 0.45) + skill.mana_loss
                    self_player_info.player_ga.mana -= own_loss_mana
                    base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} để triệu hồi **{enemy.ga_emoji} - {enemy.ga_name}** lên gia nhập đội!"
                    self_player_info.has_used_summoning = True
                    #Tạo memory
                    if self_player_info.player_profile != None and roll_chance_legendary:
                        ProfileMongoManager.add_memory_guardian(
                            guild_id=self.guild_id,
                            user_id=self_player_info.player_profile.user_id,
                            channel_name=self.channel_name,
                            memory_description=f"{self_player_info.player_ga.ga_name} đã thực sự triệu hồi được {enemy.ga_name} huyền thoại gia nhập phe",
                            tag=GuardianMemoryTag.BATTLE.value
                        )
                    return base_text
        
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="brain_wash_skill")
        if skill != None and current_mana_percent >= 45 and allow_brain_wash_skill: #Loại C không dùng chiêu này
            #Skill này sẽ tẩy não opponent vào phe của self_player  
            #Dựa vào is_upper để xác định opponent sẽ vào phe nào
            
            self_player_team = self.upper_attack_class if is_upper else self.lower_attack_class
            opponent_team = self.lower_attack_class if is_upper else self.upper_attack_class
            
            #Nếu phe ta tổng GuardianAngelAttackClass dưới ba và phe địch trên hai mới được kích hoạt
            if len(self_player_team) < 3 and len(opponent_team) > 1:
                try:
                    #Xem đối thủ có khiên không, có khiên thì coi như tẩy não thất bại
                    shield = self.get_random_skill(list_skills=opponent_alive_attack_info.player_ga.list_skills, skill_id="shield_skill")
                    if shield != None and opponent_alive_attack_info.max_shield > 0 and int(opponent_alive_attack_info.player_ga.mana/opponent_alive_attack_info.player_ga.max_mana*100) > shield.percent_min_mana_req:
                        #Đối thủ có khiên
                        #Trừ stats của self player như bình thường
                        own_loss_mana = self.calculate_mana_loss_for_guardian(max_mana=self_player_info.player_ga.max_mana, skill_mana_loss=skill.mana_loss)
                        self_player_info.player_ga.mana -= own_loss_mana
                        
                        opponent_loss_mana = self.calculate_mana_loss_for_guardian(max_mana=opponent_alive_attack_info.player_ga.max_mana, skill_mana_loss=shield.mana_loss, reference_mana=opponent_alive_attack_info.player_ga.mana)
                        opponent_alive_attack_info.player_ga.mana -= opponent_loss_mana
                        
                        base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã tung chiêu {skill.emoji} - {skill.skill_name} nhưng [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} đã có khiên chắn! **[{self_player_info.player_ga.ga_name}]** mất **{own_loss_mana}** mana và [{opponent_alive_attack_info.player_ga.ga_name}] đã mất **{opponent_loss_mana}** mana!"
                        #Trừ khiên đối thủ
                        opponent_alive_attack_info.max_shield -= 1
                        #Tạo memory
                        if self_player_info.player_profile != None and mem_chance:
                            ProfileMongoManager.add_memory_guardian(
                                guild_id=self.guild_id,
                                user_id=self_player_info.player_profile.user_id,
                                channel_name=self.channel_name,
                                memory_description=f"{self_player_info.player_ga.ga_name} đã cố tẩy não được kẻ địch {opponent_alive_attack_info.player_ga.ga_name} nhưng bất thành",
                                tag=GuardianMemoryTag.BATTLE.value
                            )
                        if opponent_alive_attack_info.player_profile != None and mem_chance:
                            ProfileMongoManager.add_memory_guardian(
                                guild_id=self.guild_id,
                                user_id=opponent_alive_attack_info.player_profile.user_id,
                                channel_name=self.channel_name,
                                memory_description=f"{opponent_alive_attack_info.player_ga.ga_name} đã có khiên và chống bị kẻ địch {self_player_info.player_ga.ga_name} tẩy não",
                                tag=GuardianMemoryTag.BATTLE.value
                            )
                        return base_text
                    #Không tẩy não người đã bị tẩy não
                    if opponent_alive_attack_info.brain_washed_round == 0:
                        if opponent_alive_attack_info.is_upper_side == False:
                            self.remove_ga_by_player_ga(lst=self.lower_temp_list, target=opponent_alive_attack_info)
                            self.add_ga_by_player_ga(lst=self.upper_temp_list, target=opponent_alive_attack_info)
                        else:
                            self.remove_ga_by_player_ga(lst=self.lower_temp_list, target=opponent_alive_attack_info)
                            self.add_ga_by_player_ga(lst=self.upper_temp_list, target=opponent_alive_attack_info)
                except Exception as e:
                    print(f"Exception when remove brain washed ga from team, {e}")
                opponent_alive_attack_info.brain_washed_round = 4
                opponent_alive_attack_info.stunned_round = 1
                # print(f"{opponent_alive_attack_info.player_ga.ga_name} has been brain washed for 4 rounds!")
                #Trừ % mana của bản thân chiếu theo skill
                own_loss_mana = int(self_player_info.player_ga.max_mana * skill.mana_loss / 100)
                self_player_info.player_ga.mana -= own_loss_mana
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} để tẩy não {opponent_alive_attack_info.player_ga.ga_name} vào đội của mình!"
                
                if self_player_info.player_profile != None and mem_chance:
                    ProfileMongoManager.add_memory_guardian(
                        guild_id=self.guild_id,
                        user_id=self_player_info.player_profile.user_id,
                        channel_name=self.channel_name,
                        memory_description=f"{self_player_info.player_ga.ga_name} đã tẩy não được kẻ địch {opponent_alive_attack_info.player_ga.ga_name} trong lúc giao tranh",
                        tag=GuardianMemoryTag.BATTLE.value
                    )
                if opponent_alive_attack_info.player_profile != None and mem_chance:
                    ProfileMongoManager.add_memory_guardian(
                        guild_id=self.guild_id,
                        user_id=opponent_alive_attack_info.player_profile.user_id,
                        channel_name=self.channel_name,
                        memory_description=f"{opponent_alive_attack_info.player_ga.ga_name} đã bị kẻ địch {opponent_alive_attack_info.player_ga.ga_name} tẩy não trong lúc giao tranh",
                        tag=GuardianMemoryTag.BATTLE.value
                    )
                return base_text
        
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_resurrection")
        if skill != None and current_mana_percent >= 45 and self_player_info.is_used_skill_resurrection == False:
            #Skill này sẽ hồi sinh đồng đội đã chết
            #Dựa vào is_upper để xác định opponent sẽ vào phe nào
            self_player_team = self.upper_attack_class if is_upper else self.lower_attack_class
            opponent_team = self.lower_attack_class if is_upper else self.upper_attack_class
            count_dead_member = 0
            for e in self_player_team:
                if e.player_ga.health <= 0:
                    count_dead_member += 1
            #Chỉ kích hoạt khi có thành viên bỏ mạng
            if count_dead_member >= 1:
                for e in self_player_team:
                    #Hồi phục 35% chỉ số cho phe mình
                    if e.player_ga.health <= 0:
                        e.player_ga.health = int(e.player_ga.max_health*0.3)
                        e.player_ga.stamina = int(e.player_ga.max_stamina*0.3)
                        e.player_ga.mana = int(e.player_ga.max_mana*0.3)
                for e in opponent_team:
                    #Hồi phục 40% máu cho phe địch
                    e.player_ga.health += int(e.player_ga.max_health*0.4)
                    if e.player_ga.health > e.player_ga.max_health: e.player_ga.health = e.player_ga.max_health
            
                #Trừ hết mana của bản thân chiếu theo skill
                self_player_info.player_ga.mana = 0
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã hy sinh mana để dùng chiêu {skill.emoji} - {skill.skill_name} và đưa cả đội của mình từ cõi chết trở về! Kẻ địch đã mạnh hơn"
                self_player_info.is_used_skill_resurrection = True
                if self_player_info.player_profile != None and mem_chance:
                    ProfileMongoManager.add_memory_guardian(
                        guild_id=self.guild_id,
                        user_id=self_player_info.player_profile.user_id,
                        channel_name=self.channel_name,
                        memory_description=f"{self_player_info.player_ga.ga_name} đã hồi sinh {count_dead_member} thành viên trọng thương trong đội",
                        tag=GuardianMemoryTag.BATTLE.value
                    )
                return base_text
        
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="mass_heal_skill")
        if skill != None and current_mana_percent >= skill.percent_min_mana_req and current_health_percent <= 50:
            #Chỉ kích hoạt khi cả máu dưới 50%
            #Hồi phục 15% máu cho cả đội
            if is_upper:
                for info in self.upper_attack_class:
                    additional_health = int(info.player_ga.max_health*0.15)
                    info.player_ga.health += additional_health
                    if info.player_ga.health > info.player_ga.max_health: info.player_ga.health = info.player_ga.max_health
            else:
                for info in self.lower_attack_class:
                    additional_health = int(info.player_ga.max_health*0.15)
                    info.player_ga.health += additional_health
                    if info.player_ga.health > info.player_ga.max_health: info.player_ga.health = info.player_ga.max_health
            #Trừ mana bản thân
            #Trừ % mana của bản thân chiếu theo skill
            own_loss_mana = int(self_player_info.player_ga.max_mana * skill.mana_loss / 100)
            self_player_info.player_ga.mana -= own_loss_mana
            if self_player_info.player_ga.mana <= 0: self_player_info.player_ga.mana = 0
            base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} để hồi phục cho cả đội!"
            if self_player_info.player_profile != None and mem_chance:
                ProfileMongoManager.add_memory_guardian(
                    guild_id=self.guild_id,
                    user_id=self_player_info.player_profile.user_id,
                    channel_name=self.channel_name,
                    memory_description=f"{self_player_info.player_ga.ga_name} đã hồi phục máu cho cả đội mình!",
                    tag=GuardianMemoryTag.BATTLE.value
                )
            return base_text
        
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_summon_sacrifice")
        if skill != None and current_mana_percent >= skill.percent_min_mana_req and self_player_info.max_summon_sacrifice > 0:
            #Tìm xem trong team của player có triệu hồi không, có thì sẽ hiến tế triệu hồi đó
            summon = None
            if is_upper:
                for info in self.upper_attack_class:
                    if info.is_summoned and info != self_player_info:
                        summon = info
                        break
            else:
                for info in self.lower_attack_class:
                    if info.is_summoned and info != self_player_info:
                        summon = info
                        break
            if summon != None:
                #Trừ mana bản thân
                #Trừ % mana của bản thân chiếu theo skill
                own_loss_mana = int(self_player_info.player_ga.max_mana * skill.mana_loss / 100)
                self_player_info.player_ga.mana -= own_loss_mana
                if self_player_info.player_ga.mana <= 0: self_player_info.player_ga.mana = 0

                #Trừ toàn bộ stats của summon, cộng lại 50% vào stats của bản thân
                health_to_add = int(summon.player_ga.health/2)
                stamina_to_add = int(summon.player_ga.stamina/2)
                mana_to_add = int(summon.player_ga.mana/2)
                power_to_add = int(summon.player_ga.attack_power/2)
                self_player_info.player_ga.health += health_to_add
                self_player_info.player_ga.max_health += health_to_add
                self_player_info.player_ga.stamina += stamina_to_add
                self_player_info.player_ga.max_stamina += stamina_to_add
                self_player_info.player_ga.mana += mana_to_add
                self_player_info.player_ga.max_mana += mana_to_add
                self_player_info.player_ga.attack_power += power_to_add

                try:
                    #loại summon khỏi team
                    if summon in self.upper_attack_class:
                        self.upper_attack_class.remove(summon)
                    elif summon in self.lower_attack_class:
                        self.lower_attack_class.remove(summon)
                except Exception as e:
                    print(f"Exception when remove summon sacrifice ga from team, {e}")
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã hiến tế linh hồn triệu hồi {summon.player_ga.ga_name} để tăng sức mạnh của bản thân!"
                #Trừ số lượng hiến tế
                self_player_info.max_summon_sacrifice -= 1
                return base_text
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="mass_restored_mana_skill")
        if skill != None and current_mana_percent <= 25 and self_player_info.max_mass_restored_mana_skill > 0:
            #Chỉ kích hoạt khi cả mana dưới 25%
            #Hồi phục 20% mana cho cả đội
            if is_upper:
                for info in self.upper_attack_class:
                    additional_mana = int(info.player_ga.max_mana*0.2)
                    info.player_ga.mana += additional_mana
                    if info.player_ga.mana > info.player_ga.max_mana: info.player_ga.mana = info.player_ga.max_mana
            else:
                for info in self.lower_attack_class:
                    additional_mana = int(info.player_ga.max_mana*0.2)
                    info.player_ga.mana += additional_mana
                    if info.player_ga.mana > info.player_ga.max_mana: info.player_ga.mana = info.player_ga.max_mana
            #Trừ một lần dùng
            self_player_info.max_mass_restored_mana_skill -= 1
            base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} để hồi phục Mana cho cả đội!"
            if self_player_info.player_profile != None and mem_chance:
                ProfileMongoManager.add_memory_guardian(
                    guild_id=self.guild_id,
                    user_id=self_player_info.player_profile.user_id,
                    channel_name=self.channel_name,
                    memory_description=f"{self_player_info.player_ga.ga_name} đã hồi phục mana cho cả đội mình!",
                    tag=GuardianMemoryTag.BATTLE.value
                )
            return base_text
        
        #Khi mana dưới 50% thì kích hoạt chiêu Bo Kích Huyết nếu có
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_health_sacrifice")
        if skill != None and current_mana_percent >= skill.percent_min_mana_req and current_mana_percent <= 50 and current_health_percent > 10: #Phải có máu trên 10%
            #Dùng skill này sẽ huỷ 5% máu của bản thân, và trừ tất cả máu của cả hai phe, sau đó
            #cộng mana lên tương ứng với lượng máu đã mất
            mana_to_add = 0
            loss_percent = 0.05
            loss_health = int(self_player_info.player_ga.max_health*loss_percent)
            if loss_health < 20: loss_health = 20 #Tối thiểu 20 máu
            self_player_info.player_ga.health -= loss_health
            for e in self.upper_attack_class:
                #skip qua self_player_info
                if e.player_profile != None and self_player_info.player_profile != None and e.player_profile.user_id == self_player_info.player_profile.user_id: continue
                e.player_ga.health -= loss_health
                mana_to_add += loss_health
            for e in self.lower_attack_class:
                #skip qua self_player_info
                if e.player_profile != None and self_player_info.player_profile != None and e.player_profile.user_id == self_player_info.player_profile.user_id: continue
                e.player_ga.health -= loss_health
                mana_to_add += loss_health

            #Cộng mana lên tương ứng với tất cả số lượng máu đã mất
            self_player_info.player_ga.mana += mana_to_add
            #Trừ % mana của bản thân chiếu theo skill
            own_loss_mana = int(self_player_info.player_ga.max_mana * skill.mana_loss / 100)
            self_player_info.player_ga.mana -= own_loss_mana
            base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng {skill.emoji} -{skill.skill_name}, trừ đi **{loss_health}** máu của tất cả mọi người và nhận về **{mana_to_add}** Mana!"
            return base_text
        
        #Khi máu dưới 10% thì kích hoạt chiêu tự kích nếu có
        if current_health_percent <= 10:
            skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_self_explosion")
            if skill != None:
                #Dùng skill này sẽ tự huỷ mọi thứ và gây damage lên toàn bộ người dùng, tốn tất cả mana và stamina, máu
                self_player_info.player_ga.health = 0
                self_player_info.player_ga.mana = 0
                self_player_info.player_ga.stamina = 0
                self.minus_all_reward_percent = 40
                loss_percent = 0.3
                for e in self.upper_attack_class:
                    e.player_ga.health -= int(e.player_ga.max_health*loss_percent)
                    e.player_ga.stamina -= int(e.player_ga.max_health*loss_percent)
                    e.player_ga.mana -= int(e.player_ga.max_health*loss_percent)
                for e in self.lower_attack_class:
                    e.player_ga.health -= int(e.player_ga.max_health*loss_percent)
                    e.player_ga.stamina -= int(e.player_ga.max_health*loss_percent)
                    e.player_ga.mana -= int(e.player_ga.max_health*loss_percent)
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} không còn gì để mất, và quyết định ra đi với chiêu {skill.emoji} -{skill.skill_name} khủng bố khiến mọi người đều dính sát thương!"
                if self_player_info.player_profile != None and mem_chance:
                    ProfileMongoManager.add_memory_guardian(
                        guild_id=self.guild_id,
                        user_id=self_player_info.player_profile.user_id,
                        channel_name=self.channel_name,
                        memory_description=f"{self_player_info.player_ga.ga_name} đã quyết định tự kích nổ bản thân để kéo theo cả bọn xuống mồ cùng mình!",
                        tag=GuardianMemoryTag.BATTLE.value
                    )
                return base_text
            
        #Khi máu dưới 15% thì kích hoạt chiêu chạy trốn nếu có
        if current_health_percent <= 15:
            skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_run_away")
            if skill != None and self_player_info.player_profile != None:
                #Dùng skill này sẽ remove ra khỏi list list attack class ngay lập tức, tốn tất cả mana và stamina
                if CustomFunctions.check_if_dev_mode() == False:
                    ProfileMongoManager.set_guardian_current_stats(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id,stamina=0, health=self_player_info.player_ga.health, mana=0)
                #Kiểm tra trong upper hay lower
                try:
                    if self_player_info in self.upper_attack_class:
                        self.upper_attack_class.remove(self_player_info)
                    if self_player_info in self.lower_attack_class:
                        self.lower_attack_class.remove(self_player_info)
                except Exception as e:
                    print(f"Exception when ga run away from team, {e}")
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} cảm thấy không ổn với trận chiến, và đã dùng chiêu {skill.emoji} -{skill.skill_name} để sủi ngay lập tức!"
                if self_player_info.player_profile != None and mem_chance:
                    ProfileMongoManager.add_memory_guardian(
                        guild_id=self.guild_id,
                        user_id=self_player_info.player_profile.user_id,
                        channel_name=self.channel_name,
                        memory_description=f"{self_player_info.player_ga.ga_name} buộc phải chạy trốn để bảo toàn tính mạng!",
                        tag=GuardianMemoryTag.BATTLE.value
                    )
                return base_text
        
        if current_health_percent <= 30 and self_player_info.is_used_skill_critical_strike == False:
            skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_critical_strike")
            if skill != None:
                #Dùng skill này sẽ lập tức tăng 40% sức tấn công cho user
                self_player_info.player_ga.attack_power += int(self_player_info.player_ga.attack_power * 0.3)
                self_player_info.is_used_skill_critical_strike = True
                #Tăng lại 20% stamina bản thân
                additional_stamina = int(self_player_info.player_ga.max_stamina * 0.2)
                self_player_info.player_ga.stamina += additional_stamina
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} và hoá rồ để tăng sức mạnh tấn công của bản thân!"
                return base_text
    
    #region execute_after_attack_skill
    def execute_after_attack_skill(self, self_player_info: GuardianAngelAttackClass, opponent_alive_attack_info: GuardianAngelAttackClass, text_target_profile_exist: str, text_own_profile_exist: str):
        base_text = None
        is_upper = False
        if self_player_info in self.upper_attack_class:
            is_upper = True
        current_mana_percent = int(self_player_info.player_ga.mana/self_player_info.player_ga.max_mana*100)
        current_mana_percent_opponent = int(opponent_alive_attack_info.player_ga.mana/opponent_alive_attack_info.player_ga.max_mana*100)
        current_health_percent = int(self_player_info.player_ga.health/self_player_info.player_ga.max_health*100)
        current_health_percent_opponent = int(opponent_alive_attack_info.player_ga.health/opponent_alive_attack_info.player_ga.max_health*100)
        skill = self.get_random_skill(list_skills=opponent_alive_attack_info.player_ga.list_skills, skill_id="skill_spike_arnour")
        if skill != None and current_mana_percent_opponent >= skill.percent_min_mana_req:
            #Nếu kẻ địch có kỹ năng này thì self player sẽ bị dính chưởng
            loss_health = int(self_player_info.player_ga.attack_power*0.35)
            self_player_info.player_ga.health -= loss_health
            
            #trừ mana của kẻ địch theo tỉ lệ skill
            loss_own_mana = int(opponent_alive_attack_info.player_ga.max_mana * skill.mana_loss/100) - skill.mana_loss #Không hẳn là trừ quá nhiều, vì thường magic sẽ mạnh hơn, nên buff một tý cho chắc. Để balance sau
            if loss_own_mana <= 10: loss_own_mana = 20
            opponent_alive_attack_info.player_ga.mana -= loss_own_mana
            base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã đánh mất **{loss_health}** Máu của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} nhưng bị phản đòn ngược lại!"
            #Random 10% tăng stun
            stun_chance = UtilitiesFunctions.get_chance(15)
            if stun_chance:
                self_player_info.stunned_round += 1
                base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã đánh mất **{loss_health}** Máu của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} nhưng bị phản đòn ngược lại và bị choáng!"
            return base_text
        
        #Nếu máu đối thủ thấp thì cũng kích hoạt chiêu ngưỡng máu tử luôn
        skill = self.get_random_skill(list_skills=opponent_alive_attack_info.player_ga.list_skills, skill_id="skill_critical_strike")
        if skill != None and current_health_percent_opponent <= 30 and opponent_alive_attack_info.is_used_skill_critical_strike == False:
            #Dùng skill này sẽ lập tức tăng 30% sức tấn công cho đối thủ
            opponent_alive_attack_info.player_ga.attack_power += int(opponent_alive_attack_info.player_ga.attack_power * 0.3)
            opponent_alive_attack_info.is_used_skill_critical_strike = True
            #Tăng lại 20% stamina bản thân
            additional_stamina = int(opponent_alive_attack_info.player_ga.max_stamina * 0.2)
            opponent_alive_attack_info.player_ga.stamina += additional_stamina
            base_text =  f"- **[{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã đánh trúng [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist} và khiến đối thủ hóa rồ để tăng sức mạnh tấn công!"
            return base_text
    
    
    def calculate_mana_loss_for_guardian(self, max_mana: int, skill_mana_loss: int, reference_mana: int = 100) -> int:
        additional_scaling = 2.0
        scaling_factor = (reference_mana / max_mana) * additional_scaling
        effective_mana_loss = skill_mana_loss * scaling_factor
        if max_mana <= reference_mana:
            return int(skill_mana_loss*scaling_factor)
        if max_mana >= 900:
            skill_mana_loss = int(skill_mana_loss * 1.9)
        if max_mana >= 700:
            skill_mana_loss = int(skill_mana_loss * 1.7)
        if max_mana >= 600:
            skill_mana_loss = int(skill_mana_loss * 1.5)
        elif max_mana >= 500:
            skill_mana_loss = int(skill_mana_loss * 1.3)
        return max(skill_mana_loss, min(int(effective_mana_loss), skill_mana_loss * 2))
    
    def remove_ga_by_player_ga(
        self,
        lst: List['GuardianAngelAttackClass'],
        target: GuardianAngelAttackClass
    ) -> GuardianAngelAttackClass | None:
        for i, item in enumerate(lst):
            if item.ga_attack_uid == target.ga_attack_uid:
                removed = lst.pop(i)
                return removed
        return None


    def add_ga_by_player_ga(
        self,
        lst: List['GuardianAngelAttackClass'],
        target: GuardianAngelAttackClass
    ) -> GuardianAngelAttackClass:
        for i, item in enumerate(lst):
            if item.ga_attack_uid == target.ga_attack_uid:
                return item
        lst.append(target)
        return target

    def apply_pending_team_changes(self):
        for ga in self.upper_temp_list:
            self.remove_ga_by_player_ga(self.lower_attack_class, ga)
            self.add_ga_by_player_ga(self.upper_attack_class, ga)

        for ga in self.lower_temp_list:
            self.remove_ga_by_player_ga(self.upper_attack_class, ga)
            self.add_ga_by_player_ga(self.lower_attack_class, ga)

        self.upper_temp_list.clear()
        self.lower_temp_list.clear()

