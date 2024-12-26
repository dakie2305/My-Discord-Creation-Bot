import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

SELECT_OPTIONS  = [
            discord.SelectOption(label=f'Nâng chỉ số tấn công', value='attack', description='Nâng chỉ số tấn công', emoji="🦾", default=True),
            discord.SelectOption(label=f'Nâng máu', value='health', description='Nâng máu', emoji=discord.PartialEmoji(name="HP", id=1320777603358920724)),
            discord.SelectOption(label=f'Nâng thể lực', value='stamina', description='Nâng thể lực', emoji = discord.PartialEmoji(name="stamina", id=1320777620874592288)),
            discord.SelectOption(label=f'Nâng mana', value='mana', description='Nâng mana', emoji= discord.PartialEmoji(name="MP", id=1320777612926386256)),
        ]

class RankUpView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member):
        super().__init__(timeout=30)
        self.message : discord.Message = None
        self.user: discord.Member = user
        self.user_profile = user_profile
        self.selected_value: str = None

    async def on_timeout(self):
        #Delete
        if self.message != None: 
            await self.message.delete()
            return

    @discord.ui.select(placeholder='Chọn chỉ số muốn nâng cấp',min_values=1, max_values=1, options= SELECT_OPTIONS)
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != self.user.id:
            await interaction.followup.send(f'Đây không phải là chỗ để bạn chỉnh sửa', ephemeral=True)
            return
        selected_option = select.values[0]
        self.selected_value = selected_option
        if selected_option == "attack":
            await interaction.followup.send(f'Bạn đã chọn nâng cấp chỉ số tấn công 🦾', ephemeral=True)
        elif selected_option == "health":
            await interaction.followup.send(f'Bạn đã chọn nâng cấp chỉ số Máu {EmojiCreation2.HP.value}', ephemeral=True)
        elif selected_option == "stamina":
            await interaction.followup.send(f'Bạn đã chọn nâng cấp chỉ số Thể Lực {EmojiCreation2.STAMINA.value}', ephemeral=True)
        elif selected_option == "mana":
            await interaction.followup.send(f'Bạn đã chọn nâng cấp chỉ số Mana {EmojiCreation2.MP.value}', ephemeral=True)
        return
    
    @discord.ui.button(label="💱 Nâng Cấp", style=discord.ButtonStyle.green)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user.id != self.user.id: return
            await interaction.response.send_modal(TextInputModal(selected_value= self.selected_value))


# Create a custom modal for text input
class TextInputModal(discord.ui.Modal):
    def __init__(self, selected_value):
        super().__init__(title="Nhập số điểm mà bạn muốn nâng cho Hộ Vệ Thần")
        self.selected_value = selected_value if selected_value else "attack"
        self.input_field = discord.ui.TextInput(
            label="Nhập số điểm",
            placeholder="1",
            required=True,
            default = "1",
            max_length=2
        )
        self.add_item(self.input_field)
        
        
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        user_input = self.input_field.value
        try:
            amount = int(user_input)
            if amount <= 0:
                await interaction.followup.send(f"{interaction.user.mention} Vui lòng nhập giá trị lớn hơn 0!", ephemeral=True)
                return
            user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
            if user_profile == None:
                await interaction.followup.send(f"{interaction.user.mention} Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
                return
            elif user_profile.guardian == None:
                await interaction.followup.send(f"{interaction.user.mention} Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True)
                return
            elif user_profile.guardian.stats_point == 0:
                await interaction.followup.send(f"{interaction.user.mention} Hộ Vệ Thần của bạn không còn điểm cộng nào hết!", ephemeral=True)
                return
            
            
            amount = int(user_input)
            point = 5
            if self.selected_value == "attack": point = 10
            
            if amount > user_profile.guardian.stats_point: amount = user_profile.guardian.stats_point
            point = point*amount
            
            #Dựa vào selected_value để xác định nên nâng cái gì
            text = f"Thể Lực {EmojiCreation2.STAMINA.value}"
            if self.selected_value == "attack":
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, attack_power=point)
                text = f"Sức Tấn Công 🦾"
            elif self.selected_value == "health":
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, max_health=point, health= user_profile.guardian.max_health+point)
                text = f"Máu {EmojiCreation2.HP.value}"
            elif self.selected_value == "mana":
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, max_mana=point, mana= user_profile.guardian.max_mana+point)
                text = f"Mana {EmojiCreation2.MP.value}"
            else:
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, max_stamina=point, stamina= user_profile.guardian.max_stamina+point)
            #Trừ điểm stats point
            ProfileMongoManager.set_guardian_stats_points(guild_id=interaction.guild_id,user_id=interaction.user.id, stats_point=-amount)
            await interaction.followup.send(f"{interaction.user.mention} đã dùng **{amount}** điểm nâng cấp để nâng **{point}** chỉ số {text} cho Hộ Vệ Thần của bản thân!", ephemeral=False)
        except ValueError:
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
            return
        