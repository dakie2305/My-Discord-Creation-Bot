import discord
from discord.ext import commands
from discord.app_commands import Choice
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Economy.Couple.CouplePairView import CouplePairView
from Handling.Economy.Couple.CoupleBreakupView import CoupleBreakupView
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
from datetime import datetime, timedelta

async def setup(bot: commands.Bot):
    await bot.add_cog(CoupleCog(bot=bot))
    print("Couple is ready!")

class CoupleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    couple_group = discord.app_commands.Group(name="couple", description="Các lệnh liên quan đến Couple!")
    #region pair
    @couple_group.command(name="pair", description="Kết đôi với một người bất kỳ")
    @discord.app_commands.checks.cooldown(1, 30)
    @discord.app_commands.describe(user="Người mà bạn muốn thành đôi tri kỉ.")
    async def couple_pair_slash_command(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        if user.bot and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không thể thành đôi với bot được!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Kiểm tra xem cả hai đã là đôi của ai khác chưa
        first_user_check  = CoupleMongoManager.find_couple_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if first_user_check != None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn đã có bạn kết đôi, không được phép lập harem! Muốn kết đôi người khác thì chia tay người cũ đi!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        second_user_check  = CoupleMongoManager.find_couple_by_id(guild_id=interaction.guild_id, user_id=user.id)
        if second_user_check != None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Đối phương là hoa đã có chủ!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        
        first_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if first_profile == None:
            first_profile = ProfileMongoManager.create_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name)
        
        time_window = timedelta(days=3)
        if first_profile.last_breakup != None:
            check = UtilitiesFunctions.check_if_within_time_delta(input=first_profile.last_breakup, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng thêm xem chừng nào mới được thực hiện lại lệnh
                next_time = first_profile.last_breakup + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"💔 Bạn vừa chia tay người cũ không lâu. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:f> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
        
        
        
        second_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=user.id)
        if second_profile == None:
            second_profile = ProfileMongoManager.create_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name)
        
        if second_profile.last_breakup != None:
            check = UtilitiesFunctions.check_if_within_time_delta(input=second_profile.last_breakup, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng thêm xem chừng nào mới được thực hiện lại lệnh
                next_time = second_profile.last_breakup + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"💔 Đối phương vừa chia tay người cũ không lâu. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:f> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
        
        
        chosen_gift = None
        #Phải có ít nhất một gift mới có thể kết đôi
        if first_profile.list_items == None:
            view = SelfDestructView(timeout=60)
            embed = discord.Embed(title=f"Bạn phải mua ít nhất một món quà trong {SlashCommand.SHOP_GLOBAL.value} thì mới có thể tặng quà kết đôi!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        else:
            #Kiểm xem có gift không
            gift_available = False
            for item in first_profile.list_items:
                if item.item_type == "gift":
                    gift_available = True
                    break
            if gift_available == False:
                view = SelfDestructView(timeout=60)
                embed = discord.Embed(title=f"Bạn phải mua ít nhất một món quà trong {SlashCommand.SHOP_GLOBAL.value} thì mới có thể tặng quà kết đôi!",color=discord.Color.blue())
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
            #Chọn ra gift mắc nhất
            chosen_gift = self.get_most_expensive_item(items=first_profile.list_items)
        if chosen_gift == None:
            view = SelfDestructView(timeout=60)
            embed = discord.Embed(title=f"Không thể tìm được món quà phù hợp để kết đôi!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        #Tạo embed thành đôi
        embed = discord.Embed(title=f"", description=f"**{interaction.user.mention} đã bày tỏ tấm lòng với {user.mention}**", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"{interaction.user.mention} đã đem [{chosen_gift.emoji} - **{chosen_gift.item_name}**] để tặng cho {user.mention}!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        view = CouplePairView(user=interaction.user, user_profile=first_profile, target=user, target_profile=second_profile, chosen_gift=chosen_gift)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.old_message = mess
        return
        
    @couple_pair_slash_command.error
    async def couple_pair_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    #region breakup
    @couple_group.command(name="breakup", description="Chia tay với cặp đôi của bản thân")
    @discord.app_commands.checks.cooldown(1, 30)
    @discord.app_commands.describe(force="Đơn phương chia tay mà không cần sự đồng ý của đối phương.")
    async def couple_breakup_slash_command(self, interaction: discord.Interaction, force: bool = None):
        await interaction.response.defer(ephemeral=True)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        couple  = CoupleMongoManager.find_couple_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if couple == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn làm gì có người yêu mà đòi chia tay!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        target_id = None
        if interaction.user.id == couple.first_user_id:
            target_id = couple.second_user_id
        else:
            target_id = couple.first_user_id
        if force == None or force == False:
            await interaction.followup.send(content=f"Bạn đã quyết định chia tay với cặp đôi của mình!")
            channel = interaction.channel
            #Hiện embed cho đối phương trả lời
            embed = discord.Embed(title=f"", description=f"{interaction.user.mention} muốn chia tay với bạn", color=0xddede7)
            view = CoupleBreakupView(user=interaction.user, couple=couple, target_id=target_id)
            mess = await channel.send(embed=embed, view=view, content= f"<@{couple.first_user_id}> <@{couple.second_user_id}>")
            view.old_message = mess
        else:
            await interaction.followup.send(content=f"Bạn đã lạnh lùng chia tay với cặp đôi của mình!")
            channel = interaction.channel
            #Xoá couple và trừ 50 điểm nhân phẩm
            CoupleMongoManager.delete_couple_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
            ProfileMongoManager.update_last_breakup_now(guild_id=interaction.guild_id, user_id=couple.first_user_id)
            ProfileMongoManager.update_last_breakup_now(guild_id=interaction.guild_id, user_id=couple.second_user_id)
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_display_name="", user_name="", dignity_point=-50)
            await channel.send(f"{interaction.user.mention} đã nhẫn tâm chia tay thẳng thừng với <@{target_id}> một cách lạnh lùng.\n{interaction.user.mention} đã mất **50** điểm nhân phẩm!")
            return
        return
        
        
    @couple_breakup_slash_command.error
    async def couple_breakup_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)



    def get_most_expensive_item(self, items):
        type_multiplier = {
            "C": 1,
            "S": 100,
            "G": 10000,
            "D": 1000000
        }
        items.sort(key=lambda item: item.item_type == "gift" and item.item_worth_amount * type_multiplier[item.item_worth_type])
        return items[-1]
