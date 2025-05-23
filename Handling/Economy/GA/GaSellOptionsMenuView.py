import discord
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Economy.GA.ConfirmSellGuardianView import ConfirmSellGuardianView
from Handling.Economy.GA.SellSkillMenuView import SellSkillMenuView
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
import random
from datetime import datetime, timedelta

class GaSellOptionsMenuView(discord.ui.View):
    def __init__(self, user: discord.Member, user_profile: Profile):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.user = user
        self.user_profile = user_profile
        
    async def on_timeout(self):
        if self.message != None:
            try:
                await self.message.delete()
            except Exception:
                return
    
    @discord.ui.button(label="Bán Hộ Vệ Thần", style=discord.ButtonStyle.blurple)
    async def sell_guardian(self, interaction: discord.Interaction, button: discord.ui.Button):
        #Tính toán số tiền bán hộ vệ thần
        money = UtilitiesFunctions.calculate_guardian_sell_money(self.user_profile.guardian.worth_amount, self.user_profile.guardian.level, self.user_profile.guardian.is_dead, self.user_profile.guardian.attack_power, self.user_profile.guardian.max_health, self.user_profile.guardian.max_mana, self.user_profile.guardian.max_stamina)
        embed = discord.Embed(title=f"", description=f"Bán Hộ Vệ Thần", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Bạn có sẵn sàng bán Hộ Vệ Thần [{self.user_profile.guardian.ga_emoji} - **{self.user_profile.guardian.ga_name}**] với giá **{money}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.user_profile.guardian.worth_type)} không?", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.set_footer(text=f"Hãy nâng cấp của Hộ Vệ Thần lên thật cao thì bán mới được giá nhé!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        view = ConfirmSellGuardianView(money=money, money_type=self.user_profile.guardian.worth_type, guardian=self.user_profile.guardian, user=interaction.user)
        mess = await interaction.channel.send(embed=embed, view=view)
        view.message = mess
        await self.message.delete()
        return
    
    @discord.ui.button(label="Bán Kỹ Năng", style=discord.ButtonStyle.green)
    async def sell_skills(self, interaction: discord.Interaction, button: discord.ui.Button):
        shop_rate = 1.0
        conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=interaction.guild_id)
        if conversion_rate == None:
            ConversionRateMongoManager.create_update_shop_rate(guild_id=interaction.guild_id, rate=1)
            conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=interaction.guild_id)
        elif conversion_rate != None and conversion_rate.last_reset_shop_rate != None and conversion_rate.last_reset_shop_rate.date() != datetime.now().date():
            #Random tỷ lệ rate
            allowed_values = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 2.6]
            new_rate = random.choice(allowed_values)
            ConversionRateMongoManager.create_update_shop_rate(guild_id=interaction.guild_id, rate=new_rate)
            conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=interaction.guild_id)
        elif conversion_rate != None and conversion_rate.last_reset_shop_rate == None:
            #Random tỷ lệ rate
            allowed_values = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 2.6]
            new_rate = random.choice(allowed_values)
            ConversionRateMongoManager.create_update_shop_rate(guild_id=interaction.guild_id, rate=new_rate)
            conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=interaction.guild_id)
        if conversion_rate:
            shop_rate = conversion_rate.shop_rate
        
        #Tính toán số tiền bán hộ vệ thần
        embed = discord.Embed(title=f"", description=f"Menu bán kỹ năng Hộ Vệ Thần", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Chọn kỹ năng của [{self.user_profile.guardian.ga_emoji} - **{self.user_profile.guardian.ga_name}**] để bán", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        view = SellSkillMenuView(user_profile=self.user_profile, user=interaction.user, rate=shop_rate)
        mess = await interaction.channel.send(embed=embed, view=view)
        view.message = mess
        await self.message.delete()
        return