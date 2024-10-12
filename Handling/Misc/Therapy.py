import discord
from discord.ext import commands
import PIL
import db.DbMongoManager as db
import CustomFunctions
import os
import google.generativeai as genai


class TherapyHandling():
    def __init__(self, bot: commands.Bot, model: genai.GenerativeModel):
        self.bot = bot
        self.model = model

    async def handling_therapy_ai(self, message: discord.Message):
        if message.guild.id != 1256987900277690470 and message.guild.id != 1194106864582004849: #Chỉ True Heaven, học viện 2ten mới không bị dính
            if CustomFunctions.is_inside_working_time() == False:
                await message.channel.send(f"Tính năng AI của Bot chỉ hoạt động đến 12h đêm, vui lòng đợi đến 8h sáng hôm sau.")
                return
        flag, mess = await CustomFunctions.check_message_nsfw(message, self.bot)
        if flag != 0:
            await message.reply(mess)
            return
        bots_creation1_name = ["creation 1", "creation số 1", "creation no 1", "creation no. 1"]
        ref_message: discord.Message = None
        async with message.channel.typing():
            if message.reference is not None and message.reference.resolved is not None:
                if message.reference.resolved.author == self.bot.user or CustomFunctions.contains_substring(message.content.lower(), bots_creation1_name):
                    ref_message = await message.channel.fetch_message(message.reference.message_id)
            #Lấy prompt
            prompt = await CustomFunctions.get_therapy_prompt(message=message, extra_message=ref_message)
            print(prompt)
            file_image_path = None
            if len(message.attachments)>0:
                #Lấy ảnh đầu tiên thôi
                for att in message.attachments:
                    if 'image' in att.content_type:
                        file_image_path = await CustomFunctions.download_image_file_from_url(url=att.url, content_type=att.content_type,filename= att.filename)
                        break
            if file_image_path!= None:
                response = self.model.generate_content([f"{prompt}", PIL.Image.open(file_image_path)])
                #Xoá file
                os.remove(file_image_path)
            else:
                response = self.model.generate_content(f"{prompt}")
            bot_response = (f"{response.text}")
            #Kiểm tra xem bot reponse có nhiều emoji không, nếu nhiều quá thì remove emoji
            if CustomFunctions.count_emojis_in_text(bot_response) > 4:
                bot_response = CustomFunctions.remove_emojis_from_text(bot_response)    
            await message.channel.send(f"{message.author.mention} {bot_response}")
        return
