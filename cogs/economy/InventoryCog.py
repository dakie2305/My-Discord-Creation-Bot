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
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.Inventory_Shop.InventoryUseView import InventoryUseView
from Handling.Economy.Inventory_Shop.InventorySellView import InventorySellView
from Handling.Economy.Inventory_Shop.InventoryAttackAuthorityInterceptView import InventoryAttackAuthorityInterceptView
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from datetime import datetime, timedelta
import asyncio
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager

async def setup(bot: commands.Bot):
    await bot.add_cog(InventoryEconomy(bot=bot))
    print("Inventory Economy is ready!")

class InventoryEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    inventory_group = discord.app_commands.Group(name="inventory", description="Các lệnh liên quan đến Inventory!")
    
    @inventory_group.command(name="use", description="Chọn và sử dụng vật phẩm trong kho đồ")
    @discord.app_commands.checks.cooldown(1, 60)
    async def inventory_use_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        # #Không cho dùng bot nếu không phải user
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
        elif self.contains_specific_item_types(user_profile.list_items) == False:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn không có vật phẩm phù hợp để dùng!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if user_profile.last_attack_item_used != None:
            time_window = timedelta(minutes=2)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.last_attack_item_used, time_window=time_window)
            if check:
                embed = discord.Embed(title=f"", description=f"🚫 Vui lòng đợi hai phút thì hãy sử dụng lại lệnh này!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
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
    
    def contains_specific_item_types(self, items):
        target_types = ["self_protection", "self_support", "attack"]
        for item in items:
            if item.item_type in target_types:
                return True
        return False
    
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
        
        if user_profile.last_attack_item_used != None:
            time_window = timedelta(minutes=2)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.last_attack_item_used, time_window=time_window)
            if check:
                embed = discord.Embed(title=f"", description=f"🚫 Vui lòng đợi hai phút thì hãy sử dụng lại lệnh này!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
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
    
    #region attack
    @inventory_group.command(name="attack", description="Chọn vũ khí để tấn công người khác")
    @discord.app_commands.checks.cooldown(1, 30)
    async def inventory_attack_slash_command(self, interaction: discord.Interaction, target: discord.Member):
        await interaction.response.defer(ephemeral=True)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if interaction.user.id == target.id:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không được chọn chính bản thân!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        if target.bot:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không được chọn bot!",color=discord.Color.blue())
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
        elif user_profile.dignity_point < 20:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Nhân phẩm bạn quá thấp, không được dùng vũ khí!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        elif user_profile.attack_item == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn không có vũ khí để dùng! Vui lòng dùng lệnh {SlashCommand.INVENTORY_USE.value} và dùng vũ khí nếu có",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        elif user_profile.last_attack_item_used != None:
            time_window = timedelta(hours=1)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.last_attack_item_used, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào timedelta xem chừng nào mới làm tiếp được
                work_next_time = user_profile.last_attack_item_used + time_window
                unix_time = int(work_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã dùng vũ khí tấn công người khác rồi. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
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
        
        target_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=target.id)
        if target_profile == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"{target.display_name} chưa dùng lệnh {SlashCommand.PROFILE.value}!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        elif target_profile.level <= 15:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"{target.display_name} cấp quá thấp, bạn không được tấn công người có rank thấp hơn 15!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        elif target_profile.level + 100 <= user_profile.level:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"{target.display_name} cấp quá thấp, bạn không được tấn công người có rank thấp hơn bản thân tận 100 cấp!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if "legend_" in user_profile.attack_item.item_id:
            if target_profile.level < 15:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Kẻ địch cấp quá thấp, chỉ nên nhắm vào những người trên cấp 15!",color=discord.Color.blue())
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
                view.message = mess
                return
            
        #Cập nhật last_use_attack
        ProfileMongoManager.update_last_attack_item_now(guild_id=interaction.guild_id, user_id=interaction.user.id)
        await interaction.followup.send(content="Bạn đã tấn công đối phương", ephemeral=True)
        await self.handling_attack(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority)
        #Xử lý tình huống tấn công
        
        
    @inventory_attack_slash_command.error
    async def inventory_attack_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    #region logic attack
    async def handling_attack(self, interaction: discord.Interaction, target: discord.Member, user_profile: Profile, target_profile: Profile, authority: Profile):
        is_legend_weapon = False
        if "legend_" in user_profile.attack_item.item_id:
            is_legend_weapon = True
        channel = interaction.channel
        view = InventoryAttackAuthorityInterceptView(user=interaction.user, user_profile=user_profile, target=target, target_profile=target_profile, authority_user=authority)
        embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã cầm [{user_profile.attack_item.emoji} - **{user_profile.attack_item.item_name}**] và lao đến {target.mention}!", color=0xc379e0)
        if user_profile.is_authority == False and is_legend_weapon == False:
            message = await channel.send(embed=embed, view=view, content=f"{target.mention}")
        else:
            message = await channel.send(embed=embed, view=None, content=f"{target.mention}")
        view.message = message
        await asyncio.sleep(20)
        if view.interrupted == True: return
        if is_legend_weapon:
            await self.handling_attack_legend(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, message= message)
            return
        
        embed.add_field(name=f"", value="▬▬▬ι═════>", inline=False)
        destroy_armor = True
        success = True
        #region crime_evident
        if user_profile.attack_item.item_id == "crime_evident":
            text = f"{interaction.user.mention} đã gài **{user_profile.attack_item.item_name}** lên người {target.mention}!"
            result = f"{target.mention} đã không kịp trở tay, và nó đã lọt vào túi đồ của mình!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                #Thêm crime_evident cho target
                ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=user_profile.attack_item, amount= 1)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        #region whipping
        elif user_profile.attack_item.item_id == "whipping":
            text = f"{interaction.user.mention} định dùng **{user_profile.attack_item.item_name}** để quật sml {target.mention} một cách không thương tiếc!"
            result = f"{target.mention} đã bị roi quất nhừ tử, và mất 10 nhân phẩm!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                #trừ 10 nhân phẩm cho target
                ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, dignity_point= -10)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        #region sword_1
        elif user_profile.attack_item.item_id == "sword_1":
            text = f"{interaction.user.mention} vung thanh **{user_profile.attack_item.item_name}** và chém thẳng vào {target.mention}!"
            result = f"{target.mention} đã bị đánh lên bờ xuống ruộng, và mất 25 nhân phẩm!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                #trừ 25 nhân phẩm cho target
                ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, dignity_point= -25)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        
        #region sword_2
        elif user_profile.attack_item.item_id == "sword_2":
            lost_money = int(target_profile.copper * 10 / 100)
            if lost_money < 0: lost_money = 10000 
            if lost_money > 1000000: lost_money = 1000000 
            text = f"{interaction.user.mention} dùng thanh **{user_profile.attack_item.item_name}** và lia thẳng vào đầu của {target.mention}!"
            result = f"{target.mention} đã bị chém gần chết, và làm rớt **{UtilitiesFunctions.shortened_currency(lost_money)}** {EmojiCreation2.COPPER.value}!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                #trừ tiền copper cho target
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, copper= -lost_money)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)

        #region sword_3
        elif user_profile.attack_item.item_id == "sword_3":
            lost_money = int(target_profile.copper * 10 / 100)
            if lost_money < 0: lost_money = 10000 
            if lost_money > 1000000: lost_money = 1000000
            dignity_point = 30
            dice = UtilitiesFunctions.get_chance(50)
            result = f""
            if dice:
                #Trừ tiền
                result = f"{target.mention} đã bị chém đến suýt tử nạn, và làm rớt **{UtilitiesFunctions.shortened_currency(lost_money)}** {EmojiCreation2.COPPER.value}!"
            else:
                #Trừ nhân phẩm
                result = f"{target.mention} đã bị chém đến suýt tử nạn, và đã mất **{dignity_point}** nhân phẩm vì phải cầu xin tha mạng!"
            text = f"Thanh kiếm **{user_profile.attack_item.item_name}** của {interaction.user.mention} vút lên, lưỡi thép sáng loáng cắt ngang không khí, mang theo một tiếng rít lạnh lẽo lia thẳng vào đầu của {target.mention}!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                if dice:
                    #trừ tiền copper cho target
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, copper= -lost_money)
                else:
                    #Trừ nhân phẩm target
                    ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, dignity_point= -dignity_point)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        
        #region sword_4
        elif user_profile.attack_item.item_id == "sword_4":
            lost_money = int(target_profile.copper * 10 / 100)
            if lost_money < 0: lost_money = 10000 
            if lost_money > 1000000: lost_money = 1000000
            percent = 10
            dice = UtilitiesFunctions.get_chance(50)
            result = f""
            if dice:
                #Trừ tiền
                result = f"Thanh kiếm cắm phập vào ngực {target.mention}, máu tươi chảy ra không ngừng, và đã làm rớt **{UtilitiesFunctions.shortened_currency(lost_money)}** {EmojiCreation2.COPPER.value}!"
            else:
                #Trừ % rank
                result = f"Thanh kiếm cắm phập vào tay {target.mention}, suýt chém đứt lìa nó, và phế đi cánh tay ấy. {target.mention} đã mất **{percent}%** rank!"
            text = f"Thanh kiếm **{user_profile.attack_item.item_name}** của {interaction.user.mention} vung vun vút như vũ bão, với sát khí chết người nhắm thẳng vào {target.mention}!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                if dice:
                    #trừ tiền copper cho target
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, copper= -lost_money)
                else:
                    #Trừ rank
                    old_progressing = target_profile.level_progressing
                    calculated_new_progressing = old_progressing - 100
                    level_reduction = 0
                    if calculated_new_progressing <= 10:
                        level_reduction = 1
                        calculated_new_progressing = 990
                    ProfileMongoManager.reduce_level_progressing(guild_id=interaction.guild_id,user_id=target.id,level_progressing=calculated_new_progressing, level_reduction_point=level_reduction)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        
        #region sword_5
        elif user_profile.attack_item.item_id == "sword_5":
            lost_money = int(target_profile.silver * 10 / 100)
            if lost_money < 0: lost_money = 1000
            if lost_money > 1000000: lost_money = 1000000
            percent = 15
            dice = UtilitiesFunctions.get_chance(50)
            result = f""
            if dice:
                #Trừ tiền
                result = f"Thanh kiếm cắm phập vào tay {target.mention}, máu tươi chảy ra không ngừng, và {target.mention} đã làm rớt **{UtilitiesFunctions.shortened_currency(lost_money)}** {EmojiCreation2.SILVER.value}!"
            else:
                #Trừ % rank
                result = f"Thanh kiếm cắm phập vào chân {target.mention}, suýt chém đứt lìa nó, và phế đi cái chân ấy. {target.mention} đã mất **{percent}%** rank!"
            text = f"Thanh kiếm **{user_profile.attack_item.item_name}** của {interaction.user.mention} cong vút và lao thẳng vào {target.mention} với tốc độ vượt trội!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                if dice:
                    #trừ tiền silver cho target
                    ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, silver= -lost_money)
                else:
                    #Trừ rank
                    old_progressing = target_profile.level_progressing
                    calculated_new_progressing = old_progressing - 150
                    level_reduction = 0
                    if calculated_new_progressing <= 10:
                        level_reduction = 1
                        calculated_new_progressing = 990
                    ProfileMongoManager.reduce_level_progressing(guild_id=interaction.guild_id,user_id=target.id,level_progressing=calculated_new_progressing, level_reduction_point=level_reduction)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        
        #region crime_knife
        elif user_profile.attack_item.item_id == "crime_knife":
            text = f"{interaction.user.mention} lia cây **{user_profile.attack_item.item_name}** và chém thẳng vào tay của {target.mention}!"
            result = f"{target.mention} đã bị chém trúng tay, suýt rớt bốn ngón tay và không thể phạm tội trong một giờ tới!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                #Update crime
                ProfileMongoManager.update_last_crime(guild_id=interaction.guild_id, user_id=target.id)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        #region cuff
        elif user_profile.attack_item.item_id == "cuff":
            text = f"{interaction.user.mention} đã dùng đến **{user_profile.attack_item.item_name}** và giam giữ {target.mention}!"
            result = f"{target.mention} đã bị còng tay và giam lệnh trong hai giờ tới!"
            success = True
            if target_profile.protection_item != None:
                result, success, destroy_armor = self.target_profile_protection(interaction=interaction, target=target, user_profile=user_profile, target_profile=target_profile, authority=authority, result=result)
            if success:
                #Update jail
                value = datetime.now() + timedelta(hours=2)
                ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=target.id, jail_time=value)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
            
        else:
            await channel.send(content=f"Darkie chưa code công dụng của vũ khí [{user_profile.attack_item.emoji} - **{user_profile.attack_item.item_name}**]")
            return
        
        #Xoá amour của target
        if target_profile.protection_item != None and destroy_armor:
            #gỡ giáp
            ProfileMongoManager.equip_protection_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.protection_item, unequip= True)
            #xoá giáp
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.protection_item, amount= -1)
        
        #Gỡ vật phẩm đang dùng
        ProfileMongoManager.equip_attack_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=user_profile.attack_item, unequip=True)
        #Xoá vật phẩm
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=user_profile.attack_item, amount= -1)
        #Cập nhật last_use_attack
        ProfileMongoManager.update_last_attack_item_now(guild_id=interaction.guild_id, user_id=interaction.user.id)
        #Trừ 20 điểm nhân phẩm của người tấn công
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, dignity_point=-20)
        
        #Cộng exp cho người tấn công
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        embed.add_field(name=f"", value="▬▬▬ι═════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Ngoài ra, vì đã dùng vũ khí tấn công nên {interaction.user.mention} đã mất thêm **20** điểm nhân phẩm", inline=False)
        await message.edit(embed=embed, view=None, content=f"{target.mention}")
        return
    
    
    
    def target_profile_protection(self, interaction: discord.Interaction, target: discord.Member, user_profile: Profile, target_profile: Profile, authority: Profile, result: str):
        result = result
        #Nếu là armor_protection_1 thì 50% success
        success = True
        destroy_armor = True
        if target_profile.protection_item.item_id == "armor_protection_1":
            dice = UtilitiesFunctions.get_chance(50)
            if dice == False:
                result = f"May là {target.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên kịp thời chạy đi!"
                success = False
            else:
                result = f"Bộ giáp [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] của {target.mention} đã không thể ngăn dược và đã hỏng!"
        elif target_profile.protection_item.item_id == "armor_protection_2":
            success = False
            result = f"May là {target.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên không hề hấn gì cả!"
        elif target_profile.protection_item.item_id == "armor_protection_3":
            success = False
            result = f"{target.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên không hề hấn gì, và còn khiến {interaction.user.mention} mất thêm **20** nhân phẩm!"
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, dignity_point=-20)
        elif target_profile.protection_item.item_id == "armor_protection_4":
            #Phá giáp và trừ copper của kẻ tấn công
            success = False
            fine_money = int(user_profile.copper * 10 / 100)
            if fine_money < 0: fine_money = 10000 
            if fine_money > 100000: fine_money = 100000 
            result = f"{target.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên không hề hấn gì, và còn khiến {interaction.user.mention} mất thêm **{fine_money}** {EmojiCreation2.COPPER.value}!"
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, copper=-fine_money)
        elif target_profile.protection_item.item_id == "armor_protection_5":
            #Phá giáp và trừ silver hoặc trừ 5% tỉ lệ rank của kẻ tấn công
            success = False
            dice = UtilitiesFunctions.get_chance(50)
            if dice:
                #Trừ silver
                fine_money = int(user_profile.silver * 10 / 100)
                if fine_money < 0: fine_money = 100 
                if fine_money > 100000: fine_money = 100000 
                result = f"{target.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên không hề hấn gì, và còn khiến{interaction.user.mention} mất thêm **{fine_money}** {EmojiCreation2.SILVER.value}!"
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, copper=-fine_money)
            else:
                #Trừ level progress
                percent = 10
                result = f"{target.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên không hề hấn gì, và còn khiến{interaction.user.mention} mất đi {percent}% rank!"
                old_progressing = user_profile.level_progressing
                calculated_new_progressing = old_progressing - 100
                level_reduction = 0
                if calculated_new_progressing <= 10:
                    level_reduction = 1
                    calculated_new_progressing = 990
                ProfileMongoManager.reduce_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id, level_progressing=calculated_new_progressing, level_reduction_point=level_reduction)
        else:
            #10% success nếu là giáp khác
            dice = UtilitiesFunctions.get_chance(10)
            if dice:
                success = False
                result = f"May là {target.mention} đã mặc sẵn [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**] nên kịp thời chạy đi!"
            else:
                success = True
                result = result
                destroy_armor = False
        return result, success, destroy_armor

#region handling_attack_legend
    async def handling_attack_legend(self, interaction: discord.Interaction, target: discord.Member, user_profile: Profile, target_profile: Profile, authority: Profile, message: discord.Message):
              
        embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã cầm [{user_profile.attack_item.emoji} - **{user_profile.attack_item.item_name}**] và lao đến {target.mention}!", color=0xc379e0)
        embed.add_field(name=f"", value="▬▬▬ι═════>", inline=False)
        #region legend_axe
        if user_profile.attack_item.item_id == "legend_axe":
            text = f"{interaction.user.mention} vung thẳng thanh **{user_profile.attack_item.item_name}** để đánh {target.mention} mạnh đến nỗi từng nhát chém đều như chặt đứt thần hồn lẫn hộ giáp của {target.mention}!"
            result = f"{target.mention} đã bị rìu bổ đến mức kinh động thần hồn và run rẩy như cầy sấy!"
            if target_profile.protection_item != None:
                result = f"{target.mention} đã bị rìu bổ mạnh đến mức tan nát thần hồn và vỡ tan tất cả giáp [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**]!"
            
            #Xoá toàn bộ những armour mà target đang mặc
            if target_profile.protection_item != None:
                ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.protection_item, amount= -99)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        
        elif user_profile.attack_item.item_id == "legend_axe_2":
            text = f"{interaction.user.mention} vung thẳng thanh **{user_profile.attack_item.item_name}** để đánh {target.mention} mạnh đến nỗi từng nhát chém đều như chặt đứt thần hồn lẫn hộ giáp của {target.mention}!"
            result = f"{target.mention} đã bị rìu bổ đến mức bị phế công và mất tận 10 cấp độ!"
            #trừ 10 cấp
            ProfileMongoManager.reduce_level_progressing(guild_id=interaction.guild_id, user_id=target.id, level_progressing=target_profile.level_progressing, level_reduction_point=10)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
            
        elif user_profile.attack_item.item_id == "legend_karambit":
            text = f"{interaction.user.mention} lia thanh **{user_profile.attack_item.item_name}** toả sáng huyền ảo, những hoa văn cổ xưa trên đó như bừng sáng và vụt thẳng tới vũ khí của {target.mention}!"
            result = f"{target.mention} đã bị chém đến mất vũ khí đang cầm!"
            
            if target_profile.attack_item != None:
                result = f"{target.mention} đã bị chém đến mất toàn bộ vũ khí [{target_profile.attack_item.emoji} - **{target_profile.attack_item.item_name}**]!"
                #Gỡ vật phẩm đang dùng
                ProfileMongoManager.equip_attack_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.attack_item, unequip=True)
                ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.attack_item, amount= -99)
            elif target_profile.list_items!= None and len(target_profile.list_items) > 0:
                #Chọn ra một vũ khí sẽ bị phế
                chosen_item = None
                for item in target_profile.list_items:
                    if item.item_type == "attack":
                        chosen_item = item
                        break
                if chosen_item != None:
                    result = f"{target.mention} đã bị chém đến mất toàn bộ vũ khí [{chosen_item.emoji} - **{chosen_item.item_name}**]!"
                    ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=chosen_item, amount= -99)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
            
        elif user_profile.attack_item.item_id == "legend_scythe":
            text = f"{interaction.user.mention} lia **{user_profile.attack_item.item_name}** vào đầu của {target.mention} nhằm gặt và xé toàn linh hồn của {target.mention}!"
            result = f"{target.mention} đã bị lưỡi liềm vung đến mất tất cả mọi vụ mùa!"
            #Nếu có seed thì huỷ hết, huỷ luôn cả plant
            ProfileMongoManager.update_plant(guild_id=interaction.guild_id, user_id=target.id, plant=None)
            if target_profile.list_items!= None and len(target_profile.list_items) > 0:
                for item in target_profile.list_items:
                    if item.item_type == "seed":
                        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=item, amount= -99)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
            
        elif user_profile.attack_item.item_id == "legend_spear_1":
            text = f"Với một động tác uyển chuyển, {interaction.user.mention} đâm thẳng **{user_profile.attack_item.item_name}** vào đầu của {target.mention} với sức mạnh kinh thiên động địa!"
            result = f"{target.mention} đã bị đóng băng toàn bộ mệnh lệnh trong vòng ít nhất vài tiếng tới!"
            #Update lại thời gian của tất cả lệnh
            value = datetime.now() + timedelta(hours=4)
            ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=target.id, jail_time=value)
            ProfileMongoManager.update_last_crime(guild_id=interaction.guild_id, user_id=target.id, last_crime=value)
            ProfileMongoManager.update_last_attack_item_now(guild_id=interaction.guild_id, user_id=target.id)
            ProfileMongoManager.update_last_fishing_now(guild_id=interaction.guild_id, user_id=target.id)
            ProfileMongoManager.update_last_riot_now(guild_id=interaction.guild_id, user_id=target.id)
            ProfileMongoManager.update_last_work_now(guild_id=interaction.guild_id, user_id=target.id)
            ProfileMongoManager.update_last_gift_now(guild_id=interaction.guild_id, user_id=target.id)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        
        elif user_profile.attack_item.item_id == "legend_spear_2":
            text = f"Với một động tác thuần thục điêu luyện, {interaction.user.mention} vung **{user_profile.attack_item.item_name}** nhanh như chớp nhắm thẳng vào ngực {target.mention} với sức mạnh hủy diệt!"
            result = f"{target.mention} đã bị đâm liên tiếp đến mức nát cả bộ giáp đang dùng!"
            if target_profile.protection_item != None:
                result = f"{target.mention} đã bị đâm liên tiếp đến mức nát [{target_profile.protection_item.emoji} - **{target_profile.protection_item.item_name}**]!"
                #Gỡ vật phẩm đang dùng
                ProfileMongoManager.equip_protection_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.protection_item, unequip=True)
                ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.protection_item, amount= -99)
            elif target_profile.list_items!= None and len(target_profile.list_items) > 0:
                #Chọn ra một bộ giáp sẽ bị phế
                chosen_item = None
                for item in target_profile.list_items:
                    if item.item_type == "self_protection":
                        chosen_item = item
                        break
                if chosen_item != None:
                    result = f"{target.mention} đã bị đâm nhiều đến mức nát hết [{chosen_item.emoji} - **{chosen_item.item_name}**]!"
                    ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=chosen_item, amount= -99)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
            
        elif user_profile.attack_item.item_id == "legend_sword_1":
            text = f"Với tốc độ khủng bố, {interaction.user.mention} lia thanh **{user_profile.attack_item.item_name}** rạch qua không khí và nhắm thẳng vào đầu {target.mention} với đường kiếm hoàn hảo!"
            
            money = 1
            money_type = EmojiCreation2.COPPER.value
            if target_profile.darkium >0:
                money = int(target_profile.darkium*10/100)
                if money > 1000: money = 1000
                money_type = EmojiCreation2.DARKIUM.value
            elif target_profile.gold >0:
                money = int(target_profile.gold*10/100)
                if money > 100000: money = 100000
                money_type = EmojiCreation2.GOLD.value
            elif target_profile.silver > 0:
                money = int(target_profile.silver*10/100)
                if money > 1000000: money = 1000000
                money_type = EmojiCreation2.SILVER.value
            elif target_profile.copper > 0:
                money = int(target_profile.copper*10/100)
                if money > 100000000: money = 100000000
                money_type = EmojiCreation2.COPPER.value
            if money <= 0: money = 1
            
            if money_type == EmojiCreation2.COPPER.value:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, copper=-money)
            elif money_type == EmojiCreation2.SILVER.value:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, silver=-money)
            elif money_type == EmojiCreation2.GOLD.value:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, gold=-money)
            elif money_type == EmojiCreation2.DARKIUM.value:
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, darkium=-money)
            result = f"{target.mention} chưa kịp phản ứng đã bị một nhát chém chính xác vào vai, máu tươi tuôn trào và đã mất **{UtilitiesFunctions.shortened_currency(money)}** {money_type}!"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
            
        elif user_profile.attack_item.item_id == "legend_sword_2":
            text = f"Với tốc độ khủng bố, {interaction.user.mention} vung thanh **{user_profile.attack_item.item_name}** với tất cả sức mạnh của mình và cắt xuyên qua lớp giáp {target.mention}!"
            result = f"Khuôn mặt {target.mention} tái nhợt, buộc phải quỳ gối xin tha mạng, và đã bị chém cho phế hết tất cả tiến trình, và mất toàn bộ nhân phẩm!"
            bonus = 50
            bonus += target_profile.dignity_point*2
            bonus += target_profile.level_progressing
            #Cộng exp thêm cho người tung đòn
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=user_profile.user_id, bonus_exp=bonus)
            ProfileMongoManager.update_plant_date(guild_id=interaction.guild_id, user_id=target.id)
            ProfileMongoManager.reduce_level_progressing(guild_id=interaction.guild_id, user_id=target.id, level_progressing=0, level_reduction_point=0)
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, dignity_point=-1000)
            CoupleMongoManager.set_love_point_value(guild_id=interaction.guild_id, user_id=target.id, love_point=0)
            CoupleMongoManager.set_love_progressing_value(guild_id=interaction.guild_id, user_id=target.id, love_progressing=0)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        elif user_profile.attack_item.item_id == "legend_sword_3":
            text = f"Với tốc độ thần sầu, {interaction.user.mention} vung thanh **{user_profile.attack_item.item_name}** với tất cả sức mạnh của mình và cắt nát toàn bộ vật phẩm quà tặng của {target.mention}!"
            result = f"{target.mention} gào thét trong đau đớn, nhưng {interaction.user.mention} vẫn không dừng lại, lưỡi kiếm tiếp tục đâm sâu hơn!"
            #Nếu có gift thì huỷ hết
            if target_profile.list_items!= None and len(target_profile.list_items) > 0:
                for item in target_profile.list_items:
                    if item.item_type == "gift":
                        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=item, amount= -99)
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=result, inline=False)
        
        else:
            await interaction.channel.send(content=f"Darkie chưa code công dụng của vũ khí [{user_profile.attack_item.emoji} - **{user_profile.attack_item.item_name}**]")
            return
        
        
        #Xoá amour của target
        if target_profile.protection_item != None:
            #gỡ giáp
            ProfileMongoManager.equip_protection_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.protection_item, unequip= True)
            #xoá giáp
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=target.id, user_name=target.name, user_display_name=target.display_name, item=target_profile.protection_item, amount= -1)
        
        #Gỡ vật phẩm đang dùng
        ProfileMongoManager.equip_attack_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=user_profile.attack_item, unequip=True)
        #Xoá vật phẩm
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=user_profile.attack_item, amount= -1)
        #Cập nhật last_use_attack
        ProfileMongoManager.update_last_attack_item_now(guild_id=interaction.guild_id, user_id=interaction.user.id)
        #Trừ 20 điểm nhân phẩm của người tấn công
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, dignity_point=-20)
        
        #Cộng exp cho người tấn công
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        embed.add_field(name=f"", value="▬▬▬ι═════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Ngoài ra, vì đã dùng vũ khí tấn công nên {interaction.user.mention} đã mất thêm **20** điểm nhân phẩm", inline=False)
        await message.edit(embed=embed, view=None, content=f"{target.mention}")
        return
    