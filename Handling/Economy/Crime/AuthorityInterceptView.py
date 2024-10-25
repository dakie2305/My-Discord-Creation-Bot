import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import EmojiCreation2
from datetime import datetime, timedelta
from Handling.Misc.SelfDestructView import SelfDestructView
import random

class AuthorityInterceptView(discord.ui.View):
    def __init__(self, user: discord.Member, user_profile: Profile, crime_type: str, target_profile: Profile = None,target_user: discord.Member = None, authority_user: Profile = None):
        super().__init__(timeout=30)
        self.old_message: discord.Message = None
        self.crime_type = crime_type
        self.user = user
        self.target_user = target_user
        self.user_profile = user_profile
        self.target_profile = target_profile
        self.target_profile = target_profile
        self.authority_user = authority_user
        
    @discord.ui.button(label="🚨 Chính Quyền Vào Cuộc 🚨", style=discord.ButtonStyle.red)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        if self.authority_user == None:
            await interaction.followup.send(f"Server này không có chính quyền để giải quyết!", ephemeral=True)
            return
        elif interaction.user.id != self.authority_user.id:
            await interaction.followup.send(f"Chỉ Chính Quyền <@{self.authority_user.user_id}> mới có thể giải quyết, vui lòng gọi Chính Quyền!", ephemeral=True)
            return
        
        if self.crime_type == "fight":
            if self.old_message != None: await self.old_message.delete()
            #Trừ tiền và trừ điểm nhân phẩm của người gây gỗ
            fine_money = int(self.user_profile.copper * 0.1) if self.user_profile != None else 500
            if fine_money == None or fine_money <500 : fine_money = 500
            if fine_money == None or fine_money > 45000 : fine_money = 45000
            dignity_point = 10
            embed = discord.Embed(title=f"", description=f"{self.user.mention} đã bị Chính Quyền <@{self.authority_user.user_id}> phát hiện gây rối mất trật tự!", color=0xc379e0)
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
            ProfileMongoManager.update_last_crime_now(guild_id=interaction.guild_id, user_id=self.user.id)
            await interaction.followup.send(embed=embed, ephemeral=False)
            return
        
        elif self.crime_type == "rob":
            if self.old_message != None: await self.old_message.delete()
            #Trừ tiền và trừ điểm nhân phẩm của người gây án
            #Random chọn giữa silver và copper
            silver_chance = self.get_chance(35)
            money = 0
            emoji = EmojiCreation2.COPPER.value
            if silver_chance and self.user_profile != None and self.user_profile.silver >= 3:
                #Trừ 20% silver
                money = int(self.user_profile.silver*0.2)
                if money == 0: money = 1
                emoji = EmojiCreation2.SILVER.value
            else:
                #Trừ 35% copper
                money = int(self.user_profile.copper*0.35)
                emoji = EmojiCreation2.COPPER.value
            
            dignity_point = 10
            embed = discord.Embed(title=f"", description=f"{self.user.mention} đã bị Chính Quyền <@{self.authority_user.user_id}> phát hiện ăn cắp!", color=0xc379e0)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{money}** {emoji}", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{dignity_point} nhân phẩm**", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tống vào tù trong 3 tiếng!", inline=False)
            
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, dignity_point= -dignity_point)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name,copper= -money)
            
            time_window = timedelta(hours=3)
            jail_time = datetime.now() + time_window
            #Jail 3 tiếng
            ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=self.user.id, jail_time=jail_time)
            #Cập nhật last crime
            ProfileMongoManager.update_last_crime_now(guild_id=interaction.guild_id, user_id=self.user.id)
            await interaction.followup.send(embed=embed, ephemeral=False)
            return
        
        elif self.crime_type == "laundry":
            if self.old_message != None: await self.old_message.delete()
            #Trừ tiền và trừ điểm nhân phẩm của người gây án
            #Random chọn giữa silver và copper
            silver_chance = self.get_chance(50)
            money = 0
            emoji = EmojiCreation2.COPPER.value
            if silver_chance and self.user_profile != None and self.user_profile.silver >= 1:
                #Trừ 35% silver
                money = int(self.user_profile.silver*0.35)
                if money == 0: money = 1
                emoji = EmojiCreation2.SILVER.value
            else:
                #Trừ 45% copper
                money = int(self.user_profile.copper*0.45)
                emoji = EmojiCreation2.COPPER.value
            
            dignity_point = 15
            embed = discord.Embed(title=f"", description=f"{self.user.mention} đã bị Chính Quyền <@{self.authority_user.user_id}> phát hiện tội trốn thuế và rửa tiền!", color=0xc379e0)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{money}** {emoji}", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{dignity_point} nhân phẩm**", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tống vào tù trong 5 tiếng!", inline=False)
            
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, dignity_point= -dignity_point)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name,copper= -money)
            
            time_window = timedelta(hours=5)
            jail_time = datetime.now() + time_window
            #Jail 5 tiếng
            ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=self.user.id, jail_time=jail_time)
            #Cập nhật last crime
            ProfileMongoManager.update_last_crime_now(guild_id=interaction.guild_id, user_id=self.user.id)
            await interaction.followup.send(embed=embed, ephemeral=False)
            return
        
        elif self.crime_type == "smuggler":
            if self.old_message != None: await self.old_message.delete()
            #Trừ tiền và trừ điểm nhân phẩm của người gây án
            #Trừ 45% copper
            money = int(self.user_profile.copper*0.45)
            money += 2000
            emoji = EmojiCreation2.COPPER.value
            dignity_point = 15
            embed = discord.Embed(title=f"", description=f"{self.user.mention} đã bị Chính Quyền <@{self.authority_user.user_id}> phát hiện tội buôn lậu hàng cấm!", color=0xc379e0)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{money}** {emoji}", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Trừ **{dignity_point} nhân phẩm**", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tống vào tù trong 3 tiếng!", inline=False)
            
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, dignity_point= -dignity_point)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name,copper= -money)
            
            time_window = timedelta(hours=3)
            jail_time = datetime.now() + time_window
            #Jail 3 tiếng
            ProfileMongoManager.update_jail_time(guild_id=interaction.guild_id, user_id=self.user.id, jail_time=jail_time)
            #Cập nhật last crime
            ProfileMongoManager.update_last_crime_now(guild_id=interaction.guild_id, user_id=self.user.id)
            await interaction.followup.send(embed=embed, ephemeral=False)
            return
        
        return
    
    def get_chance(self, chance: int):
        rand_num = random.randint(0, 100)
        if rand_num < chance:
            return True
        else:
            return False