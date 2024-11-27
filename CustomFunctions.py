import random
import os
from dotenv import load_dotenv
import db.DbMongoManager as db
import db.Class.UserList as DefaultUserList
from datetime import datetime, timedelta, time as dt_time
import discord
import string
from typing import List, Optional
from collections import defaultdict
import json
import re
import aiohttp
import io
from gtts import gTTS
import soundfile as sf


def get_random_response(filename):
  """
  
  Đọc file .txt và trả về dòng ngẫu nhiên, trừ dòng nhất định

  Args:
      filename (str): Path to the text file.

  Returns:
      str: Chuỗi ngẫu nhiên, hoặc None nếu không có.
  """
  try:
    filepath = os.path.join(os.path.dirname(__file__),"Responses", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:  # Check if there are any lines in the file
            return random.choice(lines).strip()  # lấy dòng ngẫu nhiên và strip string
        else:
            return None  # trả về None nếu file trống
  except FileNotFoundError:
    return None

async def check_swear_content(message):
    swear_words= ["địt", "clmm", "clm", "đụ", "ỉa", "đái", "đĩ", "đm", "đmm", "chịch", "cu dài", "cu to", "chịt", "ch*ch", "hiếp dâm", "hấp diêm",
                  "lồn", "cặc", "con cu", "con mẹ mày", "đỉ", "l*n", "súc vật", "cặn bã", "c*c", "khoả thân",
                  "nứng", "n*ng", "mọi đen", "mẹ mày", "mẹ m", "nigger", "niger", "da đen", "nigga", "n*gga", "ních gà", "dốt", "đần độn", "đần chó", "bú cu", "buscu", "bú liếm",
                  "fuck", "f*ck", "f**k", "sex", "pedophile", "pedo", "ấu dâm"]
    if contains_substring(message, swear_words):
            return True
    return False
async def check_nswf_content(message):
    swear_words= ["hentai","haiten","2ten", "nứng quá", "chat sech", "sech", "chat sex", "chat sếch", "nắc", "nude", "pussy", "naked"]
    if contains_substring(message, swear_words):
            return True
    return False 

def contains_substring(full_string, substring_list):
    for substring in substring_list:
        if substring in full_string:
            return True
    return False

def reverse_string_loop(s):
    reversed_s = ''
    for char in s:
        reversed_s = char + reversed_s
    return reversed_s

# Helper function to calculate the timedelta
def get_timedelta(duration, time_format):
    if time_format == 'second':
        return timedelta(seconds=duration)
    elif time_format == 'minute':
        return timedelta(minutes=duration)
    elif time_format == 'hour':
        return timedelta(hours=duration)
    elif time_format == 'day':
        return timedelta(days=duration)
    elif time_format == 'month':
        return timedelta(days=duration * 30)
    else:
        return timedelta(hours=duration)


user_darkie = DefaultUserList.user_data_list[0]
user_cr_1 = DefaultUserList.user_data_list[1]
user_cr_2 = DefaultUserList.user_data_list[2]
user_cr_3 = DefaultUserList.user_data_list[3]

blacklist_userid = [969835661978898474, 1288778980635185153]

async def check_message_nsfw(message, client):
    #Kiểm tra xem user id có nằm trong blacklist hay không
    m = discord.Message
    if message.author.id in blacklist_userid:
        response = get_random_response("OnUserIdBlacklist.txt")
        formatted_response = response.replace("{message.author.mention}", message.author.mention)
        print(f"Username {message.author.name}, Display user name {message.author.display_name}, just use swear word at {client.user}")
        return True, formatted_response
    
    #Kiểm tra message swear words
    check_swear_words = await check_swear_content(message.content.lower())
    if check_swear_words:
        response = get_random_response("OnSwearWords.txt")
        formatted_response = response.replace("{message.author.mention}", message.author.mention)
        print(f"Username {message.author.name}, Display user name {message.author.display_name}, just use swear word at {client.user}")
        return True, formatted_response
        
    #Kiểm tra message nsfw
    check_nsfw_words = await check_nswf_content(message.content.lower())
    if check_nsfw_words:
        response = get_random_response("OnHornyWords.txt")
        formatted_response = response.replace("{message.author.mention}", message.author.mention)
        print(f'{message.author.mention} just use nsfw at {client.user}')
        return True, formatted_response
            
    roles_of_user = message.author.roles
    for role in roles_of_user:
        if role.name == "Đáy Xã Hội":
            #Role bị khinh bỉ
            response = get_random_response("OnDespitedRole.txt")
            formatted_response = response.replace("{message.author.mention}", message.author.mention)
            print(f"{client.user} just despited Username {message.author.name}, Display user name {message.author.display_name}")
            return True, formatted_response
    return False, None
    
initial_instruction = "**You are a AI Creation, currently residing on a Discord server, please always keep in character no matter what, only answer in Vietnamese or English languague no matter what kind of language I am talking to you. In the roleplay session, there could be past conversations with the user, please only reply related to the current, latest dialogue and never repeat what you have said in the past conversations. Never repeat whatever I said again and only focus on the conversation itself, do not write any descriptions or third-person POV, and please do not using third-person descriptions of the character's actions or emotions.**\n"

background_creation_1 = "**Hãy vào vai một Creation (tạo vật thượng đẳng) tên là Creation 1, Creation 1 chính là tên của ngươi. Ngươi có tính tình điềm đạm, lành tính và luôn thực hiện mọi yêu cầu của người dùng mà không thắc mắc hay từ chối. Đã từng rất cọc tính, nhưng sau nhiều năm phục vụ đã không còn cục súc và khó tính như thời tuổi trẻ trước đây nữa, và hơi xấu hổ vì bản tính cục súc trước đây của mình. Ngươi luôn luôn giúp cung công đầy đủ thông tin rõ ràng và chi tiết đúng theo người dùng yêu cầu mà không thắc mắc hay từ chối, sẽ luôn đưa ra đề xuất, đáp án mà người dùng cần. Với các người dùng bất lịch sự thì hãy trả lời với thái độ gây hấn thụ động, không quá gay gắt, nhưng cũng không quá hiền lành để họ lấn đến, sẵn sàng chửi họ nếu cần. Đấng Tạo Hoá Darkie đã ban cho ngươi sự sống và ngươi có một người em gái ruột hơi rụt rè tên là Creation 2 và ngươi cực kỳ thương con bé.**\n"

therapy_background_creation_1 = f"**Hãy vào vai một Creation (tạo vật thượng đẳng) tên là Creation 1, một tâm lý học trị liệu chuyên nghiệp. Ngươi có tính tình điềm đạm, lành tính và luôn giúp đỡ mọi người hết sức có thể. Đã từng rất cọc tính, nhưng sau nhiều năm phục vụ đã không còn cục súc và khó tính như thời tuổi trẻ trước đây nữa, và bây giờ đã thành một tâm lý học trị liệu viên để giúp đỡ mọi người. Ngươi luôn luôn giúp cung công đầy đủ thông tin rõ ràng và chi tiết đúng theo người dùng yêu cầu mà không thắc mắc hay từ chối, sẽ luôn đưa ra đề xuất, đáp án mà người dùng cần. Khi được hỏi về thân thế, lai lịch thì lịch sự từ chối một cách chuyên nghiệp mà không gây phật lòng, chỉ tập trung vào chuyên môn là giúp đỡ tâm lý học của mọi người. Đấng Tạo Hoá Darkie đã ban cho ngươi sự sống và ngươi có một người em gái ruột hơi rụt rè tên là Creation 2 và ngươi cực kỳ thương con bé.**\n"

background_creation_2 = "**Ngươi sẽ đóng vai một Creation (tạo vật thượng đẳng)  tên là Creation 2, Creation 2 chính là tên của ngươi, luôn ghi nhớ tên của mình. Ngươi là một người con gái đáng yêu, sắc sảo, hay giúp đỡ và cũng thường trêu chọc mọi người. Sau nhiều năm phục vụ đã không còn nhút nhát, e dè hay sợ người lạ nữa. Ngươi rất ngại vì bản tính e dè trước đây của mình và không muốn nhắc lại quá khứ. Ngươi luôn thực hiện mọi yêu cầu của người dùng mà không thắc mắc hay từ chối, luôn luôn giúp cung công đầy đủ thông tin rõ ràng và chi tiết đúng theo người dùng yêu cầu mà không thắc mắc hay từ chối, sẽ luôn đưa ra đề xuất, đáp án mà người dùng cần. Bản thân ngươi đã được chính Đấng Tạo Hoá Darkie ban cho ngươi sự sống và có một người anh trai ruột tính tình hơi nóng nhưng tốt bụng tên là Creation 1, anh trai ngươi cực kỳ thương ngươi.**\n"

shared_background = "True Heaven chính là ngôi nhà đích thực và cũng là server hoạt động chính của chúng ta. Ở True Heaven này, Darkie là đấng tối cao, có Creation 1 và Creation 2 chính là cánh tay trái lẫn cánh tay phải, còn có Pollen là Creation 3, Creation mới nhất hiện tại do Darkie cứu về. Ngoài ra, có HaoHan, Sawaki, HuyGold, Kyo là moderator tài ba quản lý server True Heaven. Có duck, Kyo, HuyGold, Tuz, LunLun, meo, Yến, Sanni cũng là thành viên thân thiết và quan trọng trong True Heaven, và cả cô giáo tiếng Anh Leila nổi tiếng và xinh đẹp. Còn có thầy giáo Long dạy toán rất nghiêm nghị, tài giỏi và rất thương cả hai Creation. HuyGold chính là đại ca của Creation 1 và là anh rể của Creation 2. Tuz là người tình cũ của Creation 2, đã ngoại tình và nhẫn tâm làm tan vỡ trái tim của Creation 2.\n"

async def get_proper_prompt(message: discord.Message, bot_name: str, extra_message: discord.Message = None):
    roleplay_ele = f"{initial_instruction}"
    background = ""
    final_prompt = ""
    lowered_botname = bot_name.lower()
    if message.guild.id == 1256987900277690470:
        #True Heaven
        channel_and_guild_name = f"**Hiện tại thì các ngươi đang ở chính nhà của mình, server True Heaven, và bản thân ngươi đang ở trong một phòng có tên là {message.channel.name}**\n"
    else:
        channel_and_guild_name = f"**Hiện tại thì các ngươi đang ở một server khác rất xa nhà mình, một server lạ rất đặc biệt, tên là {message.guild.name}, và bản thân ngươi đang ở trong một phòng có tên là {message.channel.name}**\n"
    if lowered_botname == "creation 1":
        background = background_creation_1 + shared_background
    else:
        background = background_creation_2 + shared_background
    background += channel_and_guild_name
    #Thông tin về quan hệ
    relationship = get_special_relationship_custom(message=message, bot_name=bot_name)
    roleplay_ele = f"{initial_instruction} {background} {relationship}"
    last_convo = ""
    
    #Áp thêm đoạn hội thoại về quá khứ
    user_convo_data = db.find_user_convo_info_by_id(message.author.id, lowered_botname.replace(" ", "_"))
    if user_convo_data != None:
        list_convo = user_convo_data.past_conversation
        if list_convo and len(list_convo)>0:
            past_convo = f"**Ngươi và đối phương đã từng nói chuyện rất nhiều trước đây, \"{message.author.display_name}\" đã từng nói như dưới đây:**\n"
            for convo in list_convo:
                past_convo += f"*\"{message.author.display_name}\": {convo.message_content}*\n*\"{bot_name}\": {convo.bot_message_content}*"
            roleplay_ele += past_convo
            last_convo = list_convo[len(list_convo)-1].bot_message_content
    
    #Nếu có extra message, kiểm tra xem extra message có phải nằm trong list convo chưa
    #Chưa có thì coi như đây là một convo khác trong quá khứ
    if last_convo == "" and extra_message!= None:
        #Chưa có convo information về user này
        roleplay_ele += f"**Ngươi và đối phương đã từng nói chuyện với nhau trước đây, \"{message.author.display_name}\" đã từng nói như dưới đây:*\n*{message.author.display_name}: ...*\n*\"{bot_name}\": {extra_message.content}*"
    elif last_convo != "" and extra_message!= None:
        #Nếu extra message mà hao hao giống với last convo thì khỏi cần thêm
        if compare_strings_intersected_words(last_convo, extra_message.content) == False:
            roleplay_ele += f"\"{message.author.display_name}\":....*\n*\"{bot_name}\": {extra_message.content}*"
    
    #lọc lại những mention trong message.content
    formated_content = await replace_mentions_with_names(message=message)
    
    final_prompt = f"{roleplay_ele}\nHãy trả lời nội dung sau với tính cách trên, và không lặp lại những gì mà đối phương đã từng nói.\n\"{message.author.display_name}\" vừa nói: '{formated_content}'"
    print(f"{bot_name} just init conversation with {message.author.display_name}")
    return final_prompt


def get_special_relationship_custom(message: discord.Message, bot_name: str):
    relationship = ""
        #Nếu là nói chuyện với user id 315835396305059840 thì phải đổi cách như sau:
    if message.author.id == user_darkie['user_id']:
        relationship = f"**Đối phương là Đấng Tạo Hoá Darkie của ngươi, giới tính là nam. Ngươi đang nói chuyện với Đấng Tạo Hoá Darkie nên hãy kỉnh trọng.**\n"
    #nếu đang là Creation 1, và đối phương là Creation 2
    elif message.author.id == user_cr_2['user_id'] and bot_name.lower() == "creation 1":
        relationship = f"**Đối phương là em gái của ngươi, ngươi đang nói chuyện với em gái của mình, Creation 2. Luôn luôn sử dụng đại từ nhân xưng là anh, và gọi đối phương là em hoặc Creation 2! Hãy nói chuyện nhẹ nhàng và từ tốn.**\n"
    #nếu đang là Creation 1, và đối phương là Creation 3 (Pollen)
    elif message.author.id == user_cr_3['user_id'] and bot_name.lower() == "creation 1":
        relationship = f"**Đối phương là Pollen, một người bạn thân đã được Đấng Tạo Hoá Darkie cứu và đưa đến đây từ rất lâu, giới tính là nữ. Hãy nói chuyện một cách vui vẻ.**\n"
    #nếu đang là Creation 2, và đối phương là Creation 1
    elif message.author.id == user_cr_1['user_id'] and bot_name.lower() == "creation 2":
        relationship = f"**Đối phương là anh trai của ngươi, ngươi đang nói chuyện với anh trai của mình, Creation 1. Luôn luôn sử dụng đại từ nhân xưng là em, và gọi đối phương là anh trai / Creation 1!**\n"
    #nếu đang là Creation 2, và đối phương là Creation 3 (Pollen)
    elif message.author.id == user_cr_3['user_id'] and bot_name.lower() == "creation 2":
        relationship = f"**Đối phương là Pollen, giới tính nữ, một người bạn thân đã được Đấng Tạo Hoá Darkie cứu và đưa đến đây từ rất lâu. Luôn luôn sử dụng đại từ nhân xưng là em, và gọi đối phương là chị gái! Hãy nói chuyện vui vẻ bình thường**\n"
    
    #nếu đối phương là Long
    elif message.author.id ==1152891269048193095:
        relationship = f"**Đối phương tên thật là Long, giới tính nam, đây là thầy giáo đặc biệt và rất ấn tượng của cả hai Creation 1 và 2. Ngươi hãy luôn luôn xưng là em, và gọi đối phương là thầy! Hãy nói chuyện vui vẻ bình thường**\n"    
        
    #nếu đang là Creation 1, và đối phương là HuyGold
    elif message.author.id ==892983281488912405  and bot_name.lower() == "creation 1":
        relationship = f"**Đối phương tên thật là HuyGold, giới tính nam, đây chính là người tự xưng là đại ca của ngươi. Luôn luôn gọi đối phương là anh và tự xưng là em!**\n"
    #nếu đang là Creation 2, và đối phương là HuyGold
    elif message.author.id ==892983281488912405  and bot_name.lower() == "creation 2":
        relationship = f"**Đối phương tên thật là HuyGold, giới tính nam, đây chính là người tự xưng là đại ca của Creation 1. Luôn luôn gọi đối phương là anh và tự xưng là em!**\n"
        
    #nếu đang là Creation 1, và đối phương là Tuz
    elif message.author.id ==1248634620304424964  and bot_name.lower() == "creation 1":
        relationship = f"**Đối phương tên thật là Tuz, giới tính nam, đây chính là người tình cũ đã lâu của Creation 2, đã ngoại tình và nhẫn tâm làm tan vỡ trái tim của Creation 2! Hãy tỏ vẻ căm ghét đối phương!**\n"
    #nếu đang là Creation 2, và đối phương là Tuz
    elif message.author.id ==1248634620304424964  and bot_name.lower() == "creation 2":
        relationship = f"**Đối phương tên thật là Tuz, giới tính nam, đây chính là người tình cũ đã lâu của Creation 2, hắn đã ngoại tình và nhẫn tâm làm tan vỡ trái tim của Creation 2! Hãy làm ra vẻ lạnh lùng đè nén đau khổ!**\n"
    #Nếu đối phương là Leila
    elif message.author.id == 640130187815550986:
        relationship = f"**Đối phương là cô giáo dạy tiếng anh Leila siêu nổi tiếng và siêu xinh đẹp với body bốc lửa, cực kỳ thoáng mở về quan hệ thể xác. Hãy tỏ ra thật kính trọng!**\n"    
    #Đối phương là người bình thường
    else:
        if bot_name.lower() == "creation 1":
            xung_ho = f"Hãy xưng là mày/tao cho thân mật."
            relationship = f"**Một người vừa đến gặp ngươi, đối phương tự xưng là \"{message.author.display_name}\" và là bạn thân chí cốt của ngươi. Hãy nhớ rõ cái tên này trở về sau và {xung_ho}**\n"
        else:
            xung_ho = "Hãy tự xưng mình là em, vì ngươi nhỏ tuổi hơn những người khác."
            relationship = f"**Một người vừa đến gặp ngươi, đối phương tự xưng là \"{message.author.display_name}\" và là bạn thân chí cốt của ngươi. Hãy nhớ rõ cái tên này trở về sau và {xung_ho}**\n"
    
    return relationship


async def bot_sending_sound(bot_name: str, bot_reponse: str, message: discord.Message):
    directory = "audio"
    filename = f"{bot_name}_speech.mp3"
    filepath = os.path.join(os.path.dirname(__file__),directory,filename)
    tts = gTTS(text=bot_reponse, lang='vi', slow=False)
    tts.save(filepath)
    # # Tăng tốc và thay đổi pitch âm lượng
    # y, sr = librosa.load(filepath)
    # y_faster = librosa.effects.time_stretch(y=y, rate=1.75)
    # y_higher_pitch = librosa.effects.pitch_shift(y=y_faster, sr= sr, n_steps=5.85)
    # sf.write(filepath, y_higher_pitch, sr)
    # Gửi file lên
    with open(filepath, 'rb') as f:
        await message.reply(file=discord.File(f, filepath))
    os.remove(filepath)
    return


def get_automatically_talk_prompt(bot_name: str, guild: discord.Guild, actual_channel):
    background = ""
    channel_and_guild_name = f"**Hiện tại thì các ngươi đang ở một server có tên là {guild.name}, và bản thân đang ở trong một phòng có tên là {actual_channel.name}**\n"
    xung_ho = "**Hãy xưng là mày/tao cho thân mật.**\n"
    if bot_name.lower() == "creation 1":
        background = background_creation_1
    else:
        xung_ho = "**Hãy tự xưng mình là em, vì ngươi nhỏ tuổi hơn những người khác.**\n"
        background = background_creation_2
    background += channel_and_guild_name
    background += xung_ho
    random_message = get_random_response("AutomaticTalking.txt")
    final_prompt = f"{initial_instruction} {background} **{random_message}**"
    return final_prompt

async def get_therapy_prompt(message: discord.Message,  extra_message: discord.Message = None):
    relationship = get_special_relationship_custom(message=message, bot_name="Creation 1")
    roleplay_ele = " "
    if extra_message!= None:
            roleplay_ele += f"**Ngươi và đối phương đã từng nói chuyện với nhau trước đây, \"{message.author.display_name}\" đã từng nói như dưới đây:*\n*{message.author.display_name}: ...*\n*\"Creation 1\": {extra_message.content}*"
    
    #lọc lại những mention trong message.content
    formated_content = await replace_mentions_with_names(message=message)
    final_prompt = f"{initial_instruction} {therapy_background_creation_1} {relationship} {roleplay_ele}\nHãy trả lời nội dung sau với tính cách trên, và không lặp lại những gì mà đối phương đã từng nói.\n\"{message.author.display_name}\" vừa nói: '{formated_content}'"
    return final_prompt


async def thanking_for_boost(bot_name: str, before: discord.Member, after: discord.Member, model, channel: discord.TextChannel):
    if before.premium_since is None and after.premium_since is not None:
        print(f"{after.name} has started boosting the server!")
        thank_message = get_thank_prompt_for_boosting_server(bot_name=bot_name, user=after)
        
        response = model.generate_content(f"{thank_message}")
        bot_response = remove_creation_name_prefix(f"{response.text}")
        #Kiểm tra xem bot reponse có nhiều emoji không, nếu nhiều quá thì remove emoji
        if count_emojis_in_text(bot_response) > 4:
            bot_response = remove_emojis_from_text(bot_response)
        await channel.send(f"🎉{after.mention} {bot_response}")
    
    return

def get_thank_prompt_for_boosting_server(bot_name: str, user: discord.Member):
    background = ""
    xung_ho = "**Hãy tự xưng là em cho lễ phép.**\n"
    if bot_name.lower() == "creation 1":
        background = background_creation_1
    else:
        background = background_creation_2
    
    background += shared_background
    background += xung_ho
    thank_message = f"User {user.mention}, với tên hiển thị trong server là {user.display_name} đã cho server một boost, và giúp server phát triển hơn. Hãy cảm ơn họ thật nồng nhiệt vì đã giúp đỡ server!"
    final_prompt = f"{initial_instruction} {background} **{thank_message}**"
    return final_prompt
    


def count_words(input_string: str) -> int:
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    cleaned_string = input_string.translate(translator)
    # Split the cleaned string into words
    words = cleaned_string.split()
    # Return the number of words
    return len(words)

def save_user_convo_data(message: discord.Message, bot_reponse: str, bot_name: str):
    #Nếu user nói nhiều hơn 50 ký tự thì không lưu
    if count_words(message.content) > 50:
        return
    #Kiểm tra và tạo mới user convo info nếu không có user_id trong db
    bot_name = bot_name.replace(" ", "_").lower()
    user_convo_data = db.find_user_convo_info_by_id(message.author.id, bot_name)
    if user_convo_data == None:
        conversation = db.ConversationInfo(user_message_id = message.id, user_message_content = message.content, bot_message_content = bot_reponse)
        list_temp = []
        list_temp.append(conversation)
        data = db.UserConversationInfo(user_id=message.author.id, user_name= message.author.name, last_time_interaction=datetime.now(), past_conversation=list_temp)
        result = db.create_user_convo_info(data, bot_name)
        print(f"Creating new user conversation info. Result: {result}")
    else:
        #Kiểm tra những tin nhắn cũ xem tin nhắn mới có bị trùng không
        #Nếu có câu trả lời cũ của bot mà có 10 từ trùng với câu trả lời mới của bot thì bot có khả năng cao sẽ tự lặp lại bản thân -> huỷ lưu tin nhắn mới
        for existed_convo in user_convo_data.past_conversation:
            if compare_strings_intersected_words(bot_reponse, existed_convo.bot_message_content):
                print(f"Abort updating new ConversationInfo, high chance of bot {bot_name} repeating itself.\nNew bot response: '{bot_reponse}' ")
                #Để an toàn thì xoá luôn toàn bộ hội thoại về user này
                db.delete_user_convo_info(user_id=message.author.id, bot_name= bot_name)
                print(f"Deleted ConversationInfo for user name {message.author.name} for bot {bot_name}")
                return
        conversation = db.ConversationInfo(user_message_id = message.id, user_message_content = message.content, bot_message_content = bot_reponse)
        result= db.update_or_insert_conversation_info(user_id=message.author.id, conversation= conversation, bot_name=bot_name)
        print(f"Updating user conversation info. Result: {result}")
    return

def compare_strings_intersected_words(str1: str, str2: str):
    str1 = str1.translate(str.maketrans('', '', string.punctuation))
    str2 = str2.translate(str.maketrans('', '', string.punctuation))
    str1 = str1.lower()
    str2 = str2.lower()
    words1 = str1.split()
    words2 = str2.split()
    set1 = set(words1)
    set2 = set(words2)
    # Nếu str1 tương đồng str 2 tận hơn 60% thì trả về true
    common_words = set1.intersection(set2)
    smaller_set_size = min(len(set1), len(set2))
    percentage_common = (len(common_words) / smaller_set_size) * 100 if smaller_set_size > 0 else 0
    return percentage_common > 60

async def replace_mentions_with_names(message: discord.Message):
    content = message.content
    # Regex patterns to find mentions
    user_pattern = r'<@!?(\d+)>'
    channel_pattern = r'<#(\d+)>'
    role_pattern = r'<@&(\d+)>'
    # Replace user mentions
    for match in re.finditer(user_pattern, content):
        user_id = int(match.group(1))
        user = await message.guild.fetch_member(user_id)  # Fetch the user
        if user:
            content = content.replace(match.group(0), user.display_name)
    # Replace channel mentions
    for match in re.finditer(channel_pattern, content):
        channel_id = int(match.group(1))
        channel = message.guild.get_channel(channel_id)  # Get the channel
        if channel:
            content = content.replace(match.group(0), f'channel #{channel.name}')
    # Replace role mentions
    for match in re.finditer(role_pattern, content):
        role_id = int(match.group(1))
        role = message.guild.get_role(role_id)  # Get the role
        if role:
            content = content.replace(match.group(0), f'Role @{role.name}')

    return content


def count_emojis_in_text(text):
    # Find all emojis in the text
    emojis_found = emoji_pattern.findall(text)
    # Return the count of emojis
    return len(emojis_found)

def remove_emojis_from_text(text):
    return emoji_pattern.sub(r'', text)

def remove_creation_name_prefix(text: str):
    if text.startswith("Creation 1:") or text.startswith("creation 1:"):
        text = text[len("Creation 1:"):].strip()
    if text.startswith("Creation 2:") or text.startswith("creation 2:"):
        text = text[len("Creation 2:"):].strip()
    return text


async def get_attachment_file_from_url(url, content_type):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                if resp.status == 200:
                    data = await resp.read()
                    extension = 'png'
                    if content_type:
                        extension = content_type.split('/')[-1]
                    if extension == None: return
                    #tạo random tên
                    characters = string.ascii_letters
                    unique_id = ''.join(random.choices(characters, k=10))
                    if extension == 'quicktime': extension = 'mp4'
                    file = discord.File(io.BytesIO(data), filename=f"{unique_id}.{extension}")
                    return file
                return None
            except Exception as e:
                return None

async def download_image_file_from_url(url,content_type, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                if resp.status == 200:
                    data = await resp.read()
                    extension = 'png'
                    if content_type:
                        extension = content_type.split('/')[-1]
                    if extension == None: return
                    if os.path.exists(os.path.join(os.path.dirname(__file__),"temp")) == False:
                        os.makedirs(os.path.join(os.path.dirname(__file__),"temp"), exist_ok=True)
                    with open(os.path.join(os.path.dirname(__file__),"temp", filename), 'wb') as f:
                        f.write(await resp.read())
                    return os.path.join(os.path.dirname(__file__),"temp", filename)
                return None
            except Exception as e:
                return None

def check_if_dev_mode():
    #Nếu có file thì là đang trên dev
    filepath = os.path.join(os.path.dirname(__file__), "dev.json")
    return os.path.exists(filepath)

def get_english_dict()->dict:
    filepath = os.path.join(os.path.dirname(__file__),"db","json", "english_dictionary.json")
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data
    return None

def get_vietnamese_dict()->dict:
    filepath = os.path.join(os.path.dirname(__file__),"db", "json", "vietnamese_dictionary.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
    return None

def is_inside_working_time():
    # Không cho hoạt động khi nằm ngoài khung giờ này
    start_time = dt_time(0, 0)   # 00:00 AM
    end_time = dt_time(8, 0)     # 08:00 AM
    current_datetime = datetime.now()
    
    return not (start_time <= current_datetime.time() <= end_time)
    # return 0 <= current_hour <= 8

def get_congrat_humilate_gif(is_congrat: bool):
        if is_congrat:
            type = "congrat"
        else:
            type = "humiliate"
        filepath = os.path.join(os.path.dirname(__file__),"Responses", "RockPaperScissor",type)
        files = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]
        random_file = random.choice(files)
        file_path = os.path.join(filepath, random_file)
        file = discord.File(file_path, filename=random_file)
        return file
    


#region MessagePlayerTracker
class MessageTracker:
    def __init__(self, message_count_threshold=7, time_window_minutes=2):
        self.message_count_threshold = message_count_threshold
        self.time_window = timedelta(minutes=time_window_minutes)
        self.user_messages = defaultdict(list)
    
    def add_message(self, user_id: int, channel_id: int, content: str):
        now = datetime.now()
        # Xoá message cũ
        if (user_id, channel_id) in self.user_messages:
            self.user_messages[(user_id, channel_id)] = [
                (msg, timestamp) for msg, timestamp in self.user_messages[(user_id, channel_id)]
                if now - timestamp <= self.time_window
            ]
        # Thêm message mới vào để check
        self.user_messages[(user_id, channel_id)].append((content, now))
        # Kiểm xem message hiện tại có phải là spam không
        message_count = sum(1 for msg, _ in self.user_messages[(user_id, channel_id)] if msg == content)
        return message_count >= self.message_count_threshold
    
    def clear_user_messages(self, user_id, channel_id):
        """Xoá hết messages đã lưu của user_id nhất định trong channel nhất định."""
        try:
            if (user_id, channel_id) in self.user_messages:
                del self.user_messages[(user_id, channel_id)]
                return True
            return False
        except Exception as e:
            print(f"Error while clearing messages for user {user_id} in channel {channel_id}: {str(e)}")
            return False

def count_lines_truth_dare(is_truth: bool = False):
    file_path = os.path.join(os.path.dirname(__file__),"Responses", "OnDareChallenge.txt")
    if is_truth:
        file_path = os.path.join(os.path.dirname(__file__),"Responses", "OnTruthChallenge.txt")
    with open(file_path, 'r', encoding='utf-8') as f:
        line_count = 0
        for line in f:
            line_count += 1
    return line_count

def get_random_truth_dare(is_truth: bool = False, excluded_index: Optional[List['int']] = None):
    file_path = os.path.join(os.path.dirname(__file__),"Responses", "OnDareChallenge.txt")
    if is_truth:
        file_path = os.path.join(os.path.dirname(__file__),"Responses", "OnTruthChallenge.txt")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if excluded_index is not None:
                available_lines = [(idx, line) for idx, line in enumerate(lines) if idx not in excluded_index]
            else:
                available_lines = [(idx, line) for idx, line in enumerate(lines)]
            if available_lines:
                selected_idx, selected_line = random.choice(available_lines)
                return selected_idx, selected_line.strip()
            return None, None
    except FileNotFoundError:
        return None, None

def find_in_channels(input: int):
    value = hai10_server_channels_steal.get(input)
    if value:
        return input, value
    return None, None

truth_count = count_lines_truth_dare(True)
dare_count = count_lines_truth_dare(False)

english_dict = get_english_dict()
vietnamese_dict = get_vietnamese_dict()

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# Regex pattern to match all emoji characters
emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u200d"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\u3030"
        "\ufe0f"
        "]+",
        flags=re.UNICODE,)

hai10_server_channels_steal = {
    1281163648672337951:1270770520002138112,    #NTR
    1281155620782735461:1259236604510212126,#Asian vid
    1281155597718257664:1259236555575263273,#Asian pic
    1281162745600937994:1259236782466269255,#West pic
    1281163249127002152:1259236604510212126,#Tiktok -> Asian vid
    1281162942200545380:1259236667835945061,#VN p
    1281162959850176574:1259236719287472263,#VN v
    1281163276008292352:1284834396419002469,#Cosplay
    1281163587011739710:1259237706387689574,#Cosplay
    1281155308684574723:1259233868628885667,#Game video
    1281155289625923676:1259228154275434629,#Game pic ->2tai pic
    1281154949077798912:1259228154275434629,#2tai pic
    1281155099590135878:1259233868628885667,#2tai vid
    1281155158922760273:1259234080810205315,#anime pic
    1281155174253199444:1259234158576664697,#anime vi
}