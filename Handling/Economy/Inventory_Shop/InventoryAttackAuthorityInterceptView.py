import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List
from datetime import datetime, timedelta
from db.Class.CustomClass import UserInfo
import db.DbMongoManager as db 

class InventoryAttackAuthorityInterceptView(discord.ui.View):
    def __init__(self, user_profile: Profile, user: discord.Member, target_profile: Profile, target: discord.Member, authority_user: Profile):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.user_profile = user_profile
        self.user = user
        self.target_profile = target_profile
        self.target = target
        self.authority_user = authority_user
        self.use_button = discord.ui.Button(label="🚨 Chính Quyền Vào Cuộc 🚨", style=discord.ButtonStyle.green)
        self.use_button.callback = self.use_button_callback
        self.add_item(self.use_button)
        self.interrupted = False

    async def on_timeout(self):
        if self.message != None: 
            try:
                await self.message.delete()
            except Exception: return
            return
    
    async def use_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.authority_user == None:
            await interaction.followup.send(f"Server này không có chính quyền để giải quyết!", ephemeral=True)
            return
        elif interaction.user.id != self.authority_user.user_id:
            await interaction.followup.send(f"Chỉ Chính Quyền <@{self.authority_user.user_id}> mới có thể giải quyết, vui lòng gọi Chính Quyền!", ephemeral=True)
            return
        self.interrupted = True
        await interaction.followup.send(content="Bạn đã ngăn chặn tấn công!")
        channel = interaction.channel
        #Trừ tiền và trừ điểm nhân phẩm của người gây gỗ
        fine_money = int(self.user_profile.silver * 0.2) if self.user_profile != None else 100
        if fine_money == None or fine_money <100 : fine_money = 100
        if fine_money == None or fine_money > 450000 : fine_money = 450000
        dignity_point = 20
        
        embed = discord.Embed(title=f"", description=f"<@{self.user_profile.user_id}> đã bị Chính Quyền <@{self.authority_user.user_id}> phát hiện dùng vũ khí trái phép!", color=0xc379e0)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{fine_money}** {EmojiCreation2.SILVER.value}", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{dignity_point} nhân phẩm**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tống vào tù trong 2 tiếng!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tịch thu loại vũ khí [{self.user_profile.attack_item.emoji}-{self.user_profile.attack_item.item_name}]!", inline=False)
        
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, dignity_point= -dignity_point)
        ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name,copper= -fine_money)
        
        #Xoá vũ khí
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.user_profile.attack_item, amount= -100)
        time_window = timedelta(hours=2)
        jail_time = datetime.now() + time_window
        #Jail
        ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=self.user.id, jail_time=jail_time)
        #Cập nhật last crime
        ProfileMongoManager.update_last_crime_now(guild_id=interaction.guild_id, user_id=self.user.id)
        me = await channel.send(embed=embed)
        await self.jail_real(interaction=interaction, actual_user=self.user, message=me)
        return        
    
    
    async def jail_real(self, interaction: discord.Interaction, actual_user: discord.Member, message: discord.Message):
                #Server True Heavens sẽ jail thật luôn
                if interaction.guild_id !=  1256987900277690470: return
                # Calculate the end time
                end_time = datetime.now() + timedelta(minutes=10)
                mordern_date_time_format = end_time.strftime(f"%d/%m/%Y %H:%M")
                # Save user's roles
                original_roles = [role for role in actual_user.roles if not role.is_default() and not role.is_premium_subscriber()]
                stored_original_roles = []
                for role in original_roles:
                    old_role = {
                                    "role_id": role.id,
                                    "role_name": role.name
                                    }
                    stored_original_roles.append(old_role)
                    # Remove all roles and add jail role
                jail_role = discord.utils.get(actual_user.guild.roles, name="Đáy Xã Hội")
                if not jail_role:
                    jail_role = await actual_user.guild.create_role(name="Đáy Xã Hội")
                user_info = UserInfo(
                        user_id=actual_user.id,
                        user_name=actual_user.name,
                        user_display_name=actual_user.display_name,
                        reason= f"Thành phần thực hiện phạm tội tại <#{message.channel.id}>",
                        jail_until= end_time,
                        roles=stored_original_roles
                        )
                    #Tìm xem user này đã có chưa, chưa có thì insert
                jail_db = "jailed_user"
                search_user = db.find_user_by_id(user_info.user_id, jail_db)
                if search_user == None:
                        #Insert
                        db.create_user(user_info= user_info, chosen_collection= jail_db)
                else:
                        #Update lại jail_until và reason
                        updated_data = {"jail_until": end_time.isoformat(), "reason" :user_info.reason }
                        db.update_guild_extra_info(guild_id=user_info.user_id, update_data= updated_data)
                try:
                        for ori_role in original_roles:
                            try:
                                await actual_user.remove_roles(ori_role)
                            except Exception:
                                continue
                        await actual_user.add_roles(jail_role)
                        
                        # Create embed object
                        embed = discord.Embed(title="Đại Lao Thẳng Tiến", description=f"Kẻ tội đồ {self.user.mention} đã bị chính quyền <@{self.authority_user.user_id}> bắt quả tang định dùng vũ khí trái phép!", color=0x00FF00)  # Green color
                        embed.add_field(name="Lý do bị tù đày:", value=user_info.reason, inline=False)  # Single-line field
                        embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
                        embed.add_field(name="Ghi chú", value="Nếu quá thời hạn phạt tù mà chưa được ra tù thì hãy la làng lên nhé!", inline=False) 
                        embed.set_footer(text=f"Đã bị tống giam bởi: Chính Quyền")  # Footer text
                        channel = interaction.guild.get_channel(1257012036718563380)
                        if channel:
                            await channel.send(embed=embed)
                        
                except Exception as e:
                        print(e)
        
        