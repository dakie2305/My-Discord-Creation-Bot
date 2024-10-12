import discord
from discord.ext import commands
from discord import app_commands
from typing import List, Optional
import random
import mini_game.RockPaperScissor.RpsMongoManager as RpsMongoManager
import os
import CustomFunctions

class RPSView(discord.ui.View):
    def __init__(self, player_1: discord.Member, player_2: discord.Member, embed: discord.Embed):
        super().__init__(timeout=30)
        self.player_1 = player_1
        self.player_2 = player_2
        self.embed = embed
        self.message_id = None
        self.channel_id = None
        self.message: discord.Message = None
        self.choices = {}
    
    @discord.ui.button(label="🔨 Búa", style=discord.ButtonStyle.green)
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "rock")

    @discord.ui.button(label="🗞️ Bao", style=discord.ButtonStyle.blurple)
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_choice(interaction, "paper")

    @discord.ui.button(label="✂️ Kéo", style=discord.ButtonStyle.red)
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button,):
        await self.handle_choice(interaction, "scissors")

    async def handle_choice(self, interaction: discord.Interaction, choice: str):
        #Không quan tâm người khác ấn
        if interaction.user.id not in (self.player_1.id, self.player_2.id):
            return
        
        if interaction.user.id not in self.choices:
            self.choices[interaction.user.id] = choice
            await interaction.response.defer()

        # Nếu player 2 là bot thì liền tạo choice cho bot
        # Bot sẽ có tỷ lệ thắng 80%, 15% tỷ lệ hoà, và 5% thua 
        if self.player_2.id == 1257713292445618239 or self.player_2.id == 1257305865124581416:
            bot_choice = self.get_bot_choice(choice)
            self.choices[self.player_2.id] = bot_choice
        
        if len(self.choices) == 2:
            await self.determine_winner(interaction)
            self.stop()

    async def determine_winner(self, interaction: discord.Interaction):
        player1_choice = self.choices[self.player_1.id]
        player2_choice = self.choices[self.player_2.id]
        win_player :discord.Member = None
        lose_player :discord.Member = None
        #Hoà
        if player1_choice == player2_choice:
            result = f"Cả hai player đều chọn **`{self.translate_choice(player1_choice)}`** nên trận này coi như hoà!"
            RpsMongoManager.player_profile_on_draw(guild_id=interaction.guild.id, player_1_id= self.player_1.id, player_1_display_name=self.player_1.display_name, player_1_user_name= self.player_1.name, player_2_id=self.player_2.id, player_2_display_name=self.player_2.display_name, player_2_user_name= self.player_2.name)
        #Player 1 thắng
        elif (player1_choice == "rock" and player2_choice == "scissors") or \
             (player1_choice == "paper" and player2_choice == "rock") or \
             (player1_choice == "scissors" and player2_choice == "paper"):
            result = f"{self.player_1.mention} chọn **`{self.translate_choice(player1_choice)}`**, còn {self.player_2.mention} đã chọn **`{self.translate_choice(player2_choice)}`**. {self.player_1.mention} đã thắng trận này!\nĐừng quên dùng lệnh **`/bxh_rps`** để xem bảng xếp hạng nhé!"
            win_player = self.player_1
            lose_player = self.player_2
        #PLayer 2 thắng
        else:
            result = f"{self.player_1.mention} chọn **`{self.translate_choice(player1_choice)}`**, còn {self.player_2.mention} đã chọn **`{self.translate_choice(player2_choice)}`**. {self.player_2.mention} đã thắng trận này!\nĐừng quên dùng lệnh **`/bxh_rps`** để xem bảng xếp hạng nhé!"
            win_player = self.player_2
            lose_player = self.player_1
        
        if win_player != None and lose_player != None:
            #Kiểm tra humi point và len point trước
            flagLegend = False
            flagHumi = False
            player_profile_win_player = RpsMongoManager.find_player_profile_by_id(guild_id=interaction.guild.id, user_id=win_player.id)
            player_profile_lose_player = RpsMongoManager.find_player_profile_by_id(guild_id=interaction.guild.id, user_id=lose_player.id)
            if player_profile_win_player!= None and player_profile_win_player.game_consecutive_round_win == 4: #Chuẩn bị được điêm legend
                flagLegend = True
            if player_profile_lose_player!= None and player_profile_lose_player.game_consecutive_round_lose == 4: #Chuẩn bị được điểm humi
                flagHumi = True
            #win point +1, cons_win + 1
            RpsMongoManager.create_update_player_profile(guild_id=interaction.guild.id, user_id= win_player.id, user_name=win_player.name,user_display_name=win_player.display_name, win_point=1, game_consecutive_round_win=1)
            #lose point +1, cons_lose +1
            RpsMongoManager.create_update_player_profile(guild_id=interaction.guild.id, user_id= lose_player.id, user_name=lose_player.name,user_display_name=lose_player.display_name, lose_point=1, game_consecutive_round_lose=1)
            
            if flagLegend:
                file = CustomFunctions.get_congrat_humilate_gif(is_congrat=True)
                await interaction.message.reply(content=f"{win_player.mention} đã thắng 5 ván liên tiếp và được cộng **`1`** điểm Huyền Thoại!", file= file)
            if flagHumi:
                file = CustomFunctions.get_congrat_humilate_gif(is_congrat=False)
                await interaction.message.reply(content=f"Quá nhục nhã! {lose_player.mention} đã thua tận tới 5 ván liên tiếp và được cộng **`1`** điểm Sỉ Nhục!", file= file)
        
        embed = discord.Embed(title=f"", description= f"{result}", color=0xC3A757)  # Yellowish color
        await self.message.edit(embed=embed, view=None, content="")
    
    async def on_timeout(self):
        #Sẽ xoá khi player 2 không chọn gì hết
        #Và bảo rằng đáng tiếc là player đã không chọn sau 30 quy định
        if(len(self.choices)) != 2:
            if self.message:
                try:
                    await self.message.edit(content=f"{self.player_1.mention} rất đáng tiếc là {self.player_2.display_name} không muốn chơi cùng bạn.", embed=None, view=None)
                    return
                except discord.NotFound:
                    pass
                except discord.Forbidden:
                    pass
            return
        
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        await self.message.edit(view=self)
    
    def get_bot_choice(self, choice: str) -> str:
        chance = random.randint(0,100)
        bot_choice = 'paper'
        #If else đến chết
        #bot thua
        if chance >= 0 and chance <= 20:
            if choice == 'rock': bot_choice = 'scissors'
            elif choice == 'paper': bot_choice = 'rock'
            else: bot_choice = 'paper'
        #bot hoà
        elif chance >20 and chance <= 40:
            bot_choice = choice
        else:
            if choice == 'rock': bot_choice = 'paper'
            elif choice == 'paper': bot_choice = 'scissors'
            else: bot_choice = 'rock'
        return bot_choice
    
    def translate_choice(self, choice: str) -> str:
        if choice == 'paper': return '🗞️ Bao'
        elif choice == 'rock': return '🔨 Búa'
        else: return '✂️ Kéo'
        
