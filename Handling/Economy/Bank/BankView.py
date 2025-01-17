
import discord
from typing import List, Optional
import random
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from  Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
import re
from enum import Enum
from CustomEnum.EmojiEnum import EmojiCreation2


class CurrencyEmoji(Enum):
        DARKIUM = "<a:darkium:1294615481701105734>"
        GOLD = "<a:gold:1294615502588608563>"
        SILVER = "<a:silver:1294615512919048224>"
        COPPER = "<a:copper:1294615524918956052>"
    
class CurrencySlashCommand(Enum):
        PROFILE = "</profile:1294699979058970656>"
        VOTE_AUTHORITY = "</vote_authority:1294754901988999240>"

SELECT_OPTIONS  = [
            discord.SelectOption(label=f'Quy đổi sang Darkium', value='D', description='Đổi sang Darkium.', emoji=discord.PartialEmoji(name="darkium", id=1294615481701105734)),
            discord.SelectOption(label=f'Quy đổi sang Gold', value='G', description='Đổi sang Gold.', emoji=discord.PartialEmoji(name="gold", id=1294615502588608563)),
            discord.SelectOption(label=f'Quy đổi sang Silver', value='S', description='Đổi sang Silver.', emoji = discord.PartialEmoji(name="silver", id=1294615512919048224)),
            discord.SelectOption(label=f'Quy đổi sang Copper', value='C', description='Đổi sang Copper.', emoji= discord.PartialEmoji(name="copper", id=1294615524918956052), default=True),
        ]

class BankView(discord.ui.View):
    def __init__(self, authority: Profile, rate: float, user: discord.Member):
        super().__init__(timeout=20)
        self.authority = authority
        self.rate = rate
        self.message : discord.Message = None
        self.currency: str = None
        self.user: discord.Member = user

    async def on_timeout(self):
        #Delete
        if self.message != None: 
            await self.message.delete()
            return
        
        #Disable
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
            if isinstance(item, discord.ui.Select):
                item.disabled = True
        await self.message.edit(view=self)

    @discord.ui.select(placeholder='Chọn đơn vị tiền cần quy đổi',min_values=1, max_values=1, options= SELECT_OPTIONS)
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != self.user.id:
            await interaction.followup.send(f'Đây là ngân hàng do người khác tạo, bạn không được phép thay đổi! Vui lòng tự dùng lệnh `/bank`', ephemeral=True)
            return
        selected_option = select.values[0]
        self.currency = selected_option
        if selected_option == "D":
            await interaction.followup.send(f'Bạn đã chọn quy đổi sang {CurrencyEmoji.DARKIUM.value}', ephemeral=True)
        elif selected_option == "G":
            await interaction.followup.send(f'Bạn đã chọn quy đổi sang {CurrencyEmoji.GOLD.value}', ephemeral=True)
        elif selected_option == "S":
            await interaction.followup.send(f'Bạn đã chọn quy đổi sang {CurrencyEmoji.SILVER.value}', ephemeral=True)
        elif selected_option == "C":
            await interaction.followup.send(f'Bạn đã chọn quy đổi sang {CurrencyEmoji.COPPER.value}', ephemeral=True)
        return
    
    @discord.ui.button(label="💱 Quy Đổi Tiền Tệ", style=discord.ButtonStyle.green)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # await interaction.response.defer(ephemeral=True)
            await interaction.response.send_modal(TextInputModal(selected_currency= self.currency, rate=self.rate))
            # await interaction.followup.send(view=TextInputView())


# Create a custom modal for text input
class TextInputModal(discord.ui.Modal):
    def __init__(self, selected_currency, rate: float):
        super().__init__(title="Nhập số tiền mà bạn muốn đổi")
        self.selected_currency = selected_currency if selected_currency else "C"
        self.rate = rate
        self.input_field = discord.ui.TextInput(
            label="Nhập số tiền bạn cần quy đổi",
            placeholder="VD: 1000C, 100S, 1G, 1D",
            required=True
        )
        self.add_item(self.input_field)
        
        
    async def on_submit(self, interaction: discord.Interaction):
        user_input = self.input_field.value
        await interaction.response.defer(ephemeral=False)
        #Kiểm tra người bấm có nằm trong danh sách chưa
        profile_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if profile_user == None:
            await interaction.followup.send(f"Vui lòng dùng lệnh {CurrencySlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        amount, suffix = self.parse_input(user_input)
        if amount == None or suffix == None:
            await interaction.followup.send(f"Đã nhập sai giá trị tiền! Nhập như sau mới đúng: 1000C, 100S, 1G, 1D", ephemeral=True)
            return
        if suffix == user_input:
            await interaction.followup.send(f"Bạn không thể đổi cùng đơn vị được!", ephemeral=True)
            return
        not_sufficient = False
        #Kiểm tra đủ tiền hay không
        if (suffix == "C" or suffix == "c") and profile_user.copper < amount:
            not_sufficient = True
        elif (suffix == "S" or suffix == "s") and profile_user.silver < amount:
            not_sufficient = True
        elif (suffix == "G" or suffix == "g") and profile_user.gold < amount:
            not_sufficient = True
        elif (suffix == "D" or suffix == "d") and profile_user.darkium < amount:
            not_sufficient = True
        if not_sufficient:
            await interaction.followup.send(f"Bạn làm gì đủ tiền mà đổi?", ephemeral=True)
            return
        
        #Tính lại số tiền cần cộng, số tiền cần trừ
        new_money_value = self.convert_currency(amount=amount, rate=self.rate, from_currency_type=suffix, to_currency_type=self.selected_currency)
        #Trừ số tiền đã đổi
        #Nếu new money value = 0 thì khỏi
        if new_money_value != 0:
            #Dựa vào suffix với self.selected_currency để cộng trừ cho đúng chỗ
            #Suffix là trừ, selected_currency là cộng
            # if suffix == "D":
            self.add_or_remove_money(guild_int=interaction.guild_id, profile= profile_user, type=suffix, is_add=False, amount= amount)
            self.add_or_remove_money(guild_int=interaction.guild_id, profile= profile_user, type=self.selected_currency, is_add=True, amount= new_money_value)
        from_emoji = self.get_emoji_from_type(input=suffix)
        to_emoji = self.get_emoji_from_type(input=self.selected_currency)
        
        profile_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        tax = 250
        tax_emoji = EmojiCreation2.COPPER.value
        
        #Chuyển đến loại tiền nào thì đánh thuế loại tiền đó
        if profile_user.darkium > 15 and to_emoji == EmojiCreation2.DARKIUM.value:
            tax = 1
            tax_emoji = EmojiCreation2.DARKIUM.value
        if profile_user.darkium < 15 and to_emoji == EmojiCreation2.DARKIUM.value:
            #mặc định 5% số tiền quy đổi Gold
            tax = int(new_money_value * 5 / 100)
            tax_emoji = EmojiCreation2.GOLD.value
            if tax <= 0: tax = 1
            if tax > 10000: tax = 10000
        elif to_emoji == EmojiCreation2.GOLD.value:
            #mặc định 5% số tiền quy đổi
            tax = int(new_money_value * 5 / 100)
            tax_emoji = EmojiCreation2.GOLD.value
            if tax <= 0: tax = 1
            if tax > 10000: tax = 10000
        elif to_emoji == EmojiCreation2.SILVER.value:
            #mặc định 5%
            tax = int(new_money_value * 5 / 100)
            tax_emoji = EmojiCreation2.SILVER.value
            if tax <= 0: tax = 1
            if tax > 100000: tax = 100000
        elif to_emoji == EmojiCreation2.COPPER.value:
            #mặc định 10%
            tax = int(new_money_value * 10 / 100)
            tax_emoji = EmojiCreation2.COPPER.value
            if tax <= 0: tax = 1
            if tax > 10000000: tax = 10000000
            
        #Cộng tiền 200 Copper cho chính quyền nếu user_profile không phải là chính quyền
        tax_text = ""
        if profile_user.is_authority == False:
            tax_text = f"Đương nhiên là bị trừ **{tax}** {tax_emoji} để đóng thuế cho Chính Quyền!"
            if tax_emoji == EmojiCreation2.COPPER.value:
                ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, copper=tax)
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper= -tax)
            elif tax_emoji == EmojiCreation2.SILVER.value:
                ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, silver=tax)
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver= -tax)
            elif tax_emoji == EmojiCreation2.GOLD.value:
                ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=tax)
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold= -tax)
            elif tax_emoji == EmojiCreation2.DARKIUM.value:
                ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, darkium=tax)
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name= interaction.guild.name, user_id= interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium= -tax)
            
            
        extra_text = f""
        if suffix == "C" or suffix == "c":
            extra_text = f"Số {CurrencyEmoji.COPPER.value} còn lại: **{self.shortened_currency(profile_user.copper)}**"
        if suffix == "S" or suffix == "s":
            extra_text = f"Số {CurrencyEmoji.SILVER.value} còn lại: **{self.shortened_currency(profile_user.silver)}**"
        if suffix == "G" or suffix == "g":
            extra_text = f"Số {CurrencyEmoji.GOLD.value} còn lại: **{self.shortened_currency(profile_user.gold)}**"
        if suffix == "D" or suffix == "d":
            extra_text = f"Số {CurrencyEmoji.DARKIUM.value} còn lại: **{self.shortened_currency(profile_user.darkium)}**"
        await interaction.followup.send(f"**{profile_user.user_display_name}** đã đổi từ **{self.shortened_currency(amount)}** {from_emoji} -> **{self.shortened_currency(new_money_value)}** {to_emoji}. {tax_text}\n{extra_text}")
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        
    def add_or_remove_money(self, guild_int: int, profile: Profile, type: str, amount: int, is_add: bool = True):
        if type == "D":
            if is_add:
                profile.darkium += amount
            else:
                profile.darkium -= amount
            ProfileMongoManager.update_profile_money_fast(guild_id=guild_int, data= profile)
        elif type == "G":
            if is_add:
                profile.gold += amount
            else:
                profile.gold -= amount
            ProfileMongoManager.update_profile_money_fast(guild_id=guild_int, data= profile)
        elif type == "S":
            if is_add:
                profile.silver += amount
            else:
                profile.silver -= amount
            ProfileMongoManager.update_profile_money_fast(guild_id=guild_int, data= profile)
        elif type == "C":
            if is_add:
                profile.copper += amount
            else:
                profile.copper -= amount
            ProfileMongoManager.update_profile_money_fast(guild_id=guild_int, data= profile)
        return
    
    def shortened_currency(self, number: int):
        if number >= 1000000000:
            suffix = int(number % 1000000000 // 1000000)
            if suffix == 0: suffix = "" 
            return f"{int(number // 1000000000)}B{suffix}"
        elif number >= 1000000:
            suffix = int(number % 1000000 // 1000)
            if suffix == 0: suffix = "" 
            return f"{int(number // 1000000)}M{suffix}"
        elif number >= 10000:
            suffix = int(number % 1000 // 100)
            if suffix == 0: suffix = ""
            return f"{int(number // 1000)}K{suffix}"  
        else:
            return str(int(number))
    
    def get_emoji_from_type(self, input: str):
        if input == "D" or input == "D":
            return CurrencyEmoji.DARKIUM.value
        if input == "G" or input == "G":
            return CurrencyEmoji.GOLD.value
        if input == "S" or input == "S":
            return CurrencyEmoji.SILVER.value
        if input == "C" or input == "C":
            return CurrencyEmoji.COPPER.value
    
    def parse_input(self, input_string):
        pattern = r"(\d+)([DGSCT])"
        match = re.match(pattern, input_string, re.IGNORECASE)
        if match:
            integer_value = int(match.group(1))
            suffix = match.group(2).upper()
            return integer_value, suffix
        return None, None
    
    def convert_currency(self, amount: int, rate: float, from_currency_type: str, to_currency_type: str):
        #Đổi darkium sang các đơn vị khác
        if from_currency_type == to_currency_type: return amount
        result = 0
        if from_currency_type == "D":
            if to_currency_type == "G": #Base 10000
                result = int(amount * (10000 * rate))
            elif to_currency_type == "S": #Base 10000 * 5000
                result = int(amount * (10000 * rate) * (5000 * rate))
            elif to_currency_type == "C": #Base 10000 * 5000 * 5000
                result = int(amount * (10000 * rate) * (5000*rate) *  (5000 * rate))
        elif from_currency_type == "G":
            if to_currency_type == "D": #Base 1/10000
                result = int(amount / (10000 * rate))
            elif to_currency_type == "S": #Base 5000
                result = int(amount * (5000 * rate))
            elif to_currency_type == "C": #Base  5000 * 5000
                result = int(amount * (5000 * rate) * (5000 * rate))
        elif from_currency_type == "S":
            if to_currency_type == "D": #Base 1/5000/10000
                result = int(amount / (5000 * rate) / (10000 * rate))
            elif to_currency_type == "G": #Base 1/5000
                result = int(amount / (5000 * rate))
            elif to_currency_type == "C": #Base  5000
                result = int(amount * (5000 * rate))
        elif from_currency_type == "C":
            if to_currency_type == "D": #Base 1/5000/5000/10000
                result = int(amount / (5000 * rate) / (5000 * rate) / (10000 * rate))
            elif to_currency_type == "G": #Base 1/5000/5000
                result = int(amount / (5000 * rate) / (5000 * rate))
            elif to_currency_type == "S": #Base  1/5000
                result = int(amount / (5000 * rate))
        return result