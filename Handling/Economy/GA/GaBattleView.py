
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


class GaBattleView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member,enemy_ga: GuardianAngel, guild_id: int, is_players_versus_players: bool, target_profile: Profile = None, target: discord.Member = None, allowed_multiple_players: bool = False, max_players:int = 1, embed_title: str = "", gold_reward: int = 0, silver_reward: int= 0, dignity_point: int = 10, bonus_exp: int = 200):
        super().__init__(timeout=180)
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
        elif new_player_profile.guardian == None:
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
        self.lower_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_joined_battle", date_value=datetime.now())
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
            text_own_profile_exist = f"{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level})"
            if self_player_info.player_profile != None:
                text_own_profile_exist = f"Hộ Vệ Thần {self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}** (Cấp {self_player_info.player_ga.level}) của <@{self_player_info.player_profile.user_id}>"
            embed.add_field(name=f"", value=text_own_profile_exist, inline=False)
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
        try:
            await self.message.edit(embed=embed, content=formatted_string)
        except Exception as e:
            await self.message.edit(embed=embed, content=f"Lượt thứ **{self.round}**")
        if flag_end_battle: await self.end_battle()
        else:
            max_limit = 2
            if len(self.upper_attack_class) > 3 or len(self.lower_attack_class) > 3: max_limit = 1
            if self.round > max_limit:
                #Bỏ đi round đầu để tiếp kiệm chỗ
                first_key = list(self.round_number_text_report.keys())[0]
                del self.round_number_text_report[first_key]
            self.round += 1
            await self.commence_battle()
        return
    
    async def end_battle(self):
        print(f"Username {self.user_profile.user_name} has ended guardian battle in guild {self.user_profile.guild_name}!")
        #Tính toán kết quả
        self.battle_ended = True
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
        try:
            await self.message.reply(content=result_text)
            await self.message.edit(view=None)
        except Exception as e:
            print(e)
        #Cập nhật stats cho guardian nếu có profile và đang là PVE
        if self.is_players_versus_players == False:
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
            if calculated_exp > 350: calculated_exp = 350
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
    
    
    def update_stats_in_database(self, info: GuardianAngelAttackClass):
        if info.player_profile != None:
            # loss_health = int(info.player_ga.max_health - info.player_ga.health)
            # loss_stamina = int(info.player_ga.max_stamina - info.player_ga.stamina)
            # loss_mana = int(info.player_ga.max_mana - info.player_ga.mana)
            ProfileMongoManager.set_guardian_current_stats(guild_id=self.guild_id, user_id=info.player_profile.user_id,stamina=info.player_ga.stamina, health=info.player_ga.health, mana=info.player_ga.mana)
    
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
        
        #Tính tỉ lệ hồi máu nếu máu ít hơn 45% và phải có bình máu trong kho đồ
        if self_player_info.player_profile != None and self_player_info.player_ga.health < self_player_info.player_ga.max_health*0.45 and health_potion != None:
            #roll chance 40% dùng bình máu nếu có trong inventory của profile
            use_chance = UtilitiesFunctions.get_chance(40)
            if use_chance:
                #Tuỳ loại bình máu mà hồi theo phần trăm máu, mặc định 30%
                percent_restored= 0.3
                
                heal_amount = int(self_player_info.player_ga.max_health * percent_restored)
                self_player_info.player_ga.health += heal_amount
                if self_player_info.player_ga.health > self_player_info.player_ga.max_health: self_player_info.player_ga.health = self_player_info.player_ga.max_health
                
                base_text = f"- [{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã sử dụng **{health_potion.item_name}** để hồi **{heal_amount}** Máu!"
                
                self_player_info.recovery_time += 1
                #Xóa item khỏi inventory
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, user_name="", guild_name="",user_display_name="", item = health_potion, amount=-1)
                try:
                    self_player_info.player_profile.list_items.remove(health_potion)
                except Exception as e: print()
                return base_text
        
        #Tính tỉ lệ hồi thể lực nếu thể lực ít hơn 30% và phải có bình stamina trong kho đồ
        if self_player_info.player_profile != None and self_player_info.player_ga.stamina < self_player_info.player_ga.max_stamina*0.30 and stamina_potion != None:
            #roll chance 40% dùng bình nếu có trong inventory của profile
            use_chance = UtilitiesFunctions.get_chance(40)
            if use_chance:
                #Tuỳ loại bình mà hồi theo phần trăm, mặc định 50%
                percent_restored= 0.5
                
                heal_amount = int(self_player_info.player_ga.max_stamina * percent_restored)
                self_player_info.player_ga.stamina += heal_amount
                if self_player_info.player_ga.stamina > self_player_info.player_ga.max_stamina: self_player_info.player_ga.stamina = self_player_info.player_ga.max_stamina
                
                base_text = f"- [{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã sử dụng **{stamina_potion.item_name}** để hồi **{heal_amount}** Thể Lực!"
                
                #Xóa item khỏi inventory
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, user_name="", guild_name="",user_display_name="", item = stamina_potion, amount=-1)
                try:
                    self_player_info.player_profile.list_items.remove(stamina_potion)
                except Exception as e: print()
                return base_text
        
        #Tính tỉ lệ hồi mana nếu mana ít hơn 30% và phải có bình mana trong kho đồ
        if self_player_info.player_profile != None and self_player_info.player_ga.mana < self_player_info.player_ga.max_mana*0.30 and mana_potion != None:
            #roll chance 30% dùng bình nếu có trong inventory của profile
            use_chance = UtilitiesFunctions.get_chance(30)
            if use_chance:
                #Tuỳ loại bình mà hồi theo phần trăm, mặc định 40%
                percent_restored= 0.4

                heal_amount = int(self_player_info.player_ga.max_mana * percent_restored)
                self_player_info.player_ga.mana += heal_amount
                if self_player_info.player_ga.mana > self_player_info.player_ga.max_mana: self_player_info.player_ga.mana = self_player_info.player_ga.max_mana

                base_text = f"- [{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã sử dụng **{mana_potion.item_name}** để hồi **{heal_amount}** Mana!"

                #Xóa item khỏi inventory
                ProfileMongoManager.update_list_items_profile(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id, user_name="", guild_name="",user_display_name="", item = mana_potion, amount=-1)
                try:
                    self_player_info.player_profile.list_items.remove(mana_potion)
                except Exception as e: print()
                return base_text

        #Xử lý logic dùng skill nếu có skill trong list
        if self_player_info.player_ga.list_skills != None and len(self_player_info.player_ga.list_skills) > 0:
            #Ưu tiên skill passive trước
            base_passive_text_result = self.execute_passive_skill(self_player_info = self_player_info, opponent_alive_attack_info = opponent_alive_attack_info, text_target_profile_exist=text_target_profile_exist, text_own_profile_exist=text_own_profile_exist)
            if base_passive_text_result != None: return base_passive_text_result
            
            #Đến skill tấn công
            attack_skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_types=["attack"])
            if attack_skill != None: 
                attack_skill
                #Thi triển kỹ năng
                base_text = self.execute_attack_skill(self_player_info = self_player_info, opponent_alive_attack_info = opponent_alive_attack_info, skill=attack_skill, text_target_profile_exist=text_target_profile_exist, text_own_profile_exist=text_own_profile_exist)
                if base_text != None: return base_text
        
        #Tính tỉ lệ evasion
        evasion = int(opponent_alive_attack_info.player_ga.stamina/5)
        if evasion > 100: evasion = 85
        opponent_evasion_chance = self.calculate_evasion_chance(current_stamina=opponent_alive_attack_info.player_ga.stamina, max_stamina=opponent_alive_attack_info.player_ga.max_stamina, level=opponent_alive_attack_info.player_ga.level)
        evasion_dice = UtilitiesFunctions.get_chance(opponent_evasion_chance)
        if evasion_dice:
            #Chỉ trừ stamina của lower, tỉ lệ thấp hơn, tầm 50% của info.player_ga.attack_power
            loss_amount = int(self_player_info.player_ga.attack_power * 0.5)
            opponent_alive_attack_info.player_ga.stamina -= loss_amount
            if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
            base_text = f"- [{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã lao đến đánh {opponent_alive_attack_info.player_ga.ga_name} {text_target_profile_exist} nhưng mục tiêu đã kịp né tránh, và chỉ mất **{loss_amount}** thể lực!"
        else:
            #trừ máu của lower
            loss_health = int(self_player_info.player_ga.attack_power + self_player_info.player_ga.attack_power*(self_player_info.player_ga.buff_attack_percent/100))
            opponent_alive_attack_info.player_ga.health -= loss_health
            #trừ stamina của lower, tỉ lệ thấp hơn, tầm 25% của info.player_ga.attack_power
            loss_amount = int(self_player_info.player_ga.attack_power * 0.25)
            opponent_alive_attack_info.player_ga.stamina -= loss_amount
            if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
            base_text = f"- [{self_player_info.player_ga.ga_emoji} - **{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã đánh trúng [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}! Mục tiêu mất **{loss_health}** Máu và **{loss_amount}** Thể Lực!"
        
        
        additional_loss_stats_text = ""
        if opponent_alive_attack_info.player_ga.health <= 0:
            opponent_alive_attack_info.player_ga.health = 0
            additional_loss_stats_text += f" Mục tiêu đã bị hạ gục!"
        
        #Để đảm bảo stats không bị âm        
        if opponent_alive_attack_info.player_ga.health <= 0: opponent_alive_attack_info.player_ga.health = 0
        if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
        if opponent_alive_attack_info.player_ga.mana <= 0: opponent_alive_attack_info.player_ga.mana = 0
        
        base_text+= additional_loss_stats_text
        
        return base_text
        
    def calculate_evasion_chance(self, current_stamina, max_stamina, level, max_evasion=85, level_bonus=0.5):
        evasion_chance = ((current_stamina / max_stamina) * max_evasion) + (level * level_bonus)
        return int(min(evasion_chance, max_evasion))

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
            legit_skills = [skill for skill in list_skills if skill.skill_type in skill_types]
            if len(legit_skills) == 0: return None
            return random.choice(legit_skills)
        return None

    def execute_attack_skill(self, self_player_info: GuardianAngelAttackClass, opponent_alive_attack_info: GuardianAngelAttackClass, skill: GuardianAngelSkill, text_target_profile_exist: str, text_own_profile_exist: str):
        base_text = None
        #Mana của bản thân phải lớn hơn hoặc bằng mana yêu cầu của skill
        current_mana_percent = int(self_player_info.player_ga.mana/self_player_info.player_ga.max_mana*100)
        if current_mana_percent >= skill.percent_min_mana_req:
            #roll chance dùng skill
            use_magic_int = self.calculate_evasion_chance(current_stamina=self_player_info.player_ga.mana, max_stamina=self_player_info.player_ga.max_mana, level=opponent_alive_attack_info.player_ga.level)
            first_chance = UtilitiesFunctions.get_chance(use_magic_int)
            second_chance = UtilitiesFunctions.get_chance(use_magic_int)
            if first_chance == False or second_chance == False: return None #Nếu cả 2 lần không trúng thì không dùng skill

            #Tuỳ skill mà tung kỹ năng, vì một số skill tấn công có cách tính khác
            if skill.skill_id == "skill_black_fire":
                #trừ máu của đối theo attack power của profile nhân với buff attack percent của skill
                loss_health = int(self_player_info.player_ga.attack_power + self_player_info.player_ga.attack_power*(skill.buff_attack_percent/100))
                opponent_alive_attack_info.player_ga.health -= loss_health
                if opponent_alive_attack_info.player_ga.health <= 0: opponent_alive_attack_info.player_ga.health = 0
                
                #chiêu này tốn 45% mana của bản thân
                own_loss_mana = int(self_player_info.player_ga.max_mana * 0.45)
                self_player_info.player_ga.mana -= own_loss_mana
                if self_player_info.player_ga.mana <= 0: self_player_info.player_ga.mana = 0
                
                base_text =  f"- [**{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã khai chiêu {skill.emoji} - {skill.skill_name} và thiêu đốt mất {loss_health} máu của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}!"
                return base_text
                
            else: #Những skill còn lại thì sẽ quy hết vào cách tính tổng sát thương bên dưới
                #trừ máu của đối thủ theo tỉ lệ của skill
                loss_health = int(skill.attack_power + skill.attack_power*(skill.buff_attack_percent/100))
                opponent_alive_attack_info.player_ga.health -= loss_health
                if opponent_alive_attack_info.player_ga.health <= 0: opponent_alive_attack_info.player_ga.health = 0
                #trừ mana của đối thủ, tỉ lệ thấp hơn, tầm 25% của info.player_ga.attack_power
                loss_mana = int(self_player_info.player_ga.attack_power * 0.25)
                opponent_alive_attack_info.player_ga.mana -= loss_mana
                if opponent_alive_attack_info.player_ga.mana <= 0: opponent_alive_attack_info.player_ga.mana = 0
                
                #trừ mana của người dùng theo tỉ lệ skill
                loss_own_mana = int(self_player_info.player_ga.max_mana * (skill.mana_loss/100)) - skill.attack_power #Không hẳn là trừ quá nhiều, vì thường magic sẽ mạnh hơn, nên buff một tý cho chắc. Để balance sau
                if loss_own_mana <= 10: loss_own_mana = 20
                self_player_info.player_ga.mana -= loss_own_mana
                
                base_text =  f"- [**{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.skill_name} và đánh bay {loss_health} máu và {loss_mana} Mana của [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}!"
        return base_text
    
    def execute_passive_skill(self, self_player_info: GuardianAngelAttackClass, opponent_alive_attack_info: GuardianAngelAttackClass, text_target_profile_exist: str, text_own_profile_exist: str):
        base_text = None
        
        current_mana_percent = int(self_player_info.player_ga.mana/self_player_info.player_ga.max_mana*100)
        skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="summoning_skill")
        if skill != None and current_mana_percent >= 50:
            #Skill này sẽ triệu hồi một NPC vào phe của 
            is_upper = False
            if self_player_info in self.upper_attack_class:
                is_upper = True
            
            #Dựa vào is_upper để xác định phe nào sẽ triệu hồi NPC
            #Nếu phe đó tổng GuardianAngelAttackClass dưới ba mới được triệu hồi
            if is_upper:
                if len(self.upper_attack_class) < 3:
                    #Tạo NPC
                    calculated_level= int(self_player_info.player_ga.level/2)
                    roll_chance_legendary = UtilitiesFunctions.get_chance(5)
                    if roll_chance_legendary: calculated_level = self_player_info.player_ga.level*2
                    if calculated_level < 1: calculated_level = 1
                    enemy: GuardianAngel = ListGAAndSkills.get_random_ga_enemy_generic(level=calculated_level)
                    new_enemy = GuardianAngelAttackClass(player_profile=None, player_ga=enemy, starting_at_round=self.round)
                    if is_upper:
                        #Add vào phe attack upper
                        self.upper_attack_class.append(new_enemy)
                    else:
                        #Add vào phe attack lower
                        self.lower_attack_class.append(new_enemy)
                    #Trừ 50% mana của bản thân
                    own_loss_mana = int(self_player_info.player_ga.max_mana * 0.50)
                    self_player_info.player_ga.mana -= own_loss_mana
                    if self_player_info.player_ga.mana <= 0: self_player_info.player_ga.mana = 0
                    
                    base_text =  f"- [**{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} để triệu hồi **{enemy.ga_emoji} - {enemy.ga_name}** lên gia nhập đội!"
                    return base_text
            else:
                if len(self.lower_attack_class) < 3:
                    #Tạo NPC
                    calculated_level= int(self_player_info.player_ga.level/2)
                    roll_chance_legendary = UtilitiesFunctions.get_chance(10)
                    if roll_chance_legendary: calculated_level = self_player_info.player_ga.level*3
                    if calculated_level < 1: calculated_level = 1
                    enemy: GuardianAngel = ListGAAndSkills.get_random_ga_enemy_generic(level=calculated_level)
                    new_enemy = GuardianAngelAttackClass(player_profile=None, player_ga=enemy, starting_at_round=self.round)
                    if is_upper:
                        #Add vào phe attack upper
                        self.upper_attack_class.append(new_enemy)
                    else:
                        #Add vào phe attack lower
                        self.lower_attack_class.append(new_enemy)
                    #Trừ 50% mana của bản thân
                    own_loss_mana = int(self_player_info.player_ga.max_mana * 0.50)
                    self_player_info.player_ga.mana -= own_loss_mana
                    if self_player_info.player_ga.mana <= 0: self_player_info.player_ga.mana = 0
                    
                    base_text =  f"- [**{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} để triệu hồi **{enemy.ga_emoji} - {enemy.ga_name}** lên gia nhập đội!"
                    return base_text
        
        #Khi máu dưới 15% thì kích hoạt chiêu chạy trốn nếu có
        current_health_percent = int(self_player_info.player_ga.health/self_player_info.player_ga.max_health*100)
        if current_health_percent <= 15:
            skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_run_away")
            if skill != None:
                #Dùng skill này sẽ remove ra khỏi list list attack class ngay lập tức, tốn tất cả mana và stamina
                ProfileMongoManager.set_guardian_current_stats(guild_id=self.guild_id, user_id=self_player_info.player_profile.user_id,stamina=0, health=self_player_info.player_ga.health, mana=0)
                #Kiểm tra trong upper hay lower
                if self_player_info in self.upper_attack_class:
                    self.upper_attack_class.remove(self_player_info)
                if self_player_info in self.lower_attack_class:
                    self.lower_attack_class.remove(self_player_info)
                base_text =  f"- [**{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} cảm thấy không ổn với trận chiến, và đã dùng chiêu {skill.emoji} -{skill.skill_name} để sủi ngay lập tức!"
                return base_text
        
        if current_health_percent <= 25 and self_player_info.is_used_skill_critical_strike == False:
            skill = self.get_random_skill(list_skills=self_player_info.player_ga.list_skills, skill_id="skill_critical_strike")
            if skill != None:
                #Dùng skill này sẽ lập tức tăng 25% sức tấn công cho user
                self_player_info.player_ga.attack_power += int(self_player_info.player_ga.attack_power * 0.25)
                self_player_info.is_used_skill_critical_strike = True
                base_text =  f"- [**{self_player_info.player_ga.ga_name}]** {text_own_profile_exist} đã dùng chiêu {skill.emoji} - {skill.skill_name} và hoá rồ để tăng 25% sức mạnh tấn công của bản thân!"
                return base_text
        
        
            
        
        