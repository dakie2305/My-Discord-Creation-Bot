import discord
from typing import List, Optional
import random
import mini_game.SortWord.SwMongoManager as SwMongoManager
import mini_game.SortWord.SwClass
from mini_game.SortWord.SwClass import SortWordInfo
import CustomFunctions
import string

class SwHandlingFunction():
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
        # Xoá dấu khỏi string
        translator = str.maketrans('', '', string.punctuation)
        cleaned_string = random_word.translate(translator)
        return cleaned_string
    
    def count_matching_start(self, correct_word: str, input_str: str):
        # Tìm xem input_str có bao nhiêu chữ gần giống với correct_word
        min_length = min(len(correct_word), len(input_str))
        start_count = 0
        for i in range(min_length):
            if correct_word[i] == input_str[i]:
                start_count += 1
            else:
                break
        if start_count == len(correct_word): start_count = 0
        return start_count
    
    async def process_reset(self, message: discord.Message, sw_info: SortWordInfo, language: str):
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Sắp Xếp Từ", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 0
        if sw_info.player_profiles:
            sw_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for index, profile in enumerate(sw_info.player_profiles):
                user = message.guild.get_member(profile.user_id)
                if user != None and (profile.point!= 0 or len(profile.special_items)> 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 25: break
        await message.channel.send(content=f"Chúc mừng các player top đầu! <@315835396305059840> sẽ trao role đặc biệt cho những Player thuộc top 3 nhé!", embed=embed)
        #Xoá đi tạo lại
        SwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang=language)
        
        #Tạo lại
        data = SortWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="hi", unsorted_word="ih")
        result = SwMongoManager.create_info(data=data, guild_id=message.guild.id, lang='en')
        message_tu_hien_tai = f"\nTừ hiện tại: `'{data.unsorted_word}'`. Chữ này có **{len(data.current_word)}** chữ cái."
        await message.channel.send(f"Đã reset trò chơi trong channel này. {message_tu_hien_tai}")

            
    async def fail_attempt(self, message: discord.Message, sw_info: SortWordInfo, lan: str, point: int, err: str = None):
    #Reset special point nếu trả lời sai, và nếu trước đó đã có
        if sw_info.special_point:
            SwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
        if sw_info.special_item:
            SwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
        if self.message_tracker.add_message(user_id= message.author.id, channel_id= message.channel.id, content= "spam đoán từ"): #Đánh dấu những đối tượng thích spam
            #Trừ 2 điểm
            SwMongoManager.update_player_point_data_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= -2, guild_id=message.guild.id, channel_id=message.channel.id,language=lan)
            await message.reply(f"{message.author.mention} đã spam quá nhiều và bị trừ 2 điểm!")
            print(f"Player {message.author.name} got two point reduction from sort word game for spamming")
            return
        await message.add_reaction('❌')
        if err != None:
            message_tu_hien_tai = f"\nTừ hiện tại: `'{sw_info.unsorted_word}'`. Chữ này có **{len(sw_info.current_word)}** chữ cái"
            await message.reply(f"{err} {message_tu_hien_tai}")

    
    async def handling_game(self, message: discord.Message):
        if message.author.bot: return
        if str.isspace(message.content): return
        sw_info, lan = await self.check_if_message_inside_game(source=message)
        if sw_info == None: return
        if message.content[0] in string.punctuation or message.content[0] == ":": return
        if lan == 'en' and len(message.content.split()) > 1: return
        #Kiểm tra xem có nằm trong danh sách ban không
        selected_ban = None
        for player_ban in sw_info.player_bans:
                if player_ban.user_id == message.author.id and player_ban.ban_remaining>0:
                    selected_ban = player_ban
                    break
        message_tu_hien_tai = f"\nTừ hiện tại: `'{sw_info.unsorted_word}'`. Chữ này có **{len(sw_info.current_word)}** chữ cái."
        if selected_ban:
            await message.reply(f"Bạn đã bị khoá mõm trong vòng **{selected_ban.ban_remaining}** lượt chơi tới. Vui lòng chờ đi.")
            return
        # elif sw_info.current_player_id == message.author.id:
        #     await message.reply(f"Bạn đã chơi rồi, vui lòng né qua để cho người khác chơi đi. {message_tu_hien_tai}")
        #     if self.message_tracker.add_message(user_id= message.author.id, channel_id= message.channel.id, content= "spam đoán từ"): #Đánh dấu những đối tượng thích spam
        #         #Trừ 5 điểm
        #         SwMongoManager.update_player_point_data_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= -5, guild_id=message.guild.id, channel_id=message.channel.id,language=lan)
        #         await message.reply(f"{message.author.mention} không biết đọc nên bị trừ 5 điểm!")
        #         print(f"Player {message.author.name} got five point reduction from sort word game for spamming")
        #     return
        point = 1
        if sw_info.special_point != None and sw_info.special_point > 0:
            point = sw_info.special_point
        count_matching_initial = self.count_matching_start(correct_word=sw_info.current_word, input_str= message.content.lower())
        if count_matching_initial != 0:
            await self.fail_attempt(err= f"Suýt thì được rồi, nhưng chỉ mới đúng được **{count_matching_initial}** từ đầu: {sw_info.current_word[:count_matching_initial]}.", message=message, sw_info= sw_info,lan=lan,point=point)
        elif message.content.lower() != sw_info.current_word:
            await self.fail_attempt(message=message, sw_info= sw_info,lan=lan,point=point, err= "Đoán sai rồi!")
        else:
            #Coi như pass hết
            await message.add_reaction('👍')
            #Cập nhật lại thông tin
            current_word = self.get_random_current_word(lang=lan)
            SwMongoManager.update_data_info(lang=lan,channel_id=message.channel.id, guild_id= message.guild.id, current_player_id=message.author.id, current_player_name=message.author.name,current_word=current_word)
            #Cập nhật lại điểm
            SwMongoManager.update_player_point_data_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan)
            #Mỗi game 1000 round là kết thúc
            sw_info, lan = await self.check_if_message_inside_game(source=message)
            if sw_info.current_round>=1200:
                #Reset
                await message.channel.send(f"Đã chơi được 1000 round rồi. Cảm ơn mọi người đã chơi nhé. Đến lúc reset lại rồi, nên mọi người bắt đầu lại nhé!")
                await self.process_reset(message=message, sw_info=sw_info, language=lan)
                return
            else:
                #Thông báo
                message_tu_hien_tai = f"\nTừ hiện tại: `'{sw_info.unsorted_word}'`. Chữ này có **{len(sw_info.current_word)}** chữ cái"
                #Kiểm tra xem có special_item không, nếu có thì cộng cho player
                chuc_mung_item = ""
                if sw_info.special_item:
                    SwMongoManager.update_player_special_item(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= sw_info.special_item)
                    chuc_mung_item = f" và nhận được kỹ năng **{sw_info.special_item.item_name}**. Nhớ đừng quên sử dụng nó nhé"
                #Trả lời đúng thì reset special_points và special_item lại từ đầu, cập nhật lại list player ban
                await message.channel.send(f"Hay lắm {message.author.mention}, bạn đã được cộng {point} điểm{chuc_mung_item}. Để kiểm tra điểm số của mình thì hãy dùng lệnh /bxh_sw nhé. {message_tu_hien_tai}")
                #Reset special point, special item, giảm ban remain của tất cả player
                SwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
                SwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
                SwMongoManager.reduce_player_bans_after_round(channel_id= message.channel.id, guild_id= message.guild.id, language=lan)
        #Xổ số nếu chưa có special point
        so_xo = random.randint(4, 10)
        #Nếu sổ xố rơi trúng số 5 thì coi như cộng point lên x2, x3, x4 ngẫu nhiên
        if so_xo == 10:
            x_value = random.randint(2, 5)
            special_point_english = 1*x_value
            SwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= special_point_english)
            text_cong_point = f"\nCơ hội chỉ đến một lần duy nhất, nếu ai đoán đúng sẽ nhận được **{special_point_english}** điểm nhaaa! Sai là mất!\n"
            await message.channel.send(f"{text_cong_point}")
        else:
            #Sổ xố xem trúng kỹ năng đặc biệt không
            so_xo = random.randint(3, 10)
            if so_xo == 10:
                text_cong_skill = f"\n**Cơ hội chỉ đến một lần duy nhất, nếu ai thắng nhận được kỹ năng đặc biệt bên dưới! Cơ hội duy nhất thôi!**\n"
                percent = random.randint(0, 100)
                item = None
                if percent >= 0 and percent < 55:
                    #Cấp thấp
                    item = random.choice(mini_game.SortWord.SwClass.list_special_items_cap_thap)
                elif percent >= 55 and percent < 80:
                    #Cấp cao
                    item = random.choice(mini_game.SortWord.SwClass.list_special_items_cap_cao)
                elif percent >= 80 and percent < 95:
                    #Đẳng cấp
                    item = random.choice(mini_game.SortWord.SwClass.list_special_items_dang_cap)
                else:
                    #tối thượng
                    item = random.choice(mini_game.SortWord.SwClass.list_special_items_toi_thuong)
                
                instruction = f"!sws {item.item_id}"
                if item.required_target:
                    instruction = f"!sws {item.item_id} <@315835396305059840>"
                result = SwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item=item)
                embed = discord.Embed(title=f"Kỹ năng đặc biệt. Rank: {item.level}", description=f"", color=0x03F8FC)
                embed.add_field(name=f"", value=f"Tên kỹ năng: {item.item_name}", inline=False)
                embed.add_field(name=f"", value=f"Mô tả kỹ năng: {item.item_description}", inline=False)
                embed.add_field(name=f"", value=f"Cách dùng:\n**{instruction}**", inline=False)
                await message.channel.send(content=text_cong_skill, embed=embed)
                return
                