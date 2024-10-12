import PIL.Image
import discord
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import CustomFunctions
import db.Class.UserList as DefaultUserList
import google.generativeai as genai
import time
import DailyLogger
from discord.ext import commands, tasks
from discord import app_commands
import db.DbMongoManager as db
from db.DbMongoManager import UserInfo, GuildExtraInfo, SnipeChannelInfo, ConversationInfo, SnipeMessage, SnipeMessageAttachments
import random
import string
import CustomButton
from typing import Optional
from collections import deque
import requests
import PIL
import asyncio

load_dotenv()
intents = discord.Intents.all()
API_KEY = os.getenv("GOOGLE_CLOUD_KEY_2")
genai.configure(api_key=API_KEY)

interaction_logger = DailyLogger.get_logger("Creation2_Interaction")
commands_logger = DailyLogger.get_logger("Creation2_Commands")

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')
#region Bot Prefix Commands
@bot.command()
async def ping(ctx):
    await ctx.send(f"Online at {ctx.guild}")
    commands_logger.info("Someone use ping!")

@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def synccre2(ctx):
    if(ctx.author.id == CustomFunctions.user_darkie['user_id']):
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send(f"Đã đồng bộ thêm {len(fmt)} các slash commands vào Server {ctx.guild}")
    else:
        await ctx.send(f"Có phải là Darkie đâu mà dùng lệnh này?")

@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def global_sync_creation_2(ctx):
    if(ctx.author.id == CustomFunctions.user_darkie['user_id']):
        fmt = await bot.tree.sync()
        await ctx.send(f"Đã đồng bộ hết {len(fmt)} slash commands của Creation 2 vào toàn bộ server hiện hành!")
    else:
        await ctx.send(f"Có phải là Darkie đâu mà dùng lệnh này?")        
        
@bot.command()
async def guild_extra_info(ctx):
    #Kiểm tra xem guild này đã có trong db extra info chưa
    check_exist = db.find_guild_extra_info_by_id(int(ctx.guild.id))
    if check_exist:
        await ctx.send(f"Đã tồn tại thông tin Guild Extra Info về server này.")
    else:
        data = GuildExtraInfo(guild_id=ctx.guild.id, guild_name= ctx.guild.name, allowed_ai_bot=False)
        db.insert_guild_extra_info(data)
        await ctx.send(f"Lưu thành công thông tin Guild Extra Info về server này.", ephemeral=True)

@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def help(ctx):
    message: discord.Message = ctx.message
    if message:
        await help_command(message= message)    


#endregion


#region say command
@bot.tree.command(name = "say", description="Nói gì đó ẩn danh thông qua bot, có thể gắn hình ảnh và nhắn vào Channel khác", guild=discord.Object(id=1194106864582004849)) #Học viện 2ten
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def say(interaction: discord.Interaction, thing_to_say : str, image: Optional[discord.Attachment] = None, chosen_channel: Optional[discord.TextChannel]= None):
    await interaction.response.send_message(content="Đã gửi tin nhắn ẩn danh thành công", ephemeral=True)
    #Lấy channel mà người dùng gọi ra
    current_channel_id = interaction.channel_id
    current_channel = bot.get_channel(current_channel_id)
    if chosen_channel != None:
        current_channel = bot.get_channel(chosen_channel.id)

    #Lấy user-id lật ngược lại
    reversed_id = CustomFunctions.reverse_string_loop(str(interaction.user.id))
    
    #tạo random id
    characters = string.ascii_letters
    unique_id = ''.join(random.choices(characters, k=5))
    first = random.randint(0, 9)
    second = random.randint(0, 9)
    # Create embed object
    embed = discord.Embed(title=f"Ẩn danh ({unique_id})", color=0xC3A757)  # Yellowish color
    embed.add_field(name="______________", value= "", inline=False)  # Single-line field
    embed.add_field(name=f"'{thing_to_say}'", value= "", inline=False)
    if image != None:
        embed.set_image(url= image.url)
    embed.set_footer(text= f"Anon: {first}{reversed_id}{second}")  # Single-line field
    # await interaction.followup.send(content= "Đã gửi tin nhắn ẩn danh thành công.", ephemeral= True)
    await current_channel.send(embed= embed)
    commands_logger.info(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} used /say to say: {thing_to_say}")
#endregion

#region report command
@bot.tree.command(name="report", description="Báo cáo user vi phạm luật về cho admin và moderator xem xét.", guild=discord.Object(id=1194106864582004849))#Học viện 2ten
@app_commands.describe(user="Chọn user đã phạm luật để báo cáo", reason="Lý do tại sao báo cáo", message_id= "Chuột phải vào message muốn xoá, vào bấm Copy Id rồi dán vào đây", image = "Chọn hình làm bằng chứng (sẽ xử lý nhanh hơn).")
async def report(interaction: discord.Interaction, user : discord.Member, reason: str, message_id: Optional[str] = None, image: Optional[discord.Attachment] = None):
    await interaction.response.defer(ephemeral=True)
    try:
        await interaction.followup.send(f"Đã thành công gửi báo cáo {user.mention} về cho dàn admin và moderator xem xét với lý do: {reason}.", ephemeral=True)
        channel = bot.get_channel(1264455905756446740) #sân chơi creation 2
        if channel:
            # Create embed object
            embed = discord.Embed(title="Có người gửi báo cáo, admin và moderator vui lòng kiểm tra", description=f"User {interaction.user.mention} đã báo cáo {user.mention} tại <#{interaction.channel.id}>!", color=0xFC0345)
            embed.add_field(name="Lý do báo cáo:", value=reason, inline=False)  # Single-line field
            if message_id!= None:
                mess = await interaction.channel.fetch_message(int(message_id))
                if mess:
                    embed.add_field(name="Nội dung bị báo cáo:", value=mess.content, inline=True)
                    embed.add_field(name="Id Message:", value=f"{mess.jump_url}", inline=True)
            if image != None:
                embed.set_image(url= image.url)
            embed.set_footer(text=f"User ID Invoke: {interaction.user.id}")  # Footer text
            view = CustomButton.CustomReportButtonView() #Gắn nút report
            await channel.send(embed=embed, view= view)
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} report user id: {user.id} with Username {user.name}.")
            commands_logger.info(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} report user id: {user.id} with Username {user.name}.")
        else:
            await interaction.followup.send(f"<@315835396305059840> Bot không tìm được channel để gửi báo cáo!")
    except Exception as e:
        #Tag bản thân
        await interaction.followup.send(f"<@315835396305059840> Bot gặp exception trong lúc thực hiện lệnh. Exception: {str(e)}. Vui lòng liên hệ Darkie!", ephemeral=True)
        commands_logger.info(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried report user id {user.id} but got exception {str(e)}.")
#endregion

#region Snipe command
@bot.tree.command(name="snipe", description="Hiện lại message mới nhất vừa bị xoá trong channel này.", guild=discord.Object(id=1194106864582004849)) #Học viện 2ten
async def snipe(interaction: discord.Interaction):
    await interaction.response.defer()
    called_channel = interaction.channel
    snipe_channel_info = db.find_snipe_channel_info_by_id(called_channel.id, interaction.guild.id)
    if snipe_channel_info:
        list_snipe_message = snipe_channel_info.snipe_messages
        if list_snipe_message == None:
            await interaction.followup.send(f"Chưa thấy bất kỳ message nào bị xoá trong channel {interaction.channel.mention}. Vui lòng thử lại sau.")
            return
        list_snipe_message.reverse()
        temp_files = []
        first_message = list_snipe_message[0]
        if first_message != None and first_message.user_attachments!= None and len(first_message.user_attachments)>0:
            for att in first_message.user_attachments:
                file = await CustomFunctions.get_attachment_file_from_url(url= att.url, content_type= att.content_type)
                if file != None: temp_files.append(file)
        view = CustomButton.PaginationView(bot=bot, interaction=interaction, items= list_snipe_message)
        message  = await interaction.followup.send(embed=view.embed, view=view, files=temp_files)
        view.discord_message = message
        await view.countdown()
    else:
        await interaction.followup.send(f"Chưa có dữ liệu snipe cho channel {interaction.channel.mention}. Vui lòng thử lại sau.")
#endregion

#region Random AI Talk command
@bot.tree.command(name="random_ai_talk", description="Bật/tắt chế độ cho phép bot lâu lâu trò chuyện trong channel này.")
async def random_ai_talk(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral= True)
    if interaction.user.id != 315835396305059840 and interaction.user.id != interaction.guild.owner_id:
        await interaction.followup.send(f"Chỉ chủ Server mới dùng lệnh này.", ephemeral= False)
        return
    called_channel = interaction.channel
    list_channels_ai_talk = []
    check_exist = db.find_guild_extra_info_by_id(interaction.guild.id)
    if check_exist:
        list_channels_ai_talk = check_exist.list_channels_ai_talk
        add = True
        if called_channel.id not in list_channels_ai_talk:
            #thêm
            list_channels_ai_talk.append(called_channel.id)
        else:
            add = False
            list_channels_ai_talk.remove(called_channel.id)
        data_updated = {"list_channels_ai_talk": list_channels_ai_talk}
        db.update_guild_extra_info(guild_id=interaction.guild.id, update_data= data_updated)
        if add:
            await interaction.followup.send(f"Bot lâu lâu sẽ nói chuyện trong channel này.", ephemeral= True)
        else:
            await interaction.followup.send(f"Bot sẽ không còn nói chuyện trong channel này nữa.", ephemeral= True)
    else:
        list_channels_ai_talk.append(called_channel.id)
        data = GuildExtraInfo(guild_id=interaction.guild.id, guild_name= interaction.guild.name, allowed_ai_bot=True, list_channels_ai_talk= list_channels_ai_talk)
        db.insert_guild_extra_info(data)
        await interaction.followup.send(f"Đã tạo Guild Extra Info. Bot lâu lâu sẽ nói chuyện trong channel này.", ephemeral= True)
#endregion

#region Coin flip command
@bot.tree.command(name="cf", description="Tung đồng xu sấp/ngửa cho vui.")
async def cf(interaction: discord.Interaction):
    embed = discord.Embed(title=f"", description=f"{interaction.user.mention} đã tung đồng xu. Đồng xu đang quay <a:doge_coin:1287452452827697276> ...", color=0x03F8FC)
    await interaction.response.send_message(embed=embed)
    mess = await interaction.original_response()
    if mess:
        await edit_embed_coin_flip(message=mess, user=interaction.user)
    return


async def edit_embed_coin_flip(message: discord.Message, user: discord.Member):
    await asyncio.sleep(3)
    choice = random.randint(0,10)
    emoji_state = '<:coin_ngua:1287452465733570684>'
    state = 'ngửa'
    if choice > 0 and choice <=5:
        state = 'sấp'
        emoji_state = '<:coin_sap:1287452474952777750>'
    elif choice == 10:
        #Troll player
        response = CustomFunctions.get_random_response("OnCoinFlip.txt")
        embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã tung đồng xu. {response}", color=0x03F8FC)
        await message.edit(embed=embed_updated)
        return
    embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã tung đồng xu. Đồng xu đã quay ra **`{state}`** {emoji_state}!", color=0x03F8FC)
    await message.edit(embed=embed_updated)
    if choice == 0:
        await asyncio.sleep(2)
        #Troll tập 2
        if state == 'ngửa':
            state = 'sấp'
            emoji_state = '<:coin_sap:1287452474952777750>'
        else:
            state = 'ngửa'
            emoji_state = '<:coin_ngua:1287452465733570684>'
        embed_updated = discord.Embed(title=f"", description=f"Đùa thôi. Đồng xu đã quay ra **`{state}`** {emoji_state}!", color=0x03F8FC)
        await message.edit(embed=embed_updated)
    return
#endregion

#region Help Command
@bot.tree.command(name="help", description="Hiện tất cả commands và hướng dẫn sử dụng bot.")
async def help_command(interaction: discord.Interaction):
    message = interaction.message
    await help_command(message=message)
    return


async def help_command(message: discord.Message):
    #Trả về text hướng dẫn command
    text = """**-= Lệnh của Creations 2 =-**

**Lệnh trong trò chơi Kéo - Búa - Bao:**
`/keo_bua_bao [@user]`: Lệnh dùng để chơi kéo búa bao với người chơi khác. Nếu không chọn người chơi thì sẽ chơi với bot. 
`/bxh_rps [@user] [legendary|humiliate|lose|draw]`: Lệnh dùng để xem xếp hạng Kéo - Búa - Bao. Có thể xem thứ hạng của player khác và xếp hạng theo nhiều mục khác nhau.    

**Lệnh lặt vặt:**
`/random_ai_talk`: Lệnh để bật / tắt khả năng lâu lâu bot nói chuyện xàm xí trong channel.
`/say`: Lệnh dùng để gửi tin nhắn, hình ảnh ần danh.
`/truth_dare`: Lệnh dùng để gửi tạo mới trò chơi Truth Or Dare.
`/snipe`: Lệnh dùng để hiển thị lại 7 tin nhắn bị xoá gần nhất trong channel dùng lệnh.
`/cf`: Lệnh dùng để tạo một tin nhắn tung đồng xu sấp/ngửa.
    """
    await message.reply(content=text)
    
#endregion

# Task: Nói chuyện tự động
@tasks.loop(hours=3)
async def automatic_speak_randomly():
    guilds = bot.guilds
    for guild in guilds:
        print(guild)
        guild_extra_info = db.find_guild_extra_info_by_id(guild.id)
        if guild_extra_info != None and guild_extra_info.list_channels_ai_talk != None and len(guild_extra_info.list_channels_ai_talk)>0:
            random_channel_id = random.choice(guild_extra_info.list_channels_ai_talk)
            actual_channel = guild.get_channel(random_channel_id)
            if actual_channel:
                model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
                prompt = CustomFunctions.get_automatically_talk_prompt("Creation 2", guild, actual_channel)
                response = model.generate_content(f"{prompt}")
                print(f"{bot.user} started talking on its own at {guild_extra_info.guild_name}, channel {actual_channel.name}.")
                async with actual_channel.typing():
                    await actual_channel.send(f"{response.text}")
@tasks.loop(hours=24)
async def remove_old_conversation():
    #Kiểm tra các collections user_conversation_info_creation xem
    #có dữ liệu nào có last interaction cách đây 3 ngày không
    #Nếu có thì xoá luôn
    count = 0
    three_day_before = datetime.now() - timedelta(days=3)
    bot_name = "creation_2"
    list_all_user_convo_info = db.find_all_user_convo_info(bot_name)
    if list_all_user_convo_info:
        for data in list_all_user_convo_info:
            if data.last_time_interaction < three_day_before:
                db.delete_user_convo_info(data.user_id, bot_name)
                count+=1
    print(f"Found {count} old conversation in collection 'user_conversation_info_{bot_name}' and deleted them.")
        

async def sub_function_ai_response(message: discord.Message):
    bots_creation_name = ["creation 2", "creation số 2", "creation no 2", "creatiom 2", "creation no. 2"]
    coin_flip = ["tung đồng xu", "sấp ngửa", "sấp hay ngửa", "ngửa hay sấp", "ngửa sấp", "tung xu"]
    if CustomFunctions.contains_substring(message.content.lower(),coin_flip):
                #Tung đồng xu
                embed = discord.Embed(title=f"", description=f"{message.author.mention} đã tung đồng xu. Đồng xu đang quay <a:doge_coin:1287452452827697276> ...", color=0x03F8FC)
                mess_coin = await message.reply(embed=embed)
                if mess_coin:
                    await edit_embed_coin_flip(message=mess_coin, user=message.author)
                return
    guild_info = db.find_guild_extra_info_by_id(message.guild.id)
    if message.reference is not None and message.reference.resolved is not None:
        if message.reference.resolved.author == bot.user or CustomFunctions.contains_substring(message.content.lower(), bots_creation_name):
            if message.guild.id != 1256987900277690470 and message.guild.id != 1194106864582004849: #Chỉ True Heaven, Học Viện 2ten mới không bị dính
                if CustomFunctions.is_outside_working_time() == False:
                    await message.channel.send(f"Tính năng AI của Bot chỉ hoạt động đến 12h đêm, vui lòng đợi đến 8h sáng hôm sau.")
                    return
            elif message.guild.id == 1194106864582004849 and message.channel.id != 1264455905756446740: #Học viện 2ten/ channel #sân-chơi-creation-2
                await message.channel.send(f"Bạn ơi vui lòng xuống <#1264455905756446740> để nói chuyện với mình nha, ở đây mình không muốn nói chuyện.")
                return
            flag, mess = await CustomFunctions.check_message_nsfw(message, bot)
            if flag != 0:
                await message.reply(mess)
                interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} violated chat when talking to {bot.user}")
                interaction_logger.info(f"Username {message.author.name} violated chat {message.content} when talking to {bot.user}")
                return
            async with message.channel.typing():
                referenced_message = await message.channel.fetch_message(message.reference.message_id)
                model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
                prompt = await CustomFunctions.get_proper_prompt(message,"Creation 2", referenced_message)
                print(f"Prompt generated from {bot.user}: {prompt}")
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
                    print(f"Username {message.author.name}, Display user name {message.author.display_name} tell {bot.user} to send record")
                    interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} tell {bot.user} to send record")
                    return
                
                #Nếu là bot thì đương nhiên không reply, chỉ nhắn bình thường thôi
                if(message.author.id == CustomFunctions.user_cr_1["user_id"] or message.author.id == CustomFunctions.user_cr_2["user_id"] or message.author.id == CustomFunctions.user_cr_3["user_id"]):
                    await message.channel.send(f"{message.author.mention} {bot_response}")
                else:
                    await message.reply(f"{bot_response}")
                CustomFunctions.save_user_convo_data(message=message, bot_reponse= bot_response, bot_name= "Creation 2")
                print(f"Username {message.author.name}, Display user name {message.author.display_name} replied {bot.user}")
                interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} replied {bot.user}")
            
    elif CustomFunctions.contains_substring(message.content.lower(), bots_creation_name):
        if message.guild.id != 1256987900277690470 and message.guild.id != 1194106864582004849 and CustomFunctions.is_outside_working_time() == False: #Chỉ True Heaven, học viện 2ten mới không bị dính
            await message.channel.send(f"Tính năng AI của Bot chỉ hoạt động đến 12h đêm, vui lòng đợi đến 8h sáng hôm sau.")
            return
        elif message.guild.id == 1194106864582004849 and message.channel.id != 1264455905756446740: #Học viện 2ten/ channel #sân-chơi-creation-2
            await message.channel.send(f"Bạn ơi vui lòng xuống <#1264455905756446740> để nói chuyện với mình nha, ở đây mình không muốn nói chuyện.")
            return
        async with message.channel.typing():
            flag, mess = await CustomFunctions.check_message_nsfw(message, bot)
            if flag != 0:
                await message.channel.send(mess)
            else:
                model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
                prompt = await CustomFunctions.get_proper_prompt(message,"Creation 2")
                print(f"Prompt generated from {bot.user}: {prompt}")
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
                    print(f"Username {message.author.name}, Display user name {message.author.display_name} tell {bot.user} to send record")
                    interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} tell {bot.user} to send record")
                    return
                
                await message.channel.send(f"{message.author.mention} {bot_response}")
                CustomFunctions.save_user_convo_data(message=message, bot_reponse= bot_response, bot_name= "Creation 2")
                print(f"Username {message.author.name}, Display user name {message.author.display_name} directly call {bot.user}")
                interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} directly call {bot.user}")
    return


attachment_counter = {}
async def check_message_attachments(message: discord.Message):
    if message.guild and message.attachments != None and len(message.attachments) >= 1:
        req_roles = ['Đẳng Cấp']
        has_required_role = any(role.name in req_roles for role in message.author.roles)
        #Lưu lại link từng attachment theo từng channel
        user_attachments = []
        for att in message.attachments:
            if att.filename != "profile.png":
                #Trong server True Heaven thì kiểm tra xem đăng đủ 10 attachments trong channel đặc biệt không
                if message.guild.id == 1256987900277690470 and has_required_role == False and (message.channel.id == 1259237925590138880):
                    if message.channel.id not in attachment_counter:
                        attachment_counter[message.channel.id] = {}
                    if message.author.id not in attachment_counter[message.channel.id]:
                        attachment_counter[message.channel.id][message.author.id] = 0
                    attachment_counter[message.channel.id][message.author.id] += 1
                #cache lại link, tránh dead.
                response = requests.get(url=att.url, stream=True)
        
        if message.guild.id == 1256987900277690470 and message.channel.id == 1259237925590138880 and has_required_role == False and attachment_counter[message.channel.id].get(message.author.id, 0) >= 20:
        #thêm role Đẳng Cấp của server
            dc_role = discord.utils.get(message.author.guild.roles, name="Đẳng Cấp")
            if dc_role:
                await message.author.add_roles(dc_role)
                mordern_date_time_format = datetime.now().strftime(f"%d/%m/%Y %H:%M")
                embed = discord.Embed(title="Thêm Role Đẳng Cấp", description=f"{message.author.mention}, username: {message.author.name} đã đăng đủ 20 attachment trong channel đặc biệt!", color=0x00FF00)  # Green color
                embed.add_field(name="Thời gian thêm Role:", value=f"{mordern_date_time_format}", inline=True)
                channel = bot.get_channel(1257016014156206115) #Log Command
                await channel.send(embed= embed)
                print(f"Username: {message.author.name} posted 20 attachments at special channel. {attachment_counter}")
                del attachment_counter[message.channel.id][message.author.id]
    return



list_2tai_images = [] 
list_anime_image = []

async def steal_content_from_2tai(message: discord.Message):
    if message.guild.id == 1194106864582004849 and message.attachments != None and len(message.attachments) >= 1:
        random_chance =random.randint(1, 3)
        # if random_chance == 3: return
        #Tuỳ channel sẽ lấy attachment khác nhau
        true_heaven_server = bot.get_guild(1256987900277690470)
        user_attachments = []
        for att in message.attachments:
            if att.filename != "profile.png":
                #trên 25mb không lấy
                if att.size > 24 * 1024 * 1024: continue
                file = await CustomFunctions.get_attachment_file_from_url(url=att.url, content_type=att.content_type)
                if file != None: user_attachments.append(file)
        if user_attachments != None and len(user_attachments)>0:
            try:
                #Lấy theo channel 2ten, post vào channel true heavens
                source_channel = message.channel
                des_channel = None
                source_id, des_id = CustomFunctions.find_in_channels(input= source_channel.id)
                if source_id != None and des_id != None:
                    des_channel = true_heaven_server.get_channel(des_id)
                    print(des_channel)
                    if des_channel:
                        await des_channel.send(files=user_attachments)
                #Không nằm trên danh sách trên thì khỏi cần
                else:
                    return
                print(f"Found {len(message.attachments)} attachment(s) at channel {source_channel.name} and posted to channel {des_channel.name if des_channel else 'Unknow'}")
            except Exception as e:
                return
            
    return

client = discord.Client(intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    interaction_logger.info(f"Successfully logged in as {bot.user}")
    if CustomFunctions.check_if_dev_mode()==False:
        automatic_speak_randomly.start()
    remove_old_conversation.start()
    
    #Load extension
    for ext in init_extension:
        await bot.load_extension(ext)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await sub_function_ai_response(message=message)
    await check_message_attachments(message=message)
    await steal_content_from_2tai(message=message)
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    message: discord.Message = message
    channel_where_message_deleted = message.channel
    if message.guild.id == 1256987900277690470 and message.attachments != None and len(message.attachments)>0:
        #Áp dụng log images cho server true Heavens
        temp_files = []
        true_heaven_server = bot.get_guild(1256987900277690470) 
        log_image_channel = true_heaven_server.get_channel(1257004596426182757)
        embed = discord.Embed(title=f"Một tin nhắn đã bị xoá trong server {message.guild.name}", description=f"Tin nhắn của {message.author.mention} đã bị xoá tại {channel_where_message_deleted.mention}!", color=0xFC0345)
        embed.add_field(name="Nội dung tin nhắn bị xoá:", value=message.content, inline=False)
        embed.add_field(name=f"Tin nhắn chứa {len(message.attachments)} Attachments.", value="", inline=False)
        for index,attachment in enumerate(message.attachments):
            embed.add_field(name="", value=f"{index+1}. {attachment.url}", inline=False)
            file = await CustomFunctions.get_attachment_file_from_url(url=attachment.url, content_type=attachment.content_type)
            if file != None: temp_files.append(file)
        await log_image_channel.send(embed=embed, files=temp_files)
    if message.guild:
        #Kiểm tra coi có attachments không
        user_attachments = []
        if message.attachments:
            for att in message.attachments:
                new_url = att.url
                data_attachmenta = db.SnipeMessageAttachments(filename=att.filename, url=new_url,content_type=att.content_type,size=att.size)
                user_attachments.append(data_attachmenta)
        snipe_message = db.SnipeMessage(author_id=message.author.id, author_username=message.author.name, author_display_name= message.author.display_name, deleted_date= datetime.now(), user_message_content=message.content, user_attachments=user_attachments)
        print(snipe_message.to_dict())
        #Kiểm tra coi đã tồn tại SnipeChannelInfo chưa, chưa thì tạo mới
        existing_snipe_channel_info = db.find_snipe_channel_info_by_id(channel_id=channel_where_message_deleted.id, guild_id=message.guild.id)
        if existing_snipe_channel_info == None:
            list_temp = []
            list_temp.append(snipe_message)
            existing_snipe_channel_info = db.SnipeChannelInfo(channel_id=channel_where_message_deleted.id, channel_name=channel_where_message_deleted.name, snipe_messages=list_temp)
            result = db.create_snipe_channel_info(snipe_channel_info=existing_snipe_channel_info, guild_id=message.guild.id)
            print(f"Successfully create new Snipe Channel Info for guild {message.guild.name}")
        else:
            #Cập nhật snipe_messages của SnipeChannelInfo ấy
            print(snipe_message)
            result = db.update_or_insert_snipe_message_info(guild_id=message.guild.id, channel_id=channel_where_message_deleted.id, snipe_message=snipe_message)
    else:
        print("Message deleted in a private message.")
    return

#Cog command
init_extension = ["cogs.games.RockPaperScissorCog", 
                  "cogs.games.TruthDareCog",
                  "cogs.economy.ProfileCog",
                  ]

bot_token = os.getenv("BOT_TOKEN_NO2")
bot.run(bot_token)