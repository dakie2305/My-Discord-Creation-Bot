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
            money = int(user_profile.guardian.worth_amount * 30 / 100)
            if user_profile.guardian.level > 30 and user_profile.guardian.is_dead == False:
                money += int(user_profile.guardian.worth_amount*user_profile.guardian.level/100)
            if money > 500 and user_profile.guardian.worth_type == "D": money = 500
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
        if interaction.guild_id == 1256987900277690470:
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
        
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id)
        ProfileMongoManager.update_main_guardian_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id, bonus_exp=random_bonus_exp)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id,user_id=interaction.user.id, guild_name="", user_display_name="", user_name="", dignity_point=dignity_point)
        ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, mana=mana)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_meditation", date_value=datetime.now())
        
        
        await interaction.followup.send(embed=embed)
    
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
            time_window = timedelta(hours=1)
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
        if interaction.guild_id == 1256987900277690470:
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
        
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id)
        ProfileMongoManager.update_main_guardian_level_progressing(guild_id=interaction.guild_id,user_id=interaction.user.id, bonus_exp=random_bonus_exp)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id,user_id=interaction.user.id, guild_name="", user_display_name="", user_name="", dignity_point=dignity_point)
        ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_feed", date_value=datetime.now())
        ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id,user_id=interaction.user.id, health=health, stamina=stamina)
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id,user_id=interaction.user.id, user_display_name="", user_name="", guild_name="", item=chosen_item, amount=-1)
        await interaction.followup.send(embed=embed)
        
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
        gold_reward = 75
        silver_reward = 100
        exp_reward = 80
        dignity_point_reward = 10
        
        if is_players_versus_player:
            gold_reward = 45
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
        
        #Tính lại theo enemy_ga
        gold_reward = int(gold_reward + gold_reward*enemy.level*0.2)
        silver_reward = int(silver_reward + silver_reward*enemy.level*0.3)
        exp_reward = int(exp_reward + exp_reward*enemy.level*0.1)
        if CustomFunctions.check_if_dev_mode() == False:
            ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_battle", date_value=datetime.now())
            ProfileMongoManager.update_main_guardian_profile_time(guild_id=interaction.guild_id,user_id=interaction.user.id, data_type="last_joined_battle", date_value=datetime.now())
        view = GaBattleView(user=interaction.user, user_profile=user_profile, target=target, target_profile=target_profile, is_players_versus_players=is_players_versus_player, max_players=max_players_as_int, enemy_ga=enemy, embed_title=title, guild_id=interaction.guild_id, gold_reward=gold_reward, silver_reward=silver_reward, bonus_exp=exp_reward, dignity_point=dignity_point_reward)
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