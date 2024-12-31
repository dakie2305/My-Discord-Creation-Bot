import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from  Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class SellSkillMenuView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member, rate: float = 1.0):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.rate = rate
        self.user_profile = user_profile
        self.user = user
        self.add_item(SkillSelect(user, user_profile.guardian.list_skills, self))
        self.selected_skill: GuardianAngelSkill = None
        self.sell_button = discord.ui.Button(label="💵 Bán Kỹ Năng", style=discord.ButtonStyle.green)
        self.sell_button.callback = self.sell_button_callback
        self.add_item(self.sell_button)
        
    async def on_timeout(self):
        if self.message != None: 
            try:
                await self.message.delete()
            except Exception: return
            return
    
    async def sell_button_callback(self, interaction: discord.Interaction):
        if self.selected_skill == None: return
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        profile_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=self.user.id)
        if profile_user == None:
            await interaction.followup.send(f"{interaction.user.mention} Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        if profile_user.guardian == None:
            await interaction.followup.send(f"{interaction.user.mention} bạn không còn Hộ Vệ Thần nữa!", ephemeral=True)
            return
        if profile_user.guardian.list_skills == None or len(profile_user.guardian.list_skills) == 0:
            await interaction.followup.send(f"{interaction.user.mention} Hộ Vệ Thần của bạn không còn kỹ năng nào để bán nữa!", ephemeral=True)
            return
        #Kiểm tra xem item đó còn không
        check_fail = True
        for skill in profile_user.guardian.list_skills:
            if skill.skill_id == self.selected_skill.skill_id:
                check_fail = False
                break
        if check_fail:
            await interaction.channel.send(f'{interaction.user.mention} kỹ năng {self.selected_skill.emoji} - **{self.selected_skill.skill_name}** đã không còn!')
            return
        
        #Bán vật phẩm theo rate
        sell_money = int((self.selected_skill.item_worth_amount * self.rate / 2))
        if sell_money == 0: sell_money = 1
        if self.selected_skill.item_worth_type == "C":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper=sell_money)
        elif self.selected_skill.item_worth_type == "S":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=sell_money)
        elif self.selected_skill.item_worth_type == "G":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=sell_money)
        elif self.selected_skill.item_worth_type == "D":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium=sell_money)
        #Xoá khỏi inventory
        ProfileMongoManager.update_list_skills_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, skill=self.selected_skill, is_remove=True)
        await interaction.followup.send(f"{interaction.user.mention} đã bán kỹ năng [{self.selected_skill.emoji} - **{self.selected_skill.skill_name}**] và nhận được **{sell_money}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.selected_skill.item_worth_type)}", ephemeral=False)
        return

class SkillSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_skills: List[GuardianAngelSkill], view: "SellSkillMenuView"):
        seen_item_ids = set()
        options = []
        for item in list_skills:
            if item.skill_id in seen_item_ids:
                continue
            seen_item_ids.add(item.skill_id)
            options.append(
                discord.SelectOption(
                    label=f"{item.skill_name}",
                    description=(item.skill_desc[:97] + '...'),
                    value=item.skill_id
                )
            )
        super().__init__(placeholder="Chọn kỹ năng muốn bán", options=options)
        self.list_item = list_skills
        self.parent_view  = view
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        selected_item_id = self.values[0]
        selected_item = next(item for item in self.list_item if item.skill_id == selected_item_id)
        self.parent_view.selected_skill = selected_item
        await interaction.followup.send(f'Bạn đã chọn kỹ năng {selected_item.emoji} - **{selected_item.skill_name}**', ephemeral=True)