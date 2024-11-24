import PIL.Image
import discord
from datetime import datetime, timedelta
import os
from CustomEnum.EmojiEnum import EmojiCreation2
from dotenv import load_dotenv
import CustomFunctions
import google.generativeai as genai
import DailyLogger
from discord.ext import commands, tasks
from discord import app_commands
import db.DbMongoManager as db
from db.DbMongoManager import UserInfo, GuildExtraInfo
import random
import string
import CustomButton
from typing import Optional
import PIL
from Handling.Misc.AutoresponderCreation2 import AutoresponderHandling
from Handling.Economy.Quest.QuestHandling import QuestHandling
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from Handling.Misc.SelfDestructView import SelfDestructView
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from Handling.Misc.RandomDropboxEconomyView import RandomDropboxEconomyView
from Handling.MiniGame.RandomQuizz.RandomQuizzView import RandomQuizzView, random_quizzes
from Handling.Misc.AutoLevelupProfile import AutoLevelupProfileHandling
import asyncio
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager

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
        await message.reply("Vui lòng dùng lệnh /help")    

@bot.command()
async def cuu_gia(ctx):
    message: discord.Message = ctx.message
    if message:
        role: discord.Role = discord.utils.get(ctx.guild.roles, name="Cửu Gia")
        if role is None: return
        members = role.members
        
        embed = discord.Embed(title=f"", description=f"**Cửu Gia Đệ Nhất Tộc**", color=0x03F8FC)
        embed.add_field(name=f"", value=f"Thượng Cổ Thiên Tôn: <@865429551614001153>", inline=False)
        embed.add_field(name=f"", value=f"Sĩ số: **{len(members)}**", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═══════>", inline=False)
        count = 1
        for member in members:
            if member.id == 865429551614001153: continue #Không cần hiện
            embed.add_field(name=f"", value=f"- {member.mention}!", inline=False)
            count += 1
            if count > 20:
                embed.add_field(name=f"", value=f"Và còn nhiều thành viên khác nữa!", inline=False)
                break
        embed.add_field(name=f"", value="▬▬▬▬ι═══════>", inline=False)
        await message.reply(embed=embed)    


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
    
@tasks.loop(hours=1, minutes = 10)
async def random_dropbox():
    guilds = bot.guilds
    for guild in guilds:
        #Kiểm tra quest channel của server, nếu có thì mới chọn
        guild_info = db.find_guild_extra_info_by_id(guild_id=guild.id)
        if guild_info == None: continue
        if guild_info.list_channels_quests == None or len(guild_info.list_channels_quests) <= 0: continue
        list_channels_quests = guild_info.list_channels_quests
        random_quest_channel_id = random.choice(list_channels_quests)
        quest_channel = guild.get_channel(random_quest_channel_id)
        if quest_channel == None:
            #Xoá channel_id lỗi
            list_channels_quests.remove(random_quest_channel_id)
            data_updated = {"list_channels_quests": list_channels_quests}
            db.update_guild_extra_info(guild_id=guild.id, update_data= data_updated)
            #Chọn channel khác không bị lỗi
            while quest_channel == None:
                random_quest_channel_id = random.choice(list_channels_quests)
                quest_channel = guild.get_channel(random_quest_channel_id)
        if quest_channel != None:
            endtime = datetime.now() + timedelta(seconds=60)
            embed = discord.Embed(title=f"", description=f"{EmojiCreation2.GOLDEN_GIFT_BOX.value} **Hộp Quà Thần Bí** {EmojiCreation2.GOLDEN_GIFT_BOX.value}", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Một hộp quà thần bí đã xuất hiện tại đúng channel này!", inline=False)
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Ai nhanh tay thì được nhé, vì hộp quà sẽ biến mất đúng sau: <t:{int(endtime.timestamp())}:R>", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            embed.set_footer(text=f"Hộp quà sẽ xuất hiện ngẫu nhiên, và khi thấy thì nhớ nhanh tay nhé!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/9e8749a5a47cae53211484d7aee42040.webp?size=100&quot")
            print(f"Created random dropbox at channel {quest_channel.name} in guild {guild.name}.")
            view = RandomDropboxEconomyView()
            m = await quest_channel.send(embed=embed, view=view)
            view.old_message = m
            
@tasks.loop(hours=1, minutes = 10)
async def random_quizz_embed():
    guilds = bot.guilds
    for guild in guilds:
        await asyncio.sleep(5)
        #Kiểm tra quest channel của server, nếu có thì mới chọn
        guild_info = db.find_guild_extra_info_by_id(guild_id=guild.id)
        if guild_info == None: continue
        if guild_info.list_channels_quests == None or len(guild_info.list_channels_quests) <= 0: continue
        list_channels_quests = guild_info.list_channels_quests
        random_quest_channel_id = random.choice(list_channels_quests)
        quest_channel = guild.get_channel(random_quest_channel_id)
        if quest_channel == None:
            #Xoá channel_id lỗi
            list_channels_quests.remove(random_quest_channel_id)
            data_updated = {"list_channels_quests": list_channels_quests}
            db.update_guild_extra_info(guild_id=guild.id, update_data= data_updated)
            #Chọn channel khác không bị lỗi
            while quest_channel == None:
                random_quest_channel_id = random.choice(list_channels_quests)
                quest_channel = guild.get_channel(random_quest_channel_id)
        if quest_channel != None:
            
            random_quizz = random.choice(random_quizzes)
            view = RandomQuizzView(quizz=random_quizz)
            endtime = datetime.now() + timedelta(seconds=120)
            embed = discord.Embed(title=f"", description=f"{EmojiCreation2.QUESTION_MARK.value} **Hỏi Nhanh Có Thưởng** {EmojiCreation2.QUESTION_MARK.value}", color=0x0ce7f2)
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            embed.add_field(name=f"", value=f"**Câu hỏi**: {random_quizz.question}", inline=False)
            for key, value in view.option_mapping.items():
                embed.add_field(name=f"", value=f"**{key}**. {value}", inline=False)
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            embed.add_field(name=f"", value=f"Nhanh tay lên nhé, vì câu hỏi sẽ biến mất sau: <t:{int(endtime.timestamp())}:R>", inline=False)
            embed.set_footer(text=f"Hỏi Nhanh Có Thưởng sẽ xuất hiện ngẫu nhiên, và khi thấy thì nhớ trả lời đúng nhé!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/9e8749a5a47cae53211484d7aee42040.webp?size=100&quot")
            print(f"Created random quizz at channel {quest_channel.name} in guild {guild.name}.")
            m = await quest_channel.send(embed=embed, view=view)
            view.old_message = m
        

async def sub_function_ai_response(message: discord.Message, speakFlag: bool = True):
    if speakFlag == False: return
    bots_creation_name = ["creation 2", "creation số 2", "creation no 2", "creatiom 2", "creation no. 2"]
    guild_info = db.find_guild_extra_info_by_id(message.guild.id)
    if message.reference is not None and message.reference.resolved is not None:
        if message.reference.resolved.author == bot.user or CustomFunctions.contains_substring(message.content.lower(), bots_creation_name):
            if message.guild.id != 1256987900277690470 and message.guild.id != 1194106864582004849: #Chỉ True Heaven, Học Viện 2ten mới không bị dính
                if CustomFunctions.is_inside_working_time() == False:
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
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            if referenced_message.embeds: return
            async with message.channel.typing():
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
        if message.guild.id != 1256987900277690470 and message.guild.id != 1194106864582004849 and CustomFunctions.is_inside_working_time() == False: #Chỉ True Heaven, học viện 2ten mới không bị dính
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



client = discord.Client(intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    interaction_logger.info(f"Successfully logged in as {bot.user}")
    if CustomFunctions.check_if_dev_mode()==False:
        automatic_speak_randomly.start()
        random_dropbox.start()
        random_quizz_embed.start()
    remove_old_conversation.start()
    #Load extension
    for ext in init_extension:
        await bot.load_extension(ext)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    # await steal_content_from_2tai(message=message)
    speakFlag = True
    auto_rep = AutoresponderHandling(bot=bot)
    if await auto_rep.handling_auto_responder(message=message):
        speakFlag = False
    
    await sub_function_ai_response(message=message, speakFlag=speakFlag)
    quest = QuestHandling(bot=bot)
    await quest.handling_quest_progress(message=message)
    auto_level = AutoLevelupProfileHandling(bot=bot)
    await auto_level.handling_auto_level_up(message=message)
    
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    message: discord.Message = message
    if message == None: return
    if message.guild == None: return
    
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
    if message.guild and message.author.bot != True:
        #Kiểm tra coi có attachments không
        user_attachments = []
        if message.attachments:
            for att in message.attachments:
                new_url = att.url
                data_attachmenta = db.SnipeMessageAttachments(filename=att.filename, url=new_url,content_type=att.content_type,size=att.size)
                user_attachments.append(data_attachmenta)
        snipe_message = db.SnipeMessage(author_id=message.author.id, author_username=message.author.name, author_display_name= message.author.display_name, deleted_date= datetime.now(), user_message_content=message.content, user_attachments=user_attachments)
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
            result = db.update_or_insert_snipe_message_info(guild_id=message.guild.id, channel_id=channel_where_message_deleted.id, snipe_message=snipe_message)
    return

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    message: discord.Message = reaction.message
    user_target: discord.Member = user
    if user_target != None and message != None:
        check_quest_message = QuestMongoManager.increase_emoji_count(guild_id=user_target.guild.id, user_id=user_target.id, channel_id=message.channel.id)
        if check_quest_message == True:
            view = SelfDestructView(30)
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            m = await message.channel.send(embed=quest_embed, view=view, content=f"{message.author.mention}")
            view.message = m
    return

@bot.event
async def on_member_remove(member: discord.Member):
    guild = member.guild
    profile = ProfileMongoManager.find_profile_by_id(guild_id=guild.id, user_id=member.id)
    if profile!= None:
        #Xoá profile cho đỡ tốn data
        ProfileMongoManager.delete_profile(guild_id=guild.id, user_id=member.id)
        print(f"Member {member.name} left server {guild.name} so their economy profile is deleted!")
    quest = QuestMongoManager.find_quest_by_user_id(guild_id=guild.id, user_id=member.id)
    if quest != None:
        #Xoá quest cho đỡ tốn dung lượng
        QuestMongoManager.delete_quest(guild_id=guild.id, user_id=member.id)
        print(f"Member {member.name} left server {guild.name} so their quest is deleted!")
    couple = CoupleMongoManager.find_couple_by_id(guild_id=guild.id, user_id=member.id)
    if couple != None:
        #Xoá couple cho đỡ tốn dung lượng
        CoupleMongoManager.delete_couple_by_id(guild_id=guild.id, user_id=member.id)
        print(f"Member {member.name} left server {guild.name} so their couple is deleted!")
    
@bot.event
async def on_guild_remove(self, guild: discord.Guild):
    #drop collection quest và profile
    ProfileMongoManager.drop_profile_collection(guild_id=guild.id)
    QuestMongoManager.drop_quest_collection(guild_id=guild.id)
    

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    #Tạm thời không cần chạy trong server khác
    if before.guild.id != 1256987900277690470: return
    
    model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
    channel = bot.get_channel(1259392446987632661)
    await CustomFunctions.thanking_for_boost(bot_name="creation 2", before=before, after=after, model=model, channel=channel)
    
    
    # Get roles trước và sau khi update
    before_roles = set(before.roles)
    after_roles = set(after.roles)
    # Tìm role mới thêm vào
    new_roles = after_roles - before_roles
    # Nếu có role đáy xã hội thì xoá hết những role mới
    target_role_name = "Đáy Xã Hội"
    target_role = discord.utils.get(after.guild.roles, name=target_role_name)
    if target_role in after_roles:
        # Xoá role mới
        roles_to_remove = new_roles
        if roles_to_remove:
            try:
                for role in roles_to_remove:
                    if role.is_premium_subscriber: continue
                    if role.name == "Đáy Xã Hội": continue
                    try:
                        await after.remove_roles(role)
                        print(f"Removed role '{role.name}' from {after.name} due to 'Đáy Xã Hội' restriction.")
                    except Exception: continue
            except discord.Forbidden:
                print(f"Failed to update roles for {after.name}: Missing permissions.")
            except discord.HTTPException as e:
                print(f"Failed to update roles for {after.name}: {e}")


#Cog command
init_extension = ["cogs.games.RockPaperScissorCog", 
                  "cogs.games.TruthDareCog",
                  "cogs.games.CoinFlipCog",
                  "cogs.games.SicBoCog",
                  
                  "cogs.economy.ProfileCog",
                  "cogs.economy.BankCog",
                  "cogs.economy.TransferCog",
                  "cogs.economy.DailyCog",
                  "cogs.economy.WorkCog",
                  "cogs.economy.AuthorityCog",
                  "cogs.economy.QuestCog",
                  "cogs.economy.CrimeCog",
                  "cogs.economy.LeaderboardCog",
                  "cogs.economy.ShopCog",
                  "cogs.economy.GiftCog",
                  "cogs.economy.InventoryCog",
                  "cogs.economy.CoupleCog",
                  
                  "cogs.misc.HelpCog",
                  ]

bot_token = os.getenv("BOT_TOKEN_NO2")
bot.run(bot_token)