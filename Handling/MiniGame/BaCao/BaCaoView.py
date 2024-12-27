import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List, Optional, Dict
import random
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import asyncio
from datetime import datetime, timedelta


class PlayerCardInfo:
    def __init__(self, user: discord.Member, first_card: str, second_card: str, third_card: str):
        self.user = user
        self.first_card = first_card
        self.second_card = second_card
        self.third_card = third_card

class BaCaoView(discord.ui.View):
    def __init__(self, user: discord.Member, bot: discord.Member, user_profile: Profile = None, so_tien:int = None, loai_tien: int = None, timeout: int = 30):
        super().__init__(timeout=timeout)
        self.message: discord.Message = None
        self.user = user
        self.bot = bot
        self.user_profile = user_profile
        self.so_tien = so_tien
        self.loai_tien = loai_tien
        self.list_used_cards = [] 
        self.player_list: List[PlayerCardInfo] = []
        self.host_card: PlayerCardInfo = None
        
        self.remaining_time = timeout
        self.is_running = False
    
    async def start_countdown(self):
        while self.remaining_time > 0 and self.is_running:
            await asyncio.sleep(1)
            self.remaining_time -= 1
        if self.remaining_time <= 0 and self.is_running:
            self.is_running = False
            await self.trigger_result()
        return
    
    async def on_timeout(self):
        if self.message != None: 
            await self.trigger_result()
            return
    
    @discord.ui.button(label="🃏 Rút Bài", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        if len(self.player_list) >= 8:
            await interaction.followup.send(content="Sòng này đã đủ số lượng người chơi! Bạn hãy tự tạo hoặc tham gia sòng bài khác!", ephemeral=True)
            return
        
        existed_player = False
        for player in self.player_list:
            if interaction.user.id == player.user.id:
                existed_player = True
                break
        if existed_player == True:
            await interaction.followup.send(content="Bạn đã rút bài rồi! Không được rút tiếp!", ephemeral=True)
            return
        else:
            if interaction.user.id == self.user.id:
                if self.host_card != None:
                    await interaction.followup.send(content="Bạn đã rút bài rồi! Không được rút tiếp!", ephemeral=True)
                    return
                #Đây là host
                first_card = self.get_random_card()
                second_card = self.get_random_card()
                third_card = self.get_random_card()
                host = PlayerCardInfo(user=self.user,first_card=first_card, second_card=second_card, third_card=third_card)
                self.host_card = host
                await interaction.followup.send(content=f"Bạn đã rút ra ba lá bài: {UtilitiesFunctions.get_emoji_from_card_type(card_type=first_card)} | {UtilitiesFunctions.get_emoji_from_card_type(card_type=second_card)} |{UtilitiesFunctions.get_emoji_from_card_type(card_type=third_card)}", ephemeral=True)
            else:
                #Nếu là chơi tiền thì ép người này phải dùng tiền của profile
                if self.so_tien != None and self.loai_tien != None:
                    player_profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
                    if player_profile == None:
                        await interaction.followup.send(content=f"Vui lòng dùng lệnh {SlashCommand.PROFILE.value} trước đã!", ephemeral=True)
                        return
                    if self.loai_tien == "C" and player_profile.copper < self.so_tien:
                        await interaction.followup.send(content=f"Bạn không có đủ {EmojiCreation2.COPPER.value} để tham gia sòng này!", ephemeral=True)
                        return
                    if self.loai_tien == "S" and player_profile.silver < self.so_tien:
                        await interaction.followup.send(content=f"Bạn không có đủ {EmojiCreation2.SILVER.value} để tham gia sòng này!", ephemeral=True)
                        return
                    if self.loai_tien == "G" and player_profile.gold < self.so_tien:
                        await interaction.followup.send(content=f"Bạn không có đủ {EmojiCreation2.GOLD.value} để tham gia sòng này!", ephemeral=True)
                        return
                
                #Rút random ba lá bài cho player
                first_card = self.get_random_card()
                second_card = self.get_random_card()
                third_card = self.get_random_card()
                player = PlayerCardInfo(user=interaction.user,first_card=first_card, second_card=second_card, third_card=third_card)
                self.player_list.append(player)
                await interaction.followup.send(content=f"Bạn đã rút ra ba lá bài: {UtilitiesFunctions.get_emoji_from_card_type(card_type=first_card)} | {UtilitiesFunctions.get_emoji_from_card_type(card_type=second_card)} |{UtilitiesFunctions.get_emoji_from_card_type(card_type=third_card)}", ephemeral=True)
                
        return
    
    async def trigger_result(self):
        if self.message == None: return
        #Nếu ít hơn hai người thì coi như không ai chịu chơi
        try:
            if len(self.player_list) < 1:
                #Rút random ba lá bài cho bot chơi
                first_card = self.get_random_card()
                second_card = self.get_random_card()
                third_card = self.get_random_card()
                player = PlayerCardInfo(user=self.bot,first_card=first_card, second_card=second_card, third_card=third_card)
                self.player_list.append(player)
            
            if self.host_card == None:
                await self.message.edit(embed=None,view= None, content= f"Nhà cái {self.user.mention} đã sủi ván bài. Số tiền đặt cược của nhà cái coi như sẽ mất hết.")
                if self.loai_tien == "C": self.update_host_and_player_money(player=None, is_player_win=True, copper=self.so_tien)
                if self.loai_tien == "S": self.update_host_and_player_money(player=None, is_player_win=True, silver=self.so_tien)
                if self.loai_tien == "G": self.update_host_and_player_money(player=None, is_player_win=True, gold=self.so_tien)
                return
            
            l_chance = UtilitiesFunctions.get_chance(5)
            if l_chance:
                await self.police_in()
                return
            
            gambling_money_text = ""
            if self.so_tien != None and self.loai_tien != None:
                emoji = UtilitiesFunctions.get_emoji_from_loai_tien(loai_tien=self.loai_tien)
                gambling_money_text = f" với tiền cược là **{self.so_tien}**{emoji}"
            
            embed = discord.Embed(title=f"", description=f"**Sòng Bài Cào**", color=0x03F8FC)
            embed.add_field(name=f"", value="▬▬▬▬ι═══════>", inline=False)
            embed.add_field(name=f"", value=f"{self.user.mention} đã mở sòng Bài Cào{gambling_money_text}!", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι═══════>", inline=False)
            
            host_number = self.calculate_player_value(data=self.host_card)
            embed.add_field(name=f"", value=f"**Nhà cái** {self.user.mention}:\n{UtilitiesFunctions.get_emoji_from_card_type(card_type=self.host_card.first_card)} | {UtilitiesFunctions.get_emoji_from_card_type(card_type=self.host_card.second_card)} |{UtilitiesFunctions.get_emoji_from_card_type(card_type=self.host_card.third_card)}\nTổng số nút: **{host_number}**", inline=False)
            money_to_pay_by_host = 0
            for player in self.player_list:
                is_player_win = None
                player_number = self.calculate_player_value(data=player)
                if player_number != 0:
                    player_result_text = f"\nTổng số nút: **{player_number}**"
                else:
                    player_result_text = f"\nTổng số nút: **Bù**"
                if player_number > host_number:
                    is_player_win = True
                    player_result_text += " ▬ι═> Thắng!"
                    if self.so_tien != None: money_to_pay_by_host -= self.so_tien
                elif player_number < host_number:
                    is_player_win = False
                    player_result_text += " ▬ι═> Thua!"
                    if self.so_tien != None: money_to_pay_by_host += self.so_tien
                elif player_number == host_number:
                    is_player_win = None
                    player_result_text += " ▬ι═> Huề!"
                embed.add_field(name=f"", value=f"{player.user.mention}:\n{UtilitiesFunctions.get_emoji_from_card_type(card_type=player.first_card)} | {UtilitiesFunctions.get_emoji_from_card_type(card_type=player.second_card)} |{UtilitiesFunctions.get_emoji_from_card_type(card_type=player.third_card)}{player_result_text}", inline=False)
                if self.so_tien != None and self.loai_tien != None:
                    if self.loai_tien == "C": self.update_host_and_player_money(player=player, is_player_win=is_player_win, copper=self.so_tien)
                    if self.loai_tien == "S": self.update_host_and_player_money(player=player, is_player_win=is_player_win, silver=self.so_tien)
                    if self.loai_tien == "G": self.update_host_and_player_money(player=player, is_player_win=is_player_win, gold=self.so_tien)
            
            #Trừ 10% số tiền từ game
            text_tax = ""
            if self.so_tien != None:
                tax_money = int(self.so_tien*5/100)
                if tax_money <= 0: 
                    tax_money = 1
                if self.so_tien != None and self.loai_tien != None:
                    if self.loai_tien == "C": 
                        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, copper=-tax_money)
                    if self.loai_tien == "S": 
                        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, silver=-tax_money)
                    if self.loai_tien == "G":
                        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, gold=-tax_money)
                text_tax = f"\nNgoài ra, chủ sòng đã tốn thêm **{tax_money}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)} để đóng phí bảo kê sòng bạc!"
            add_text = ""
            if money_to_pay_by_host!= None and money_to_pay_by_host > 0:
                add_text = f"**Nhà cái** {self.user.mention} đã lời được **{money_to_pay_by_host}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)} từ sòng bạc này!{text_tax}"
            elif money_to_pay_by_host!= None and money_to_pay_by_host < 0:
                add_text = f"**Nhà cái** {self.user.mention} đã lỗ mất **{money_to_pay_by_host*(-1)}** {UtilitiesFunctions.get_emoji_from_loai_tien(self.loai_tien)} từ sòng bạc này!"
            
            embed.add_field(name=f"", value=add_text, inline=False)
            await self.message.edit(embed=embed, view=None)
            return
        except Exception:
            return

    def update_host_and_player_money(self, player: PlayerCardInfo = None, is_player_win = None, gold: int = 0, silver:int = 0, copper: int = 0):
        if is_player_win == None: return
        if player.user.id == 1257713292445618239:
            #Này là bot creation 2
            if self.so_tien == None: return
            if is_player_win == True:
                #Trừ tiền player, cộng 50% cho authority
                ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, gold=-gold, silver=-silver, copper=-copper)
                if self.user_profile.is_authority== False:
                    ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, gold=int(-gold/2), silver=int(-silver/2), copper=int(-copper/2))
            else:
                #Trừ tiền authority, cộng 100% cho player
                ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, gold=gold, silver=silver, copper=copper)
                if self.user_profile.is_authority== False:
                    ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, gold=-gold, silver=-silver, copper=-copper)
            return 
        #Nếu thắng thì trừ tiền của host, và cộng tiền cho player
        if is_player_win == True:
            if player != None:
                ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=player.user.id, user_name=player.user.name, user_display_name=player.user.display_name, gold=gold, silver=silver, copper=copper)
                #Cộng kinh nghiệm
                ProfileMongoManager.update_level_progressing(guild_id=self.user.guild.id, user_id=player.user.id)
            ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, gold=-gold, silver=-silver, copper=-copper)
        else:
            if player != None:
                ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=player.user.id, user_name=player.user.name, user_display_name=player.user.display_name, gold=-gold, silver=-silver, copper=-copper)
                #Trừ nhân phẩm người chơi nếu thua
                ProfileMongoManager.update_dignity_point(guild_id=self.user.guild.id, guild_name="", user_id=player.user.id, user_name=player.user.name, user_display_name=player.user.display_name, dignity_point=-1)
            ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, gold=gold, silver=silver, copper=copper)
            #Cộng kinh nghiệm
            ProfileMongoManager.update_level_progressing(guild_id=self.user.guild.id, user_id=self.user.id)
        return
    
    async def police_in(self):
        #Công an ập vào
            lost_money_text = ""
            if self.so_tien != None and self.loai_tien != None:
                lost_money_text = f"Chính Quyền tịch thu số tiền **{self.so_tien}** {UtilitiesFunctions.get_emoji_from_loai_tien(loai_tien=self.loai_tien)} của tất cả đối tượng tham gia! Những đối tượng bị tịch thu tiền: "
            else:
                lost_money_text = f"Những đối tượng bị tống giam: "
            lose_embed = discord.Embed(title=f"", description=f"Công an đã ập vào để bắt quả tang {self.user.mention} vì tổ chức chơi đánh bạc sát phạt! Tất cả đối tượng đều bị giam 30 phút!", color=0x03F8FC)
            lose_embed.add_field(name=f"", value=lost_money_text, inline=False)
            time_window = timedelta(minutes=30)
            jail_time = datetime.now() + time_window
            for player in self.player_list:
                lose_embed.add_field(name=f"", value=f"- {player.user.mention}", inline=False)
                ProfileMongoManager.update_jail_time(guild_id=self.user.guild.id, user_id=player.user.id, jail_time=jail_time)
                if self.loai_tien != None and self.so_tien != None:
                    if self.loai_tien == "G":
                        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=player.user.id, user_name=player.user.name, user_display_name=player.user.display_name, gold=-self.so_tien)
                        if self.user_profile.is_authority != True:
                            ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, gold=self.so_tien)
                    elif self.loai_tien == "S":
                        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=player.user.id, user_name=player.user.name, user_display_name=player.user.display_name, silver=-self.so_tien)
                        if self.user_profile.is_authority != True:
                            ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, silver=self.so_tien)
                    elif self.loai_tien == "C":
                        ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=player.user.id, user_name=player.user.name, user_display_name=player.user.display_name, copper=-self.so_tien)
                        if self.user_profile.is_authority != True:
                            ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, copper=self.so_tien)
            
            #Trừ tiền host
            if self.loai_tien == "G":
                ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, gold=-self.so_tien)
                if self.user_profile.is_authority != True:
                            ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, gold=self.so_tien)
            if self.loai_tien == "S":
                ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, silver=-self.so_tien)
                if self.user_profile.is_authority != True:
                            ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, silver=self.so_tien)
            if self.loai_tien == "C":
                ProfileMongoManager.update_profile_money(guild_id=self.user.guild.id, guild_name="", user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, copper=-self.so_tien)
                if self.user_profile.is_authority != True:
                            ProfileMongoManager.update_money_authority(guild_id=self.user.guild.id, copper=self.so_tien)
            #jail host chung luôn
            ProfileMongoManager.update_jail_time(guild_id=self.user.guild.id, user_id=self.user.id, jail_time=jail_time)
            await self.message.edit(embed=lose_embed, view= None)
            return

    
    def calculate_card_value(self, card: str) -> int:
        value = card[:-1]  # Lấy phần số trong bài (VD: "2" trong "2C")
        #Giá trị như sau thì bằng 0
        if value in {"J", "Q", "K", "10"}:
            return 0
        elif value == "A":
            return 1
        else:
            return int(value)

    def calculate_player_value(self, data: PlayerCardInfo) -> int:
        card_values = [
            self.calculate_card_value(data.first_card),
            self.calculate_card_value(data.second_card),
            self.calculate_card_value(data.third_card),
        ]
        return sum(card_values) % 10
    
    
    def get_random_card(self):
        all_cards = [
            "2C", "2D", "2H", "2S", 
            "3C", "3D", "3H", "3S", 
            "4C", "4D", "4H", "4S", 
            "5C", "5D", "5H", "5S", 
            "6C", "6D", "6H", "6S", 
            "7C", "7D", "7H", "7S", 
            "8C", "8D", "8H", "8S", 
            "9C", "9D", "9H", "9S", 
            "10C", "10D", "10H", "10S", 
            "AC", "AD", "AH", "AS", 
            "JC", "JD", "JH", "JS", 
            "KC", "KD", "KH", "KS", 
            "QC", "QD", "QH", "QS"
        ]
        #Lấy ra list card chưa rút
        remaining_cards = list(set(all_cards) - set(self.list_used_cards))
        random_card = random.choice(remaining_cards)
        #Thêm vào list card đã rút
        self.list_used_cards.append(random_card)
        return random_card
        