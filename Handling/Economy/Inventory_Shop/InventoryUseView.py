import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items
from Handling.Economy.Inventory_Shop.LockpickView import LockpickView
import asyncio
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager

class InventoryUseView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member):
        super().__init__(timeout=30)
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
        if self.message != None: 
            await self.message.delete()
        
        
        #Thực hiện hiệu ứng của item
        if self.selected_item.item_type == "self_protection":
            await self.using_protection_item(interaction=interaction)
        elif self.selected_item.item_type == "attack":
            await self.using_attack_item(interaction=interaction)
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
        channel = interaction.channel
        if self.selected_item.item_id == "rank_up_1":
            #Xoá vật phẩm
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, amount= -1)
            #tăng một cấp
            ProfileMongoManager.add_one_level_and_reset_progress(guild_id=interaction.guild_id, user_id=interaction.user.id)
            text = ""
            #30% bị công an ập vào túm cổ và phạt 5% gold, tối đa 2000 gold
            police_chance = UtilitiesFunctions.get_chance(30)
            if police_chance:
                money_lost = int(self.user_profile.gold*10/100)
                if money_lost > 2000: money_lost = 2000
                text = f"\nNhưng công an đã ập vào bắt quả tang {interaction.user.mention} tội chơi thuốc! {interaction.user.mention} đã mất **{money_lost}** {EmojiCreation2.GOLD.value}!"
                ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, gold=-money_lost)
            await channel.send(f'{interaction.user.mention} đã nuốt [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và đột phá cấp bậc lên cấp **{self.user_profile.level+ 1}**!{text}')
            
        elif self.selected_item.item_id == "out_jail_ticket":
            #Xoá vật phẩm
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, amount= -1)
            #Reset jail
            ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=interaction.user.id, jail_time= None)
            await channel.send(f'{interaction.user.mention} đã móc [{self.selected_item.emoji} - **{self.selected_item.item_name}**] ra, và không còn bị giam lệnh nữa!')
        elif self.selected_item.item_id == "lock_pick_jail":
            #Xoá vật phẩm
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, amount= -1)
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
            #Xoá vật phẩm
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, amount= -1)
            #Reset last_breakup
            ProfileMongoManager.update_breakup_time(guild_id=interaction.guild_id, user_id=interaction.user.id, last_breakup= None)
            await channel.send(f'{interaction.user.mention} đã ngửi [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và không còn nhớ nhung gì người xưa nữa!')
        elif self.selected_item.item_id == "weed":
            #Xoá vật phẩm
            ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, amount= -1)
            #Giảm nhân phẩm, tăng exp, tăng điểm thân mật, tăng cả tỷ lệ love progressing
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, dignity_point=-self.selected_item.bonus_dignity)
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=self.user.id, bonus_exp=self.selected_item.bonus_exp)
            CoupleMongoManager.update_love_point(guild_id=interaction.guild_id,user_id=self.user.id, love_point=10)
            CoupleMongoManager.update_love_progressing(guild_id=interaction.guild_id,user_id=self.user.id, bonus_exp=10)
            #Reset last_breakup
            ProfileMongoManager.update_breakup_time(guild_id=interaction.guild_id, user_id=self.user.id, last_breakup= None)
            
            await channel.send(f'{interaction.user.mention} đã rít một điếu [{self.selected_item.emoji} - **{self.selected_item.item_name}**] và thư thả, quên đi người cũ, thắt chặt tình cảm hiện tại, mất đi một tý nhân phẩm nhưng tăng thêm EXP!')
        else:
            await channel.send(f'Darkie vẫn chưa code xong công dụng cho vật phẩm [{self.selected_item.emoji} - **{self.selected_item.item_name}**]', ephemeral=True)
        return
            
        
class ItemSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_item: List[Item], view: "InventoryUseView"):
        options = [
            discord.SelectOption(label=f"{item.item_name} (x{item.quantity})", description=item.item_description[:97] + '...', value=item.item_id)
            for item in list_item if item.item_type != "gift" and item.item_type != "misc" and item.item_type != "trash" and item.item_type != "seed"
        ]
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