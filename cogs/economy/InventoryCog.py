from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from CustomEnum.RoleEnum import TrueHeavenRoleId
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
import random
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
import CustomFunctions
from discord.app_commands import Choice
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.Inventory_Shop.InventoryUseView import InventoryUseView
from Handling.Economy.Inventory_Shop.InventorySellView import InventorySellView
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager

async def setup(bot: commands.Bot):
    await bot.add_cog(InventoryEconomy(bot=bot))
    print("Inventory Economy is ready!")

class InventoryEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    inventory_group = discord.app_commands.Group(name="inventory", description="Các lệnh liên quan đến Inventory!")
    
    @inventory_group.command(name="use", description="Chọn và sử dụng vật phẩm trong kho đồ")
    @discord.app_commands.checks.cooldown(1, 10)
    async def inventory_use_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng sử dụng lệnh {SlashCommand.PROFILE.value} trước đã!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        elif user_profile.list_items == None or len(user_profile.list_items) == 0:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn không có vật phẩm để dùng!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        elif all(item.item_type == "gift" for item in user_profile.list_items):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn không có vật phẩm phù hợp để dùng!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        embed = discord.Embed(title=f"", description=f"Menu Sử Dụng Vật Phẩm", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hãy chọn những vật phẩm mà bạn đang sở hữu dưới đây để dùng!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        view = InventoryUseView(user_profile=user_profile, user=interaction.user)
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        view.message = mess
        return
        
    @inventory_use_slash_command.error
    async def inventory_use_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    
    @inventory_group.command(name="sell", description="Chọn và bán vật phẩm trong kho đồ. Hoặc bán hết vật phẩm.")
    @discord.app_commands.checks.cooldown(1, 10)
    async def inventory_sell_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng sử dụng lệnh {SlashCommand.PROFILE.value} trước đã!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        elif user_profile.list_items == None or len(user_profile.list_items) == 0:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn không có vật phẩm để bán!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Phải tồn tại chính quyền server thì mới làm được
        authority = ProfileMongoManager.get_authority(guild_id=interaction.guild.id)
        if authority == None:
            embed = discord.Embed(title=f"", description=f"Server vẫn chưa tồn tại Chính Quyền. Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            await interaction.followup.send(embed=embed)
            return

        authority_user = self.bot.get_guild(interaction.guild.id).get_member(authority.user_id)
        # Nếu không get được tức là authority không trong server
        if authority_user == None:
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã lưu vong khỏi server. Vui lòng dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=interaction.user.guild.id, user_id=authority.user_id)
            await interaction.followup.send(embed=embed)
            return
        
        #Kiểm xem chính quyền có mặc nợ không, có thì từ chức và phạt authority
        if ProfileMongoManager.is_in_debt(data= authority, copper_threshold=100000):
            embed = discord.Embed(title=f"", description=f"Chính Quyền đã nợ nần quá nhiều và tự sụp đổ. Hãy dùng lệnh {SlashCommand.VOTE_AUTHORITY.value} để bầu Chính Quyền mới!", color=0xddede7)
            authority.copper = -10000
            authority.silver = 0
            authority.gold = 0
            authority.darkium = 0
            ProfileMongoManager.update_profile_money_fast(guild_id= interaction.user.guild.id, data=authority)
            ProfileMongoManager.remove_authority_from_server(guild_id=interaction.user.guild.id)
            ProfileMongoManager.update_last_authority(guild_id=interaction.user.guild.id, user_id=authority.user_id)
            await interaction.followup.send(embed=embed)
            return
        
        
        
        shop_rate = 1.0
        conversion_rate = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=interaction.guild_id)
        if conversion_rate != None:
            shop_rate = conversion_rate.shop_rate
        
        embed = discord.Embed(title=f"", description=f"Menu Bán Vật Phẩm", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hãy chọn những vật phẩm mà bạn đang sở hữu dưới đây để bán nhé!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        view = InventorySellView(user_profile=user_profile, user=interaction.user, rate=shop_rate)
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        view.message = mess
        return
        
    @inventory_sell_slash_command.error
    async def inventory_sell_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)