import re
from CustomEnum.GuardianMemoryTag import GuardianMemoryTag
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import discord
from discord.ext import commands
from Handling.Economy.GA import GaQuestLineExample
from Handling.Economy.GA.GaChallengeView import GaChallengeView
from Handling.Economy.GA.GaQuestClass import GuardianAngelQuest
from Handling.Economy.GA.GaQuestView import GaQuestView
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
import CustomEnum.UserEnum as UserEnum
from typing import List, Optional, Dict
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
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
    await bot.add_cog(GuardianAngelCog(bot=bot))
    print("Guardian Angel is ready!")

class GuardianAngelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    ga_group = discord.app_commands.Group(name="ga", description="Các lệnh liên quan đến Guardian Angel!")
    #region ga sell slash
    @ga_group.command(name="sell", description="Bán Hộ Vệ Thần hiện tại!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def ga_sell_slash_command(self, interaction: discord.Interaction):
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
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.guardian == None:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        #Nếu có list skill trong guardian thì hỏi user chọn bán skill hay guardian
        if user_profile.guardian.list_skills != None and len(user_profile.guardian.list_skills) > 0 and user_profile.guardian.is_dead == False:
            embed = discord.Embed(title=f"", description=f"Menu Bán Hộ Vệ Thần", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            embed.add_field(name=f"", value=f"Chọn thứ bạn muốn bán", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            view = GaSellOptionsMenuView(user=interaction.user, user_profile=user_profile)
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
            view.message = mess
        else:
            #Tính toán số tiền bán hộ vệ thần
            money = UtilitiesFunctions.calculate_guardian_sell_money(user_profile.guardian.worth_amount, user_profile.guardian.level, user_profile.guardian.is_dead, user_profile.guardian.attack_power, user_profile.guardian.max_health, user_profile.guardian.max_mana, user_profile.guardian.max_stamina)
            embed = discord.Embed(title=f"", description=f"Bán Hộ Vệ Thần", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            embed.add_field(name=f"", value=f"Bạn có sẵn sàng bán Hộ Vệ Thần [{user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}**] với giá **{money}** {UtilitiesFunctions.get_emoji_from_loai_tien(user_profile.guardian.worth_type)} không?", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            embed.set_footer(text=f"Hãy nâng cấp của Hộ Vệ Thần lên thật cao thì bán mới được giá nhé!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
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
    
    #region ga meditate slash
    @ga_group.command(name="meditate", description="Cho Hộ Vệ Thần tu thiền để hồi phục thể lực và tăng kinh nghiệm!")
    @discord.app_commands.checks.cooldown(1, 15)
    async def ga_meditate_slash_command(self, interaction: discord.Interaction):
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
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.guardian == None or user_profile.guardian.is_dead:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        if user_profile.guardian.last_meditation != None:
            time_window = timedelta(minutes=30)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.guardian.last_meditation, time_window=time_window)
            if check:
                next_time = user_profile.guardian.last_meditation + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã cho Hộ Vệ Thần tu thiền rồi. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:t>!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
            
        if user_profile.guardian.time_to_recover != None:
            if user_profile.guardian.time_to_recover > datetime.now():
                view = SelfDestructView(timeout=30)
                next_time = user_profile.guardian.time_to_recover
                unix_time = int(next_time.timestamp())
                mess = await interaction.followup.send(content=f"Hộ Vệ Thần của bạn đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True, view=view)
                view.message = mess
                return
            else:
                #Hồi phục 50% máu, 50% thể lực
                health = int(user_profile.guardian.max_health*50/100)
                stamina = int(user_profile.guardian.max_stamina*50/100)
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
        
        special_case = False
        if interaction.guild_id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            for role in interaction.user.roles:
                if role.id == TrueHeavenEnum.TOP_1_GUARDIAN.value: 
                    special_case = True
                    break
        
        #restore tính 40% của mana
        mana = int(user_profile.guardian.max_mana*40/100)
        if special_case:
            mana = user_profile.guardian.max_mana
        
        random_bonus_exp = random.randint(15, 60)
        dignity_point = 10
        embed = discord.Embed(title=f"", description=f"Tu Thiền", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Hộ Vệ Thần [{user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}**] đã tiến nhập thiền định.", inline=False)
        if special_case:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hồi phục **toàn bộ** Mana {EmojiCreation2.MP.value}!", inline=False)
        else:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hồi phục **{mana}** Mana {EmojiCreation2.MP.value}!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cộng **{random_bonus_exp}** điểm EXP cho Hộ Vệ Thần!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cộng **{dignity_point}** nhân phẩm!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        await interaction.followup.send(embed=embed)
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id)
        ProfileMongoManager.update_main_guardian_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id, bonus_exp=random_bonus_exp)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id,user_id=interaction.user.id, guild_name="", user_display_name="", user_name="", dignity_point=dignity_point)
        ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, mana=mana)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_meditation", date_value=datetime.now())
        ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_meditation")

        # Tạo memory chỉ khi memory mới nhất không phải là tag MEDITATION
        memories = user_profile.guardian.memories or []
        latest_memory = memories[0] if memories else None
        should_add_memory = (
            latest_memory is None or latest_memory.tag != GuardianMemoryTag.MEDITATION.value
        )
        if should_add_memory:
            meditation_templates = [
                "Đã tĩnh tâm thiền định, cảm nhận luồng mana tuôn chảy trở lại.",
                "Bước vào trạng thái thiền định, Hộ Vệ Thần đã khôi phục một phần năng lượng tinh thần.",
                "Giữa yên lặng, Hộ Vệ Thần tập trung nội lực, mana dần hồi phục.",
                "Một buổi thiền định sâu sắc giúp Hộ Vệ Thần tái thiết năng lượng phép thuật.",
                "Đã nhập định bên trong tâm trí, lấy lại sự tỉnh táo và mana.",
            ]
            memory_description = random.choice(meditation_templates)
            ProfileMongoManager.add_memory_guardian(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id,
                memory_description=memory_description,
                channel_name=interaction.channel.name,
                tag=GuardianMemoryTag.MEDITATION.value
            )

    
    @ga_meditate_slash_command.error
    async def ga_meditate_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    #region ga feed slash
    @ga_group.command(name="feed", description="Cho Hộ Vệ Thần ăn để hồi phục!")
    @discord.app_commands.checks.cooldown(1, 15)
    async def ga_feed_slash_command(self, interaction: discord.Interaction):
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
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.guardian == None or user_profile.guardian.is_dead:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.list_items == None or len(user_profile.list_items) ==0:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng trồng trái cây bằng lệnh {SlashCommand.WORK_PLANTING.value} để kiếm thức ăn!", ephemeral=True, view=view)
            view.message = mess
            return
        
        allowed_item_id = ["wheat","potato", "corn", "watermelon", "weed", "g_pocky","g_chocolate", "g_stcake"]
        chosen_item = None
        for item in user_profile.list_items:
            if item.item_id in allowed_item_id:
                chosen_item = item
                break
        if chosen_item == None:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng trồng trái cây bằng lệnh {SlashCommand.WORK_PLANTING.value} hoặc mua thức ăn!", ephemeral=True, view=view)
            view.message = mess
            return
        
        if user_profile.guardian.last_feed != None:
            time_window = timedelta(minutes=30)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.guardian.last_feed, time_window=time_window)
            if check:
                next_time = user_profile.guardian.last_feed + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã cho Hộ Vệ Thần ăn rồi. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:t>!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
        
        if user_profile.guardian.time_to_recover != None:
            if user_profile.guardian.time_to_recover > datetime.now():
                view = SelfDestructView(timeout=30)
                next_time = user_profile.guardian.time_to_recover
                unix_time = int(next_time.timestamp())
                mess = await interaction.followup.send(content=f"Hộ Vệ Thần của bạn đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True, view=view)
                view.message = mess
                return
            else:
                #Hồi phục 50% máu, 50% thể lực
                health = int(user_profile.guardian.max_health*50/100)
                stamina = int(user_profile.guardian.max_stamina*50/100)
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
        

        special_case = False
        if interaction.guild_id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            for role in interaction.user.roles:
                if role.id == TrueHeavenEnum.TOP_1_GUARDIAN.value: 
                    special_case = True
                    break
        
        #heal tính 40% của max_health, 40% của max thể lực
        health = int(user_profile.guardian.max_health*40/100)
        stamina = int(user_profile.guardian.max_stamina*40/100)

        if special_case:
            health = user_profile.guardian.max_health
            stamina = user_profile.guardian.max_stamina

        random_bonus_exp = chosen_item.bonus_exp
        dignity_point = 5
        if chosen_item.item_id == "weed":
            dignity_point = 0
        embed = discord.Embed(title=f"", description=f"Cho ăn", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Hộ Vệ Thần {user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}** đã ăn [{chosen_item.emoji} - **{chosen_item.item_name}**]", inline=False)
        if special_case:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hồi phục **toàn bộ** {EmojiCreation2.HP.value} máu và {EmojiCreation2.STAMINA.value} thể lực!", inline=False)
        else:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hồi phục **{health}** {EmojiCreation2.HP.value} máu!", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hồi phục **{stamina}** {EmojiCreation2.STAMINA.value} thể lực!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cộng **{random_bonus_exp}** điểm EXP cho Hộ Vệ Thần!", inline=False)
        if dignity_point != 0:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cộng **{dignity_point}** nhân phẩm!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        await interaction.followup.send(embed=embed)
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id)
        ProfileMongoManager.update_main_guardian_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id, bonus_exp=random_bonus_exp)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id,user_id=interaction.user.id, guild_name="", user_display_name="", user_name="", dignity_point=dignity_point)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_feed", date_value=datetime.now())
        ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id,user_id=interaction.user.id, user_display_name="", user_name="", guild_name="", item=chosen_item, amount=-1)
        ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_feed")
        # Tạo memory chỉ khi memory mới nhất không phải là tag FEED
        memories = user_profile.guardian.memories or []
        latest_memory = memories[0] if memories else None
        should_add_memory = (
            latest_memory is None or latest_memory.tag != GuardianMemoryTag.FEEDING.value
        )
        if should_add_memory:
            templates = [
                    f"Đã thưởng thức {chosen_item.emoji} - **{chosen_item.item_name}** đầy đủ dưỡng chất, hồi phục thể lực và tinh thần.",
                    f"Đã được cho ăn {chosen_item.emoji} - **{chosen_item.item_name}**, lấy lại sức lực hơn.",
                    f"Một món {chosen_item.emoji} - **{chosen_item.item_name}** đơn giản nhưng tràn đầy sinh lực.",
                    f"Sau khi dùng  {chosen_item.emoji} - **{chosen_item.item_name}**, Hộ Vệ Thần cảm thấy mạnh mẽ và sẵn sàng cho thử thách tiếp theo.",
                    f"Bụng no, tâm an - Hộ Vệ Thần vừa nạp lại năng lượng cần thiết.",
                    f"Tiêu hóa {chosen_item.emoji} - **{chosen_item.item_name}** và biến nó thành nguồn sức mạnh dồi dào.",
                    f"{chosen_item.emoji} - **{chosen_item.item_name}** giúp Hộ Vệ Thần lấy lại nhiệt huyết chiến đấu.",
                ]

            memory_description = random.choice(templates)
            ProfileMongoManager.add_memory_guardian(
                guild_id=interaction.guild_id,
                user_id=interaction.user.id,
                memory_description=memory_description,
                channel_name=interaction.channel.name,
                tag=GuardianMemoryTag.FEEDING.value
            )
    
    @ga_feed_slash_command.error
    async def ga_feed_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
        
    #region ga rankup slash
    @ga_group.command(name="rankup", description="Nâng cấp chỉ số cho Hộ Vệ Thần!")
    @discord.app_commands.checks.cooldown(1, 15)
    async def ga_rankup_slash_command(self, interaction: discord.Interaction):
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
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.guardian == None or user_profile.guardian.is_dead:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.guardian.stats_point == 0:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Hộ Vệ Thần của bạn không có điểm cộng nào hết! Hãy dùng các lệnh như {SlashCommand.GA_FEED.value}, {SlashCommand.GA_MEDITATE.value} để nâng cấp cho Hộ Vệ Thần", ephemeral=True, view=view)
            view.message = mess
            return
        
        embed = discord.Embed(title=f"", description=f"Nâng điểm chỉ số Hộ Vệ Thần", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Chọn chỉ số để nâng cấp Hộ Vệ Thần {user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **1** điểm cộng có thể nâng **5** điểm tấn công", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **1** điểm cộng có thể nâng **10** điểm chỉ số Máu, Thể Lực, Mana", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"> Số điểm cộng hiện tại: **{user_profile.guardian.stats_point}**", inline=False)
        view = RankUpView(user_profile=user_profile, user=interaction.user)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        return
    
    @ga_rankup_slash_command.error
    async def ga_rankup_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    #region ga battle slash
    @ga_group.command(name="battle", description="Cho Hộ Vệ Thần đi chiến đấu! Nếu không chọn đối thủ sẽ đánh với bot!")
    @discord.app_commands.describe(target="Chọn user để chiến đấu với Hộ Vệ Thần của người đó.")
    @discord.app_commands.describe(max_players="Cho phép bấy nhiêu người gia nhập cuộc chiến.")
    @discord.app_commands.choices(max_players=[
        Choice(name="1", value="1"),
        Choice(name="2", value="2"),
        Choice(name="3", value="3"),
    ])
    @discord.app_commands.checks.cooldown(1, 20)
    async def ga_battle_slash_command(self, interaction: discord.Interaction, target: Optional[discord.Member] = None, max_players: str = None):
        await interaction.response.defer(ephemeral=False)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if target!= None and target.id == interaction.user.id:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Bạn không thể chiến đấu với bản thân mình!", ephemeral=True, view=view)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.guardian == None or user_profile.guardian.is_dead:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        if user_profile.guardian.last_battle != None:
            time_window = timedelta(minutes=30)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.guardian.last_battle, time_window=time_window)
            if check:
                next_time = user_profile.guardian.last_battle + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn đã cho Hộ Vệ Thần chiến đấu rồi. Vui lòng thực hiện lại lệnh vào lúc <t:{unix_time}:t>!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return
        
        if user_profile.guardian.last_joined_battle != None:
            time_window = timedelta(minutes=1)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.guardian.last_joined_battle, time_window=time_window)
            if check:
                next_time = user_profile.guardian.last_joined_battle + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn vừa tham chiến xong. Vui lòng đợi một phút rồi thực hiện lại lệnh!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return

        if user_profile.guardian.time_to_recover != None:
            if user_profile.guardian.time_to_recover > datetime.now():
                view = SelfDestructView(timeout=30)
                next_time = user_profile.guardian.time_to_recover
                unix_time = int(next_time.timestamp())
                mess = await interaction.followup.send(content=f"Hộ Vệ Thần của bạn đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True, view=view)
                view.message = mess
                return
            else:
                #Hồi phục 50% máu, 50% thể lực
                health = int(user_profile.guardian.max_health*50/100)
                stamina = int(user_profile.guardian.max_stamina*50/100)
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
        
        
        target_profile = None
        if target != None:
            target_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=target.id)
            if target_profile == None:
                view = SelfDestructView(timeout=30)
                mess = await interaction.followup.send(content=f"Đối thủ {target.mention} vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
                view.message = mess
                return
            elif target_profile.guardian == None or target_profile.guardian.is_dead:
                view = SelfDestructView(timeout=30)
                mess = await interaction.followup.send(content=f"Đối thủ {target.mention} vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
                view.message = mess
                return
            
            if target_profile.guardian.time_to_recover != None:
                if target_profile.guardian.time_to_recover > datetime.now():
                    view = SelfDestructView(timeout=30)
                    next_time = target_profile.guardian.time_to_recover
                    unix_time = int(next_time.timestamp())
                    mess = await interaction.followup.send(content=f"Hộ Vệ Thần của {target.mention} đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True, view=view)
                    view.message = mess
                    return
                else:
                    #Hồi phục 50% máu, 50% thể lực
                    health = int(target_profile.guardian.max_health*50/100)
                    stamina = int(target_profile.guardian.max_stamina*50/100)
                    ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=target.id, health=health, stamina=stamina)
            
        is_players_versus_player = False
        title = f""
        if target != None:
            is_players_versus_player = True
            title = f"🔥 {interaction.user.mention} VS {target.mention} 🔥"
            
                #Tính reward của battle
        gold_reward = 50
        silver_reward = 100
        exp_reward = 80
        dignity_point_reward = 10
        
        if is_players_versus_player:
            gold_reward = 35
            exp_reward = 45
            dignity_point_reward = 5
            silver_reward = 0
            #Đánh giao hữu thì 100% hết
            user_profile.guardian.health = user_profile.guardian.max_health
            user_profile.guardian.mana = user_profile.guardian.max_mana
            user_profile.guardian.stamina = user_profile.guardian.max_stamina
            target_profile.guardian.health = target_profile.guardian.max_health
            target_profile.guardian.mana = target_profile.guardian.max_mana
            target_profile.guardian.stamina = target_profile.guardian.max_stamina
        
        embed = discord.Embed(title=f"", description=title, color=0x0ce7f2)
        
        embed.add_field(name=f"", value=f"Hộ Vệ Thần {user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}** (Cấp {user_profile.guardian.level}) của {interaction.user.mention}", inline=False)
        embed.add_field(name=f"", value=f"🦾: **{user_profile.guardian.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=user_profile.guardian.health, max_value=user_profile.guardian.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=user_profile.guardian.stamina, max_value=user_profile.guardian.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=user_profile.guardian.mana, max_value=user_profile.guardian.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        text = ""
        enemy: GuardianAngel = None
        if target != None:
            text = f"Hộ Vệ Thần {target_profile.guardian.ga_emoji} - **{target_profile.guardian.ga_name}** (Cấp {target_profile.guardian.level}) của {target.mention}"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{target_profile.guardian.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=target_profile.guardian.health, max_value=target_profile.guardian.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=target_profile.guardian.stamina, max_value=target_profile.guardian.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=target_profile.guardian.mana, max_value=target_profile.guardian.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
            enemy = target_profile.guardian
        else:
            enemy: GuardianAngel = ListGAAndSkills.get_random_ga_enemy_generic(level=user_profile.guardian.level)
            text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {enemy.level})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value="", inline=False)
            embed.add_field(name=f"", value=f"🦾: **{enemy.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.health, max_value=enemy.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.stamina, max_value=enemy.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.mana, max_value=enemy.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
            
        if max_players == None: max_players = "3"
        max_players_as_int = int(max_players)

        if is_players_versus_player:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_battle_pvp")
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=target.id, count_type="count_battle_pvp")
        else:
            ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=interaction.user.id, count_type="count_battle_pve")
        
        #Tính lại theo enemy_ga
        gold_reward = int(gold_reward + gold_reward*enemy.level*0.2)
        silver_reward = int(silver_reward + silver_reward*enemy.level*0.3)
        exp_reward = int(exp_reward + exp_reward*enemy.level*0.1)
        if CustomFunctions.check_if_dev_mode() == False:
            ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_battle", date_value=datetime.now())
            ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_joined_battle", date_value=datetime.now())
        view = GaBattleView(user=interaction.user, user_profile=user_profile, target=target, target_profile=target_profile, is_players_versus_players=is_players_versus_player, max_players=max_players_as_int, enemy_ga=enemy, embed_title=title, guild_id=interaction.guild_id, gold_reward=gold_reward, silver_reward=silver_reward, bonus_exp=exp_reward, dignity_point=dignity_point_reward, channel_name=interaction.channel.name)
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        print(f"Username {interaction.user.name} has started guardian battle in guild {interaction.guild.name} at channel {interaction.channel.name}!")
        await view.commence_battle()
        return
        
    @ga_battle_slash_command.error
    async def ga_battle_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)

    
    #region ga challenge slash
    @ga_group.command(name="challenge", description="Thách đấu Hộ Vệ Thần của người khác!")
    @discord.app_commands.describe(target="Chọn user có sở hữu Hộ Vệ Thần.")
    @discord.app_commands.describe(so_tien="Chọn số tiền muốn cược.")
    @discord.app_commands.describe(loai="Chọn loại hình chiến đấu.")
    @discord.app_commands.describe(loai_tien="Chọn loại tiền muốn cược.")
    @discord.app_commands.choices(loai_tien=[
        Choice(name="Gold", value="G"),
        Choice(name="Silver", value="S"),
        Choice(name="Copper", value="C"),
    ])
    @discord.app_commands.choices(loai=[
        Choice(name="Chiến đấu bình thường (Dùng mọi kỹ năng)", value="A"),
        Choice(name="Chiến đấu không dùng bất kỳ kỹ năng nào", value="B"),
        Choice(name="Chiến đấu không dùng kỹ năng Tẩy Não", value="C"),
        Choice(name="Chiến đấu không dùng kỹ năng Triệu Linh", value="D"),
        Choice(name="Chiến đấu không dùng kỹ năng Triệu Linh và Tẩy Não", value="E"),
    ])
    @discord.app_commands.describe(max_players="Cho phép bấy nhiêu người gia nhập cuộc chiến.")
    @discord.app_commands.choices(max_players=[
        Choice(name="1", value="1"),
        Choice(name="2", value="2"),
        Choice(name="3", value="3"),
    ])
    @discord.app_commands.checks.cooldown(1, 30)
    async def ga_challenge_slash_command(self, interaction: discord.Interaction, target: discord.Member, max_players: str = "3", loai:str = "A", so_tien:int = None, loai_tien:str = None):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if target!= None and target.id == interaction.user.id:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Bạn không thể chiến đấu với bản thân mình!", ephemeral=True, view=view)
            view.message = mess
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        elif user_profile.guardian == None or user_profile.guardian.is_dead:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        if user_profile.guardian.last_joined_battle != None:
            time_window = timedelta(minutes=1)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.guardian.last_joined_battle, time_window=time_window)
            if check:
                next_time = user_profile.guardian.last_joined_battle + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn vừa tham chiến xong. Vui lòng đợi một phút rồi thực hiện lại lệnh!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return

        if user_profile.guardian.time_to_recover != None:
            if user_profile.guardian.time_to_recover > datetime.now():
                view = SelfDestructView(timeout=30)
                next_time = user_profile.guardian.time_to_recover
                unix_time = int(next_time.timestamp())
                mess = await interaction.followup.send(content=f"Hộ Vệ Thần của bạn đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True, view=view)
                view.message = mess
                return
            else:
                #Hồi phục 50% máu, 50% thể lực
                health = int(user_profile.guardian.max_health*50/100)
                stamina = int(user_profile.guardian.max_stamina*50/100)
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
        
        
        target_profile = None
        if target != None:
            target_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=target.id)
            if target_profile == None:
                view = SelfDestructView(timeout=30)
                mess = await interaction.followup.send(content=f"Đối thủ {target.mention} vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
                view.message = mess
                return
            elif target_profile.guardian == None or target_profile.guardian.is_dead:
                view = SelfDestructView(timeout=30)
                mess = await interaction.followup.send(content=f"Đối thủ {target.mention} vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
                view.message = mess
                return
            
            if target_profile.guardian.time_to_recover != None:
                if target_profile.guardian.time_to_recover > datetime.now():
                    view = SelfDestructView(timeout=30)
                    next_time = target_profile.guardian.time_to_recover
                    unix_time = int(next_time.timestamp())
                    mess = await interaction.followup.send(content=f"Hộ Vệ Thần của {target.mention} đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True, view=view)
                    view.message = mess
                    return
                else:
                    #Hồi phục 50% máu, 50% thể lực
                    health = int(target_profile.guardian.max_health*50/100)
                    stamina = int(target_profile.guardian.max_stamina*50/100)
                    ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=target.id, health=health, stamina=stamina)
        
        if (so_tien is None) != (loai_tien is None):
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Vui lòng chọn *cả* loại tiền và giá tiền hoặc để *cả hai trống*!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return

        if so_tien is not None and so_tien <= 0:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Số tiền cược phải lớn hơn 0!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if so_tien is not None:
            #Đảm bảo user đủ tiền cược
            error_message = None
            if loai_tien == "G" and (user_profile.gold < so_tien or target_profile.gold < so_tien):
                error_message = f"Bạn hoặc đối thủ không đủ tiền vàng để cược {so_tien} {EmojiCreation2.GOLD.value}!"
            if loai_tien == "S" and (user_profile.silver < so_tien or target_profile.silver < so_tien):
                error_message = f"Bạn hoặc đối thủ không đủ tiền bạc để cược {so_tien} {EmojiCreation2.SILVER.value}!"
            if loai_tien == "C" and (user_profile.copper < so_tien or target_profile.copper < so_tien):
                error_message = f"Bạn hoặc đối thủ không đủ tiền đồng để cược {so_tien} {EmojiCreation2.COPPER.value}!"
            if error_message != None:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"{error_message}",color=discord.Color.blue())
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
                view.message = mess
                return
            
        view = SelfDestructView(timeout=30)
        embed = discord.Embed(title=f"", description=f"Bạn đã thách đấu {target.mention}",color=discord.Color.blue())
        mess = await interaction.followup.send(embed=embed, view=view)
        view.message = mess
        
        loai_name_mapping = {
            "A": "Chiến đấu bình thường (Dùng mọi kỹ năng)",
            "B": "Chiến đấu không dùng bất kỳ kỹ năng nào",
            "C": "Chiến đấu không dùng kỹ năng Tẩy Não",
            "D": "Chiến đấu không dùng kỹ năng Triệu Linh",
            "E": "Chiến đấu không dùng kỹ năng Triệu Linh và Tẩy Não",
        }

        loai_label = loai_name_mapping.get(loai, "Không xác định")
        if max_players == None: max_players = "3"
        max_players_as_int = int(max_players)
        title = f"💥{interaction.user.mention} THÁCH ĐẤU {target.mention}💥"
        footer = f"Nếu ai vẫn còn chưa hiểu cách Thách Đấu Hộ Vệ Thần cứ nhắn câu\ngc help"
        embed = discord.Embed(title=f"", description=title, color=discord.Color.red())
        embed.add_field(name=f"", value=f"Hộ Vệ Thần {user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}** (Cấp {user_profile.guardian.level}) của {interaction.user.mention}", inline=False)
        embed.add_field(name=f"", value=f"🦾: **{user_profile.guardian.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=user_profile.guardian.health, max_value=user_profile.guardian.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=user_profile.guardian.stamina, max_value=user_profile.guardian.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=user_profile.guardian.mana, max_value=user_profile.guardian.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"Hộ Vệ Thần {target_profile.guardian.ga_emoji} - **{target_profile.guardian.ga_name}** (Cấp {target_profile.guardian.level}) của {target.mention}", inline=False)
        embed.add_field(name=f"", value=f"🦾: **{target_profile.guardian.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=target_profile.guardian.health, max_value=target_profile.guardian.max_health, emoji=EmojiCreation2.HP.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=target_profile.guardian.stamina, max_value=target_profile.guardian.max_stamina, emoji=EmojiCreation2.STAMINA.value)}\n{UtilitiesFunctions.progress_bar_stat(input_value=target_profile.guardian.mana, max_value=target_profile.guardian.max_mana, emoji=EmojiCreation2.MP.value)}", inline=False)
        embed.add_field(name=f"", value="----------------", inline=False)
        embed.add_field(name=f"", value=f"Thể loại: **{loai_label}**", inline=False)
        embed.add_field(name=f"", value=f"Tối đa người tham gia: **{max_players}**", inline=False)
        if so_tien is not None:
            embed.add_field(name=f"", value=f"Tiền cược: **{so_tien}** {UtilitiesFunctions.get_emoji_from_loai_tien(loai_tien=loai_tien)}", inline=False)
        embed.set_footer(text=footer, icon_url=EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value)
        #Tạo view thách đấu
        view = GaChallengeView(guild_id=interaction.guild_id, user=interaction.user, target=target, user_profile=user_profile, target_profile=target_profile, max_players=max_players_as_int, battle_type=loai, so_tien=so_tien, loai_tien=loai_tien, title=title, footer = footer, channel_name=interaction.channel.name)
        channel = interaction.channel
        mess = await channel.send(content=f"{target.mention}", embed=embed, view=view)
        view.message = mess
    
    @ga_challenge_slash_command.error
    async def ga_challenge_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    
    #region ga quest slash
    @ga_group.command(name="quest", description="Cùng Hộ Vệ Thần làm nhiệm vụ và phiêu lưu!")
    @discord.app_commands.checks.cooldown(1, 30)
    async def ga_quest_slash_command(self, interaction: discord.Interaction):
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
            mess = await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        elif user_profile.guardian == None or user_profile.guardian.is_dead:
            view = SelfDestructView(timeout=30)
            mess = await interaction.followup.send(content=f"Vui lòng mua Hộ Vệ Thần trước bằng lệnh {SlashCommand.SHOP_GUARDIAN.value} đã!", ephemeral=True, view=view)
            view.message = mess
            return
        
        if user_profile.guardian.last_quest != None:
            time_window = timedelta(minutes=20)
            check = UtilitiesFunctions.check_if_within_time_delta(input=user_profile.guardian.last_quest, time_window=time_window)
            if check:
                next_time = user_profile.guardian.last_quest + time_window
                unix_time = int(next_time.timestamp())
                embed = discord.Embed(title=f"", description=f"🚫 Bạn vừa cùng Hộ Vệ Thần làm nhiệm vụ rồi. Vui lòng đợi đến <t:{unix_time}:t>!", color=0xc379e0)
                view = SelfDestructView(timeout=120)
                mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
                view.message = mess
                return

        if user_profile.guardian.time_to_recover != None:
            if user_profile.guardian.time_to_recover > datetime.now():
                view = SelfDestructView(timeout=30)
                next_time = user_profile.guardian.time_to_recover
                unix_time = int(next_time.timestamp())
                mess = await interaction.followup.send(content=f"Hộ Vệ Thần của bạn đang bị thương! Vui lòng chờ hồi phục vào lúc <t:{unix_time}:t> hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value}!", ephemeral=True, view=view)
                view.message = mess
                return
            else:
                #Hồi phục 50% máu, 50% thể lực
                health = int(user_profile.guardian.max_health*50/100)
                stamina = int(user_profile.guardian.max_stamina*50/100)
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
        
        if not CustomFunctions.check_if_dev_mode():
            ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_quest", date_value=datetime.now())
        
        #Chọn một quest ngẫu nhiên
        random_quest = random.choice(GaQuestLineExample.all_quests)
        random_quest[0].replace_guardian_name(user_profile.guardian.ga_name)
        title = random_quest[0].title
        description = random_quest[0].description
        # description = description.replace("{guardian.ga_name}", user_profile.guardian.ga_name)
        list_des = self.split_text_to_pairs(text=description)
        
        
        
        embed = discord.Embed(title=f"{EmojiCreation2.QUEST_ICON.value} {title} {EmojiCreation2.QUEST_ICON.value}", description=f"", color=discord.Color.blue())
        embed.add_field(name=f"", value=f"*{interaction.user.mention} đã cùng Hộ Vệ Thần {user_profile.guardian.ga_emoji} - **{user_profile.guardian.ga_name}** lên đường phiêu lưu.*", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        for des in list_des:
            embed.add_field(name=f"", value=f"{des}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=F"{EmojiCreation2.LETTER_A.value}: {random_quest[0].choice_a}", inline=False)
        embed.add_field(name=f"", value=F"{EmojiCreation2.LETTER_B.value}: {random_quest[0].choice_b}", inline=False)
        embed.add_field(name=f"", value=F"{EmojiCreation2.LETTER_C.value}: {random_quest[0].choice_c}", inline=False)
        timeout = 45
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=timeout)
        unix_time = int(end_time.timestamp())
        embed.add_field(name=f"", value="_____", inline=False)
        embed.add_field(name=f"", value=f"Thời gian còn lại: <t:{unix_time}:R>", inline=False)
        guardian_quest = GuardianAngelQuest(guardian=user_profile.guardian, user_name=interaction.user.name, user_display_name=interaction.user.display_name, channel_name=interaction.channel.name, quest_lines=random_quest)
        view = GaQuestView(user=interaction.user, guardian_quest=guardian_quest, current_quest_lines=random_quest[0], override_title=title, total_ga_stamina=random_quest[0].ga_stamina, total_dignity=random_quest[0].dignity_point, total_gold=random_quest[0].gold, total_silver=random_quest[0].silver, total_ga_exp=random_quest[0].ga_exp, total_ga_hp=random_quest[0].ga_health, total_ga_mana=random_quest[0].ga_mana, channel=interaction.channel, timeout=timeout)
        mess = await interaction.followup.send(embed=embed, ephemeral=False, view=view)
        view.message = mess
        print(f"User {interaction.user.name} started guardian quest at {interaction.channel.name} in guild {interaction.guild.name}.")
        
        
        
    def split_text_to_pairs(self, text: str):
        # Split sentences on punctuation + space
        sentence_endings = re.compile(r'(?<=[.!?])\s+')
        sentences = sentence_endings.split(text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]

        pairs = []
        # Step by 2 to avoid overlapping
        for i in range(0, len(sentences), 2):
            # If last sentence has no pair, just add it alone
            if i + 1 < len(sentences):
                pair = sentences[i] + " " + sentences[i + 1]
            else:
                pair = sentences[i]
            pairs.append(pair)
        return pairs

    @ga_quest_slash_command.error
    async def ga_quest_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    