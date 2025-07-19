from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import discord
from discord.ext import commands
from Handling.Economy.Global import GlobalMongoManager
from Handling.Economy.Global.GlobalGaView import GlobalGaView
from Handling.Economy.Global.GlobalInventoryConfirmationView import GlobalInventoryConfirmationView
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
from typing import List, Optional, Dict
from Handling.Economy.GA.GuardianAngelAttackClass import GuardianAngelAttackClass
from Handling.Economy.GA.ConfirmSellGuardianView import ConfirmSellGuardianView
from Handling.Economy.GA.GaSellOptionsMenuView import GaSellOptionsMenuView
from Handling.Economy.GA.RankUpView import RankUpView
from Handling.Economy.GA.GaBattleView import GaBattleView
import random
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from discord.app_commands import Choice
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum


async def setup(bot: commands.Bot):
    await bot.add_cog(GlobalProfileCog(bot=bot))
    print("Global Profile is ready!")

class GlobalProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    global_group = discord.app_commands.Group(name="global", description="Các lệnh liên quan đến Global!")
    #region global inventory
    @global_group.command(name="inventory", description="Chuyển giao vật phẩm từ kho đồ cá nhân sang kho đồ liên thông!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def global_inventory_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        global_inventory = GlobalMongoManager.find_global_profile_by_id(user_id=interaction.user.id)
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        if global_inventory == None or global_inventory.enable_until < datetime.now():
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Bạn cần phải dùng Thẻ Liên Thông mua trong {SlashCommand.SHOP_GLOBAL.value} để kích hoạt chức năng Liên Thông!", ephemeral=True, view=view)
            view.message = mess
            return
        
        #Xuất view chọn lấy đồ từ kho liên server hoặc chuyển đồ từ kho cá nhân sang kho liên server
        embed = discord.Embed(title=f"Kho Đồ Liên Thông!", description="Kho Đồ Liên Thông là kho đồ tổng bộ, bạn có thể truy cập ở bất kỳ server nào! ",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Bạn có thể chuyển tối đa 10 vật phẩm từ kho đồ cá nhân vào Kho Đồ Liên Thông để sài ở server discord khác!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Chỉ mở khóa được tính năng này khi bạn đã mua và sử dụng Thẻ Liên Thông từ {SlashCommand.SHOP_GLOBAL.value}!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **Cá Nhân -> Liên Thông**: Chuyển vật phẩm từ kho đồ hiện tại vào Kho Đồ Liên Thông để sử dụng ở server khác!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **Liên Thông -> Cá Nhân**: Chuyển vật phẩm từ Kho Đồ Liên Thông vào kho đồ ở server hiện tại!", inline=False)
        footer_text = f"Để hiểu rõ cơ chế Liên Thông là gì thì hãy nhắn câu\n`global help`"
        embed.set_footer(text=footer_text)
        view = GlobalInventoryConfirmationView(user=interaction.user, user_profile=user_profile, guild_id=interaction.guild_id, global_inventory=global_inventory)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        return
        
    
    @global_inventory_slash_command.error
    async def global_inventory_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    #region global ga
    @global_group.command(name="ga", description="Chuyển giao Hộ Vệ Thần từ profile -> global")
    @discord.app_commands.checks.cooldown(1, 30)
    async def global_ga_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        global_profile = GlobalMongoManager.find_global_profile_by_id(user_id=interaction.user.id)
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        if global_profile == None or global_profile.enable_until < datetime.now():
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Bạn cần phải dùng Thẻ Liên Thông mua trong {SlashCommand.SHOP_GLOBAL.value} để kích hoạt chức năng Liên Thông!", ephemeral=True, view=view)
            view.message = mess
            return
        
        #Xuất view chọn lấy đồ từ kho liên server hoặc chuyển đồ từ kho cá nhân sang kho liên server
        embed = discord.Embed(title=f"Liên Thông Hộ Vệ Thần!", description="Liên Thông Hộ Vệ Thần là chức năng cho phép bạn có thể đồng bộ dữ liệu Hộ Vệ Thần của bản thân ở bất kỳ server nào!",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Bạn có thể đồng bộ chỉ số sức mạnh của Hộ Vệ Thần hiện tại để sài ở server discord khác!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Chỉ mở khóa được tính năng này khi bạn đã mua và sử dụng Thẻ Liên Thông từ {SlashCommand.SHOP_GLOBAL.value}!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **Profile -> Global**: Đồng bộ chỉ số và sức mạnh của Hộ Vệ Thần trong server lên global để có thể dùng Hộ Vệ Thần ở server khác!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **Global -> Profile**: Đồng bộ chỉ số và sức mạnh của Hộ Vệ Thần global vào trong server hiện tại!", inline=False)
        footer_text = f"Để hiểu rõ cơ chế Liên Thông Hộ Vệ Thần là gì thì hãy nhắn câu\n`global help`"
        embed.set_footer(text=footer_text)
        view = GlobalGaView(user=interaction.user, user_profile=user_profile, guild_id=interaction.guild_id, global_profile=global_profile)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        return
        
    
    @global_ga_slash_command.error
    async def global_ga_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    