import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import EmojiCreation2
from datetime import datetime, timedelta
from db.Class.CustomClass import UserInfo
import db.DbMongoManager as db 

class LockpickView(discord.ui.View):
    def __init__(self, user: discord.Member, user_profile: Profile, authority_user: Profile = None):
        super().__init__(timeout=30)
        self.old_message: discord.Message = None
        self.user = user
        self.user_profile = user_profile
        self.authority_user = authority_user
        self.interrupted = False
        
    @discord.ui.button(label="🚨 Chính Quyền Vào Cuộc 🚨", style=discord.ButtonStyle.red)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        if self.authority_user == None:
            await interaction.followup.send(f"Server này không có chính quyền để giải quyết!", ephemeral=True)
            return
        elif interaction.user.id != self.authority_user.user_id:
            await interaction.followup.send(f"Chỉ Chính Quyền <@{self.authority_user.user_id}> mới có thể giải quyết, vui lòng gọi Chính Quyền!", ephemeral=True)
            return
        self.interrupted = True
        
        #Trừ tiền và trừ điểm nhân phẩm của người vượt ngục
        fine_money = int(self.user_profile.copper * 0.1) if self.user_profile != None else 500
        if fine_money == None or fine_money <500 : fine_money = 500
        if fine_money == None or fine_money > 55000 : fine_money = 55000
        dignity_point = 10
        embed = discord.Embed(title=f"", description=f"<@{self.user_profile.user_id}> đã bị Chính Quyền <@{self.authority_user.user_id}> phát hiện định vượt ngục!", color=0xc379e0)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{fine_money}** {EmojiCreation2.COPPER.value}", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{dignity_point} nhân phẩm**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tống vào tù trong 3 tiếng!", inline=False)
        ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, dignity_point= -dignity_point)
        ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name,copper= -fine_money)
            
        time_window = timedelta(hours=3)
        jail_time = datetime.now() + time_window
        #Jail 3 tiếng
        ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=self.user.id, jail_time=jail_time)
        #Cập nhật last crime
        ProfileMongoManager.update_last_crime(guild_id=interaction.guild_id, user_id=self.user.id)
        me = await interaction.followup.send(embed=embed, ephemeral=False)
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
                        embed = discord.Embed(title="Đại Lao Thẳng Tiến", description=f"Kẻ tội đồ {self.user.mention} đã bị chính quyền <@{self.authority_user.user_id}> bắt quả tang trong lúc thực hiện hành vi phạm tội và tống vào đại lao!", color=0x00FF00)  # Green color
                        embed.add_field(name="Lý do bị tù đày:", value=user_info.reason, inline=False)  # Single-line field
                        embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
                        embed.add_field(name="Ghi chú", value="Nếu quá thời hạn phạt tù mà chưa được ra tù thì hãy la làng lên nhé!", inline=False) 
                        embed.set_footer(text=f"Đã bị tống giam bởi: Chính Quyền")  # Footer text
                        channel = interaction.guild.get_channel(1257012036718563380)
                        if channel:
                            await channel.send(embed=embed)
                        
                except Exception as e:
                        print(e)