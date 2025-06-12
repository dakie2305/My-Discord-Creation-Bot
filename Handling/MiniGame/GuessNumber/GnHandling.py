import discord
import random
from CustomEnum.EmojiEnum import EmojiCreation1
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from Handling.MiniGame.GuessNumber import GnMongoManager, ListGuessNumberSkills
from Handling.MiniGame.GuessNumber.GuessNumberClass import GuessNumberInfo
import CustomFunctions
import string
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
import re


class GnHandlingFunction():
    def __init__ (self, message: discord.Message):
        self.message = message
        self.english_words_dictionary = CustomFunctions.english_dict
        self.vietnamese_dict = CustomFunctions.vietnamese_dict
        
    async def check_if_message_inside_game(self, source: discord.Message):
        if source == None: return None
        check = GnMongoManager.find_guess_number_info_by_id(guild_id=source.guild.id, channel_id= source.channel.id)
        if check!=None:
            return check
    
    async def process_reset(self, message: discord.Message, gn_info: GuessNumberInfo):
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Đoán Số", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        embed.add_field(name=f"", value=f"Lượt hiện tại: {gn_info.current_round}", inline=False)
        count = 0
        if gn_info.player_profiles:
            gn_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for index, profile in enumerate(gn_info.player_profiles):
                if (profile.point!= 0 or len(profile.special_items)> 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** <@{profile.user_id}>. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 20: break
        text = "Chúc mừng các player top đầu!"
        await message.channel.send(content=text, embed=embed)
        #Xoá đi tạo lại
        GnMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id)
        
        num = random.randint(gn_info.range_from, gn_info.range_to)
        
        data = GuessNumberInfo(channel_id=message.channel.id, channel_name=message.channel.name, guild_name=message.guild.name, correct_number=num, range_from=gn_info.range_from, range_to=gn_info.range_to)
        GnMongoManager.create_info(data=data, guild_id=message.guild.id)
        embed = discord.Embed(title=f"{EmojiCreation1.CHECK.value} Đoán Số May Mắn", description=f"",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Hãy nhắn vào một con số bất kỳ, bot sẽ gợi ý cho bạn tìm ra con số chính xác!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Đáp án đúng sẽ thuộc khoảng từ **`{gn_info.range_from}`** đến **`{gn_info.range_to}`**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bot sẽ react {EmojiCreation1.HIGHER.value} nếu số của bạn thấp hơn đáp án", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bot sẽ react {EmojiCreation1.LOWER.value} nếu số của bạn cao hơn đáp án", inline=False)
        channel = message.channel
        await channel.send(embed=embed)
        
            
    async def fail_attempt(self, message: discord.Message, gn_info: GuessNumberInfo):
        #Reset special point nếu trả lời sai, và nếu trước đó đã có
        if gn_info.special_point:
            GnMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, special_point= 0)
        if gn_info.special_item:
            GnMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, special_item= None)
        
        list_player_penalty = gn_info.player_penalty
        selected_player = None
        for player in list_player_penalty:
            if player.user_id == message.author.id and player.penalty_point > 10:
                selected_player = player
                break
        if selected_player is not None:
            #Trừ điểm vì sai quá nhiều
            point = 2
            await message.reply(f"{message.author.mention} đã bị trừ **{point}** vì trả lời sai quá nhiều lần!")
            GnMongoManager.update_player_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point=-point)
            return
        GnMongoManager.create_and_update_player_penalty(channel_id= message.channel.id, guild_id= message.guild.id, user_id=message.author.id, user_name=message.author.name)
        
        player_guess_number = int(message.content)
        #15 round đầu là sẽ có hint, về sau sẽ roll tỉ lệ
        flag_hint = False
        chance = UtilitiesFunctions.get_chance(30)
        if gn_info.current_round < 15 or chance:
            flag_hint = True
        
        if CustomFunctions.check_if_dev_mode():
            if int(message.content) < gn_info.correct_number:
                await message.add_reaction('⤴️')
            elif int(message.content) > gn_info.correct_number:
                await message.add_reaction('⤵️')
        else:
            #Dùng custom emoji
            if int(message.content) < gn_info.correct_number:
                await message.add_reaction(EmojiCreation1.HIGHER.value)
                
            elif int(message.content) > gn_info.correct_number:
                await message.add_reaction(EmojiCreation1.LOWER.value)
        if flag_hint:
            #Tạo hint ngẫu nhiên
            text_hint = f"Số `{player_guess_number}` của bạn là quá {'thấp' if player_guess_number < gn_info.correct_number else 'cao'}.\n"
            text_hint += self.generate_hint(guess=player_guess_number, answer=gn_info.correct_number)
            await message.reply(f"{text_hint}")
            
    def generate_hint(self, guess: int, answer: int) -> str:
        hints = []
        for d in [2, 3, 5, 7, 10]:
            if answer % d == 0:
                hints.append(f"Số cần tìm chia hết cho `{d}`.")
                break

        abs_answer = abs(answer)
        abs_answer_str = str(abs_answer)

        hints.append(f"Số cần tìm có tận cùng là `{abs_answer % 10}`.")
        hints.append(f"Số cần tìm là một số {'chẵn' if answer % 2 == 0 else 'lẻ'}.")
        hints.append(f"Số cần tìm là một số {'dương' if answer > 0 else 'âm'}.")
        hints.append(f"Số cần tìm có `{len(abs_answer_str)}` chữ số.")
        hints.append(f"Chữ số đầu tiên của số cần tìm là `{abs_answer_str[0]}`.")
        hints.append(f"Tổng các chữ số của số cần tìm là `{sum(int(d) for d in abs_answer_str)}`.")

        if abs(guess - answer) <= 100:
            return f"Số bạn đoán gần đúng rồi, chỉ chênh lệch `{abs(guess - answer)}` đơn vị!"

        even_count = sum(1 for d in abs_answer_str if int(d) % 2 == 0)
        hints.append(f"Số cần tìm có `{even_count}` chữ số chẵn.")
        odd_count = sum(1 for d in abs_answer_str if int(d) % 2 != 0)
        hints.append(f"Số cần tìm có `{odd_count}` chữ số lẻ.")

        if len(abs_answer_str) >= 3:
            hints.append(f"Hai chữ số đầu của số cần tìm là `{abs_answer_str[:2]}`.")
        if len(abs_answer_str) >= 4:
            hints.append(f"Ba chữ số đầu của số cần tìm là `{abs_answer_str[:3]}`.")
        if len(abs_answer_str) >= 2:
            hints.append(f"Hai chữ số cuối của số cần tìm là `{abs_answer_str[-2:]}`.")
        if len(abs_answer_str) >= 3:
            hints.append(f"Ba chữ số cuối của số cần tìm là `{abs_answer_str[-3:]}`.")

        return random.choice(hints)
    
    async def handling_game(self, message: discord.Message):
        if message.author.bot: return
        if not message.content: return
        if str.isspace(message.content): return
        gn_info = await self.check_if_message_inside_game(source=message)
        if gn_info == None: return
        if message.content[0] in string.punctuation and message.content[0] not in ['-', '+']: return
        if not re.fullmatch(r"[+-]?\d+", message.content.strip()): return
        
        player_number = int(message.content)
        selected_ban = None
        selected_penalty = None
        for player_ban in gn_info.player_ban:
            if player_ban.user_id == message.author.id and player_ban.ban_remain > 0:
                selected_ban = player_ban
                break
                
        for player_penalty in gn_info.player_penalty:
            if player_penalty.user_id == message.author.id:
                selected_penalty = player_penalty
                break
        #Bắt đầu chơi
        #Kiểm tra xem có nằm trong danh sách ban không
        if selected_ban:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Bạn đã bị khoá lượt chơi trong vài vòng sắp tới!",color=discord.Color.red())
            embed.add_field(name=f"", value=f"\nOwner server có thể dùng lệnh {SlashCommand.SKILL_GIVE_WORD_MINIGAME.value} để lấy kỹ năng **Gỡ Khoá Mõm** hoặc **Gỡ Khoá Toàn Bộ** để mở khoá!", inline=False)
            mess = await message.reply(embed=embed)
            view.message = mess
            return
        point = 1
        if gn_info.special_point != None and gn_info.special_point > 0:
            point = gn_info.special_point
        
        if player_number != gn_info.correct_number:
            await self.fail_attempt(message=message, gn_info= gn_info)
            #Vẫn reduce dựa trên tỉ lệ
            chance = UtilitiesFunctions.get_chance(40)
            if chance:
                GnMongoManager.reduce_player_penalty_after_round(channel_id= message.channel.id, guild_id= message.guild.id)
                GnMongoManager.reduce_player_bans_after_round(channel_id= message.channel.id, guild_id= message.guild.id)
        else:
            #Coi như pass hết
            if CustomFunctions.check_if_dev_mode():
                await message.add_reaction('👍')
            else:
                await message.add_reaction(EmojiCreation1.CHECK.value)
            GnMongoManager.update_data_info(channel_id=message.channel.id, guild_id=message.guild.id)
            #Cập nhật lại điểm
            GnMongoManager.update_player_point_data_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id)
            ProfileMongoManager.update_level_progressing(guild_id=message.guild.id, user_id=message.author.id)
            end_round = 200
            if gn_info.current_round >= end_round:
                #Reset
                await message.channel.send(f"Đã chơi được **{end_round}** lượt rồi. Cảm ơn mọi người đã chơi nhé. Đến lúc reset lại rồi, nên mọi người bắt đầu lại nhé!")
                await self.process_reset(message=message, gn_info=gn_info)
                return
            else:
                #Kiểm tra xem có special_item không, nếu có thì cộng cho player
                chuc_mung_item = ""
                if gn_info.special_item:
                    GnMongoManager.update_player_special_item(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id, special_item= gn_info.special_item)
                    chuc_mung_item = f" và nhận được kỹ năng **{gn_info.special_item.item_name}**. Nhớ đừng quên sử dụng nó nhé"
                #Trả lời đúng thì reset special_points và special_item lại từ đầu, cập nhật lại list player ban
                await message.channel.send(f"{message.author.mention}, bạn đã đoán đúng số {gn_info.correct_number} và nhận được {point} điểm{chuc_mung_item}.\nSố tiếp theo nằm trong khoảng **`{gn_info.range_from}`** đến **`{gn_info.range_to}`**.\nĐể kiểm tra điểm số của mình thì hãy dùng lệnh {SlashCommand.BXH.value}.")
                #Reset special point, special item, giảm ban remain của tất cả player
                GnMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id, special_point= 0)
                GnMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id, special_item= None)
                GnMongoManager.remove_player_penalty_after_round(channel_id= message.channel.id, guild_id= message.guild.id)
                GnMongoManager.reduce_player_bans_after_round(channel_id= message.channel.id, guild_id= message.guild.id)
        #Xổ số nếu chưa có special point
        so_xo = UtilitiesFunctions.get_chance(10)
        #Nếu sổ xố rơi trúng số 5 thì coi như cộng point lên x ngẫu nhiên
        if so_xo == 10:
            x_value = random.randint(4, 10)
            special_point_english = 1*x_value
            GnMongoManager.update_special_point_data_info(channel_id= message.channel.id, guild_id= message.guild.id,  special_point= special_point_english)
            embed = discord.Embed(title=f"{EmojiCreation1.EXCLAIM_MARK.value} Điểm Thưởng Duy Nhất {EmojiCreation1.EXCLAIM_MARK.value}", description=f"",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬▬▬ι═══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Cơ hội chỉ đến một lần duy nhất, nếu ai đoán đúng sẽ nhận được **{special_point_english}** điểm!", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} **Lưu ý**: Đoán sai sẽ mất điểm ngay, nên hãy suy nghĩ cho kỹ trước khi trả lời!", inline=False)
            view = SelfDestructView(timeout=15)
            m = await message.channel.send(embed=embed, view=view)
            view.message = m
        else:
            #Sổ xố xem trúng kỹ năng đặc biệt không
            so_xo = UtilitiesFunctions.get_chance(10)
            if so_xo == 10:
                text_cong_skill = f"\n**Cơ hội chỉ đến một lần duy nhất, nếu ai thắng nhận được kỹ năng đặc biệt bên dưới! Cơ hội duy nhất thôi!**\n"
                percent = random.randint(0, 100)
                item = None
                if percent >= 0 and percent < 55:
                    #Cấp thấp
                    item = random.choice(ListGuessNumberSkills.list_special_items_cap_thap)
                elif percent >= 55 and percent < 80:
                    #Cấp cao
                    item = random.choice(ListGuessNumberSkills.list_special_items_cap_cao)
                elif percent >= 80 and percent < 95:
                    #Đẳng cấp
                    item = random.choice(ListGuessNumberSkills.list_special_items_dang_cap)
                else:
                    #tối thượng
                    item = random.choice(ListGuessNumberSkills.list_special_items_toi_thuong)
                GnMongoManager.update_special_item_data_info(channel_id= message.channel.id, guild_id= message.guild.id,  special_item=item)
                embed = discord.Embed(title=f"Kỹ năng đặc biệt. Rank: {item.level}", description=f"", color=0x03F8FC)
                embed.add_field(name=f"", value=f"Tên kỹ năng: {item.item_name}", inline=False)
                embed.add_field(name=f"", value=f"Mô tả kỹ năng: {item.item_description}", inline=False)
                view = SelfDestructView(timeout=15)
                m = await message.channel.send(content=text_cong_skill, embed=embed, view=view)
                view.message = m
                return
                