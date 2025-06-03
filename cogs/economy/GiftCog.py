import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Economy.Authority.AuthorityView import AuthorityView
from enum import Enum
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomEnum.UserEnum as UserEnum
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
from Handling.Economy.Gift.GiftView import GiftView
from datetime import datetime, timedelta

async def setup(bot: commands.Bot):
    await bot.add_cog(GiftEconomy(bot=bot))
    print("Gift Economy is ready!")

class GiftEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #region gift
    @discord.app_commands.command(name="gift", description="Tặng vật phẩm cho người khác")
    @discord.app_commands.describe(user="Chọn user muốn tặng.")
    @discord.app_commands.checks.cooldown(1, 60)
    async def gift_slash_command(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        if user.id == interaction.user.id:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không được tặng cho bản thân!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        if user.bot:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không được tặng cho bot!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            embed = discord.Embed(title=f"", description=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã.", color=0xddede7)
            embed.add_field(name=f"", value=f"Ngoài ra, bạn cần phải kiếm tiền để vào mua đồ trong {SlashCommand.SHOP_GLOBAL.value} trước!", inline=False)
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        elif user_profile != None and (user_profile.list_items == None or len(user_profile.list_items) <= 0):
            embed = discord.Embed(title=f"", description=f"Bạn không có vật phẩm gì để tặng hết.", color=0xddede7)
            embed.add_field(name=f"", value=f"Bạn cần phải kiếm tiền để vào mua đồ trong {SlashCommand.SHOP_GLOBAL.value} trước!", inline=False)
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        elif self.contains_specific_item_types(user_profile.list_items) == False:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn không có quà phù hợp để tặng!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Không cho thực hiện nếu còn last_gift
        elif user_profile != None and user_profile.last_gift != None:
            time_window = timedelta(minutes=30)
            check = self.check_if_within_time_delta(input=user_profile.last_gift, time_window=time_window)
            if check:
                next_time = user_profile.last_gift + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã tặng quà rồi. Vui lòng thực hiện lại lệnh {SlashCommand.GIFT.value} vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=60)
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
        
        target_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=user.id)
        if target_profile == None:
            embed = discord.Embed(title=f"", description=f"{user.mention} Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", color=0xddede7)
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        embed = discord.Embed(title=f"", description=f"Tặng cho {user.mention}", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hãy chọn những vật phẩm mà bạn đang sở hữu dưới đây!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        view = GiftView(user_profile=user_profile, target_profile=target_profile, user=interaction.user, target_user=user)
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        view.message = mess
        return
    
    @gift_slash_command.error
    async def gift_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    
    def check_if_within_time_delta(self, input: datetime, time_window: timedelta):
        now = datetime.now()
        if now - time_window <= input <= now + time_window:
            return True
        else:
            return False
        
    def contains_specific_item_types(self, items):
        target_types = ["gift"]
        for item in items:
            if item.item_type in target_types:
                return True
        return False
    