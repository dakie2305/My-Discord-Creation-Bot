import datetime
import discord
from discord.ext import commands
import PIL
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from CustomEnum.UserEnum import UserId
import db.DbMongoManager as db
import CustomFunctions
import os
import google.generativeai as genai
import PIL.Image
import asyncio
from collections import deque

class AIResponseHandling():
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot_name = "Creation 2" if bot.user.id == UserId.CREATION_2.value else "Creation 1"
        self.bot_to_bot_history = deque()

    async def sub_function_ai_response(self, message: discord.Message, speakFlag: bool = True):
        if speakFlag == False: return
        await self.generate_ai_response(message)
        
    async def generate_ai_response(self, message: discord.Message):
        bots_creation_2_name = ["creation 2", "creation số 2", "creation no 2", "creatiom 2", "creation no. 2"]
        bots_creation_1_name = ["creation 1", "creation số 1", "creation no 1", "creation no. 1"]
        
        if message.author.id in [UserId.CREATION_1.value, UserId.CREATION_2.value] and message.author.id != self.bot.user.id:
            now = datetime.datetime.now()
            # Clean up old timestamps
            self.bot_to_bot_history = deque(ts for ts in self.bot_to_bot_history if now - ts < datetime.timedelta(minutes=5))
            
            self.bot_to_bot_history.append(now)

            if len(self.bot_to_bot_history) >= 5:
                print(f"Too many bot-to-bot messages in 5 mins. Skipping.")
                return

        
        bots_creation_name = bots_creation_2_name if self.bot.user.id == UserId.CREATION_2.value else bots_creation_1_name
        is_reply_message = False
        referenced_message = None
        if message.reference is not None and message.reference.resolved is not None:
            if message.reference.resolved.author == self.bot.user or CustomFunctions.contains_substring(message.content.lower(), bots_creation_name):
                referenced_message = await message.channel.fetch_message(message.reference.message_id)
                if referenced_message.embeds: return
                #pass hết thì check xem có message nsfw không thì mới cho phép bot trả
                is_reply_message = True
            else: return
        elif CustomFunctions.contains_substring(message.content.lower(), bots_creation_name):
            if message.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value and message.guild.id != 1194106864582004849: #Chỉ True Heaven, Học Viện 2ten mới không bị dính
                if CustomFunctions.is_inside_working_time() == False:
                    await message.channel.send(f"Tính năng AI của Bot chỉ hoạt động đến 12h đêm, vui lòng đợi đến 8h sáng hôm sau.")
                    return
            elif message.guild.id == 1194106864582004849 and message.channel.id != 1264455905756446740: #Học viện 2ten/ channel #sân-chơi-creation-2
                return
            is_reply_message = False
        #Không trong trường hợp trên thì tắt
        else: return
        
        if message.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value and message.guild.id != 1194106864582004849: #Chỉ True Heaven, Học Viện 2ten mới không bị dính
            if CustomFunctions.is_inside_working_time() == False:
                await message.channel.send(f"Tính năng AI của Bot chỉ hoạt động đến 12h đêm, vui lòng đợi đến 8h sáng hôm sau.")
                return
        
        flag, mess = await CustomFunctions.check_message_nsfw(message, self.bot)
        if flag != 0:
            await message.reply(mess)
            print(f"Username {message.author.name}, Display user name {message.author.display_name} violated chat when talking to {self.bot.user}")
            return
        #pass hết, cho phép bot trả lời
        try:
            async with message.channel.typing():
                await asyncio.sleep(4)  # Delay
                system_instruction = ""
                if self.bot_name == "Creation 1":
                    system_instruction = f"{CustomFunctions.initial_instruction} {CustomFunctions.background_creation_1} {CustomFunctions.shared_background}"
                else:
                    system_instruction = f"{CustomFunctions.initial_instruction} {CustomFunctions.background_creation_2} {CustomFunctions.shared_background}"
                model = genai.GenerativeModel(model_name=CustomFunctions.AI_MODEL, safety_settings= CustomFunctions.safety_settings, system_instruction=system_instruction)
                prompt = await CustomFunctions.get_proper_prompt(message, self.bot_name, referenced_message)
                print(f"Prompt generated from {self.bot.user}:\n {prompt}")
                file_image_path = None
                if len(message.attachments)>0:
                    #Lấy ảnh đầu tiên thôi
                    for att in message.attachments:
                        if 'image' in att.content_type:
                            file_image_path = await CustomFunctions.download_image_file_from_url(url=att.url, content_type=att.content_type,filename= att.filename)
                            break
                if file_image_path!= None:
                    response = model.generate_content([f"{prompt}", PIL.Image.open(file_image_path)])
                    #Xoá file
                    os.remove(file_image_path)
                else:
                    response = model.generate_content(f"{prompt}")
                bot_response = CustomFunctions.remove_creation_name_prefix(f"{response.text}")

                #Kiểm tra xem bot reponse có nhiều emoji không, nếu nhiều quá thì remove emoji
                if CustomFunctions.count_emojis_in_text(bot_response) > 4:
                    bot_response = CustomFunctions.remove_emojis_from_text(bot_response)
                
                #Nếu có chữ record thì tạo file và gửi ghi âm
                if 'record' in message.content.lower():
                    await CustomFunctions.bot_sending_sound(bot_name='Creation_2', bot_reponse=bot_response, message=message)
                    print(f"Username {message.author.name}, Display user name {message.author.display_name} tell {self.bot.user} to send record")
                    return
                
                #Nếu là bot thì đương nhiên không reply, chỉ nhắn bình thường thôi
                if(message.author.id == CustomFunctions.user_cr_1["user_id"] or message.author.id == CustomFunctions.user_cr_2["user_id"] or message.author.id == CustomFunctions.user_cr_3["user_id"]):
                    await message.channel.send(f"{message.author.mention} {bot_response}")
                else:
                    #Nếu là reply message thì reply, không thì send
                    if is_reply_message == True:
                        await message.reply(f"{bot_response}")
                    else:
                        await message.channel.send(f"{message.author.mention} {bot_response}")
                CustomFunctions.save_user_convo_data(message=message, bot_reponse= bot_response, bot_name= self.bot_name)
                print(f"Username {message.author.name}, Display user name {message.author.display_name} replied {self.bot.user}")
                return
        except Exception as e:
            print(f"Username {message.author.name}, Display user name {message.author.display_name} replied {self.bot.user} but with error: {e}")
        return