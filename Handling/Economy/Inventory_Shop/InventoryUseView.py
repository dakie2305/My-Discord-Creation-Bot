import discord
from CustomEnum.GuardianMemoryTag import GuardianMemoryTag
from Handling.Economy.GA.GaDugeonView import GaDugeonView
from Handling.Economy.Global import GlobalMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items
from Handling.Economy.Inventory_Shop.LockpickView import LockpickView
import asyncio
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
from datetime import datetime, timedelta
import random
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills

class InventoryUseView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member):
        super().__init__(timeout=15)
        self.message: discord.Message = None
        self.user_profile = user_profile
        self.user = user
        self.add_item(ItemSelect(user, user_profile.list_items, self))
        self.selected_item: Item = None
        self.use_button = discord.ui.Button(label="🖲️ Sử Dụng Vật Phẩm", style=discord.ButtonStyle.green)
        self.use_button.callback = self.use_button_callback
        self.add_item(self.use_button)

    async def on_timeout(self):
        if self.message != None: 
            try:
                await self.message.delete()
            except Exception: return
            return
    
    async def use_button_callback(self, interaction: discord.Interaction):
        if self.selected_item == None: return
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        
        self.user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        #Kiểm tra xem item đó còn không
        check_fail = True
        for player_item in self.user_profile.list_items:
            if player_item.item_id == self.selected_item.item_id and player_item.quantity > 0:
                check_fail = False
                break
        if check_fail:
            await interaction.followup.send(f'Vật phẩm {self.selected_item.emoji} - **{self.selected_item.item_name}** đã không còn trong túi đồ của bạn!', ephemeral=True)
            return
        
        await interaction.followup.send(f'Bạn đã dùng vật phẩm [{self.selected_item.emoji} - **{self.selected_item.item_name}**]', ephemeral=True)

        
        
        #Thực hiện hiệu ứng của item
        if self.selected_item.item_type == "self_protection":
            await self.using_protection_item(interaction=interaction)
            if self.message != None:
                await self.message.delete()
        elif self.selected_item.item_type == "attack":
            await self.using_attack_item(interaction=interaction)
            if self.message != None:
                await self.message.delete()
        elif self.selected_item.item_type == "self_support":
            await self.using_support_item(interaction=interaction)
        else:
            await interaction.followup.send(f'Darkie vẫn chưa code xong công dụng cho vật phẩm [{self.selected_item.emoji} - **{self.selected_item.item_name}**]', ephemeral=True)
            return
    
    #region use protection item
    async def using_protection_item(self, interaction: discord.Interaction):
        channel = interaction.channel
        if self.user_profile.protection_item == None:
            #Gắn các vật phẩm vào bản thân
            #-1 vật phẩm
            ProfileMongoManager.equip_protection_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, unequip=False)
            await channel.send(f'{interaction.user.mention} đã sử dụng vật phẩm [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để bảo hộ bản thân!')
        else:
            #Gỡ vật phẩm cũ ra
            ProfileMongoManager.equip_protection_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.user_profile.protection_item, unequip=True)
            #Gắn vật phẩm mới vào
            ProfileMongoManager.equip_protection_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, unequip=False)
            await channel.send(f'{interaction.user.mention} đã gỡ [{self.user_profile.protection_item.emoji} - **{self.user_profile.protection_item.item_name}**] để dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**]')
        return
    
    #region equip attack item
    async def using_attack_item(self, interaction: discord.Interaction):
        channel = interaction.channel
        if self.user_profile.attack_item == None:
            #Gắn các vật phẩm vào bản thân
            #-1 vật phẩm
            ProfileMongoManager.equip_attack_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, unequip=False)
            await channel.send(f'{interaction.user.mention} đã mang theo vũ khí [{self.selected_item.emoji} - **{self.selected_item.item_name}**] theo bản thân!')
        else:
            #Gỡ vật phẩm cũ ra
            ProfileMongoManager.equip_attack_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.user_profile.attack_item, unequip=True)
            #Gắn vật phẩm mới vào
            ProfileMongoManager.equip_attack_item_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, unequip=False)
            await channel.send(f'{interaction.user.mention} đã cất vũ khí [{self.user_profile.attack_item.emoji} - **{self.user_profile.attack_item.item_name}**] đi, và cầm theo [{self.selected_item.emoji} - **{self.selected_item.item_name}**]')
        return

    #region use support item
    async def using_support_item(self, interaction: discord.Interaction):
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id)
        text = ""
        channel = interaction.channel
        flag_delete_item = True
        if self.selected_item.item_id == "rank_up_1":
            #tăng một cấp
            ProfileMongoManager.add_one_level_and_reset_progress(guild_id=interaction.guild_id, user_id=interaction.user.id)
            #30% bị công an ập vào túm cổ và phạt 5% gold, tối đa 2000 gold
            police_chance = UtilitiesFunctions.get_chance(30)
            if police_chance:
                money_lost = int(self.user_profile.gold*10/100)
                if money_lost > 2000: money_lost = 2000
                text = f"\nNhưng công an đã ập vào bắt quả tang {interaction.user.mention} tội chơi thuốc! {interaction.user.mention} đã mất **{money_lost}** {EmojiCreation2.GOLD.value}!"
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, gold=-money_lost)
            await channel.send(f'{interaction.user.mention} đã nuốt [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và đột phá cấp bậc lên cấp **{self.user_profile.level+ 1}**!{text}')
        elif self.selected_item.item_id == "out_jail_ticket":
            #Reset jail
            ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time= None)
            await channel.send(f'{interaction.user.mention} đã móc [{self.selected_item.emoji} - **{self.selected_item.item_name}**] ra, và không còn bị giam lệnh nữa!')
        elif self.selected_item.item_id == "lock_pick_jail":
            #Tạo embed
            preloading_text = f"{interaction.user.mention} đang sử dụng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để chuẩn bị vượt ngục!"
            if self.user_profile.is_authority == False:
                preloading_text += "\nCó thể gọi Chính Quyền vào cuộc để ngăn chặn vượt ngục!"
            embed = discord.Embed(title=f"", description=f"{preloading_text}", color=0xc379e0)
            authority_user = ProfileMongoManager.get_authority(interaction.guild_id)
            view = LockpickView(user=interaction.user, user_profile=self.user_profile, authority_user=authority_user)
            m = await channel.send(embed=embed, view=view)
            view.old_message = m
            #Đợi để xác định có thoát được không
            await asyncio.sleep(20)
            if view.interrupted == True: return
            embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã sử dụng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và vượt ngục thành công!", color=0xc379e0)
            #Reset jail
            ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time= None)
            await m.edit(embed=embed, view=None)
            return
        elif self.selected_item.item_id == "forget_flower":
            #Reset last_breakup
            ProfileMongoManager.update_breakup_time(guild_id=interaction.guild_id, user_id=interaction.user.id, last_breakup= None)
            await channel.send(f'{interaction.user.mention} đã ngửi [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và không còn nhớ nhung gì người xưa nữa!')
        elif self.selected_item.item_id == "weed":
            #Giảm nhân phẩm, tăng exp, tăng điểm thân mật, tăng cả tỷ lệ love progressing
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, dignity_point=-self.selected_item.bonus_dignity)
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=self.user.id, bonus_exp=self.selected_item.bonus_exp)
            CoupleMongoManager.update_love_point(guild_id=interaction.guild_id,user_id=self.user.id, love_point=10)
            CoupleMongoManager.update_love_progressing(guild_id=interaction.guild_id,user_id=self.user.id, bonus_exp=10)
            #Reset last_breakup
            ProfileMongoManager.update_breakup_time(guild_id=interaction.guild_id, user_id=self.user.id, last_breakup= None)
            
            #30% bị công an ập vào túm cổ và phạt 10% gold, tối đa 8000 gold
            police_chance = UtilitiesFunctions.get_chance(30)
            if police_chance:
                money_lost = int(self.user_profile.gold*10/100)
                if money_lost > 8000: money_lost = 8000
                text = f"\nNhưng công an đã ập vào bắt quả tang {interaction.user.mention} tội chơi đồ! {interaction.user.mention} đã mất **{money_lost}** {EmojiCreation2.GOLD.value}!"
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, gold=-money_lost)
            
            await channel.send(f'{interaction.user.mention} đã rít một điếu [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và thư thả, quên đi người cũ, thắt chặt tình cảm hiện tại, mất đi một tý nhân phẩm nhưng tăng thêm EXP!{text}')
        elif self.selected_item.item_id == "rank_down_1":
            #trừ một cấp
            ProfileMongoManager.add_one_level_and_reset_progress(guild_id=interaction.guild_id, user_id=interaction.user.id, level=-1)
            #30% bị công an ập vào túm cổ và phạt 5% gold, tối đa 2000 gold
            police_chance = UtilitiesFunctions.get_chance(30)
            if police_chance:
                money_lost = int(self.user_profile.gold*10/100)
                if money_lost > 2000: money_lost = 2000
                text = f"\nNhưng công an đã ập vào bắt quả tang {interaction.user.mention} tội chơi thuốc! {interaction.user.mention} đã mất **{money_lost}** {EmojiCreation2.GOLD.value}!"
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, gold=-money_lost)
            await channel.send(f'{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và tự phế một cấp bậc của bản thân xuống cấp **{self.user_profile.level - 1}**!{text}')
            
        elif self.selected_item.item_id == "trash_cot_use":
            await channel.send(f'{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để bón cho khu vườn của mình và giúp cây lớn nhanh hơn!')
            #Cộng ba mươi phút cho cây trồng
            if self.user_profile.plant != None:
                plant_date = self.user_profile.plant.plant_date - timedelta(minutes=25)
                ProfileMongoManager.update_plant_date(guild_id=interaction.guild_id, user_id=self.user.id, plant_date=plant_date)
        
        elif self.selected_item.item_id == "ga_heal_1":
            text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] nhưng quên mất mình làm gì có Hộ Vệ Thần!"
            health_to_heal = 0
            if self.user_profile.guardian!= None and self.user_profile.guardian.is_dead == False:
                health_to_heal = int(self.user_profile.guardian.max_health*0.3)
                total = health_to_heal+self.user_profile.guardian.health
                if total > self.user_profile.guardian.max_health:
                    total = self.user_profile.guardian.max_health
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id, user_id=self.user.id, health=health_to_heal)
                #roll chance
                roll_chance = UtilitiesFunctions.get_chance(15)
                if roll_chance:
                    ProfileMongoManager.add_memory_guardian(guild_id=interaction.guild_id, user_id=self.user.id, memory_description=f"Đã được {interaction.user.display_name} cho dùng bình [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để hồi phục.", tag = GuardianMemoryTag.RESTORATION.value)
                addition_text = f"\nMáu hiện tại: {total}/{self.user_profile.guardian.max_health}"
                text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và hồi phục **{health_to_heal}** Máu {EmojiCreation2.HP.value} cho Hộ Vệ Thần của mình!{addition_text}"
            await channel.send(content=text)
            
        elif self.selected_item.item_id == "ga_stamina_1":
            text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] nhưng quên mất mình làm gì có Hộ Vệ Thần!"
            stats_restored = 0
            if self.user_profile.guardian!= None and self.user_profile.guardian.is_dead == False:
                stats_restored = int(self.user_profile.guardian.max_stamina*0.5)
                total = stats_restored+self.user_profile.guardian.stamina
                if total > self.user_profile.guardian.max_stamina:
                    total = self.user_profile.guardian.max_stamina
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id, user_id=self.user.id, stamina=stats_restored)
                #roll chance
                roll_chance = UtilitiesFunctions.get_chance(15)
                if roll_chance:
                    ProfileMongoManager.add_memory_guardian(guild_id=interaction.guild_id, user_id=self.user.id, memory_description=f"Đã được {interaction.user.display_name} cho dùng bình [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để hồi phục.", tag = GuardianMemoryTag.RESTORATION.value)
                addition_text = f"\nThể lực hiện tại: {total}/{self.user_profile.guardian.max_stamina}"
                text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và hồi phục **{stats_restored}** Thể Lực {EmojiCreation2.STAMINA.value} cho Hộ Vệ Thần của mình!{addition_text}"
            await channel.send(content=text)
        elif self.selected_item.item_id == "ga_mana_1":
            text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] nhưng quên mất mình làm gì có Hộ Vệ Thần!"
            stats_restored = 0
            if self.user_profile.guardian!= None and self.user_profile.guardian.is_dead == False:
                stats_restored = int(self.user_profile.guardian.max_mana*0.5)
                total = stats_restored+self.user_profile.guardian.mana
                if total > self.user_profile.guardian.max_mana:
                    total = self.user_profile.guardian.max_mana
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id, user_id=self.user.id, mana=stats_restored)
                #roll chance
                roll_chance = UtilitiesFunctions.get_chance(15)
                if roll_chance:
                    ProfileMongoManager.add_memory_guardian(guild_id=interaction.guild_id, user_id=self.user.id, memory_description=f"Đã được {interaction.user.display_name} cho dùng bình [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để hồi phục.", tag = GuardianMemoryTag.RESTORATION.value)
                addition_text = f"\nMana hiện tại: {total}/{self.user_profile.guardian.max_mana}"
                text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và hồi phục **{stats_restored}** Mana {EmojiCreation2.MP.value} cho Hộ Vệ Thần của mình!{addition_text}"
            await channel.send(content=text)
            
        elif self.selected_item.item_id == "ga_all_restored":
            text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] nhưng quên mất mình làm gì có Hộ Vệ Thần!"
            if self.user_profile.guardian!= None and self.user_profile.guardian.is_dead == False:
                ProfileMongoManager.update_guardian_stats(guild_id=interaction.guild_id, user_id=self.user.id, health=self.user_profile.guardian.max_health, stamina=self.user_profile.guardian.max_stamina, mana=self.user_profile.guardian.max_mana)

                #roll chance
                roll_chance = UtilitiesFunctions.get_chance(30)
                if roll_chance:
                    ProfileMongoManager.add_memory_guardian(guild_id=interaction.guild_id, user_id=self.user.id, memory_description=f"Đã được {interaction.user.display_name} cho dùng bình [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để hồi phục.", tag = GuardianMemoryTag.RESTORATION.value)

                text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và hồi phục Hộ Vệ Thần về trạng thái hoàng kim!"
            await channel.send(content=text)
        elif self.selected_item.item_id == "ga_resurrection":
            text = f"{interaction.user.mention} đã sử dụng đến [{self.selected_item.emoji} - **{self.selected_item.item_name}**] nhưng quên mất mình làm gì có Hộ Vệ Thần!"
            if self.user_profile.guardian!= None:
                ProfileMongoManager.set_guardian_dead_status(guild_id=interaction.guild_id, user_id=self.user.id, is_dead=False)
                ProfileMongoManager.increase_count_guardian(guild_id=interaction.guild_id, user_id=self.user.id, count_type="count_resurrection")
                ProfileMongoManager.add_memory_guardian(guild_id=interaction.guild_id, user_id=self.user.id, memory_description="Đã được chủ nhân đưa về từ cõi chết bằng Phục Sinh Thạch.", tag = GuardianMemoryTag.RESURRECTION.value)
                text = f"{interaction.user.mention} đã lập tức dùng đến [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để Hộ Vệ Thần của mình từ cõi chết trở về!"
            await channel.send(content=text)
        elif "profile_color_" in self.selected_item.item_id:
            text = f"{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để đổi màu cho profile của bản thân!"
            color_map = {
                "profile_color_red": 0xff0000,
                "profile_color_light_red": 0xff6666,
                "profile_color_blue": 0x0000ff,
                "profile_color_teal": 0x00ffff,
                "profile_color_green": 0x33ff33,
                "profile_color_black": 0x000001,
                "profile_color_misty_rose": 0xffd1cc,
                "profile_color_pink": 0xff99aa,
                "profile_color_purple": 0x9900cc,
                "profile_color_orange": 0xff8000,
                "profile_color_yellow": 0xffff00,
            }
            color = color_map.get(self.selected_item.item_id, 0xffffff)  # Default
            ProfileMongoManager.update_profile_color(guild_id=interaction.guild_id, user_id=self.user.id, color=color)
            await channel.send(content=text)
        elif self.selected_item.item_id == "ga_boss_summoning":
            text = f"{interaction.user.mention} đã cầm [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và thực hiện nghi thức triệu hồi Hộ Vệ Thần huyền thoại!"
            await channel.send(content=text)
            if self.message != None:
                try:
                    await self.message.delete()
                except Exception as e:
                    print(f"Failed to delete message in channel {interaction.channel.name} in guild {interaction.guild.name} after using GA summoning book.\n{e}")
            await self.handling_summoning_ga_book(interaction=interaction, level=self.user_profile.guardian.level if self.user_profile.guardian else 1)
        
        elif self.selected_item.item_id == "global_card":
            GlobalMongoManager.update_enable_until(user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, guild_id=interaction.guild_id, guild_name=interaction.guild.name)
            await channel.send(f'{interaction.user.mention} đã dùng [{self.selected_item.emoji} - **{self.selected_item.item_name}**] để mở khóa chức năng Liên Thông Đa Server! Thẻ sẽ hết hiệu lực sau hai tuần!')
        else:
            #Không xoá
            flag_delete_item = False
            await channel.send(f'Darkie vẫn chưa code xong công dụng cho vật phẩm [{self.selected_item.emoji} - **{self.selected_item.item_name}**]', ephemeral=True)
        if flag_delete_item:
            #Xoá vật phẩm
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, amount= -1)
        return
    
    #region summoning ga book
    async def handling_summoning_ga_book(self, interaction: discord.Interaction, level: int):
        level = max(level, 110) # Cấp tối thiểu là 110
        guardian_chance = 100
        mysterious_stats = True
        bonus_percent = 15
        double_enemy_chance = 25
        double_enemy_dice = UtilitiesFunctions.get_chance(double_enemy_chance)
        top_1_leaderboard_dice = UtilitiesFunctions.get_chance(8)
        is_top_1_server = False
        if top_1_leaderboard_dice:
            #Lấy top 1 của leaderboard ra làm enemy
            enemy = self.get_top_1_ga_leaderboard(guild_id=interaction.guild_id)
            print(f"Top 1 GA leaderboard: {enemy.ga_name} - {enemy.level} at guild {interaction.guild.name}")
            if enemy is None:
                enemy = ListGAAndSkills.get_random_ga_enemy_generic(level=level, guardian_chance=guardian_chance)
            else: is_top_1_server = True
            enemy.health = enemy.max_health
            enemy.mana = enemy.max_mana
            enemy.stamina = enemy.max_stamina
        else:
            enemy = ListGAAndSkills.get_random_ga_enemy_generic(level=level, guardian_chance=guardian_chance)
        enemy_2 = None
        embed = discord.Embed(title=f"", description=f"{EmojiCreation2.STUN_SKILL.value} **Hộ Vệ Thần Huyền Thoại** {EmojiCreation2.STUN_SKILL.value}", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        if double_enemy_dice:
            enemy = ListGAAndSkills.get_random_ga_enemy_generic(level=int(level/2), guardian_chance=guardian_chance)
            text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {UtilitiesFunctions.replace_with_question_marks(enemy.level)})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{enemy.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.health, max_value=enemy.max_health, emoji=EmojiCreation2.HP.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.stamina, max_value=enemy.max_stamina, emoji=EmojiCreation2.STAMINA.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.mana, max_value=enemy.max_mana, emoji=EmojiCreation2.MP.value, mysterious_stats=mysterious_stats)}", inline=False)
            
            enemy_2 = ListGAAndSkills.get_random_ga_enemy_generic(level=int(level/3), guardian_chance=guardian_chance)
            text = f"Kẻ thù {enemy_2.ga_emoji} - **{enemy_2.ga_name}** (Cấp {UtilitiesFunctions.replace_with_question_marks(enemy_2.level)})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{enemy_2.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy_2.health, max_value=enemy_2.max_health, emoji=EmojiCreation2.HP.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy_2.stamina, max_value=enemy_2.max_stamina, emoji=EmojiCreation2.STAMINA.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy_2.mana, max_value=enemy_2.max_mana, emoji=EmojiCreation2.MP.value, mysterious_stats=mysterious_stats)}", inline=False)
        else:
            text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {enemy.level})"
            text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {UtilitiesFunctions.replace_with_question_marks(enemy.level)})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{enemy.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.health, max_value=enemy.max_health, emoji=EmojiCreation2.HP.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.stamina, max_value=enemy.max_stamina, emoji=EmojiCreation2.STAMINA.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.mana, max_value=enemy.max_mana, emoji=EmojiCreation2.MP.value, mysterious_stats=mysterious_stats)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        footer_text = f"Hộ Vệ Thần Huyền Thoại sẽ bắt ngẫu nhiên một người trong channel\nphải giao chiến với kẻ thù!"
        embed.set_footer(text=footer_text)
        print(f"Spawning GA boss by book, base level around {level} at channel {interaction.channel.name} in guild {interaction.guild.name}.")
        view = GaDugeonView(guild_id=interaction.guild_id, enemy_ga=enemy, enemy_ga_2=enemy_2, title=f"{EmojiCreation2.STUN_SKILL.value} **Hộ Vệ Thần Huyền Thoại** {EmojiCreation2.STUN_SKILL.value}", bonus_percent=bonus_percent, difficulty=4, footer_text=footer_text, channel_name=interaction.channel.name, is_top_1_server=is_top_1_server)
        m = await interaction.channel.send(embed=embed, view=view)
        view.message = m
        await view.catch_random_player_profile()
        return
    
    def get_top_1_ga_leaderboard(self, guild_id: int):
        #Lấy top 1 global ra
        top_1_global_dice = UtilitiesFunctions.get_chance(8)
        if top_1_global_dice:
            list_global_profiles = GlobalMongoManager.get_top_guardian_profiles(limit=2)
            if list_global_profiles and len(list_global_profiles) > 0:
                top_profile = list_global_profiles[0]
                if top_profile != None and top_profile.guardian:
                    top_profile.guardian.ga_name += f" ({top_profile.user_name})"
                    return top_profile.guardian
        #Lấy top 1 ga leaderboard ra
        list_profile_guild = ProfileMongoManager.find_all_profiles(guild_id=guild_id)
        if list_profile_guild == None or len(list_profile_guild) == 0:
            return None
        list_profile_guild = sorted(
                [profile for profile in list_profile_guild if profile.guardian], 
                key=lambda profile: profile.guardian.level, reverse=True
            )
        top_profile = list_profile_guild[0] if list_profile_guild else None
        if top_profile and top_profile.guardian:
            top_profile.guardian.ga_name += f" (<@{top_profile.user_id}>)"
            return top_profile.guardian
        else:
            return None
        
class ItemSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_item: List[Item], view: "InventoryUseView"):
        seen_item_ids = set()
        options = []

        for item in list_item:
            if item.item_type in ["gift", "misc", "trash", "seed"] or item.item_id in seen_item_ids:
                continue
            seen_item_ids.add(item.item_id)
            options.append(
                discord.SelectOption(
                    label=f"{item.item_name} (x{item.quantity})",
                    description=(item.item_description[:97] + '...') if len(item.item_description) > 100 else item.item_description,
                    value=item.item_id
                )
            )
        super().__init__(placeholder="Chọn vật phẩm muốn dùng", options=options)
        self.list_item = list_item
        self.parent_view  = view
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        selected_item_id = self.values[0]
        selected_item = next(item for item in self.list_item if item.item_id == selected_item_id)
        self.parent_view.selected_item = selected_item
        await interaction.followup.send(f'Bạn đã chọn chọn vật phẩm {selected_item.emoji} - **{selected_item.item_name}**', ephemeral=True)