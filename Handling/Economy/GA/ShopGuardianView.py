import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class ShopGuardianView(discord.ui.View):
    def __init__(self, list_ga = List[GuardianAngel], rate = 1.0):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.list_ga: List[GuardianAngel]  = list_ga
        self.current_page = 0
        self.current_ga: GuardianAngel = None
        self.total_pages = len(self.list_ga)
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
        ga = self.list_ga[self.current_page]
        embed = discord.Embed(title=f"**Cửa Hàng Hộ Vệ Thần**", description=f"", color=discord.Color.blue())
        embed.add_field(name=f"", value=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬",inline=False)
        embed.add_field(name=f"", value=f"{ga.ga_emoji} - **{ga.ga_name}**",inline=False)
        embed.add_field(name=f"", value=f"Cấp bậc: **{UtilitiesFunctions.get_text_on_guardian_level(ga.level)}** [{ga.level}]", inline=False)
        embed.add_field(name=f"", value=f"Máu: \n{EmojiCreation2.HP.value}: {ga.max_health}", inline=True)
        embed.add_field(name=f"", value=f"Mana: \n{EmojiCreation2.MP.value}: {ga.max_mana}", inline=True)
        embed.add_field(name=f"", value=f"Thể lực: \n{EmojiCreation2.STAMINA.value}: {ga.max_stamina}", inline=True)
        embed.add_field(name=f"", value=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬",inline=False)
        embed.add_field(name=f"", value=f"Giá: **{int(ga.worth_amount* self.rate)}** {UtilitiesFunctions.get_emoji_from_loai_tien(ga.worth_type)}",inline=False)
        embed.set_footer(text=f"Trang 1/{len(self.list_ga)}")
        
        ga_urls = ListGAAndSkills.get_list_back_ground_on_ga_id(ga.ga_id)
        url = None
        if ga_urls != None and len(ga_urls)>0:
            url= ga_urls[0]
            if url:
                embed.set_image(url=url)
        
        return embed
    
    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="Mua", style=discord.ButtonStyle.green)
    async def buy_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False)
        self.current_ga = self.list_ga[self.current_page]
        
        profile_user = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if profile_user == None:
            await interaction.followup.send(f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        elif profile_user.guardian!=None:
            await interaction.followup.send(f"Bạn đã có Hộ Vệ Thần rồi! Vui lòng bán Hộ Vệ Thần bằng lệnh {SlashCommand.GA_SELL.value}", ephemeral=True)
            return
        try:
            
            cost_money = int(self.current_ga.worth_amount*self.rate)
            if self.current_ga.worth_amount == "C" and profile_user.copper < cost_money:
                await interaction.followup.send(f"{interaction.user.mention}, bạn không đủ {EmojiCreation2.COPPER.value} để mua!", ephemeral=True)
                return
            elif self.current_ga.worth_amount == "S" and profile_user.silver < cost_money:
                await interaction.followup.send(f"{interaction.user.mention}, bạn không đủ {EmojiCreation2.SILVER.value} để mua!", ephemeral=True)
                return
            elif self.current_ga.worth_amount == "G" and profile_user.gold < cost_money:
                await interaction.followup.send(f"{interaction.user.mention}, bạn không đủ {EmojiCreation2.GOLD.value} để mua!", ephemeral=True)
                return
            elif self.current_ga.worth_amount == "D" and profile_user.darkium < cost_money:
                await interaction.followup.send(f"{interaction.user.mention}, bạn không đủ {EmojiCreation2.DARKIUM.value} để mua!", ephemeral=True)
                return
            
            money_for_authority = int(cost_money/2)
            if money_for_authority == 0: money_for_authority = 1
            
            if self.current_ga.worth_type == "C":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, copper=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, copper=money_for_authority)
            elif self.current_ga.worth_type == "S":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, silver=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, silver=money_for_authority)
            elif self.current_ga.worth_type == "G":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, gold=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, gold=money_for_authority)
            elif self.current_ga.worth_type == "D":
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name= interaction.user.name, user_display_name= interaction.user.display_name, darkium=-cost_money)
                if profile_user.is_authority != True:
                    ProfileMongoManager.update_money_authority(guild_id=interaction.guild_id, darkium=money_for_authority)
            
            ProfileMongoManager.set_main_guardian_profile(guild_id=interaction.guild_id, user_id=interaction.user.id, guardian=self.current_ga)
                
            authority_text = f"Chính Quyền đã nhận được một nửa số tiền trên!"
            if profile_user.is_authority == True:
                authority_text = ""
            await interaction.followup.send(f"{interaction.user.mention} đã chọn mua [{self.current_ga.ga_emoji}- **{self.current_ga.ga_name}**] với giá {cost_money} {UtilitiesFunctions.get_emoji_from_loai_tien(self.current_ga.worth_type)}!\n{authority_text}", ephemeral=False)
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        except ValueError:
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
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