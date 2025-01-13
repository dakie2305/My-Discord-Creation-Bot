import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
from Handling.Economy.Couple.CoupleClass import Couple
from typing import List
import asyncio

class GuessInfo:
    def __init__(self, user: discord.Member, money_type: str = None, money: int = 0):
        self.user = user
        self.money = money
        self.money_type = money_type

class CoupleMarryView(discord.ui.View):
    def __init__(self, couple: Couple, gif: str, timeout: int = 30):
        super().__init__(timeout= timeout)
        self.old_message: discord.Message = None
        self.couple = couple
        self.guest_list: List[GuessInfo] = []
        self.darkium = 0
        self.gold = 0
        self.silver = 0
        self.copper = 0
        self.gif = gif
        self.guild :discord.Guild = None
        
        self.remaining_time = timeout
        self.is_running = True
    
    async def start_countdown(self):
        while self.remaining_time > 0 and self.is_running:
            await asyncio.sleep(1)
            self.remaining_time -= 1
        if self.remaining_time <= 0 and self.is_running:
            self.is_running = False
            await self.trigger_result()
        return
    
    async def on_timeout(self):
        if self.old_message != None and self.is_running: 
            await self.trigger_result()
            return
    
    async def trigger_result(self):
        if self.old_message == None: return
        try:
            date_created = self.couple.date_created
            unix_time = int(date_created.timestamp())
            embed = discord.Embed(title=f"Đám Cưới Tân Uyên Ương",color=discord.Color.blue())
            embed.add_field(name=f"", value=f"Cặp đôi uyên ương <@{self.couple.first_user_id}> -`{UtilitiesFunctions.get_heart_emoji_on_rank(self.couple.love_rank)}´- <@{self.couple.second_user_id}> đã về chung một nhà!", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Ngày bắt đầu quen nhau: <t:{unix_time}:D>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Điểm thân mật **{self.couple.love_point}**", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            if len(self.guest_list)>0:
                embed.add_field(name=f"", value=f"Danh sách khách tham dự: ", inline=False)
                count = 0
                for guest in self.guest_list:
                    text = f"{guest.user.mention}"
                    if guest.money >0 and guest.money_type != None:
                        text=f"- {guest.user.mention} đi phong bì: **{UtilitiesFunctions.shortened_currency(guest.money)}** {guest.money_type}"
                    embed.add_field(name=f"", value=text, inline=False)
                    count+=1
                    if count > 10:
                        embed.add_field(name=f"", value=f"Và thêm **{len(self.guest_list) - count}** khách mời khác nữa", inline=False)
                        break
            text_money_receive = ""
            if self.darkium >0:
                text_money_receive += f"**{self.darkium}** {EmojiCreation2.DARKIUM.value}\n"
                #Chia hai, và chia cho cặp đôi mỗi người một nửa
                in_half = int(self.darkium/2)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.first_user_id, user_name="", user_display_name="", darkium=in_half)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.second_user_id, user_name="", user_display_name="", darkium=in_half)
            if self.gold >0:
                text_money_receive += f"**{self.gold}** {EmojiCreation2.GOLD.value}\n"
                in_half = int(self.gold/2)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.first_user_id, user_name="", user_display_name="", gold=in_half)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.second_user_id, user_name="", user_display_name="", gold=in_half)
            if self.silver >0:
                text_money_receive += f"**{self.silver}** {EmojiCreation2.SILVER.value}\n"
                in_half = int(self.silver/2)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.first_user_id, user_name="", user_display_name="", silver=in_half)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.second_user_id, user_name="", user_display_name="", silver=in_half)
            if self.copper >0:
                text_money_receive += f"**{self.copper}** {EmojiCreation2.COPPER.value}\n"
                in_half = int(self.copper/2)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.first_user_id, user_name="", user_display_name="", copper=in_half)
                ProfileMongoManager.update_profile_money(guild_id=self.guild.id, guild_name="", user_id=self.couple.second_user_id, user_name="", user_display_name="", copper=in_half)
            embed.add_field(name=f"Tổng tiền nhận được", value=f">>> {text_money_receive}", inline=False)
            embed.set_image(url=self.gif)
            
            channel = self.old_message.channel
            if channel:
                #Chỉnh rank lên 20, love progressing max
                CoupleMongoManager.set_love_progressing_value(guild_id=self.guild.id, user_id=self.couple.first_user_id, love_progressing= 1000)
                CoupleMongoManager.set_love_rank_value(guild_id=self.guild.id, user_id=self.couple.first_user_id, love_rank= 20)
                await channel.send(embed=embed, view=None)
                await self.old_message.delete()
            return
        except Exception as e:
            print(e)
            return
        
    @discord.ui.button(label="Mừng Tiền Cặp Tân Hôn", style=discord.ButtonStyle.blurple)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.couple.first_user_id or interaction.user.id == self.couple.second_user_id: return
        await interaction.response.defer(ephemeral=True)
        
        existed = False
        for guest in self.guest_list:
            if interaction.user.id == guest.user.id:
                existed = True
                break
        if existed == True:
            await interaction.followup.send(content="Bạn đã tham dự rồi! Không được bấm tiếp!", ephemeral=True)
            return
        
        user_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if user_profile == None:
            #Chỉ thêm vào guest list, không cần cộng tiền
            data = GuessInfo(user=interaction.user)
            self.guest_list.append(data)
            await interaction.followup.send(content="Cảm ơn bạn đã tham gia!", ephemeral=True)
        else:
            #Trừ 10% tiền lớn nhất
            money = 0
            money_type = None
            if user_profile.darkium > 2:
                money = int(user_profile.darkium*5/100)
                if money > 1000: money = 1000
                money_type = EmojiCreation2.DARKIUM.value
                self.darkium += money
                user_profile.darkium = user_profile.darkium - money
                ProfileMongoManager.update_profile_money_fast(guild_id=interaction.guild_id, data=user_profile) 
            elif user_profile.gold > 0:
                money = int(user_profile.gold*5/100)
                if money > 1000000: money = 1000000
                money_type = EmojiCreation2.GOLD.value
                self.gold += money
                user_profile.gold = user_profile.gold - money
                ProfileMongoManager.update_profile_money_fast(guild_id=interaction.guild_id, data=user_profile) 
            elif user_profile.silver > 0:
                money = int(user_profile.silver*5/100)
                if money > 1000000: money = 1000000
                money_type = EmojiCreation2.SILVER.value
                self.silver += money
                user_profile.silver = user_profile.silver - money
                ProfileMongoManager.update_profile_money_fast(guild_id=interaction.guild_id, data=user_profile) 
            elif user_profile.copper > 0:
                money = int(user_profile.copper*5/100)
                if money > 10000000: money = 10000000
                money_type = EmojiCreation2.COPPER.value
                self.copper += money
                user_profile.copper = user_profile.copper - money
                ProfileMongoManager.update_profile_money_fast(guild_id=interaction.guild_id, data=user_profile) 

            text = "Bạn đã tham dự lễ cưới này"
            if money > 0 and money_type != None:
                text += f" và tặng phong bì **{money}** {money_type} cho cặp đôi!"
            data = GuessInfo(user=interaction.user, money_type=money_type, money=money)
            self.guest_list.append(data)
            await interaction.followup.send(content=text, ephemeral=True)