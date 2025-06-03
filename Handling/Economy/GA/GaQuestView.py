import copy
import re
import discord
from Handling.Economy.GA.GaQuestClass import GuardianAngelQuest, GuardianQuestLines, NextSteps
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from datetime import datetime, timedelta
import random
import CustomFunctions
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_small_copper_fish,list_gold_fish, list_silver_fish, list_gift_items, list_trash, list_plant, list_legend_weapon_1, list_legend_weapon_2, list_support_ga_items, list_protection_items,list_attack_items,list_support_items

class GaQuestView(discord.ui.View):
    def __init__(self, user: discord.Member, guardian_quest: GuardianAngelQuest, current_quest_lines: GuardianQuestLines, override_title: str, channel: discord.TextChannel, total_dignity = 0, total_gold = 0, total_silver = 0, total_ga_exp = 0, total_ga_hp = 0, total_ga_mana = 0, total_ga_stamina = 0, force_injury = False, force_dead = False):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.guardian_quest = guardian_quest
        self.current_quest_lines = current_quest_lines
        self.user = user
        self.override_title = override_title
        self.not_choose = True
        self.total_dignity = total_dignity
        self.total_gold = total_gold
        self.total_silver = total_silver
        self.total_ga_exp = total_ga_exp
        self.total_ga_hp = total_ga_hp
        self.total_ga_mana = total_ga_mana
        self.total_ga_stamina = total_ga_stamina
        self.channel = channel
        self.force_injury = force_injury
        self.force_dead = force_dead
        
        if current_quest_lines.choice_a and current_quest_lines.choice_a.strip() != "":
            self.choice_a_button = discord.ui.Button(label="A", style=discord.ButtonStyle.primary)
            self.choice_a_button.callback = self.choice_a_button_function
            self.add_item(self.choice_a_button)
            
        if current_quest_lines.choice_b and current_quest_lines.choice_b.strip() != "":
            self.choice_b_button = discord.ui.Button(label="B", style=discord.ButtonStyle.primary)
            self.choice_b_button.callback = self.choice_b_button_function
            self.add_item(self.choice_b_button)
        
        if current_quest_lines.choice_c and current_quest_lines.choice_c.strip() != "":
            self.choice_c_button = discord.ui.Button(label="C", style=discord.ButtonStyle.primary)
            self.choice_c_button.callback = self.choice_c_button_function
            self.add_item(self.choice_c_button)
        
    async def choice_a_button_function(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Đây không phải nhiệm vụ của bạn!", ephemeral=True)
            return
        self.not_choose = False
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f"Bạn đã chọn A!", ephemeral=True)
        await self.handle_choice("A")
    
    async def choice_b_button_function(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Đây không phải nhiệm vụ của bạn!", ephemeral=True)
            return
        self.not_choose = False
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f"Bạn đã chọn B!", ephemeral=True)
        await self.handle_choice("B")
        
    async def choice_c_button_function(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("Đây không phải nhiệm vụ của bạn!", ephemeral=True)
            return
        self.not_choose = False
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(content=f"Bạn đã chọn C!", ephemeral=True)
        await self.handle_choice("C")
    
    async def on_timeout(self):
        if self.message and self.not_choose:
            self.not_choose = False
            await self.handle_choice("timeout")
        
    async def handle_choice(self, choice: str):
        # Get next quest line ID
        next_id = self.current_quest_lines.next_steps.get_next_id(choice)
        if not next_id:
            await self.message.edit(content="Không thể tìm thấy bước tiếp theo! Liên hệ Darkie ngay!", embed=None, view=None)
            print(f"User {self.user.name} at channel {self.guardian_quest.channel_name} cant find next step id in quest {self.override_title}, choice {choice}, current line {self.current_quest_lines.title}")
            await self.send_result_embed()
            return

        # Find the next GuardianQuestLines by ID
        next_quest_line = next((q for q in self.guardian_quest.quest_lines if q.id == next_id), None)
        if not next_quest_line:
            await self.message.edit(content="Câu chuyện kết thúc!", embed=None, view=None)
            print(f"User {self.user.name} at channel {self.guardian_quest.channel_name} cant find next quest line in {self.override_title}, choice {choice}, current line {self.current_quest_lines.title}")
            await self.send_result_embed()
            return
        
        next_quest_line.replace_guardian_name(guardian_name=self.guardian_quest.guardian.ga_name)
        title = next_quest_line.title
        description = next_quest_line.description.replace("{guardian.ga_name}", self.guardian_quest.guardian.ga_name)
        list_des = self.split_text_to_pairs(text=description)

        if next_quest_line.force_injury:
            self.force_injury = True
        if next_quest_line.force_dead:
            self.force_dead = True
        
        embed = discord.Embed(title=f"{EmojiCreation2.QUEST_ICON.value} {self.override_title} {EmojiCreation2.QUEST_ICON.value}", description=f"", color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"*{title}*", value=f"", inline=False)
        for des in list_des:
            embed.add_field(name=f"", value=f"{des}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        
        self.total_ga_stamina += next_quest_line.ga_stamina
        self.total_ga_hp += next_quest_line.ga_health
        self.total_ga_mana += next_quest_line.ga_mana
        self.total_ga_exp += next_quest_line.ga_exp
        self.total_silver += next_quest_line.silver
        self.total_gold += next_quest_line.gold
        
        flag_a = False
        flag_b = False
        flag_c = False
        if next_quest_line.choice_a and next_quest_line.choice_a.strip() != "":
            embed.add_field(name=f"", value=F"{EmojiCreation2.LETTER_A.value}: {next_quest_line.choice_a}", inline=False)
            flag_a = True
        if next_quest_line.choice_b and next_quest_line.choice_b.strip() != "":
            embed.add_field(name=f"", value=F"{EmojiCreation2.LETTER_B.value}: {next_quest_line.choice_b}", inline=False)
            flag_b = True
        if next_quest_line.choice_c and next_quest_line.choice_c.strip() != "":
            embed.add_field(name=f"", value=F"{EmojiCreation2.LETTER_C.value}: {next_quest_line.choice_c}", inline=False)
            flag_c = True
        if not (flag_a or flag_b or flag_c):
            #end
            try:
                await self.message.edit(embed=embed, view=None)  # Remove view
                print(f"User {self.user.name} at channel {self.guardian_quest.channel_name} finished their GA quest")
                await self.send_result_embed()
            except Exception as e:
                print(f"Exception when trying to end quest line for user {self.user.name} at channel {self.guardian_quest.channel_name}: {e}")
            return
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=30)  # 30 seconds from now
        unix_time = int(end_time.timestamp())
        embed.add_field(name=f"", value="_____", inline=False)
        embed.add_field(name=f"", value=f"Thời gian còn lại: <t:{unix_time}:R>", inline=False)
        # Create new view with the next step
        new_view = GaQuestView(self.user, self.guardian_quest, next_quest_line, override_title=self.override_title, total_dignity=self.total_dignity, total_gold=self.total_gold, total_silver=self.total_silver, total_ga_exp=self.total_ga_exp, total_ga_hp=self.total_ga_hp, total_ga_mana=self.total_ga_mana, total_ga_stamina=self.total_ga_stamina, channel=self.channel, force_dead=self.force_dead, force_injury=self.force_injury)
        try:
            mess = await self.message.edit(embed=embed,view=new_view)
            new_view.message = mess
        except Exception as e:
            print(f"Exception when trying to edit quest line for user {self.user.name} at channel {self.guardian_quest.channel_name}: {e}")

    #region end quest
    async def send_result_embed(self):
        
        #Nếu tiền dương thì buff mạnh
        if self.total_gold > 0: self.total_gold * 5
        if self.total_silver > 0: self.total_silver * 5

        #giới hạn exp
        if self.total_ga_exp < 50: self.total_ga_exp = 50
        if self.total_ga_exp > 500: self.total_ga_exp = 500

        #Tính lại stats
        total_hp = self.guardian_quest.guardian.health - self.total_ga_hp
        if total_hp < 0 or self.force_injury or self.force_dead: total_hp = 0 #Nếu nhận flag thì set về 0
        total_stamina = self.guardian_quest.guardian.stamina - self.total_ga_stamina
        if total_stamina<0: total_stamina = 0
        total_mana = self.guardian_quest.guardian.mana - self.total_ga_mana
        if total_mana < 0: total_mana = 0

        is_dead = False
        if total_hp <= 0:
            if self.force_dead:
                is_dead = True
            else:
                actual_death_chance = UtilitiesFunctions.guardian_death_chance(level=self.guardian_quest.guardian.level)
                is_dead = UtilitiesFunctions.get_chance(actual_death_chance)


        if not CustomFunctions.check_if_dev_mode():
            ProfileMongoManager.set_guardian_current_stats(guild_id=self.user.guild.id, user_id=self.user.id,stamina=total_stamina, health=total_hp, mana=total_mana, is_dead=is_dead)
        #Cập nhật nhân phẩm
        ProfileMongoManager.update_dignity_point(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", dignity_point=self.total_dignity)
        #Cập nhật tiền
        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", gold=self.total_gold, silver=self.total_silver)
        additional_reward = self.get_result_additional_reward()

        embed = discord.Embed(title=f"Phần thưởng", description=f"", color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{self.user.mention} đã hoàn thành nhiệm vụ, và nhận được:", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **{self.total_gold}** {EmojiCreation2.GOLD.value} **{self.total_silver}** {EmojiCreation2.SILVER.value} **{self.total_dignity}** Điểm Nhân Phẩm", inline=False)
        text = f"{self.guardian_quest.guardian.ga_emoji} - {self.guardian_quest.guardian.ga_name} thì:"
        if is_dead:
            text = f"{self.guardian_quest.guardian.ga_emoji} - {self.guardian_quest.guardian.ga_name} (Tử Nạn) thì:"
        elif total_hp < 0:
            text = f"{self.guardian_quest.guardian.ga_emoji} - {self.guardian_quest.guardian.ga_name} (Trọng Thương) thì:"
        embed.add_field(name=f"", value=f"{text}", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **{self.total_ga_hp}** {EmojiCreation2.HP.value} **{self.total_ga_mana}** {EmojiCreation2.MP.value} **{self.total_ga_stamina}** {EmojiCreation2.STAMINA.value} **{self.total_ga_exp}** EXP", inline=False)
        embed.add_field(name=f"", value=f"Ngoài ra còn nhận được thưởng thêm: {additional_reward}", inline=False)
        await self.channel.send(embed=embed)
        return
    
    def get_result_additional_reward(self):
        reward_text = ""
        amount = 1
        #point
        roll_dice = UtilitiesFunctions.get_chance(15)
        if roll_dice:
            amount = random.randint(1, 2)
            ProfileMongoManager.set_guardian_stats_points(guild_id=self.user.guild.id, user_id=self.user.id, stats_point=amount)
            reward_text = f"x{amount} **Điểm Cộng Chỉ Số**"
            return reward_text
        
        #legendary weapon chance
        roll_dice = UtilitiesFunctions.get_chance(5)
        if roll_dice:
            dice_check = UtilitiesFunctions.get_chance(50)
            if dice_check:
                item = copy.deepcopy(random.choice(list_legend_weapon_1))
                item.item_worth_amount = 10
                reward_text = f"x1 **[{item.emoji} - {item.item_name}]**"
                ProfileMongoManager.update_list_items_profile(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", item=item, amount=1)
                return reward_text
            else:
                item = copy.deepcopy(random.choice(list_legend_weapon_2))
                item.item_worth_amount = 10
                reward_text = f"x1 **[{item.emoji} - {item.item_name}]**"
                ProfileMongoManager.update_list_items_profile(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", item=item, amount=1)
                return reward_text
        
        #darkium
        roll_dice =UtilitiesFunctions.get_chance(10)
        if roll_dice:
            amount = random.randint(1, 3)
            reward_text = f"**{amount}** {EmojiCreation2.DARKIUM.value}"
            ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", darkium=amount)
            return reward_text
        
        #Random gift
        roll_dice =UtilitiesFunctions.get_chance(35)
        if roll_dice:
            amount = random.randint(1, 5)
            item = random.choice(list_gift_items)
            reward_text = f"x{amount} **[{item.emoji} - {item.item_name}]**"
            ProfileMongoManager.update_list_items_profile(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #random potion
        roll_dice =UtilitiesFunctions.get_chance(35)
        if roll_dice:
            amount = random.randint(1, 3)
            #Roll xem trúng bình nào
            item = copy.deepcopy(random.choice(list_support_ga_items))
            roll_dice = UtilitiesFunctions.get_chance(70)
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
            ProfileMongoManager.update_list_items_profile(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #random weapon
        roll_dice =UtilitiesFunctions.get_chance(35)
        if roll_dice:
            amount = random.randint(1, 3)
            item = random.choice(list_attack_items)
            reward_text = f"x{amount} **[{item.emoji} - {item.item_name}]**"
            ProfileMongoManager.update_list_items_profile(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #random armour
        roll_dice =UtilitiesFunctions.get_chance(25)
        if roll_dice:
            amount = random.randint(1, 2)
            item = random.choice(list_protection_items)
            reward_text = f"x{amount} **[{item.emoji} - {item.item_name}]**"
            ProfileMongoManager.update_list_items_profile(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", item=item, amount=amount)
            return reward_text
        #gold
        amount = random.randint(1000, 30000)
        reward_text = f"**{amount}** {EmojiCreation2.GOLD.value}"
        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_display_name="", user_name="", gold=amount)
        return reward_text

    
    def split_text_to_pairs(self, text: str):
        # Split sentences on punctuation + space
        sentence_endings = re.compile(r'(?<=[.!?])\s+')
        sentences = sentence_endings.split(text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]

        pairs = []
        # Step by 2 to avoid overlapping
        for i in range(0, len(sentences), 2):
            # If last sentence has no pair, just add it alone
            if i + 1 < len(sentences):
                pair = sentences[i] + " " + sentences[i + 1]
            else:
                pair = sentences[i]
            pairs.append(pair)

        return pairs