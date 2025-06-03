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

class GaQuestView(discord.ui.View):
    def __init__(self, user: discord.Member, guardian_quest: GuardianAngelQuest, current_quest_lines: GuardianQuestLines, override_title: str):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.guardian_quest = guardian_quest
        self.current_quest_lines = current_quest_lines
        self.user = user
        self.override_title = override_title
        self.not_choose = True
        
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
            return

        # Find the next GuardianQuestLines by ID
        next_quest_line = next((q for q in self.guardian_quest.quest_lines if q.id == next_id), None)
        if not next_quest_line:
            await self.message.edit(content="Câu chuyện kết thúc!", embed=None, view=None)
            print(f"User {self.user.name} at channel {self.guardian_quest.channel_name} cant find next quest line in {self.override_title}, choice {choice}, current line {self.current_quest_lines.title}")
            return
        next_quest_line.replace_guardian_name(guardian_name=self.guardian_quest.guardian.ga_name)
        title = next_quest_line.title
        description = next_quest_line.description.replace("{guardian.ga_name}", self.guardian_quest.guardian.ga_name)
        list_des = self.split_text_to_pairs(text=description)
        
        embed = discord.Embed(title=f"{EmojiCreation2.QUEST_ICON.value} {self.override_title} {EmojiCreation2.QUEST_ICON.value}", description=f"", color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"*{title}*", value=f"", inline=False)
        for des in list_des:
            embed.add_field(name=f"", value=f"{des}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        
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

            except Exception as e:
                print(f"Exception when trying to end quest line for user {self.user.name} at channel {self.guardian_quest.channel_name}: {e}")
            return
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=30)  # 30 seconds from now
        unix_time = int(end_time.timestamp())
        embed.add_field(name=f"", value="_____", inline=False)
        embed.add_field(name=f"", value=f"Thời gian còn lại: <t:{unix_time}:R>", inline=False)
        # Create new view with the next step
        new_view = GaQuestView(self.user, self.guardian_quest, next_quest_line, override_title=self.override_title)
        try:
            mess = await self.message.edit(embed=embed,view=new_view)
            new_view.message = mess
        except Exception as e:
            print(f"Exception when trying to edit quest line for user {self.user.name} at channel {self.guardian_quest.channel_name}: {e}")

    
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