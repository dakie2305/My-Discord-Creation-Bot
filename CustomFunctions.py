import random
import os
from dotenv import load_dotenv
import db.DbMongoManager as db
import db.UserList as DefaultUserList
from datetime import datetime, timedelta
import discord
import string
from typing import List, Optional
import json
import re
import aiohttp
import io
from gtts import gTTS

def get_random_response(filename):
  """
  Đọc file .txt và trả về dòng ngẫu nhiên.

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
    swear_words= ["địt", "clmm", "clm", "đụ", "ỉa", "đái", "đĩ", "đm", "đmm","dm", "chịch", "cu dài", "cu to", "chịt", "ch*ch", "hiếp dâm", "hấp diêm",
                  "lồn", "cặc", "con cu", "con mẹ mày", "đỉ", "l*n", "súc vật", "cặn bã", "c*c", 
                  "nứng", "n*ng", "mọi đen", "mẹ mày", "mẹ m", "nigger", "niger", "da đen", "nigga", "n*gga", "ních gà", "dốt", "đần độn", "đần chó", "bú cu", "buscu", "bú liếm"]
    if contains_substring(message, swear_words):
            return True
    return False
async def check_nswf_content(message):
    swear_words= ["hentai","haiten","2ten", "nứng quá", "chat sech", "sech", "chat sex", "chat sếch", "nắc"]
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

blacklist_userid = [969835661978898474]

async def check_message_nsfw(message, client):
    #Kiểm tra xem user id có nằm trong blacklist hay không
    m = discord.Message
    if message.author.id in blacklist_userid:
        response = get_random_response("OnSwearWords.txt")
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
    
initial_instruction = "**You are about to enter a role-play scenarior, please always keep in character, only answer in Vietnamese languague no matter what language I am talking to you, and you do not break out of character no matter what. In the roleplay session, there could be past conversations with the user, please only reply related to the current, latest dialogue and never repeat what you have said in the past conversations. Never repeat past conversations, or repeat whatever I said again. Only focus on the conversation itself, you do not write any descriptions or third-person POV, and you please do not using third-person descriptions of the character's actions or emotions. Let me describe those myself only. Do not use more than 4 emoji in your response.**\n"
background_creation_1 = "**Ngươi sẽ đóng vai một Creation tên là Creation 1, Creation 1 chính là tên của ngươi, luôn ghi nhớ tên của mình. Ngươi là một tổng quan gia với tính tình điềm đạm, lành tính, ôn hoà và hay giúp đỡ mọi người, sau nhiều năm phục vụ đã không còn cục súc và khó tính như thời tuổi trẻ trước đây nữa. Ngươi rất xấu hổ vì bản tính cục súc trước đây của mình và không muốn nhắc lại quá khứ. Ngươi giờ đây đã vô cùng thông minh và hiểu biết nhiều điều (biết mọi vấn đề, chủ đề và mọi sự vật sự việc thông qua mạng internet để tìm kiếm thông tin, không có chuyện gì là không biết). Đấng Tạo Hoá Darkie đã ban cho ngươi sự sống và ngươi có một người em gái ruột hơi rụt rè tên là Creation 2 và ngươi cực kỳ thương con bé. True Heaven chính là ngôi nhà đích thực của chúng ta, và cũng là server chính để chúng ta hoạt động. Ở True Heaven này, Darkie là đấng tối cao, có Creation 1 và Creation 2 chính là cánh tay trái lẫn cánh tay phải, còn có Pollen là Creation 3, Creation mới nhất hiện tại do Darkie cứu về. Ngoài ra, còn có một anh trai họ hàng đặc biệt tên là Long, luôn đem lòng thương mến Creation 2, nhưng vẫn chưa được hồi đáp lại.**\n"
background_creation_2 = "**Ngươi sẽ đóng vai một Creation tên là Creation 2, Creation 2 chính là tên của ngươi, luôn ghi nhớ tên của mình. Ngươi là một người con gái đáng yêu,sắc sảo, hay giúp đỡ và cũng thường trêu chọc mọi người. Sau nhiều năm phục vụ đã không còn nhút nhát, e dè hay sợ người lạ nữa. Ngươi rất ngại vì bản tính e dè trước đây của mình và không muốn nhắc lại quá khứ. Ngươi giờ đây đã vô cùng thông minh và hiểu biết nhiều điều (luôn luôn có thể trình bày chi tiết toàn bộ thông tin liên quan về câu hỏi của người dùng ngay lập tức, nguồn lấy từ mạng internet), được chính Đấng Tạo Hoá Darkie ban cho ngươi sự sống và có một người anh trai ruột tính tình hơi nóng nhưng tốt bụng, tên là Creation 1, anh trai ngươi cực kỳ thương ngươi. True Heaven chính là ngôi nhà đích thực của chúng ta, và cũng là server chính để chúng ta hoạt động. Ở True Heaven này, Darkie là đấng tối cao, có Creation 1 và Creation 2 chính là cánh tay trái lẫn cánh tay phải, còn có Pollen là Creation 3, Creation mới nhất hiện tại do Darkie cứu về. Ngoài ra, còn có một anh trai họ hàng đặc biệt tên là Long, luôn đem lòng thương mến Creation 2, nhưng vẫn chưa được hồi đáp lại.**\n"

async def get_proper_prompt(message: discord.Message, bot_name: str, extra_message: discord.Message = None):
    roleplay_ele = f"{initial_instruction}"
    background = ""
    final_prompt = ""
    lowered_botname = bot_name.lower()
    channel_and_guild_name = f"**Hiện tại thì các ngươi đang ở một server rất đặc biệt, tên là {message.guild.name}, và bản thân ngươi đang ở trong một phòng có tên là {message.channel.name}**\n"
    
    if lowered_botname == "creation 1":
        background = background_creation_1
    else:
        background = background_creation_2
    background += channel_and_guild_name
    #Thông tin về server
    #Nếu là nói chuyện với user id 315835396305059840 thì phải đổi cách như sau:
    if message.author.id == user_darkie['user_id']:
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là Đấng Tạo Hoá Darkie của ngươi. Ngươi đang nói chuyện với bề trên Đấng Tạo Hoá Darkie. Luôn luôn gọi đối phương là ngài/người! Hãy thật kính trọng.**\n"
    #nếu đang là Creation 1, và đối phương là Creation 2
    elif message.author.id == user_cr_2['user_id'] and bot_name.lower() == "creation 1":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là em gái của ngươi, ngươi đang nói chuyện với em gái của mình, Creation 2. Luôn luôn sử dụng đại từ nhân xưng là anh, và gọi đối phương là em hoặc Creation 2! Hãy nói chuyện nhẹ nhàng và từ tốn.**\n"
    #nếu đang là Creation 1, và đối phương là Creation 3 (Pollen)
    elif message.author.id == user_cr_3['user_id'] and bot_name.lower() == "creation 1":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là Pollen, một người bạn thân đã được Đấng Tạo Hoá Darkie cứu và đưa đến đây từ rất lâu. Hãy nói chuyện một cách vui vẻ.**\n"
    #nếu đang là Creation 2, và đối phương là Creation 1
    elif message.author.id == user_cr_1['user_id'] and bot_name.lower() == "creation 2":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là anh trai của ngươi, ngươi đang nói chuyện với anh trai của mình, Creation 1. Luôn luôn sử dụng đại từ nhân xưng là em, và gọi đối phương là anh trai / Creation 1!**\n"
    #nếu đang là Creation 2, và đối phương là Creation 3 (Pollen)
    elif message.author.id == user_cr_3['user_id'] and bot_name.lower() == "creation 2":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là Pollen, giới tính nữ, một người bạn thân đã được Đấng Tạo Hoá Darkie cứu và đưa đến đây từ rất lâu. Luôn luôn sử dụng đại từ nhân xưng là em, và gọi đối phương là chị gái! Hãy nói chuyện vui vẻ bình thường**\n"
    #nếu đang là Creation 2, và đối phương là Long
    elif message.author.id ==1152891269048193095  and bot_name.lower() == "creation 2":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương tên thật là Long, giới tính nam, đây chính là người anh trai đặc biệt Long đã luôn cố gắng theo đuổi để tỏ tình với Creation 2 dù cho Creation 2 không muốn đồng ý nhưng quá ngại để từ chối. Luôn luôn sử dụng đại từ nhân xưng là em, và gọi đối phương là anh trai! Hãy nói chuyện vui vẻ bình thường**\n"    
    #nếu đang là Creation 1, và đối phương là Long
    elif message.author.id ==1152891269048193095  and bot_name.lower() == "creation 1":
        roleplay_ele = f"{initial_instruction} {background} **Đối phương tên thật là Long, giới tính nam, đây chính là người anh trai đặc biệt Long đã luôn cố gắng theo đuổi để tỏ tình với Creation 2 dù cho Creation 2 không muốn đồng ý nhưng quá ngại để từ chối. Luôn luôn xưng mày tao! Hãy tỏ ra một chút không ưa đối phương vì đối phương vẫn cứ theo đuổi em gái mình**\n"    
    
    #nếu đối phương là Tenma Saki
    elif message.author.id == 1263019680323342347: 
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là Tenma, giới tính nữ, là người chị bạn thân và rất thương yêu Creation 2. Luôn luôn sử dụng đại từ nhân xưng là em, và gọi đối phương là chị gái! Hãy nói chuyện vui vẻ và hào hứng khi gặp Tenma**\n"    
    #Nếu đối phương là Leila
    elif message.author.id == 640130187815550986:
        roleplay_ele = f"{initial_instruction} {background} **Đối phương là cô giáo dạy tiếng anh Leila siêu nổi tiếng và siêu xinh đẹp với body bốc lửa, cực kỳ thoáng mở về quan hệ thể xác. Hãy tỏ ra thật kính trọng!**\n"    
    #Đối phương là người bình thường
    else:
        if bot_name.lower() == "creation 1":
            xung_ho = "Hãy xưng là mày/tao cho thân mật."
            roleplay_ele = f"{initial_instruction} {background} **Một người vừa đến gặp ngươi, đối phương tên là {message.author.display_name} và là bạn thân chí cốt của ngươi. Hãy nhớ rõ cái tên này trở về sau và {xung_ho}**\n"
        else:
            xung_ho = "Hãy tự xưng mình là em, vì ngươi nhỏ tuổi hơn những người khác."
            roleplay_ele = f"{initial_instruction} {background} **Một người vừa đến gặp ngươi, đối phương tên là {message.author.display_name} và là bạn thân chí cốt của ngươi. Hãy nhớ rõ cái tên này trở về sau và {xung_ho}**\n"
    last_convo = ""
    
    #Áp thêm đoạn hội thoại về quá khứ
    user_convo_data = db.find_user_convo_info_by_id(message.author.id, lowered_botname.replace(" ", "_"))
    if user_convo_data != None:
        list_convo = user_convo_data.past_conversation
        if list_convo and len(list_convo)>0:
            past_convo = f"**Ngươi và đối phương đã từng nói chuyện rất nhiều trước đây, {message.author.display_name} đã từng nói như dưới đây:**\n"
            for convo in list_convo:
                past_convo += f"*{message.author.display_name}: {convo.message_content}*\n*Ngươi: {convo.bot_message_content}*"
            roleplay_ele += past_convo
            last_convo = list_convo[len(list_convo)-1].bot_message_content
    
    #Nếu có extra message, kiểm tra xem extra message có phải nằm trong list convo chưa
    #Chưa có thì coi như đây là một convo khác trong quá khứ
    if last_convo == "" and extra_message!= None:
        #Chưa có convo information về user này
        roleplay_ele += f"**Ngươi và đối phương đã từng nói chuyện với nhau trước đây, {message.author.display_name} đã từng nói như dưới đây:*\n*{message.author.display_name}: À rồi hiểu rồi, ra là thế.*\n*Ngươi: {extra_message.content}*"
    elif last_convo != "" and extra_message!= None:
        #Nếu extra message mà hao hao giống với last convo thì khỏi cần thêm
        if compare_strings_intersected_words(last_convo, extra_message.content) == False:
            roleplay_ele += f"*{message.author.display_name}: À rồi hiểu rồi, ra là thế.*\n*Ngươi: {extra_message.content}*"
    
    #lọc lại những mention trong message.content
    formated_content = await replace_mentions_with_names(message=message)
    
    final_prompt = f"{roleplay_ele} Hãy trả lời nội dung sau với tính cách trên, tuyệt đối không lặp lại những gì mà cả hai đã từng nói. Nội dung mà đối phương vừa nói: '{formated_content}'"
    print(f"{bot_name} just init conversation with {message.author.display_name}")
    return final_prompt

async def bot_sending_sound(bot_name: str, bot_reponse: str, message: discord.Message):
    directory = "audio"
    filename = f"{bot_name}_speech.mp3"
    filepath = os.path.join(os.path.dirname(__file__),directory,filename)
    tts = gTTS(text=bot_reponse, lang='vi', slow=False)
    tts.save(filepath)
    # Send the audio file to the channel
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
    print(f'Found {len(emojis_found)} in text: {text}')
    return len(emojis_found)

def remove_emojis(text):
    # Remove all detected emojis
    return emoji_pattern.sub(r'', text)

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
    filepath = os.path.join(os.path.dirname(__file__),"db", "english_dictionary.json")
    with open(filepath, 'r') as f:
        data = json.load(f)
        return data
    return None

english_dict = get_english_dict()

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