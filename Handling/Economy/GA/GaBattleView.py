
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

class GaBattleView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member,enemy_ga: GuardianAngel, guild_id: int, is_players_versus_players: bool, target_profile: Profile = None, target: discord.Member = None, allowed_multiple_players: bool = False, max_players:int = 1, embed_title: str = "", gold_reward: int = 0, silver_reward: int= 0, dignity_point: int = 10, bonus_exp: int = 200):
        super().__init__(timeout=300)
        self.message : discord.Message = None
        self.user: discord.Member = user
        self.target: discord.Member = target
        self.user_profile = user_profile
        self.target_profile = target_profile
        self.enemy_ga = enemy_ga
        self.allowed_multiple_players = allowed_multiple_players
        self.max_players = max_players
        self.is_players_versus_players = is_players_versus_players
        
        self.upper_attack_class: List['GuardianAngelAttackClass'] = []
        self.lower_attack_class: List['GuardianAngelAttackClass'] = []
        
        self.round_number_text_report = {}
        self.round = 1
        self.text = ""
        self.embed_title = embed_title
        self.joined_player_id : List[int]= []
        
        self.upper_attack_won = False
        self.dignity_point = dignity_point
        self.gold_reward = gold_reward
        self.silver_reward = silver_reward
        self.bonus_exp = bonus_exp
        
        self.guild_id = guild_id
        
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
        
            
    async def on_timeout(self):
        #Delete
        if self.message != None: 
            await self.message.edit(view= None)
            return


    #region battle event
    async def commence_battle(self):
        if len(self.upper_attack_class) == 0 or len(self.lower_attack_class) == 0: return
        await asyncio.sleep(3)
        
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
        
        if not self.is_empty_or_whitespace(full_text):
            self.round_number_text_report.update({self.round: full_text.strip()})
        
        #Cập nhật embed chiến đấu
        embed = discord.Embed(title=f"", description=self.embed_title, color=0x0ce7f2)
        for self_player_info in self.upper_attack_class:
            embed.add_field(name=f"", value=f"Hộ Vệ Thần {self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level}) của <@{self_player_info.player_profile.user_id}>", inline=False)
            embed.add_field(name=f"", value=f"🦾: **{self_player_info.player_ga.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.health, max_value=self_player_info.player_ga.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.stamina, max_value=self_player_info.player_ga.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.mana, max_value=self_player_info.player_ga.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        for self_player_info in self.lower_attack_class:
            text_target_profile_exist = f"Kẻ Thù {self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level})"
            if self_player_info.player_profile != None:
                text_target_profile_exist = f"Hộ Vệ Thần {self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level}) của <@{self_player_info.player_profile.user_id}>"
            embed.add_field(name=f"", value=text_target_profile_exist, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{self_player_info.player_ga.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.health, max_value=self_player_info.player_ga.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.stamina, max_value=self_player_info.player_ga.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=self_player_info.player_ga.mana, max_value=self_player_info.player_ga.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        
        formatted_string = "\n".join(f"Lượt thứ **{key}**.\n{value}\n" for key, value in self.round_number_text_report.items())
        # await self.message.edit(embed=embed, content=f"Lượt thứ **{self.round}**")
        await self.message.edit(embed=embed, content=formatted_string)
        if flag_end_battle: await self.end_battle()
        else:
            if self.round > 4:
                #Bỏ đi round đầu để tiếp kiệm chỗ
                first_key = list(self.round_number_text_report.keys())[0]
                del self.round_number_text_report[first_key]
            self.round += 1
            await self.commence_battle()
        return
    
    async def end_battle(self):
        #Tính toán kết quả
        
        result_text = "**Tổng Kết Chiến Đấu**\n"
        if self.upper_attack_won:
            result_text += f"Phe trên đã chiến thắng!\n▬▬▬ι════>\n"
            for info in self.upper_attack_class:
                additional_stats = self.get_result_addition_stats(info)
                result_text += additional_stats
                
        else:
            result_text += f"Phe dưới đã chiến thắng!\n"
            for info in self.lower_attack_class:
                additional_stats = self.get_result_addition_stats(info)
                result_text += additional_stats
        result_text += f"▬▬▬ι════>\nPhe thua quá gà, chẳng xứng đáng nhận gì hết!"
        await self.message.reply(content=result_text)
        return
    
    
    def calculate_contribution(self, entry_turn):
        if entry_turn > self.round:
            return 0
        turns_participated = self.round - entry_turn + 1
        contribution_percentage = int(turns_participated / self.round) * 100
        return contribution_percentage
    
    def is_empty_or_whitespace(self, s: str):
        return not s.strip()
    
    def get_result_addition_stats(self, info: GuardianAngelAttackClass):
        if info.player_profile == None: return ""
        #Nhân theo lượng người tham gia
        bonus_exp = int(self.bonus_exp * len(self.upper_attack_class) + self.bonus_exp*len(self.lower_attack_class))
        gold_reward = int(self.gold_reward * len(self.upper_attack_class) + self.bonus_exp*len(self.lower_attack_class))
        silver_reward = int(self.silver_reward * len(self.upper_attack_class) + self.bonus_exp*len(self.lower_attack_class))
        contribution = self.calculate_contribution(info.starting_at_round)
        
        text_target_profile_exist = f"<@{info.player_profile.user_id}> [{info.starting_at_round}] cống hiến **{contribution}%**, nhận: "
        calculated_exp = int(bonus_exp * (contribution / 100))
        if calculated_exp > 0: 
            text_target_profile_exist += f"**{calculated_exp}** EXP. "
            ProfileMongoManager.update_level_progressing(guild_id=self.guild_id, user_id=info.player_profile.user_id, bonus_exp=int(calculated_exp*0.3))
            ProfileMongoManager.update_main_guardian_level_progressing(guild_id=self.guild_id, user_id=info.player_profile.user_id, bonus_exp=calculated_exp)
        
        calculated_gold_reward = int(gold_reward * (contribution / 100))
        if calculated_gold_reward > 0:
            text_target_profile_exist += f"**{calculated_gold_reward}** {EmojiCreation2.GOLD.value}. "
        
        calculated_silver_reward = int(silver_reward * (contribution / 100))
        if calculated_silver_reward > 0:
            text_target_profile_exist += f"**{calculated_silver_reward}** {EmojiCreation2.SILVER.value}. "
        
        ProfileMongoManager.update_profile_money(guild_id=self.guild_id, user_id=info.player_profile.user_id, guild_name="",user_display_name="", user_name="", gold=calculated_gold_reward, silver=calculated_silver_reward)
        
        if self.dignity_point > 0:
            text_target_profile_exist += f"**{self.dignity_point}** Nhân phẩm. "
            ProfileMongoManager.update_dignity_point(guild_id=self.guild_id, user_id=info.player_profile.user_id, guild_name="",user_display_name="", user_name="", dignity_point=self.dignity_point)
        text_target_profile_exist += "\n"
        return text_target_profile_exist
    
    
    
    
    def get_ga_stil_alive(self, side: str):
        if side == "upper":
            legit_attack_classes = [attack_class for attack_class in self.upper_attack_class if attack_class.player_ga.health > 0]
            if len(legit_attack_classes) == 0: return None
            return random.choice(legit_attack_classes)
        else:
            legit_attack_classes = [attack_class for attack_class in self.lower_attack_class if attack_class.player_ga.health > 0]
            if len(legit_attack_classes) == 0: return None
            return random.choice(legit_attack_classes)

    def execute_attack(self, self_player_info: GuardianAngelAttackClass, opponent_alive_attack_info: GuardianAngelAttackClass):
        #Chỉ để check xem profile của đối thủ có hay không
        text_target_profile_exist = ""
        if opponent_alive_attack_info.player_profile != None:
            text_target_profile_exist = f"của <@{opponent_alive_attack_info.player_profile.user_id}>"
        #Chỉ để check xem profile của bản thân có hay không
        text_own_profile_exist = ""
        if self_player_info.player_profile != None:
            text_own_profile_exist = f"của <@{self_player_info.player_profile.user_id}>"
        #Tính tỉ lệ evasion
        base_text = f"[{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã lao đến đánh [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}"
        evasion = int(opponent_alive_attack_info.player_ga.stamina/5)
        if evasion > 100: evasion = 85
        
        opponent_evasion_chance = self.calculate_evasion_chance(current_stamina=opponent_alive_attack_info.player_ga.stamina, max_stamina=opponent_alive_attack_info.player_ga.max_stamina, level=opponent_alive_attack_info.player_ga.level)
        evasion_dice = UtilitiesFunctions.get_chance(opponent_evasion_chance)
        if evasion_dice:
            #Chỉ trừ stamina của lower, tỉ lệ thấp hơn, tầm 50% của info.player_ga.attack_power
            loss_amount = int(self_player_info.player_ga.attack_power * 0.5)
            opponent_alive_attack_info.player_ga.stamina -= loss_amount
            base_text += f"nhưng mục tiêu đã kịp né tránh! Mục tiêu mất **{loss_amount}** thể lực!"
            #Nếu là player vs npc thì lưu lại
            if self.is_players_versus_players == False and opponent_alive_attack_info.player_profile!= None:
                ProfileMongoManager.update_guardian_stats(guild_id=self.guild_id, user_id=opponent_alive_attack_info.player_profile.user_id,stamina=-loss_amount)
        else:
            #trừ máu của lower
            loss_health = int(self_player_info.player_ga.attack_power + self_player_info.player_ga.attack_power*(self_player_info.player_ga.buff_attack_percent/100))
            opponent_alive_attack_info.player_ga.health -= loss_health
            #trừ stamina của lower, tỉ lệ thấp hơn, tầm 10% của info.player_ga.attack_power
            loss_amount = int(self_player_info.player_ga.attack_power * 0.25)
            opponent_alive_attack_info.player_ga.stamina -= loss_amount
            base_text += f"và mục tiêu đã dính đòn! Mục tiêu mất **{loss_health}** Máu và **{loss_amount}** thể lực!"
            
            additional_loss_stats_text = ""
            if opponent_alive_attack_info.player_ga.health <= 0:
                opponent_alive_attack_info.player_ga.health = 0
                additional_loss_stats_text += f" Mục tiêu đã bị hạ gục!"
            
            if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
            if opponent_alive_attack_info.player_ga.mana <= 0: opponent_alive_attack_info.player_ga.mana = 0
            
            if self.is_players_versus_players == False and opponent_alive_attack_info.player_profile!= None:
                ProfileMongoManager.update_guardian_stats(guild_id=self.guild_id, user_id=opponent_alive_attack_info.player_profile.user_id,stamina=-loss_amount, health=-loss_health)
            
            base_text+= additional_loss_stats_text
        
        return base_text
        
    def calculate_evasion_chance(self, current_stamina, max_stamina, level, max_evasion=85, level_bonus=0.5):
        evasion_chance = ((current_stamina / max_stamina) * max_evasion) + (level * level_bonus)
        return int(min(evasion_chance, max_evasion))

    
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
        elif new_player_profile.guardian == None:
            await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True)
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
        elif new_player_profile.guardian == None:
            await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True)
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
        self.lower_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
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
        elif new_player_profile.guardian == None:
            await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True)
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
        return