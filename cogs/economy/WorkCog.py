from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import discord
from discord.ext import commands
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import random
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
import CustomFunctions
import asyncio
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_small_copper_fish,list_gold_fish, list_silver_fish, list_gift_items, list_trash, list_plant, list_legend_weapon_1, list_legend_weapon_2, list_attack_items, list_support_ga_items, list_protection_items
from Handling.Economy.Work.WorkPlantView import WorkPlantView
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
import copy

async def setup(bot: commands.Bot):
    await bot.add_cog(WorkEconomy(bot=bot))
    print("Work Economy is ready!")

class WorkEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.random_title_at_work = ["sếp", "đồng nghiệp", "nhân viên cùng chỗ làm", "thanh niên", "công đoàn"]
        self.random_user = ["Rui", "Darkie", "Leila", "Duck", "LunLun", "ẩn danh", "bí ẩn", "mới", "cũ", "nào đó", "HuyGold", "Kyo", "Tuz"]
        self.random_praise = [
            "Vì thành tích công việc tốt, nên {title} {person} đã có chút khen thưởng về thành quả mà {user_name} đạt được. ", 
            "Trong lúc làm việc, {title} {person} rất hài lòng khi thấy {user_name} đã làm việc chăm chỉ. ",
            "Trong lúc test lệnh trong server {server_name}, {title} {person} gửi lời cảm ơn đến {user_name} vì đã dùng lệnh thường xuyên. ",
            "Vì hoàn thành KPI, {title} {person} không ngớt lời khen ngợi {user_name} về thành quả đạt được. ",
            "Vì hoàn thành KPI đăng content trong server {server_name}, {title} {person} quyết định thưởng cho {user_name} một chút để làm động lực. ",
            "Vì đã lo rất tốt cho {server_name}, {title} {person} đã biểu dương thành tích của {user_name} và đánh giá cao thành quả đạt được. ",
            "Vì không để nơi này thành dead server, {title} {person} nhiệt liệt tán thưởng {user_name} vì đã nói nhiều. ",
            "Là thành viên ưu tú của server {server_name}, {user_name} được thưởng thêm một chút. ",
            "Nhờ việc lảm nhảm nhiều nên server {server_name} không dead, nên {title} {person} gửi chút cà phê cho {user_name}. ",
                              ]
        self.random_critizie = [
                "Vì thành tích công việc quá dở tệ, nên {title} {person} đã kêu {user_name} vào phòng riêng để làm việc lại về thái độ. ", 
                "Trong lúc làm việc, {title} {person} đã thấy {user_name} chểnh mảng và làm hư đồ tùm lum, gây hại cho nhân loại. ",
                "Trong lúc test lệnh trong server {server_name}, {user_name} đã spam quá nhiều và bị {title} {person} phát hiện và báo cáo admin. ",
                "Để gáng hoàn thành KPI, {user_name} đã không từ thủ đoạn bỉ ổi nào, và đã bị chính quyền server {server_name} phát giác. ",
                "Vì không hoàn thành KPI đăng content trong server {server_name}, {title} {person} quyết định phạt {user_name} một chút để làm gương. ",
                "Vì chuyên gia quậy phá và spam trong {server_name}, {title} {person} đã quyết định giam thưởng và trừ lương {user_name}. ",
                "Vì liên tục spam không ngừng trong {server_name}, {user_name} đã bị chính quyền tiễn vong lương thưởng. ",
                "Là thành viên đáy xã hội trong server {server_name}, {user_name} đã vi phạm luật và bị admin trừng phạt. ",
                "Nhờ việc lảm nhảm trong server {server_name}, nên {title} {person} quyết định giam lương và trừ tiền {user_name}. ",
                                ]
    
    @commands.command()
    async def work(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            
            embed, view = await self.embed_work_command(user=message.author)
            mes = await message.reply(embed=embed, view=view)
            if view != None:
                view.message = mes

            check_quest_message = QuestMongoManager.increase_quest_objective_count(guild_id=message.guild.id, user_id=message.author.id, quest_type="work_normal_count")
            if check_quest_message == True:
                view = SelfDestructView(60)
                quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
                ms = await message.channel.send(embed=quest_embed, content=f"{message.author.mention}", view=view)
                view.message = ms
            return
    
    work_group = discord.app_commands.Group(name="work", description="Các lệnh liên quan đến làm việc kiếm tiền!")
    
    #region work
    @work_group.command(name="normal", description="Lệnh lao động trong server!")
    async def work_slash_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        embed, view = await self.embed_work_command(user=interaction.user)
        mess = await interaction.followup.send(embed=embed)
        if view != None:
            view.message = mess
        
        check_quest_message = QuestMongoManager.increase_quest_objective_count(guild_id=interaction.guild_id, user_id=interaction.user.id, quest_type="work_normal_count")
        if check_quest_message == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            ms = await interaction.channel.send(embed=quest_embed, content=f"{interaction.user.mention}", view=view)
            view.message = ms
        return
        
    async def embed_work_command(self, user: discord.Member):
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        
        if user_profile == None:
            user_profile = ProfileMongoManager.create_profile(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name)
        
        if user_profile != None and user_profile.last_work != None:
            time_window = timedelta(minutes=10)
            check = self.check_if_within_time_delta(input=user_profile.last_work, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào xem chừng nào mới làm việc được tiếp
                work_next_time = user_profile.last_work + time_window
                unix_time = int(work_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã làm việc rồi. Vui lòng thực hiện lại lệnh {SlashCommand.WORK.value} vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                return embed, view
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                return embed, None
            else:
                ProfileMongoManager.update_jail_time(guild_id=user.guild.id, user_id=user.id, jail_time=None)
        
        authority_user = ProfileMongoManager.is_authority(guild_id=user.guild.id, user_id= user.id)
        dignity_point = 50
        tax = 80
        pay_tax = True
        bonus = False
        
        if user_profile != None and user_profile.dignity_point != None:
            dignity_point = user_profile.dignity_point
            if user_profile.dignity_point == 0: 
                #Gian Thượng Đại Đạo không cần trả thuế, nhưng cũng không được bonus
                pay_tax = False
                bonus = False
            else:
                dignity_rate = int(user_profile.dignity_point/10)
                if dignity_rate == 0:
                    #Không thể trốn thuế, nhưng chắc chắn bonus
                    pay_tax = True
                    bonus = True
                else:
                    #Roll tỉ lệ trốn thuế dựa trên rate và tỉ lệ bonus dựa trên dignity_rate
                    dice_tax_evade = random.randint(0, 10)
                    if dignity_rate <= dice_tax_evade:
                        #Có thể trốn thuế
                        pay_tax = False
                    #Roll tỉ lệ bonus dựa trên rate và tỉ lệ bonus dựa trên dignity_rate
                    dice_bonus = random.randint(0, 10)
                    if dignity_rate >= dice_bonus:
                        bonus = True
        level_bonus = int(user_profile.level/20*500) if user_profile.level != None else 0
        money_based_on_level = level_bonus
        base_money = 600 + money_based_on_level
        base_authority_money = 2
        text_authority = ""
        if authority_user!=None:
            text_authority = f" và **{2}** {EmojiCreation2.SILVER.value}"
        base_text = f"Hôm nay bạn đã làm việc chăm chỉ, và nhận được **{base_money}** {EmojiCreation2.COPPER.value}{text_authority}! "
        #random thêm để xem có được cộng trừ bonus không
        chance = random.randint(0, 10)
        if chance >= 5:
            #Dựa vào bonus để cộng hoặc trừ
            if bonus:
                text = self.get_bonus_message(True, user.guild.name, user.mention)
                base_text += text
                #Cộng thêm tiền dựa trên phần trăm của điểm dignity point
                if dignity_point == 0: dignity_point = 1
                bonus_money = int(base_money/dignity_point*10)
                base_money += bonus_money
                base_text += f"Bạn được cộng thêm {bonus_money} {EmojiCreation2.COPPER.value}! "
            else:
                text = self.get_bonus_message(False, user.guild.name, user.mention)
                base_text += text
                #Trừ tiền dựa trên phần trăm của điểm dignity point
                if dignity_point == 0: dignity_point = 1
                bonus_money = int(base_money/dignity_point*10)
                base_money -= bonus_money
                base_text += f"Bạn bị trừ {bonus_money} {EmojiCreation2.COPPER.value}! "
        
        #dựa vào Pay_tax để xác định trốn thuế hay đóng thuế
        text_tax = f"Là công dân gương mẫu nên bạn đã đóng thêm thuế {tax} {EmojiCreation2.COPPER.value}."
        if pay_tax:
            base_money -= tax
            text_tax = f"\nLà công dân gương mẫu nên bạn đã đóng thêm thuế {tax} {EmojiCreation2.COPPER.value}."
        else:
            text_tax = f"\nVới chút tài mọn, bạn đã trốn đóng thuế thành công."
        
        
        
        if base_money == 0: base_money = 300
        base_text += text_tax
        base_text += f"\n\n> Tổng tiền nhận từ {SlashCommand.WORK.value} hôm nay: **{base_money}** {EmojiCreation2.COPPER.value}{text_authority}."
        
        #Cộng tiền, cộng 2 điểm nhân phẩm
        ProfileMongoManager.update_profile_money(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, copper=base_money)
        ProfileMongoManager.update_dignity_point(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, dignity_point=2)
        #Cộng thuế cho chính quyền
        if pay_tax:
            ProfileMongoManager.update_money_authority(guild_id=user.guild.id, copper= tax)
        ProfileMongoManager.update_last_work_now(guild_id=user.guild.id, user_id=user.id)
        
        #Cộng thêm cho chính quyền
        if authority_user != None:
            ProfileMongoManager.update_money_authority(guild_id=user.guild.id, silver=base_authority_money)
        
        #Cập nhập level progressing
        ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id= user.id)
        
        embed = discord.Embed(title=f"", description=f"{base_text}", color=0x1ae8e8)
        return embed, None
    
    #region fishing
    @work_group.command(name="fishing", description="Dùng cần câu để câu cá")
    @discord.app_commands.checks.cooldown(1, 10)
    async def work_fising_slash_command(self, interaction: discord.Interaction):
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
            user_profile = ProfileMongoManager.create_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name)
        
        if user_profile != None and user_profile.last_fishing != None:
            time_window = timedelta(minutes=15)
            check = self.check_if_within_time_delta(input=user_profile.last_fishing, time_window=time_window)
            if check:
                #Lấy thời gian cũ để cộng vào xem chừng nào mới làm được tiếp
                work_next_time = user_profile.last_fishing + time_window
                unix_time = int(work_next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã câu cá rồi. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
            else:
                ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time=None)
        
        #Kiểm tra có cần câu không
        if user_profile.list_items == None or len(user_profile.list_items) == 0:
            embed = discord.Embed(title=f"", description=f"🚫 Bạn không có cần câu, vui lòng dùng lệnh {SlashCommand.SHOP_GLOBAL.value} để mua cần câu!", color=0xc379e0)
            view = SelfDestructView(timeout=120)
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
            view.message = mess
            return
        flag = False
        for item in user_profile.list_items:
            if "fish_rod" in item.item_id:
                flag = True
                break
        if flag == False:
            embed = discord.Embed(title=f"", description=f"🚫 Bạn không có cần câu, vui lòng dùng lệnh {SlashCommand.SHOP_GLOBAL.value} để mua cần câu!", color=0xc379e0)
            view = SelfDestructView(timeout=120)
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
            view.message = mess
            return
        
        fish_rod = self.get_most_expensive_fishing_rod(items=user_profile.list_items)
        embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã dùng [{fish_rod.emoji} - **{fish_rod.item_name}**] để câu cá",color=discord.Color.blue())
        mess = await interaction.followup.send(embed=embed)
        await asyncio.sleep(10)
        fishup_item = self.get_fished_up_item(fish_rod = fish_rod)
        embed.add_field(name=f"", value="▬▬▬▬ι═══════>", inline=False)
        embed.add_field(name=f"", value=f"{interaction.user.mention} đã câu lên được: x{fishup_item.quantity} [{fishup_item.emoji} - **{fishup_item.item_name}**]!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Mô tả: {fishup_item.item_description}", inline=False)
        text = ""
        if fishup_item.bonus_dignity != 0 and fishup_item.bonus_exp != 0:
            text = f"{EmojiCreation2.SHINY_POINT.value} Nhận được: "
            if fishup_item.bonus_dignity != 0:
                text += f"**{fishup_item.bonus_dignity}** Nhân Phẩm. "
            if fishup_item.bonus_exp != 0:
                text += f"**{fishup_item.bonus_exp}** Điểm Kinh Nghiệm. "
            embed.add_field(name=f"", value=f"{text}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═══════>", inline=False)
        #Thêm item cho player
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=fishup_item, amount= fishup_item.quantity)
        #Trừ 1 cần câu
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=fish_rod, amount= -1)
        #Cập nhật fishing time
        ProfileMongoManager.update_last_fishing_now(guild_id=interaction.guild_id, user_id=interaction.user.id)
        #Cập nhập level progressing và nhân phẩm
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id, bonus_exp=fishup_item.bonus_exp)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name= "", user_display_name="", user_name="", user_id=interaction.user.id, dignity_point=fishup_item.bonus_dignity)
        await mess.edit(embed=embed)

        check_quest_message = QuestMongoManager.increase_quest_objective_count(guild_id=interaction.guild_id, user_id=interaction.user.id, quest_type="work_fishing_count")
        if check_quest_message == True:
            view = SelfDestructView(60)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            ms = await interaction.channel.send(embed=quest_embed, content=f"{interaction.user.mention}", view=view)
            view.message = ms

    @work_fising_slash_command.error
    async def work_fising_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            # Send a cooldown message to the user, formatted nicely
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            # Handle any other errors that might occur
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    @work_group.command(name="planting", description="Làm anh nông dân trồng trọt vui vẻ")
    @discord.app_commands.checks.cooldown(1, 10)
    async def work_planting_slash_command(self, interaction: discord.Interaction):
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
            user_profile = ProfileMongoManager.create_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name)
        
        #Không cho thực hiện nếu còn jail_time
        if user_profile != None and user_profile.jail_time != None:
            if user_profile.jail_time > datetime.now():
                unix_time = int(user_profile.jail_time.timestamp())
                embed = discord.Embed(title=f"", description=f"⛓️ Bạn đã bị chính quyền bắt giữ rồi, vui lòng đợi đến <t:{unix_time}:t> !", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
            else:
                ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time=None)
        
        if user_profile.plant == None:
            #Kiểm tra trong list profile có cây trồng không
            if user_profile.list_items == None or len(user_profile.list_items) == 0:
                embed = discord.Embed(title=f"", description=f"🚫 Bạn không có hạt giống nào cả, vui lòng dùng lệnh {SlashCommand.SHOP_GLOBAL.value} để mua!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
            flag = False
            for item in user_profile.list_items:
                if "seed_" in item.item_id:
                    flag = True
                    break
            if flag == False:
                embed = discord.Embed(title=f"", description=f"🚫 Bạn không có hạt giống nào cả, vui lòng dùng lệnh {SlashCommand.SHOP_GLOBAL.value} để mua!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
            #Hiện embed chọn cây trồng
            embed = discord.Embed(title=f"", description=f"Menu Chọn Cây Trồng", color=0xddede7)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hãy chọn những hạt giống mà bạn đang sở hữu dưới đây để trồng trọt nhé!", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            view = WorkPlantView(user_profile=user_profile, user=interaction.user)
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        else:
            time_window = timedelta(hours=user_profile.plant.hour_require)
            #Kiểm tra xem trồng xong chưa
            check = self.check_if_within_time_delta(input=user_profile.plant.plant_date, time_window=time_window)
            if check:
                 #Lấy thời gian cũ để cộng vào
                next_time = user_profile.plant.plant_date + time_window
                unix_time = int(next_time.timestamp())
                #Chưa trồng xong
                #Hiện lại embed plant
                embed = discord.Embed(title="", description=f"**Vườn nhà của {interaction.user.mention}**", color=0xddede7)
                if interaction.user.avatar != None:
                    embed.set_thumbnail(url=interaction.user.avatar.url)
                embed.add_field(name=f"", value=f"Thông tin cây trồng", inline=True)
                embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
                embed.add_field(name=f"", value=f"Hạt giống đang trồng: [{user_profile.plant.source_item.emoji} - **{user_profile.plant.source_item.item_name}**]", inline=False)
                embed.add_field(name=f"", value=f"Tiến trình:", inline=False)
                embed.add_field(name=f"", value=f"{UtilitiesFunctions.progress_bar_plant(start_time=user_profile.plant.plant_date, end_time=next_time)}", inline=False)
                embed.add_field(name=f"", value=f"Thời gian thu hoạch: <t:{unix_time}:t>", inline=False)
                embed.add_field(name=f"", value=f"Sẽ thu hoạch được:", inline=False)
                embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} [{user_profile.plant.des_item.emoji} - **{user_profile.plant.des_item.item_name}**]", inline=False)
                embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
                mess = await interaction.followup.send(embed=embed, ephemeral=False)
                return
            else:
                #Đã trồng xong
                random_quantity = random.randint(2,6)
                if user_profile.plant.des_item.item_id == "seed_weed":
                    random_quantity = random.randint(1,3)
                embed = discord.Embed(title="", description=f"**Vườn nhà của {interaction.user.mention}**", color=0xddede7)
                if interaction.user.avatar != None:
                    embed.set_thumbnail(url=interaction.user.avatar.url)
                embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
                embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Chúc mừng {interaction.user.mention} đã thu hoạch được: **{random_quantity}** [{user_profile.plant.des_item.emoji} - **{user_profile.plant.des_item.item_name}**]", inline=False)
                text = f"{EmojiCreation2.SHINY_POINT.value} Và {interaction.user.mention} nhận được: "
                if user_profile.plant.des_item.bonus_dignity != 0:
                    text += f"**{user_profile.plant.des_item.bonus_dignity}** Nhân Phẩm. "
                if user_profile.plant.des_item.bonus_exp != 0:
                    text += f"**{user_profile.plant.des_item.bonus_exp}** Điểm Kinh Nghiệm. "
                embed.add_field(name=f"", value=f"{text}", inline=False)
                embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
                
                #Cộng level progress và dignity point
                ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id, bonus_exp=user_profile.plant.des_item.bonus_exp)
                ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name= "", user_display_name="", user_name="", user_id=interaction.user.id, dignity_point=user_profile.plant.des_item.bonus_dignity)
                #Cộng thêm đồ
                ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, item=user_profile.plant.des_item, amount= random_quantity)
                #Xoá plant
                ProfileMongoManager.update_plant(guild_id=interaction.guild_id, user_id=interaction.user.id, plant=None)
                mess = await interaction.followup.send(embed=embed, ephemeral=False)

                check_quest_message = QuestMongoManager.increase_quest_objective_count(guild_id=interaction.guild_id, user_id=interaction.user.id, quest_type="work_planting_count")
                if check_quest_message == True:
                    view = SelfDestructView(60)
                    quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
                    ms = await interaction.channel.send(embed=quest_embed, content=f"{interaction.user.mention}", view=view)
                    view.message = ms
                return
        
    
    @work_planting_slash_command.error
    async def work_planting_slash_command_error(self, interaction: discord.Interaction, error):
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
    
    def get_bonus_message(self, is_add_bonus, server_name: str, user_name: str):
        title = random.choice(self.random_title_at_work)
        person = random.choice(self.random_user)
        if is_add_bonus:
            text = random.choice(self.random_praise)
        else:
            text = random.choice(self.random_critizie)
        text = text.replace("{title}", title)
        text = text.replace("{person}", person)
        text = text.replace("{server_name}", server_name)
        text = text.replace("{user_name}", user_name)
        return text
    
    def get_most_expensive_fishing_rod(self, items):
        type_multiplier = {
            "C": 1,
            "S": 100,
            "G": 10000,
            "D": 1000000
        }
        items.sort(key=lambda item: "fish_rod" in item.item_id and item.item_worth_amount * type_multiplier[item.item_worth_type])
        return items[-1]
    
    def get_fished_up_item(self, fish_rod: Item):
        if fish_rod.item_id == "fish_rod_1":
            dice_trash = UtilitiesFunctions.get_chance(20)
            if dice_trash: return random.choice(list_trash)
            
            dice_legend = UtilitiesFunctions.get_chance(5)
            if dice_legend:
                dice_check = UtilitiesFunctions.get_chance(50)
                if dice_check:
                    item = copy.deepcopy(random.choice(list_legend_weapon_1))
                    item.item_worth_amount = 10
                    return item
                else: 
                    item = copy.deepcopy(random.choice(list_legend_weapon_2))
                    item.item_worth_amount = 10
                    return item
            
            dice_fish_silver = UtilitiesFunctions.get_chance(10)
            if dice_fish_silver: return random.choice(list_silver_fish)
            else: return random.choice(list_small_copper_fish)
            
        elif fish_rod.item_id == "fish_rod_2":
            dice_trash = UtilitiesFunctions.get_chance(10)
            if dice_trash: return random.choice(list_trash)
            
            dice_legend = UtilitiesFunctions.get_chance(5)
            if dice_legend:
                dice_check = UtilitiesFunctions.get_chance(50)
                if dice_check:
                    item = copy.deepcopy(random.choice(list_legend_weapon_1))
                    item.item_worth_amount = 10
                    return item
                else: 
                    item = copy.deepcopy(random.choice(list_legend_weapon_2))
                    item.item_worth_amount = 10
                    return item
            
            dice_fish_silver = UtilitiesFunctions.get_chance(45)
            if dice_fish_silver: return random.choice(list_silver_fish)
            else: return random.choice(list_small_copper_fish)
        elif fish_rod.item_id == "fish_rod_3":
            dice_trash = UtilitiesFunctions.get_chance(6)
            if dice_trash: return random.choice(list_trash)
            
            dice_gift = UtilitiesFunctions.get_chance(5)
            if dice_gift: return random.choice(list_gift_items)
            
            dice_attack_weapon = UtilitiesFunctions.get_chance(5)
            if dice_attack_weapon: return random.choice(list_attack_items)
            
            dice_armour = UtilitiesFunctions.get_chance(5)
            if dice_armour: return random.choice(list_protection_items)
            
            #potion ga support
            dice_potion = UtilitiesFunctions.get_chance(5)
            if dice_potion:
                item = copy.deepcopy(random.choice(list_support_ga_items))
                dice = UtilitiesFunctions.get_chance(50)
                if dice:
                    #Trúng 3 bình bình thường
                    filtered_items = [
                        item for item in list_support_ga_items 
                        if item.item_id in ["ga_heal_1", "ga_stamina_1", "ga_mana_1"]
                    ]
                    item =  copy.deepcopy(random.choice(filtered_items))
                    item.item_worth_amount = 1000
                    return item
                else:
                    item_id = "ga_all_restored"
                    additional_dice = UtilitiesFunctions.get_chance(35)
                    if additional_dice: item_id = "ga_resurrection"
                    for randomitem in list_support_ga_items:
                        if randomitem.item_id == item_id:
                            item = copy.deepcopy(randomitem)
                            break
                if item == None: item = copy.deepcopy(random.choice(list_support_ga_items))
                item.item_worth_amount = 5
                return item
            dice_fish_gold = UtilitiesFunctions.get_chance(30)
            if dice_fish_gold: return random.choice(list_gold_fish)
            else: return random.choice(list_silver_fish)
            
        elif fish_rod.item_id == "fish_rod_4":
            dice_trash = UtilitiesFunctions.get_chance(5)
            if dice_trash: return random.choice(list_trash)
            dice_gift = UtilitiesFunctions.get_chance(10)
            if dice_gift: return random.choice(list_gift_items)
            
            dice_attack_weapon = UtilitiesFunctions.get_chance(10)
            if dice_attack_weapon: return random.choice(list_attack_items)
            
            dice_armour = UtilitiesFunctions.get_chance(10)
            if dice_armour: return random.choice(list_protection_items)
            
            #potion ga support
            dice_potion = UtilitiesFunctions.get_chance(10)
            if dice_potion:
                item = copy.deepcopy(random.choice(list_support_ga_items))
                dice = UtilitiesFunctions.get_chance(50)
                if dice:
                    #Trúng 3 bình bình thường
                    filtered_items = [
                        fitem for fitem in copy.deepcopy(list_support_ga_items) 
                        if fitem.item_id in ["ga_heal_1", "ga_stamina_1", "ga_mana_1"]
                    ]
                    item = copy.deepcopy(random.choice(filtered_items))
                    item.item_worth_amount = 1000
                    return item
                else:
                    item_id = "ga_all_restored"
                    additional_dice = UtilitiesFunctions.get_chance(35)
                    if additional_dice: item_id = "ga_resurrection"
                    for randomitem in copy.deepcopy(list_support_ga_items):
                        if randomitem.item_id == item_id:
                            item = copy.deepcopy(randomitem)
                            break
                if item == None: item = copy.deepcopy(random.choice(list_support_ga_items))
                item.item_worth_amount = 5
                return item
            
            dice_fish_gold = UtilitiesFunctions.get_chance(80)
            if dice_fish_gold: 
                fish = copy.deepcopy(random.choice(list_gold_fish))
                return fish
            else:
                fish = copy.deepcopy(random.choice(list_silver_fish))
                return fish
            
        elif fish_rod.item_id == "fish_rod_5":
            dice_trash = UtilitiesFunctions.get_chance(10)
            if dice_trash:
                fish = random.choice(list_trash)
                return fish

            dice_attack_weapon = UtilitiesFunctions.get_chance(15)
            if dice_attack_weapon: return random.choice(list_attack_items)
            
            dice_armour = UtilitiesFunctions.get_chance(15)
            if dice_armour: return random.choice(list_protection_items)
            
            #potion ga support
            dice_potion = UtilitiesFunctions.get_chance(15)
            if dice_potion:
                item = copy.deepcopy(random.choice(list_support_ga_items))
                dice = UtilitiesFunctions.get_chance(50)
                if dice:
                    #Trúng 3 bình bình thường
                    filtered_items = [
                        fitem for fitem in copy.deepcopy(list_support_ga_items) 
                        if fitem.item_id in ["ga_heal_1", "ga_stamina_1", "ga_mana_1"]
                    ]
                    item =  copy.deepcopy(random.choice(filtered_items))
                    item.item_worth_amount = 1000
                    return item
                else:
                    item_id = "ga_all_restored"
                    additional_dice = UtilitiesFunctions.get_chance(35)
                    if additional_dice: item_id = "ga_resurrection"
                    for randomitem in list_support_ga_items:
                        if randomitem.item_id == item_id:
                            item = copy.deepcopy(randomitem)
                            break
                if item == None: item = copy.deepcopy(random.choice(list_support_ga_items))
                item.item_worth_amount = 5
                return item
            
            dice_fish_gold = UtilitiesFunctions.get_chance(80)
            if dice_fish_gold: 
                fish = random.choice(list_gold_fish)
                return fish
            else:
                fish = random.choice(list_silver_fish)
                return fish
        else:
            return random.choice(list_trash)