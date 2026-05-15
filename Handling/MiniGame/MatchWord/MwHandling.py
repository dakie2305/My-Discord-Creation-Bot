import discord
from typing import List, Optional
import random
from CustomEnum.EmojiEnum import EmojiCreation1
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from Handling.MiniGame.MatchWord import ListSkills, MwMongoManager, MwClass
import CustomFunctions
import string
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.MiniGame.MatchWord.MwClass import MatchWordInfo, PlayerBan, SpecialItem, PlayerProfile
from Handling.Misc.SelfDestructView import SelfDestructView

class MwHandlingFunction():
    def __init__ (self, message: discord.Message):
        self.message = message
        self.english_words_dictionary = CustomFunctions.english_dict
        self.vietnamese_dict = CustomFunctions.vietnamese_dict
        
    async def check_if_message_inside_game(self, source: discord.Message):
        if source == None: return None, None
        langs = ['en', 'vn']
        for lan in langs:
            check = MwMongoManager.find_match_word_info_by_id(lang=lan, guild_id=source.guild.id, channel_id= source.channel.id)
            if check!=None:
                return check, lan
        return None, None
    
    async def process_reset(self, message: discord.Message, mw_info: MatchWordInfo, language: str):
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Nối Từ", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        embed.add_field(name=f"", value=f"Lượt hiện tại: {mw_info.current_round}", inline=False)
        count = 0
        if mw_info.player_profiles:
            mw_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for index, profile in enumerate(mw_info.player_profiles):
                if (profile.point!= 0 or len(profile.special_items)> 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** <@{profile.user_id}>. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 20: break
        text = "Chúc mừng các player top đầu!"
        if message.guild.id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            text+= " <@315835396305059840> sẽ trao role đặc biệt cho những Player thuộc top 3 nhé!"
        await message.channel.send(content=text, embed=embed)
        #Xoá đi tạo lại
        MwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang=language)
        lan_label = "Tiếng Anh" if language == "en" else "Tiếng Việt"
        #Nếu là tiếng anh thì cứ tạo bình thường
        if language == "en":
            data = MwClass.MatchWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, guild_name=message.guild.name, current_word="hello", remaining_word= 1000, correct_start_word= "o", type="B", special_case=False)
            MwMongoManager.create_info(data=data, guild_id=message.guild.id, lang=language)
            embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Nối Từ {lan_label}", description=f"",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Từ hiện tại:", inline=False)
            embed.add_field(name=f"{data.current_word}", value=f"", inline=False)
            channel = message.channel
            await channel.send(embed=embed)
        else:
            type_label = "Nối Theo Từ Cuối" if mw_info.type == "A" else "Nối Theo Âm Cuối"
            is_special = True if mw_info.type == "A" else False
            correct_word = "anh" if mw_info.type == "A" else "h"
            data = MwClass.MatchWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, guild_name=message.guild.name, current_word="anh", special_case=is_special, type=mw_info.type, remaining_word=300, correct_start_word=correct_word)
            MwMongoManager.create_info(data=data, guild_id=message.guild.id, lang=language)
            embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Nối Từ {lan_label}", description=f"Thể Loại: **{type_label}**",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Từ hiện tại:", inline=False)
            embed.add_field(name=f"{data.current_word}", value=f"", inline=False)
            channel = message.channel
            await channel.send(embed=embed)
            
    async def fail_attempt(self, message: discord.Message, mw_info: MatchWordInfo, lan: str, point: int, err: str = None):
        #Reset special point nếu trả lời sai, và nếu trước đó đã có
        if mw_info.special_point:
            MwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
        if mw_info.special_item:
            MwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
        
        list_player_penalty = mw_info.player_penalty
        selected_player = None
        for player in list_player_penalty:
            if player.user_id == message.author.id and player.penalty_point > 5:
                selected_player = player
                break
        if selected_player is not None:
            #Trừ điểm vì sai quá nhiều
            point = 2
            await message.reply(f"{message.author.mention} đã bị trừ **{point}** vì trả lời sai quá nhiều lần!")
            MwMongoManager.update_player_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point=-point)
            return
        MwMongoManager.create_and_update_player_penalty(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, user_id=message.author.id, user_name=message.author.name)
        if CustomFunctions.check_if_dev_mode():
            await message.add_reaction('❌')
        else:
            await message.add_reaction('<a:x_cross_red:1378265390110474362>')
        if err != None:
            message_tu_hien_tai = f"\nTừ hiện tại: `'{mw_info.current_word}'`. \nCó **{mw_info.remaining_word if mw_info.remaining_word else 0}** bắt đầu bằng `{mw_info.correct_start_word}`"
            view = SelfDestructView(timeout=30)
            mess = await message.reply(f"{err} {message_tu_hien_tai}")
            view.message = mess

    
    async def handling_game(self, message: discord.Message):
        if message.author.bot: return
        if not message.content: return
        if str.isspace(message.content): return
        mw_info, lan = await self.check_if_message_inside_game(source=message)
        if mw_info == None: return
        if message.content[0] in string.punctuation or message.content[0] == ":": return
        if lan == 'en' and len(message.content.split()) > 1: return
        
        selected_ban = None
        selected_penalty = None
        for player_ban in mw_info.player_ban:
            if player_ban.user_id == message.author.id and player_ban.ban_remain>0:
                selected_ban = player_ban
                break
                
        for player_penalty in mw_info.player_penalty:
            if player_penalty.user_id == message.author.id:
                selected_penalty = player_penalty
                break
        #Bắt đầu chơi
        message_tu_hien_tai = f"\nTừ hiện tại: `'{mw_info.current_word}'`. \nCó **{mw_info.remaining_word if mw_info.remaining_word else 0}** bắt đầu bằng `{mw_info.correct_start_word}`"
        #Kiểm tra xem có nằm trong danh sách ban không
        if selected_ban:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Bạn đã bị khoá lượt chơi trong vòng **{selected_ban.ban_remain}** lượt chơi tới!",color=discord.Color.red())
            embed.add_field(name=f"", value=f"\nOwner server có thể dùng lệnh {SlashCommand.SKILL_GIVE_WORD_MINIGAME.value} để lấy kỹ năng **Gỡ Khoá Mõm** hoặc **Gỡ Khoá Toàn Bộ** để mở khoá!", inline=False)
            mess = await message.reply(embed=embed)
            view.message = mess
            return
        point = 1
        if mw_info.special_point != None and mw_info.special_point > 0:
            point = mw_info.special_point
        if mw_info.current_player_id == message.author.id:
            #Kiểm coi bao nhiều penalty rồi.
            #Trên 5 thì trừ điểm luôn
            if selected_penalty != None and selected_penalty.penalty_point >=5:
                point = 2
                await message.reply(f"{message.author.mention} đã bị trừ **{point}** vì không chịu nhường cho người khác chơi!")
                MwMongoManager.update_player_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point=-point)
                return
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Bạn đã chơi rồi, vui lòng né qua một bên cho người khác nối từ!",color=discord.Color.red())
            mess = await message.reply(embed=embed)
            view.message = mess
            MwMongoManager.create_and_update_player_penalty(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=message.author.id, user_name=message.author.name)
            return
        elif not message.content.lower().startswith(mw_info.correct_start_word.lower()):
            await self.fail_attempt(message=message, mw_info= mw_info,lan=lan,point=point, err= f"Từ mới phải bắt đầu bằng `'{mw_info.correct_start_word}'`")
        elif message.content.lower() in mw_info.used_words:
            await self.fail_attempt(message=message, mw_info= mw_info,lan=lan,point=point, err= f"Từ `{message.content}` đã có người nối rồi bạn ơi")
        #Kiểm tra xem từ này có tồn tại không
        elif lan == 'en' and message.content.lower() not in self.english_words_dictionary.keys():
            await self.fail_attempt(message=message, mw_info= mw_info,lan=lan,point=point, err= f"Từ `{message.content}` không tồn tại trong từ điển của bot")
        elif lan == 'vn' and message.content.lower() not in self.vietnamese_dict.keys():
            await self.fail_attempt(message=message, mw_info= mw_info,lan=lan,point=point, err= f"Từ `{message.content}` không tồn tại trong từ điển của bot")
        else:
            #Coi như pass hết
            if CustomFunctions.check_if_dev_mode():
                await message.add_reaction('👍')
            else:
                await message.add_reaction('<a:check:1378265379419193354>')
            #Cập nhật lại thông tin
            current_player_id=message.author.id
            if CustomFunctions.check_if_dev_mode(): current_player_id = 1
            #Nếu trong game việt nam, gặp những từ có đuôi như sau thì đánh special case để xử lý tiếp
            special_words = ["à", "ả","ã", "ạ", "ẳ", "ẵ","ặ", "ẫ", "ẩ", "ậ", "õ", "ẽ", "ó", "ọ", "ờ","ớ", "ỡ", "ỗ", "ĩ", "ỉ","í", "ị", "ì", "ũ", "ủ", "ỹ", "ỳ", "ỵ", "ử", "ự", "ộ","ẻ","è", "ể", "ề", "ễ", "ệ", "ẹ", "ợ", "ữ"]
            special_case = False
            if lan == 'vn' and message.content[-1].lower() in special_words:
                special_case = True
            MwMongoManager.update_data_info(channel_id=message.channel.id, guild_id=message.guild.id, current_player_id=current_player_id, current_player_name=message.author.display_name, current_word=message.content.lower(), type= mw_info.type, special_case=special_case, lang=lan)
            #Cập nhật lại điểm
            MwMongoManager.update_player_point_data_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan)
            ProfileMongoManager.update_level_progressing(guild_id=message.guild.id, user_id=message.author.id)
            
            end_round = 500
            if mw_info.current_round>=end_round:
                #Reset
                await message.channel.send(f"Đã chơi được **{end_round}** lượt rồi. Cảm ơn mọi người đã chơi nhé. Đến lúc reset lại rồi, nên mọi người bắt đầu lại nhé!")
                await self.process_reset(message=message, mw_info=mw_info, language=lan)
                return
            else:
                mw_info, lan = await self.check_if_message_inside_game(source=message)
                if mw_info.remaining_word<=0:
                    await message.channel.send(f"Kinh nhờ, chơi hết từ khả dụng rồi. Cảm ơn mọi người đã chơi nhé. Đến lúc reset thông tin từ rồi. Mọi người bắt đầu lại nhé!")
                    await self.process_reset(message=message, mw_info=mw_info, language=lan)
                    return
                #Thông báo
                message_tu_hien_tai = f"\nTừ hiện tại: `'{mw_info.current_word}'`. \nCó **{mw_info.remaining_word if mw_info.remaining_word else 0}** bắt đầu bằng `{mw_info.correct_start_word}`"
                #Kiểm tra xem có special_item không, nếu có thì cộng cho player
                chuc_mung_item = ""
                if mw_info.special_item:
                    MwMongoManager.update_player_special_item(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= mw_info.special_item)
                    chuc_mung_item = f" và nhận được kỹ năng **{mw_info.special_item.item_name}**. Nhớ đừng quên sử dụng nó nhé"
                #Trả lời đúng thì reset special_points và special_item lại từ đầu, cập nhật lại list player ban
                await message.channel.send(f"{message.author.mention}, bạn đã được cộng {point} điểm{chuc_mung_item}. Để kiểm tra điểm số của mình thì hãy dùng lệnh {SlashCommand.BXH.value}. {message_tu_hien_tai}")
                #Reset special point, special item, giảm ban remain của tất cả player
                MwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
                MwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
                MwMongoManager.remove_player_penalty_after_round(channel_id= message.channel.id, guild_id= message.guild.id, language=lan)
                MwMongoManager.reduce_player_bans_word_matching_info_after_round(channel_id= message.channel.id, guild_id= message.guild.id, language=lan)
                
        #Xổ số nếu chưa có special point
        so_xo = random.randint(4, 10)
        #Nếu sổ xố rơi trúng số 5 thì coi như cộng point lên x2, x3, x4 ngẫu nhiên
        if so_xo == 10:
            x_value = random.randint(2, 5)
            special_point_english = 1*x_value
            MwMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= special_point_english)
            embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Điểm Thưởng Duy Nhất {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Cơ hội chỉ đến một lần duy nhất, nếu ai đoán đúng sẽ nhận được **{special_point_english}** điểm!", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} **Lưu ý**: Đoán sai sẽ mất điểm ngay, nên hãy suy nghĩ cho kỹ trước khi trả lời!", inline=False)
            view = SelfDestructView(timeout=45)
            m = await message.channel.send(embed=embed, view=view)
            view.message = m
        else:
            #Sổ xố xem trúng kỹ năng đặc biệt không
            so_xo = random.randint(3, 10)
            if so_xo == 10:
                text_cong_skill = f"\n**Cơ hội chỉ đến một lần duy nhất, nếu ai thắng nhận được kỹ năng đặc biệt bên dưới! Cơ hội duy nhất thôi!**\n"
                percent = random.randint(0, 100)
                item = None
                if percent >= 0 and percent < 55:
                    #Cấp thấp
                    item = random.choice(ListSkills.list_special_items_cap_thap)
                elif percent >= 55 and percent < 80:
                    #Cấp cao
                    item = random.choice(ListSkills.list_special_items_cap_cao)
                elif percent >= 80 and percent < 95:
                    #Đẳng cấp
                    item = random.choice(ListSkills.list_special_items_dang_cap)
                else:
                    #tối thượng
                    item = random.choice(ListSkills.list_special_items_toi_thuong)
                
                result = MwMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item=item)
                embed = discord.Embed(title=f"Kỹ năng đặc biệt. Rank: {item.level}", description=f"", color=0x03F8FC)
                embed.add_field(name=f"", value=f"Tên kỹ năng: {item.item_name}", inline=False)
                embed.add_field(name=f"", value=f"Mô tả kỹ năng: {item.item_description}", inline=False)
                view = SelfDestructView(timeout=45)
                m = await message.channel.send(content=text_cong_skill, embed=embed, view=view)
                view.message = m
                return
                