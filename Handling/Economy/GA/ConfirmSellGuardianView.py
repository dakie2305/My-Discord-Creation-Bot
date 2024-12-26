import discord
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class ConfirmSellGuardianView(discord.ui.View):
    def __init__(self, money: int, money_type: str, guardian: GuardianAngel, user: discord.Member):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.money = money
        self.money_type = money_type
        self.user = user
        self.guardian = guardian
        self.is_sold = False
        
        
    async def on_timeout(self):
        if self.message != None:
            try:
                await self.message.delete()
            except Exception:
                return
            
    @discord.ui.button(label="Chấp Nhận Bán", style=discord.ButtonStyle.primary)
    async def confirm_sell(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        if self.money_type == "C":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, copper=self.money)
        elif self.money_type == "S":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, silver=self.money)
        elif self.money_type == "G":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, gold=self.money)
        elif self.money_type == "D":
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, darkium=self.money)
        
        ProfileMongoManager.set_main_guardian_profile(guild_id=interaction.guild_id, user_id=interaction.user.id, guardian=None)
        text = f"{interaction.user.mention} đã chấp nhận bán {self.guardian.ga_emoji} - {self.guardian.ga_name} với giá **{self.money}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.money_type)}!"
        channel = interaction.channel
        await channel.send(content=text)
        if self.message != None:
            try:
                await self.message.delete()
            except Exception:
                return 
        
        
        
    