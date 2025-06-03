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
from Handling.Economy.Couple.CoupleMarryView import CoupleMarryView
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
from datetime import datetime, timedelta
import random

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
        
        if user.id == interaction.user.id:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không thể tự thành đôi với bản thân được!",color=discord.Color.blue())
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
        # if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
        #     view = SelfDestructView(timeout=30)
        #     embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
        #     mess = await interaction.followup.send(embed=embed, view=view)
        #     view.message = mess
        #     return
        
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
            channel = interaction.channel
            #Hiện embed cho đối phương trả lời
            embed = discord.Embed(title=f"", description=f"{interaction.user.mention} muốn chia tay với bạn", color=0xddede7)
            view = CoupleBreakupView(user=interaction.user, couple=couple, target_id=target_id)
            mess = await channel.send(embed=embed, view=view, content= f"<@{couple.first_user_id}> <@{couple.second_user_id}>")
            view.old_message = mess
            await interaction.followup.send(content=f"Bạn đã quyết định chia tay với cặp đôi của mình!")
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

    #region intimate
    @couple_group.command(name="intimate", description="Thân mật cùng với đối phương")
    @discord.app_commands.checks.cooldown(1, 30)
    async def couple_intimate_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
            else:
                ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time=None)
        
        couple  = CoupleMongoManager.find_couple_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if couple == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn làm gì có người yêu đâu?!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        if couple.last_love_action != None:
            time_window = timedelta(minutes=30)
            check = UtilitiesFunctions.check_if_within_time_delta(input=couple.last_love_action, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào 1h xem chừng nào mới làm tiếp
                work_next_time = couple.last_love_action + time_window
                unix_time = int(work_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã hẹn hò rồi. Vui lòng thực hiện lại lệnh {SlashCommand.COUPLE_INTIMATE.value} vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view)
                return
        
        
        target_id = None
        if interaction.user.id == couple.first_user_id:
            target_id = couple.second_user_id
        else:
            target_id = couple.first_user_id
            
        #"user.id và target_id quyết định chọn đi... để cải thiện tình cảm cả hai "
        random_date_choice = ["hẹn hò", "hâm nóng tình cảm", "ấy ấy", "chơi bởi", "quẩy bar", "ăn uống", "xập xình", "dẫy phố", "phá làng phá xóm", "hò hẹn", "chơi vòng vòng", "dạo phố", "lên bar", "cafe", "triển lãm lịch sử", "tham gia show của anh Jack 97", "gặp anh Jack 97"]
        #"ở..."
        random_date_place = ["địa ngục", "Đà Lạt", "biển", "văn phòng Công An Tỉnh", "Nha Trang", "Vũng Tàu", "Phan Thiết", "Phố Đi Bộ", "công viên gần nhà", "khách sạn", "nhà nghỉ","nhà trọ", "Mũi Né", "Cam Ranh", "Thái Lan", "Cà Mau", "Trà Vinh", "Mỹ", "Anh", "nghĩa địa", "nghĩa trang", "đồi thông hai mộ", "nhà ma", "đại học FPT", "đại học HUTECH", "quán net gần nhà"]
        #succes
        random_success_message = [
            "{second_person} đã cảm thấy rất ấn tượng với vẻ đẹp của nơi này, và ôm {first_person} thật lâu",
            "{second_person} như bị hớp hồn bởi nơi này, và hôn {first_person} thật lâu",
            "{first_person} đã hôn {second_person} thật sâu trong khung cảnh lãng mạn này",
            "{second_person} rất thích nơi tuyệt vời này",
            "{second_person} và {first_person} đã rất hạnh phúc ở nơi đây",
            "{first_person} đã nhẹ nhàng đặt một nụ hôn lên má {second_person}",
            "{first_person} đã dành tặng {second_person} một bó hoa hồng đỏ thắm",
            "{first_person} đã cùng {second_person} ăn bữa tối vui vẻ ở nơi đây",
            "{second_person} cùng {first_person} du ngoạn nơi này và dành nhiều thời gian yên bình bên nhau",
            "{second_person} đã cùng {first_person} \"nồng thắm\" với nhau tại nơi tuyệt vời này",
            "{second_person} rất trầm trồ vì nơi này, và đã cùng {first_person} dành thời gian \"ân ái\" với nhau tại đây",
        ]
        #Fail
        random_fail_message = [
            "{second_person} đã vô tình làm đổ nước lên {first_person} và làm hỏng chiếc điện thoại mới của {first_person}",
            "{first_person} và {second_person} đã bị lạc đường và phải đi bộ về nhà trong đêm tối",
            "{second_person} đã vô tình làm hỏng món quà mà {first_person} chuẩn bị",
            "{first_person} và {second_person} đã mắc mưa lớn và ướt sũng người",
            "{first_person} và {second_person} đã bị  fan anh Jack 97 cướp mất tiền",
            "{second_person} đã vô tình gọi nhầm tên người yêu cũ trước mặt {first_person}",
            "{second_person} đã bị người yêu cũ bắt gặp khi đang hẹn hò với {first_person}",
            "{first_person} đã nói một điều gì đó rất ngớ ngẩn và khiến {second_person} cảm thấy xấu hổ",
            "{second_person} đã không xuất hiện đúng hẹn, khiến {first_person} phải chờ đợi rất lâu",
        ]
        date_choice = random.choice(random_date_choice)
        date_place = random.choice(random_date_place)
        is_success = UtilitiesFunctions.get_chance(70)
        result = random.choice(random_success_message)
        bonus_love_point = 10
        bonus_love_rank_exp = random.randint(20, 60)
        if is_success == False:
            result = random.choice(random_fail_message)
            bonus_love_point = bonus_love_point*(-1)
        result = result.replace("{first_person}", interaction.user.mention)
        result = result.replace("{second_person}", f"<@{target_id}>")
        
        text = f"Trong buổi hẹn tới, {interaction.user.mention} và <@{target_id}> đã quyết định chọn đi {date_choice} ở {date_place}."
        text += f"\n{result}."
        embed = discord.Embed(title=f"", description=f"", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"{text}", inline=False)
        embed.add_field(name=f"", value=f"**Kết quả buổi hẹn:**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **{bonus_love_rank_exp}** Điểm thăng hoa cảm xúc", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **{bonus_love_point}** Điểm thân mật", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        
        CoupleMongoManager.update_love_point(guild_id=interaction.guild_id,user_id=interaction.user.id, love_point=bonus_love_point)
        CoupleMongoManager.update_love_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id, bonus_exp=bonus_love_rank_exp)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, dignity_point=5)
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=target_id)
        #Cập nhật lại thời gian
        CoupleMongoManager.update_last_date_time_now(guild_id=interaction.guild_id, user_id=interaction.user.id, is_last_love_action=True)
        await interaction.followup.send(embed=embed)
    
    @couple_intimate_slash_command.error
    async def couple_intimate_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    #region fight
    @couple_group.command(name="fight", description="Cãi vã với đối phương")
    @discord.app_commands.checks.cooldown(1, 30)
    async def couple_fight_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
            else:
                ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time=None)
        
        couple  = CoupleMongoManager.find_couple_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if couple == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn làm gì có người yêu đâu?!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        if couple.last_fight_action != None:
            time_window = timedelta(hours=1)
            check = UtilitiesFunctions.check_if_within_time_delta(input=couple.last_fight_action, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào 1h xem chừng nào mới làm tiếp
                work_next_time = couple.last_fight_action + time_window
                unix_time = int(work_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã cãi nhau rồi. Vui lòng thực hiện lại lệnh {SlashCommand.COUPLE_FIGHT.value} vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view)
                return
        target_id = None
        if interaction.user.id == couple.first_user_id:
            target_id = couple.second_user_id
        else:
            target_id = couple.first_user_id
        
        #"user.id cảm thấy...
        random_hard_feeling = [
            "không thích cách ăn mặc của {second_person}",
            "không ưa tính hỏi nhiều về {second_person}",
            "không vui về thái độ cọc cằn của {second_person}",
            "không vui gì khi thấy {second_person} làm hư đồ mình",
            "không thích khi thấy {second_person} còn lưu ảnh người yêu cũ",
            "bực bội vì đã thấy {second_person} nói chuyện với người yêu cũ",
            "khó chịu vì {second_person} chiến tranh lạnh với mình",
            "khó chịu khi {second_person} làm mất cái áo của mình",
            "khó chịu khi {second_person} làm vỡ màn hình điện thoại",
            "đau lòng khi {second_person} không nhớ ngày sinh của mình",
            "khó chịu vì cảm thấy bị {second_person} xem nhẹ, không được đối xử công bằng",
            "khó chịu vì cảm thấy bị {second_person} so sánh với người cũ",
            "bực bội vì {second_person} làm phiền trong lúc làm việc",
            "không vui vì {second_person} quấy rầy giấc ngủ",
            "không vui vì {second_person} kiểm soát quá mức",
            "không vui vì luôn bị {second_person} đổ lỗi",
            "buồn vì luôn bị {second_person} chế giễu",
            "buồn vì {second_person} hứa hẹn nhưng không thực hiện",
            "buồn vì {second_person} tạo cảm giác cô đơn, lạc lõng trong mối quan hệ",
            ]
        
        #"và quyết định..."
        random_decision_message = [
            "nói cho ra lẽ",
            "chửi một trận thật nặng",
            "hai mặt một lời cho rõ ràng",
            "nói chuyện thẳng mặt cho thật rõ sự tình",
            "nói bóng nói gió về chuyện đó",
            "tỏ rõ thái độ không hài lòng",
            "chiến tranh lạnh và không muốn nói chuyện nữa",
            "nói xấu về {second_person} với bạn bè",
            "nặng nhẹ về sự việc đó",
            "nhẹ nhàng bảo ban về chuyện đó",
            "nhẹ nhàng nói chuyện cho ra lẽ",
            "bỏ đi mà không nói lời nào.",
            "bỏ ăn, bỏ ngủ.",
            "tự cô lập bản thân",
            "cố tình gây sự với {second_person}",
        ]
        
        #success
        random_success_message = [
            "{second_person} đã hiểu rõ tại sao {first_person} cảm thấy vậy và ôm {first_person} thật chặt",
            "{second_person} đã thấu hiểu nỗi tình của {first_person}",
            "{second_person} đã ôm hôn {first_person} thật lâu vì hối hận",
            "{second_person} đã hứa sẽ thay đổi và không tái phạm lỗi lầm",
            "{first_person} và {second_person} đã cùng nhau tìm ra giải pháp cho vấn đề",
            "{first_person} đã tha thứ cho {second_person} và cả hai đã ôm nhau thật chặt",
            "{second_person} đã tặng {first_person} một món quà nhỏ để thể hiện sự hối hận",
            "{first_person} và {second_person} đã ngồi xuống, tâm sự thật lòng với nhau và giải quyết hiểu lầm",
            "{second_person} đã nấu cho {first_person} một bữa ăn ngon để bày tỏ lời xin lỗi",
            "{second_person} đã tổ chức một buổi hẹn hò lãng mạn để làm lành",
            "{first_person} và {second_person} đã cùng nhau chia sẻ những nỗi sợ hãi và mong muốn của mình",
            "{first_person} và {second_person} đã nhận ra rằng tình cảm của nhau mới là thật sự quan trọng",
            "{first_person} và {second_person} đã cùng nhau nấu ăn, cười đùa và hàn gắn mối quan hệ",
            "{first_person} và {second_person} đã cùng nhau ngắm sao trời và trò chuyện tâm sự",
        ]
        #Fail
        random_fail_message = [
            "{second_person} đã cảm thấy bị xúc phạm bởi lời nói của {first_person}",
            "{first_person} cảm thấy như thể {second_person} không hề lắng nghe mình và chỉ hứa suông",
            "{second_person} không vui với thái độ chỉ trích của {first_person}",
            "{second_person} thấy buồn vì {first_person} đã khác trước",
            "{second_person} thấy buồn vì {first_person} trông như không còn quan tâm mình",
            "{second_person} giận ngược lại {first_person}",
            "{second_person} đã không chịu xin lỗi {first_person}",
            "{first_person} và {second_person} đã không thể tìm được tiếng nói chung",
            "{first_person} và {second_person} cãi nhau to thêm chỉ vì chuyện đó",
            "{first_person} đã mất niềm tin vào tình cảm của {second_person}",
            "{first_person} và {second_person} đã không thể hàn gắn mối quan hệ",
            "{second_person} trong cơn tức giận đã ném đồ đạc",
            "{second_person} đã bỏ đi mà không thèm chịu nghe giải thích",
            "{second_person} chỉ xin lỗi hời hợt cho có, và {first_person} cảm thấy mệt mỏi với mối quan hệ này",
            "{second_person} đã cố tình làm tổn thương {first_person} bằng cách nhắc lại những lỗi lầm trong quá khứ",
        ]
        hard_feeling = random.choice(random_hard_feeling)
        decision_message = random.choice(random_decision_message)
        is_success = UtilitiesFunctions.get_chance(50)
        result = random.choice(random_success_message)
        bonus_love_point = 30
        bonus_love_rank_exp = random.randint(50, 100)
        if is_success == False:
            result = random.choice(random_fail_message)
            bonus_love_point = 20
            bonus_love_point = bonus_love_point*(-1)
        hard_feeling = hard_feeling.replace("{first_person}", interaction.user.mention)
        hard_feeling = hard_feeling.replace("{second_person}", f"<@{target_id}>")
        decision_message = decision_message.replace("{first_person}", interaction.user.mention)
        decision_message = decision_message.replace("{second_person}", f"<@{target_id}>")
        result = result.replace("{first_person}", interaction.user.mention)
        result = result.replace("{second_person}", f"<@{target_id}>")
        
        text = f"{interaction.user.mention} cảm thấy {hard_feeling} và quyết định sẽ {decision_message}."
        text += f"\n{result}."
        embed = discord.Embed(title=f"", description=f"", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"{text}", inline=False)
        embed.add_field(name=f"", value=f"**Kết quả:**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **{bonus_love_rank_exp}** Tỉ lệ thăng hoa cảm xúc", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **{bonus_love_point}** Điểm thân mật", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        
        CoupleMongoManager.update_love_point(guild_id=interaction.guild_id,user_id=interaction.user.id, love_point=bonus_love_point)
        CoupleMongoManager.update_last_date_time_now(guild_id=interaction.guild_id, user_id=interaction.user.id, is_last_fight_action=True)
        CoupleMongoManager.update_love_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id, bonus_exp=bonus_love_rank_exp)
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=target_id)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, user_id=target_id, guild_name="", user_name="", user_display_name="", dignity_point=5)
        await interaction.followup.send(embed=embed)
    
    @couple_fight_slash_command.error
    async def couple_fight_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    #region marry
    @couple_group.command(name="marry", description="Cưới cặp đôi của mình!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def couple_marry_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                mess = await interaction.followup.send(embed=embed, view=view)
                view.message = mess
                return
            else:
                ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time=None)
        
        if user_profile.list_items == None or len(user_profile.list_items) == 0:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng dùng lệnh {SlashCommand.SHOP_GLOBAL.value} để mua Nhẫn Kim Cương!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        couple  = CoupleMongoManager.find_couple_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if couple == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn làm gì có người yêu đâu?!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        elif couple.date_married != None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Bạn đã làm đám cưới rồi mà?!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        chosen_item = None
        #Cần phải có nhẫn kim cương để cưới nhau
        for item in user_profile.list_items:
            if item.item_id == "g_dring":
                chosen_item = item
                break
        if chosen_item == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng dùng lệnh {SlashCommand.SHOP_GLOBAL.value} để mua Nhẫn Kim Cương!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        if couple.love_rank == 19 and couple.love_progressing >= 990 and couple.love_point >= 90:
            gif_links = [
            "https://i.pinimg.com/originals/10/d9/d3/10d9d362a1532da2e7916ed4da2cec46.gif",
            "https://i.pinimg.com/originals/3f/4d/5f/3f4d5f06e024ccce77a9249ff30db093.gif",
            "https://i.pinimg.com/originals/65/0c/3b/650c3bf600925ca4458ece0b464ca204.gif",
            "https://i.pinimg.com/originals/81/c2/7e/81c27e549a30d9d006464a21d038a2c6.gif",
            "https://i.pinimg.com/originals/a1/9d/78/a19d784a8f8cb7d832d5e50a86bfbf1a.gif",
            "https://i.pinimg.com/originals/d1/56/ea/d156ea8eb781ef680e91ea8764e3eaca.gif",
        ]
            gif = random.choice(gif_links)
        
            date_created = couple.date_created
            unix_time = int(date_created.timestamp())
            #Tạo embed cưới nhau
            embed = discord.Embed(title=f"Đám Cưới Tân Uyên Ương",color=discord.Color.blue())
            embed.add_field(name=f"", value=f"Cặp đôi uyên ương <@{couple.first_user_id}> -`{UtilitiesFunctions.get_heart_emoji_on_rank(couple.love_rank)}´- <@{couple.second_user_id}> đã về chung một nhà!", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Ngày lành quen nhau: <t:{unix_time}:D>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Điểm thân mật **{couple.love_point}**", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.set_image(url=gif)
            CoupleMongoManager.update_married_time_now(guild_id=interaction.guild_id, user_id=interaction.user.id)
            view = CoupleMarryView(couple=couple, gif=gif, timeout=60)
            mess = await interaction.followup.send(embed=embed, view = view)
            view.old_message = mess
            view.guild = interaction.guild
            await view.start_countdown()
            return
        else:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không đủ điều kiện để cưới",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"Cặp đôi cần phải đạt hết điều kiện dưới đây mới có thể cưới nhau:", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tình trạng cặp đôi cần phải đạt **19**", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tỉ lệ thăng hoa cảm xúc phải **99%**", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Điểm thân mật cũng phải đạt trên **90**", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
    @couple_marry_slash_command.error
    async def couple_marry_slash_command_error(self, interaction: discord.Interaction, error):
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
