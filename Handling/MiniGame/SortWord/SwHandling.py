import discord
import random
from CustomEnum.EmojiEnum import EmojiCreation1
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import Handling.MiniGame.SortWord.SwMongoManager as SwMongoManager
import Handling.MiniGame.SortWord.SwClass
from Handling.MiniGame.SortWord.SwClass import SortWordInfo
import CustomFunctions
import string
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView

class SwHandlingFunction():
    def __init__ (self, message: discord.Message):
        self.message = message
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
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Đoán Từ", color=0x03F8FC)
        embed.add_field(name=f"", value=f"Lượt chơi thứ: {sw_info.current_round}/1200", inline=False)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 0
        if sw_info.player_profiles:
            sw_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for index, profile in enumerate(sw_info.player_profiles):
                if (profile.point!= 0 or len(profile.special_items)> 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** <@{profile.user_id}>. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 20: break
        text = "Chúc mừng các player top đầu!"
        if message.guild.id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            text+= " <@315835396305059840> sẽ trao role đặc biệt cho những Player thuộc top 3 nhé!"
        await message.channel.send(content=text, embed=embed)
        #Xoá đi tạo lại
        SwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang=language)
        #Tạo mới
        lan_label = "Tiếng Anh" if language == "en" else "Tiếng Việt"
        current_word = "hello" if language == "en" else "trai"
        unsorted = "olehl" if language == "en" else "rtia"
        data = SortWordInfo(channel_id=self.message.channel, channel_name=message.channel.name, guild_name=message.guild.name, current_word=current_word, unsorted_word=unsorted, special_case=False)
        SwMongoManager.create_info(data=data, guild_id=message.guild.id, lang=language)
        embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Đoán Từ {lan_label}", description=f"",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hướng dẫn chơi Tiếng Anh:\n `ih` -> `hi`, `ytr` -> `try`", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hướng dẫn chơi Tiếng Việt:\n `han rtai` -> `anh trai`, `me rait` -> `em trai`", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Đoán từ hiện tại:", inline=False)
        embed.add_field(name=f"{data.unsorted_word}", value=f"", inline=False)
        await message.channel.send(embed=embed)

            
    async def fail_attempt(self, message: discord.Message, sw_info: SortWordInfo, lan: str, point: int, err: str = None):
    #Reset special point nếu trả lời sai, và nếu trước đó đã có
        if sw_info.special_point:
            SwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
        if sw_info.special_item:
            SwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
        
        list_player_penalty = sw_info.player_penalty
        selected_player = None
        for player in list_player_penalty:
            if player.user_id == message.author.id and player.penalty_point > 5:
                selected_player = player
                break
        if selected_player is not None:
            #Trừ điểm vì sai quá nhiều
            point = 2
            await message.reply(f"{message.author.mention} đã bị trừ **{point}** vì trả lời sai quá nhiều lần!")
            SwMongoManager.update_player_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point=-point)
            return
        SwMongoManager.create_and_update_player_penalty(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, user_id=message.author.id, user_name=message.author.name)
        if CustomFunctions.check_if_dev_mode():
            await message.add_reaction('❌')
        else:
            await message.add_reaction('<a:x_cross_red:1378265390110474362>')
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
        message_tu_hien_tai = f"\nTừ hiện tại: `'{sw_info.unsorted_word}'`. Chữ này có **{len(sw_info.current_word)}** chữ cái."
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
            if CustomFunctions.check_if_dev_mode():
                await message.add_reaction('👍')
            else:
                await message.add_reaction('<a:check:1378265379419193354>')
            #Cập nhật lại thông tin
            current_word = self.get_random_current_word(lang=lan)
            current_player_id=message.author.id
            if CustomFunctions.check_if_dev_mode(): current_player_id = 1
            SwMongoManager.update_data_info(lang=lan,channel_id=message.channel.id, guild_id= message.guild.id, current_player_id=current_player_id, current_player_name=message.author.name,current_word=current_word)
            #Cập nhật lại điểm
            SwMongoManager.update_player_point_data_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan)
            ProfileMongoManager.update_level_progressing(guild_id=message.guild.id, user_id=message.author.id)
            end_round = 500
            if sw_info.current_round>=end_round:
                #Reset
                await message.channel.send(f"Đã chơi được **{end_round}** lượt rồi. Cảm ơn mọi người đã chơi nhé. Đến lúc reset lại rồi, nên mọi người bắt đầu lại nhé!")
                await self.process_reset(message=message, sw_info=sw_info, language=lan)
                return
            else:
                #Thông báo
                sw_info, lan = await self.check_if_message_inside_game(source=message)
                message_tu_hien_tai = f"\nTừ hiện tại: `'{sw_info.unsorted_word}'`. Chữ này có **{len(sw_info.current_word)}** chữ cái"
                #Kiểm tra xem có special_item không, nếu có thì cộng cho player
                chuc_mung_item = ""
                if sw_info.special_item:
                    SwMongoManager.update_player_special_item(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= sw_info.special_item)
                    chuc_mung_item = f" và nhận được kỹ năng **{sw_info.special_item.item_name}**. Nhớ đừng quên sử dụng nó nhé"
                #Trả lời đúng thì reset special_points và special_item lại từ đầu, cập nhật lại list player ban
                await message.channel.send(f"{message.author.mention}, bạn đã được cộng {point} điểm{chuc_mung_item}. Để kiểm tra điểm số của mình thì hãy dùng lệnh {SlashCommand.BXH.value} nhé. {message_tu_hien_tai}")
                #Reset special point, special item, giảm ban remain của tất cả player
                SwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
                SwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
                SwMongoManager.remove_player_penalty_after_round(channel_id= message.channel.id, guild_id= message.guild.id, language=lan)
                
        #Xổ số nếu chưa có special point
        so_xo = random.randint(4, 10)
        #Nếu sổ xố rơi trúng số 5 thì coi như cộng point lên x2, x3, x4 ngẫu nhiên
        if so_xo == 10:
            x_value = random.randint(2, 5)
            special_point_english = 1*x_value
            SwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= special_point_english)
            embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Điểm Thưởng Duy Nhất {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Cơ hội chỉ đến một lần duy nhất, nếu ai đoán đúng sẽ nhận được **{special_point_english}** điểm!", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} **Lưu ý**: Đoán sai sẽ mất điểm ngay, nên hãy suy nghĩ cho kỹ trước khi trả lời!", inline=False)
            view = SelfDestructView(timeout=45)
            m = await message.channel.send(embed=embed, view=view)
            view.message
        else:
            #Sổ xố xem trúng kỹ năng đặc biệt không
            so_xo = random.randint(3, 10)
            if so_xo == 10:
                text_cong_skill = f"\n**Cơ hội chỉ đến một lần duy nhất, nếu ai thắng nhận được kỹ năng đặc biệt bên dưới! Cơ hội duy nhất thôi!**\n"
                percent = random.randint(0, 100)
                item = None
                if percent >= 0 and percent < 55:
                    #Cấp thấp
                    item = random.choice(Handling.MiniGame.SortWord.SwClass.list_special_items_cap_thap)
                elif percent >= 55 and percent < 80:
                    #Cấp cao
                    item = random.choice(Handling.MiniGame.SortWord.SwClass.list_special_items_cap_cao)
                elif percent >= 80 and percent < 95:
                    #Đẳng cấp
                    item = random.choice(Handling.MiniGame.SortWord.SwClass.list_special_items_dang_cap)
                else:
                    #tối thượng
                    item = random.choice(Handling.MiniGame.SortWord.SwClass.list_special_items_toi_thuong)
                result = SwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item=item)
                embed = discord.Embed(title=f"Kỹ năng đặc biệt. Rank: {item.level}", description=f"", color=0x03F8FC)
                embed.add_field(name=f"", value=f"Tên kỹ năng: {item.item_name}", inline=False)
                embed.add_field(name=f"", value=f"Mô tả kỹ năng: {item.item_description}", inline=False)
                embed.add_field(name=f"", value=f"Cách dùng:\n{SlashCommand.SKILL_USE.value}", inline=False)
                view = SelfDestructView(timeout=45)
                m = await message.channel.send(content=text_cong_skill, embed=embed, view=view)
                view.message = m
                return
                