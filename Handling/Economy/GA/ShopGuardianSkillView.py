import discord
from Handling.Economy.Global import GlobalMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class ShopGuardianSkillView(discord.ui.View):
    def __init__(self, rate: float = 1.0, list_all_shops: Dict[str, List[GuardianAngelSkill]] = {}):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.list_all_shops = list_all_shops
        self.keys = list(list_all_shops.keys())  # Shop names
        self.current_page = 0
        self.total_pages = len(self.keys)
        self.current_list_item: List[GuardianAngelSkill] = None
        self.rate = rate
        self.update_buttons()

    def update_buttons(self):
        if(self.total_pages == 1):
            self.next_button.disabled = True
            self.prev_button.disabled = True
        elif self.current_page + 1 == self.total_pages:
            #Trang cuối, ẩn nút next
            self.next_button.disabled = True
            self.prev_button.disabled = False
        elif self.current_page == 0:
            #Trang đầu, ẩn nút prev
            self.next_button.disabled = False
            self.prev_button.disabled = True
        else:
            self.next_button.disabled = False
            self.prev_button.disabled = False
    
    def create_embed(self):
        shop_name = self.keys[self.current_page]
        items = self.list_all_shops[shop_name]
        self.current_list_item = items
        # Tạo embed cho shop
        embed = discord.Embed(title=f"**{shop_name}**", description=f"Tỷ giá hiện tại: **{self.rate}**", color=discord.Color.blue())
        embed.add_field(name=f"", value=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬",inline=False)
        count = 1
        for item in items:
            actual_power = item.attack_power + int(item.attack_power*item.buff_attack_percent/100)
            embed.add_field(name=f"`{count}` {item.emoji} - {item.skill_name}", value=f"{EmojiCreation2.SHINY_POINT.value} Giá: **{int(item.item_worth_amount*self.rate)}**{self.get_emoji_money_from_type(type=item.item_worth_type)}\n{EmojiCreation2.SHINY_POINT.value} Sức mạnh: **{actual_power}**\n{EmojiCreation2.SHINY_POINT.value} {item.skill_desc}",inline=False)
            embed.add_field(name=f"", value=f"\n",inline=False)
            count+=1
        embed.set_footer(text=f"Trang {self.current_page + 1}/{self.total_pages}")
        return embed
    
    def get_emoji_money_from_type(self, type: str):
        if type == "C": return EmojiCreation2.COPPER.value
        if type == "S": return EmojiCreation2.SILVER.value
        if type == "G": return EmojiCreation2.GOLD.value
        if type == "D": return EmojiCreation2.DARKIUM.value
        
    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="Mua", style=discord.ButtonStyle.green)
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextShopInputModal(rate=self.rate, message=self.message, current_list_item=self.current_list_item))
        return

    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        
    async def on_timeout(self):
        if self.message != None:
            try:
                await self.message.delete()
            except Exception:
                return

# Create a custom modal for text input
class TextShopInputModal(discord.ui.Modal):
    def __init__(self, current_list_item: List[GuardianAngelSkill],message: discord.Message, rate: float = 1.0):
        super().__init__(title="Chọn mã kỹ năng mà bạn muốn mua")
        self.rate = rate
        self.message: discord.Message = message
        self.current_list_item = current_list_item
        self.input_id_field = discord.ui.TextInput(
            label="Nhập số thứ tự của kỹ năng muốn mua",
            placeholder="VD: 1, 2, 3, 4,...",
            required=True,
            default = "1",
            max_length=2
        )
        self.add_item(self.input_id_field)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        profile_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if profile_user == None:
            await interaction.followup.send(f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        if profile_user.guardian == None:
            await interaction.followup.send(f"Bạn không còn Hộ Vệ Thần nữa!", ephemeral=True)
            return
        
        if profile_user.guardian.list_skills != None and len(profile_user.guardian.list_skills) >= profile_user.guardian.max_skills:
            await interaction.followup.send(f"Hộ Vệ Thần của bạn không còn slot kỹ năng trống!", ephemeral=True)
            return
        
        input_id_field = self.input_id_field.value
        try:
            skill_id = int(input_id_field) - 1
            if skill_id < 0:
                await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
                return
            if self.is_valid_index(skill_id, self.current_list_item) == False:
                await interaction.followup.send(f"Id kỹ năng nhập vào không hợp lệ!", ephemeral=True)
                return
            item = self.current_list_item[skill_id]

            #Kiểm tra phải kỹ năng đại đế không
            if item.skill_id == 'emperor_stare_skill':
                top_1_ga = self.get_top_1_ga_leaderboard()
                if top_1_ga == None or top_1_ga.user_id != interaction.user.id:
                    await interaction.followup.send(f"Một Hộ Vệ Thần hạ đẳng, thấp kém không xứng đáng sở hữu [{item.emoji}- **{item.skill_name}**].\nChỉ Hộ Vệ Thần Top 1 liên thông server trong lệnh {SlashCommand.LEADERBOARD.value} mới được phép sở hữu", ephemeral=True)
                    return
                
            #Kiểm tra xem trong list skill có skill này chưa
            if profile_user.guardian.list_skills != None and len(profile_user.guardian.list_skills) > 0:
                for skill in profile_user.guardian.list_skills:
                    if skill.skill_id == item.skill_id:
                        await interaction.followup.send(f"Bạn đã có kỹ năng [{item.emoji}- **{item.skill_name}**] rồi!", ephemeral=True)
                        return
                
            cost_money = int(item.item_worth_amount*self.rate)
            
            if item.item_worth_type == "C" and profile_user.copper < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.COPPER.value}!", ephemeral=True)
                return
            elif item.item_worth_type == "S" and profile_user.silver < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.SILVER.value}!", ephemeral=True)
                return
            elif item.item_worth_type == "G" and profile_user.gold < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.GOLD.value}!", ephemeral=True)
                return
            elif item.item_worth_type == "D" and profile_user.darkium < cost_money:
                await interaction.followup.send(f"Bạn không đủ {EmojiCreation2.DARKIUM.value}!", ephemeral=True)
                return
            
            money_for_authority = int(cost_money/2)
            if money_for_authority == 0: money_for_authority = 1
            
            if item.item_worth_type == "C":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, copper=money_for_authority)
            elif item.item_worth_type == "S":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, silver=money_for_authority)
            elif item.item_worth_type == "G":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=money_for_authority)
            elif item.item_worth_type == "D":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, darkium=money_for_authority)
            ProfileMongoManager.update_list_skills_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, skill=item)
            authority_text = f"Trong giao dịch này, Chính Quyền đã nhận được **{money_for_authority}** {self.get_emoji_money_from_type(item.item_worth_type)} để làm tiền thuế!"
            if profile_user.is_authority == True:
                authority_text = ""
            await interaction.followup.send(f"{interaction.user.mention} đã chọn mua kỹ năng [{item.emoji}- **{item.skill_name}**] với giá {cost_money} {self.get_emoji_money_from_type(item.item_worth_type)}! {authority_text}", ephemeral=False)
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        except ValueError:
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
            return
        
    def is_valid_index(self, value: int, lst: list) -> bool:
        return 0 <= value < len(lst)
    
    def get_emoji_money_from_type(self, type: str):
        if type == "C": return EmojiCreation2.COPPER.value
        if type == "S": return EmojiCreation2.SILVER.value
        if type == "G": return EmojiCreation2.GOLD.value
        if type == "D": return EmojiCreation2.DARKIUM.value
    
    def get_top_1_ga_leaderboard(self):
        list_global_profiles = GlobalMongoManager.get_top_guardian_profiles(limit=2)
        if list_global_profiles and len(list_global_profiles) > 0:
            top_profile = list_global_profiles[0]
            if top_profile != None and top_profile.guardian:
                return top_profile
        return None