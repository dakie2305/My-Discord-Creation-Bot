import discord
from typing import List, Optional
import random
import mini_game.SortWord.SwMongoManager as SwMongoManager
from mini_game.SortWord.SwClass import SortWordInfo
import os
import CustomFunctions
import string

class handling_function():
    def __init__ (self, message: discord.Message, message_tracker):
        self.message = message
        self.message_tracker = message_tracker
        self.english_words_dictionary = CustomFunctions.english_dict
        self.vietnamese_dict = CustomFunctions.vietnamese_dict
        
    async def check_if_message_inside_game(self, source: discord.Message):
        if source == None: return None, None
        langs = ['en', 'vn']
        for lan in langs:
            check = SwMongoManager.find_sort_word_info_by_id(lang=lan, guild_id=source.guild.id, channel_id= source.channel.id)
            if check!=None:
                return check, lan
        return None, None
    
    def get_random_current_word(self, lang: str):
        if lang == 'en' or lang == 'eng':
            dictionary = self.english_words_dictionary
        else:
            dictionary = self.vietnamese_dict
        random_word = random.choice(list(dictionary.keys()))
        return random_word
        
    async def fail_attempt(self, message: discord.Message, sw_info: SortWordInfo, lan: str, point: int, err: str = None):
    #Reset special point nếu trả lời sai, và nếu trước đó đã có
        if sw_info.special_point:
            SwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
        if sw_info.special_item:
            SwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
        if self.message_tracker.add_message(user_id= message.author.id, channel_id= message.channel.id, content= "spam đoán từ"): #Đánh dấu những đối tượng thích spam
            #Ban 5 vòng
            SwMongoManager.create_and_update_player_bans(channel_id= message.channel.id, guild_id= message.guild.id, language= lan, user_id= message.author.id, user_name=message.author.name, ban_remaining=5)
            await message.reply(f"{message.author.mention} đã spam quá nhiều và bị khoá mõm trong vòng **5** lượt chơi tiếp theo!")
            print(f"Player {message.author.name} is banned 5 round from sort word game for spamming")
            return
        await message.add_reaction('❌')
        if err != None:
            message_tu_hien_tai = f"\nTừ hiện tại: `'{sw_info.unsorted_word}'`."
            await message.reply(f"{err} {message_tu_hien_tai}")

    
    async def handling_game(self, message: discord.Message):
        if message == None or message.content == None or message.content == "": return
        sw_info, lan = await self.check_if_message_inside_game(source=message)
        if sw_info == None: return
        if message.content[0] in string.punctuation or message.content[0] == ":": return
        #Kiểm tra xem có nằm trong danh sách ban không
        selected_ban = None
        for player_ban in sw_info.player_bans:
                if player_ban.user_id == message.author.id and player_ban.ban_remaining>0:
                    selected_ban = player_ban
                    break
        message_tu_hien_tai = f"\nTừ hiện tại: `'{sw_info.unsorted_word}'`."
        if selected_ban:
            await message.reply(f"Bạn đã bị khoá mõm trong vòng **{selected_ban.ban_remaining}** lượt chơi tới. Vui lòng chờ đi.")
            return
        elif sw_info.current_player_id == message.author.id:
            await message.reply(f"Bạn đã chơi rồi, vui lòng né qua để cho người khác chơi đi. {message_tu_hien_tai}")
            if self.message_tracker.add_message(user_id= message.author.id, channel_id= message.channel.id, content= "spam đoán từ"): #Đánh dấu những đối tượng thích spam
                #Ban 5 vòng
                SwMongoManager.create_and_update_player_bans(channel_id= message.channel.id, guild_id= message.guild.id, language= lan, user_id= message.author.id, user_name=message.author.name, ban_remaining=5)
                await message.reply(f"{message.author.mention} đã spam quá nhiều và bị khoá mõm trong vòng **5** lượt chơi tiếp theo!")
                print(f"Player {message.author.name} is banned 5 round from sort word game for spamming")
            return
        point = 1
        if sw_info.special_point != None and sw_info.special_point > 0:
            point = sw_info.special_point
        #Kiểm tra xem, nếu trùng từ đầu, hoặc trùng từ cuối thì vẫn đánh là fail, nhưng vẫn hint rằng đúng
        if message.content.lower()[0] == sw_info.current_word[0] and message.content.lower() != sw_info.current_word:
            await self.fail_attempt(err= f"Suýt thì được rồi, nhưng chỉ đúng từ đầu thôi à.", message=message, sw_info= sw_info,lan=lan,point=point)
        elif message.content.lower()[-1] == sw_info.current_word[-1] and message.content.lower() != sw_info.current_word:
            await self.fail_attempt(err= f"Suýt thì được rồi, nhưng chỉ đúng từ cuối thôi à.", message=message, sw_info= sw_info,lan=lan,point=point)
        elif message.content.lower() != sw_info.current_word:
            await self.fail_attempt(message=message, sw_info= sw_info,lan=lan,point=point)
        else:
            #Coi như pass hết
            await message.add_reaction('👍')
            return
        