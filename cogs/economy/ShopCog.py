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
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items, list_protection_items, list_support_items, list_attack_items, list_fishing_rod, list_legend_weapon_1, list_legend_weapon_2
from Handling.Economy.Inventory_Shop.ShopGlobalView import ShopGlobalView
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
import random
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions


async def setup(bot: commands.Bot):
    await bot.add_cog(ShopEconomy(bot=bot))
    print("Shop Economy is ready!")

class ShopEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.list_all_shops: Dict[str, List[Item]] = {}
    
    shop_group = discord.app_commands.Group(name="shop", description="Các lệnh liên quan đến Shop Item!")
    #region shop slash
    @shop_group.command(name="global", description="Hiển thị các mặt hàng trong thị trường toàn cầu")
    @discord.app_commands.checks.cooldown(1, 30)
    async def shop_global_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Phải tồn tại chính quyền server thì mới có shop
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

        #View đầu tiên luôn là gift shop
        self.list_all_shops["Shop Quà Tặng Cuộc Sống"] = list_gift_items
        self.list_all_shops["Shop Hàng Bổ Trợ"] = list_support_items
        self.list_all_shops["Shop Nông Trại"] = list_fishing_rod
        self.list_all_shops["Shop Bảo Hộ"] = list_protection_items
        self.list_all_shops["Shop Vũ Khí"] = list_attack_items
        
        
        if interaction.user.id == 315835396305059840 or (datetime.now().hour == 0 and datetime.now().minute == 0):
            dice = UtilitiesFunctions.get_chance(50)
            if dice:
                self.list_all_shops["Thất Truyền Huyền Khí Nhất Đẳng"] = list_legend_weapon_1
            else:
                self.list_all_shops["Thất Truyền Huyền Khí Nhị Đẳng"] = list_legend_weapon_2
        
        
        keys = list(self.list_all_shops.keys())  # Shop names
        # Tạo embed cho shop
        embed = discord.Embed(title=f"**Shop Quà Tặng Cuộc Sống**", description=f"Tỷ giá hiện tại: **{conversion_rate.shop_rate}**", color=discord.Color.blue())
        embed.add_field(name=f"", value=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬",inline=False)
        count = 1
        for item in self.list_all_shops["Shop Quà Tặng Cuộc Sống"]:
            embed.add_field(name=f"`{count}` {item.emoji} - {item.item_name}", value=f"{EmojiCreation2.SHINY_POINT.value} Giá: **{int(item.item_worth_amount*shop_rate)}**{self.get_emoji_money_from_type(type=item.item_worth_type)}\n{EmojiCreation2.SHINY_POINT.value} Rank tối thiểu: **{item.rank_required}**\n{EmojiCreation2.SHINY_POINT.value} {item.item_description}",inline=False)
            embed.add_field(name=f"", value=f"\n",inline=False)
            count+=1
        embed.set_footer(text=f"Trang 1/{len(keys)}")
        view = ShopGlobalView(rate= shop_rate,list_all_shops= self.list_all_shops)
        view.current_list_item = self.list_all_shops["Shop Quà Tặng Cuộc Sống"]
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
        view.message = mess
        
    @shop_global_slash_command.error
    async def shop_global_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
        
    def get_emoji_money_from_type(self, type: str):
        if type == "C": return EmojiCreation2.COPPER.value
        if type == "S": return EmojiCreation2.SILVER.value
        if type == "G": return EmojiCreation2.GOLD.value
        if type == "D": return EmojiCreation2.DARKIUM.value
