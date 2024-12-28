
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

class GaBattleView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member,enemy_ga: GuardianAngel, is_players_versus_players: bool, target_profile: Profile = None, target: discord.Member = None, allowed_multiple_players: bool = False, max_players:int = 1, embed_title: str = ""):
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
        
        if allowed_multiple_players:
            self.joined_allied_button = discord.ui.Button(label="Gia Nhập Phe Trên", style=discord.ButtonStyle.primary)
            self.joined_allied_button.callback = self.joined_allied_button_event
            self.add_item(self.joined_allied_button)
            
            self.joined_target_button = discord.ui.Button(label="Gia Nhập Phe Dưới", style=discord.ButtonStyle.red)
            self.joined_target_button.callback = self.joined_target_button_event
            self.add_item(self.joined_target_button)
        else:
            self.joined_fight_button = discord.ui.Button(label="⚔️ Chiến Đấu", style=discord.ButtonStyle.green)
            self.joined_fight_button.callback = self.joined_the_fight_button_event
            self.add_item(self.joined_fight_button)
            
        if is_players_versus_players:
            first_player_class = GuardianAngelAttackClass(player_profile=user_profile, player_ga=user_profile.guardian)
            self.upper_attack_class.append(first_player_class)
            second_player_class = GuardianAngelAttackClass(player_profile=target_profile, player_ga=target_profile.guardian)
            self.lower_attack_class.append(second_player_class)
            self.joined_player_id.append(user.id)
            self.joined_player_id.append(target.id)
        else:
            first_player_class = GuardianAngelAttackClass(player_profile=user_profile, player_ga=user_profile.guardian)
            self.upper_attack_class.append(first_player_class)
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
        #upper attack sẽ đánh trước
        full_text = ""
        for info in self.upper_attack_class:
            #Skip qua guardian đã chết
            if info.player_ga.health <= 0: continue
            #Mỗi guardian trong upper sẽ chọn ngẫu nhiên một lower để đánh
            opponent_alive_attack_info = self.get_ga_stil_alive("lower")
            if opponent_alive_attack_info == None:
                #phe trên đã thua, kết thúc trận chiến
                await self.end_battle()
                return
            #Chỉ để check xem profile của đối thủ có hay không
            text_target_profile_exist = ""
            if opponent_alive_attack_info.player_profile != None:
                text_target_profile_exist = f"của <@{opponent_alive_attack_info.player_profile.user_id}>"
            #Chỉ để check xem profile của bản thân có hay không
            text_own_profile_exist = ""
            if info.player_profile != None:
                text_own_profile_exist = f"của <@{info.player_profile.user_id}>"
                
            #Tính tỉ lệ evasion
            base_text = f"[{info.player_ga.ga_emoji} - **{info.player_ga.ga_name}]** {text_own_profile_exist} đã lao đến đánh [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}"
            evasion = int(opponent_alive_attack_info.player_ga.stamina/10)
            if evasion > 100: evasion = 90
            evasion_chance = UtilitiesFunctions.get_chance(evasion)
            if evasion_chance:
                #Chỉ trừ stamina của lower, tỉ lệ thấp hơn, tầm 50% của info.player_ga.attack_power
                loss_amount = int(info.player_ga.attack_power * 0.5)
                opponent_alive_attack_info.player_ga.stamina -= loss_amount
                
                base_text += f"nhưng mục tiêu đã kịp né tránh! Mục tiêu chỉ mất **{loss_amount}** thể lực!"
            else:
                #trừ máu của lower
                loss_health = int(info.player_ga.attack_power*info.player_ga.buff_attack_percent)
                opponent_alive_attack_info.player_ga.health -= loss_health
                #trừ stamina của lower, tỉ lệ thấp hơn, tầm 10% của info.player_ga.attack_power
                loss_amount = int(info.player_ga.attack_power * 0.25)
                opponent_alive_attack_info.player_ga.stamina -= loss_amount
                base_text += f"và mục tiêu đã dính đòn! Mục tiêu mất **{loss_health}** Máu và **{loss_amount}** thể lực!"
                
                if opponent_alive_attack_info.player_ga.health <= 0: opponent_alive_attack_info.player_ga.health = 0
                if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
                if opponent_alive_attack_info.player_ga.mana <= 0: opponent_alive_attack_info.player_ga.mana = 0
            full_text += base_text + "\n"
            
        #tới lượt của phe lower
        for info in self.lower_attack_class:
            #Skip qua guardian đã chết
            if info.player_ga.health <= 0: continue
            
            #Mỗi guardian trong lower sẽ chọn ngẫu nhiên một upper để đánh
            opponent_alive_attack_info = self.get_ga_stil_alive("upper")
            if opponent_alive_attack_info == None:
                #phe dưới đã thua, kết thúc trận chiến
                await self.end_battle()
                return
            #Chỉ để check xem profile của đối thủ có hay không
            text_target_profile_exist = ""
            if opponent_alive_attack_info.player_profile != None:
                text_target_profile_exist = f"của <@{opponent_alive_attack_info.player_profile.user_id}>"
            #Chỉ để check xem profile của bản thân có hay không
            text_own_profile_exist = ""
            if info.player_profile != None:
                text_own_profile_exist = f"của <@{info.player_profile.user_id}>"
                
            #Tính tỉ lệ evasion
            base_text = f"[{info.player_ga.ga_emoji} - **{info.player_ga.ga_name}]** {text_own_profile_exist} đã lao đến đánh [{opponent_alive_attack_info.player_ga.ga_emoji} - {opponent_alive_attack_info.player_ga.ga_name}] {text_target_profile_exist}"
            evasion = int(opponent_alive_attack_info.player_ga.stamina/10)
            if evasion > 100: evasion = 90
            evasion_chance = UtilitiesFunctions.get_chance(evasion)
            if evasion_chance:
                #Chỉ trừ stamina của lower, tỉ lệ thấp hơn, tầm 50% của info.player_ga.attack_power
                loss_amount = int(info.player_ga.attack_power * 0.5)
                opponent_alive_attack_info.player_ga.stamina -= loss_amount
                base_text += f"nhưng mục tiêu đã kịp né tránh! Mục tiêu chỉ mất **{loss_amount}** thể lực!"
            else:
                #trừ máu của lower
                loss_health = int(info.player_ga.attack_power*info.player_ga.buff_attack_percent)
                opponent_alive_attack_info.player_ga.health -= loss_health
                
                #trừ stamina của lower, tỉ lệ thấp hơn, tầm 10% của info.player_ga.attack_power
                loss_amount = int(info.player_ga.attack_power * 0.25)
                opponent_alive_attack_info.player_ga.stamina -= loss_amount
                base_text += f"và mục tiêu đã dính đòn! Mục tiêu mất **{loss_health}** Máu và **{loss_amount}** thể lực!"
                if opponent_alive_attack_info.player_ga.health <= 0: opponent_alive_attack_info.player_ga.health = 0
                if opponent_alive_attack_info.player_ga.stamina <= 0: opponent_alive_attack_info.player_ga.stamina = 0
                if opponent_alive_attack_info.player_ga.mana <= 0: opponent_alive_attack_info.player_ga.mana = 0
                
            full_text += base_text + "\n"
        
        self.round_number_text_report.update({self.round: full_text})
        self.round += 1
        
        if self.round > 10:
            #Bỏ đi round đầu để tiếp kiệm chỗ
            self.round_number_text_report.pop(0)
        
        await asyncio.sleep(3)
        
        #Cập nhật embed chiến đấu
        embed = discord.Embed(title=f"", description=self.embed_title, color=0x0ce7f2)
        for info in self.upper_attack_class:
            embed.add_field(name=f"", value=f"Hộ Vệ Thần {info.player_ga.ga_emoji} - **{info.player_ga.ga_name}** (Cấp {info.player_ga.level}) của <@{info.player_profile.user_id}>", inline=False)
            embed.add_field(name=f"", value=f"🦾: **{info.player_ga.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=info.player_ga.health, max_value=info.player_ga.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=info.player_ga.stamina, max_value=info.player_ga.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=info.player_ga.mana, max_value=info.player_ga.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        for info in self.lower_attack_class:
            text_target_profile_exist = f"Kẻ Thù {info.player_ga.ga_emoji} - **{info.player_ga.ga_name}** (Cấp {info.player_ga.level})"
            if info.player_profile != None:
                text_target_profile_exist = f"Hộ Vệ Thần {info.player_ga.ga_emoji} - **{info.player_ga.ga_name}** (Cấp {info.player_ga.level}) của <@{info.player_profile.user_id}>"
            embed.add_field(name=f"", value=text_target_profile_exist, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{info.player_ga.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=info.player_ga.health, max_value=info.player_ga.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=info.player_ga.stamina, max_value=info.player_ga.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=info.player_ga.mana, max_value=info.player_ga.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        
        formatted_string = "\n".join(f"Lượt thứ **{key}**.\n{value}\n" for key, value in self.round_number_text_report.items())
        await self.message.edit(embed=embed, content=f"Lượt thứ **{self.round}**")
        await self.commence_battle()
        return
    
    async def end_battle(self):
        #Tính toán kết quả
        return
    
    def get_ga_stil_alive(self, side: str):
        if side == "upper":
            legit_attack_classes = [attack_class for attack_class in self.upper_attack_class if attack_class.player_ga.health > 0]
            if len(legit_attack_classes) == 0: return None
            return random.choice(legit_attack_classes)
        else:
            legit_attack_classes = [attack_class for attack_class in self.lower_attack_class if attack_class.player_ga.health > 0]
            if len(legit_attack_classes) == 0: return None
            return random.choice(legit_attack_classes)

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
        
        data = GuardianAngelAttackClass(player_profile=new_player_profile, player_ga=new_player_profile.guardian)
        self.upper_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
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
        
        data = GuardianAngelAttackClass(player_profile=new_player_profile, player_ga=new_player_profile.guardian)
        self.lower_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
        
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
        
        data = GuardianAngelAttackClass(player_profile=new_player_profile, player_ga=new_player_profile.guardian)
        self.upper_attack_class.append(data)
        self.joined_player_id.append(interaction.user.id)
        
        return