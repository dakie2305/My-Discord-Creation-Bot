from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
from typing import List, Optional, Dict
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
from Handling.Economy.GA.ShopGuardianView import ShopGuardianView
from Handling.Economy.GA.ConfirmSellGuardianView import ConfirmSellGuardianView
from Handling.Economy.Inventory_Shop.ShopGlobalView import ShopGlobalView
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
import random
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

async def setup(bot: commands.Bot):
    await bot.add_cog(GuardianAngel(bot=bot))
    print("Guardian Angel is ready!")

class GuardianAngel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    ga_group = discord.app_commands.Group(name="ga", description="Các lệnh liên quan đến Guardian Angel!")
    #region ga slash
    @ga_group.command(name="sell", description="Bán Hộ Vệ Thần hiện tại!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def ga_sell_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            await interaction.followup.send(f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        elif user_profile.guardian == None:
            await interaction.followup.send(f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True)
            return
        #Tính toán số tiền bán hộ vệ thần
        money = int(user_profile.guardian.worth_amount * 30 / 100)
        if user_profile.guardian.level > 30:
            money += int(user_profile.guardian.worth_amount*user_profile.guardian.level/100)
        embed = discord.Embed(title=f"", description=f"Bán Hộ Vệ Thần", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Bạn có sẵn sàng bán Hộ Vệ Thần [{user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}**] với giá **{money}** {UtilitiesFunctions.get_emoji_from_loai_tien(user_profile.guardian.worth_type)} không?", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.set_footer(text=f"Hãy nâng cấp của Hộ Vệ Thần lên thật cao thì bán mới được giá nhé!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
        view = ConfirmSellGuardianView(money=money, money_type=user_profile.guardian.worth_type, guardian=user_profile.guardian, user=interaction.user)
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
        view.message = mess
        return
        
    @ga_sell_slash_command.error
    async def ga_sell_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
            
    @ga_group.command(name="meditate", description="Cho Hộ Vệ Thần tu thiền để hồi phục thể lực và tăng kinh nghiệm!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def ga_meditate_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            await interaction.followup.send(f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
            return
        elif user_profile.guardian == None:
            await interaction.followup.send(f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True)
            return
        
        if user_profile.guardian.last_meditation != None:
            time_window = timedelta(hours=1)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.guardian.last_meditation, time_window=time_window)
            if check:
                next_time = user_profile.guardian.last_meditation + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã cho Hộ Vệ Thần tu thiền rồi. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:t>!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
        
        random_bonus_exp = random.randint(15, 60)
        dignity_point = 10
        embed = discord.Embed(title=f"", description=f"Tiến Nhập Thiền Định", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Hộ Vệ Thần [{user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}**] đã tiến nhập thiền định.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hồi phục toàn bộ Mana {EmojiCreation2.MP.value}!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cộng **{random_bonus_exp}** điểm EXP cho Hộ Vệ Thần!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cộng **{dignity_point}** nhân phẩm!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id)
        ProfileMongoManager.update_main_guardian_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id, bonus_exp=random_bonus_exp)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id,user_id=interaction.user.id, guild_name="", user_display_name="", user_name="", dignity_point=dignity_point)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_meditation", date_value=datetime.now())
        await interaction.followup.send(embed=embed)
    
    @ga_meditate_slash_command.error
    async def ga_meditate_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
        