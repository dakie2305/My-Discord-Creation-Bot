import discord
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import CustomFunctions
import google.generativeai as genai
from discord.ext import commands, tasks
from discord import app_commands
from Handling.MiniGame.GuessNumber import GnHandling, GnMongoManager
from Handling.MiniGame.MatchWord import MwHandling, MwMongoManager
from Handling.Misc import AntiSpamHandling, DonatorMongoManager
import db.DbMongoManager as db
from db.DbMongoManager import UserInfo
import random
import string
import CustomButton
from typing import Optional
import asyncio
from Handling.MiniGame.SortWord import SwHandling as SwHandling
from Handling.Misc.Therapy import TherapyHandling
from Handling.Misc.StickyMessage import StickyMessageHandling
from discord.app_commands import Choice
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
import Handling.MiniGame.SortWord.SwMongoManager as SwMongoManager
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from Handling.Misc.UnbanView import UnbanView
from Handling.Misc.RemoveTimeoutView import RemoveTimeoutView
from Handling.Misc.AIResponse import AIResponseHandling

load_dotenv()
intents = discord.Intents.all()
intents.presences = False
API_KEY = os.getenv("GOOGLE_CLOUD_KEY")
genai.configure(api_key=API_KEY)


bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')
#region Bot Prefix Commands
@bot.command()
async def ping(ctx):
    await ctx.send(f"Online at {ctx.guild}")

@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def global_sync_creation_1(ctx):
    if(ctx.author.id == CustomFunctions.user_darkie['user_id']):
        fmt = await bot.tree.sync()
        await ctx.send(f"Đã đồng bộ hết {len(fmt)} slash commands của Creation 1 vào toàn bộ server hiện hành!")
    else:
        await ctx.send(f"Có phải là Darkie đâu mà dùng lệnh này?")        
        
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
@app_commands.checks.has_role(1256989385744846989)
async def sync(ctx):
    if(ctx.author.id == CustomFunctions.user_darkie['user_id']):
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        await ctx.send(f"Đồng bộ {len(fmt)} commands vào {ctx.guild}")
    else:
        await ctx.send(f"Có phải là Darkie đâu mà dùng lệnh này?")
        

#region say command
@bot.tree.command(name = "say", description="Nói gì đó ẩn danh thông qua bot, có thể gắn hình ảnh và nhắn vào Channel khác")
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def say(interaction: discord.Interaction, thing_to_say : str, image: Optional[discord.Attachment] = None, chosen_channel: Optional[discord.TextChannel]= None):
    black_list_id = [1194106864582004849]
    if interaction.guild_id in black_list_id:
        await interaction.response.send_message(content="Không thể gửi tin nhắn ẩn danh trong server", ephemeral=True)
        return
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
#endregion

#region delete_message command
@bot.tree.command(name="delete_message", description="Xoá một hoặc nhiều tin nhắn bất kỳ.", guild=discord.Object(id=TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value))
@app_commands.describe(reason= "Lý do tại sao xoá tin nhắn này", message_id= "Chuột phải vào message muốn xoá, vào bấm Copy Id rồi dán vào đây", chosen_channel = "Channel chứa message cần xoá. Tất cả message id phải chung một channel")
async def delete_message(interaction: discord.Interaction, reason : str, message_id: str, chosen_channel: Optional[discord.TextChannel]= None):
    await interaction.response.defer(ephemeral=True)
    req_roles = ['Supervisor', 'Server Master', 'Moderator', 'Ultimate Admins']
    has_required_role = any(role.name in req_roles for role in interaction.user.roles)
    if not has_required_role:
        await interaction.followup.send("Không đủ thẩm quyền để thực hiện lệnh.")
        return
    list_mess_id = message_id.split(",")
    for mess in list_mess_id:
        try:
            mess_to_delete: discord.Message = None
            if chosen_channel:
                mess_to_delete = await chosen_channel.fetch_message(int(mess))
            else:
                mess_to_delete = await interaction.channel.fetch_message(int(mess))
            user_reported = mess_to_delete.author
            if user_reported != None:
                is_user_admin = any(role.name in req_roles for role in user_reported.roles)
                if is_user_admin and interaction.user.id != 315835396305059840:        #Chỉ Darkie mới được quyền xoá tin nhắn của admin, moderator
                    await interaction.followup.send("Không thể xoá tin nhắn của admin/moderator. Vui lòng liên hệ <@315835396305059840>.")
                    return
            # Create embed object
            if len(mess_to_delete.content) > 1000:
                mess_to_delete.content = mess_to_delete.content[:1000] + "..."
            embed = discord.Embed(title="Một tin nhắn đã bị xoá", description=f"User {interaction.user.mention} đã xoá một tin nhắn của {mess_to_delete.author.mention} đăng tại <#{mess_to_delete.channel.id}>!", color=0xFC0345)
            embed.add_field(name="Lý do xoá tin nhắn:", value=reason, inline=False)  # Single-line field
            embed.add_field(name="Nội dung tin nhắn bị xoá:", value=mess_to_delete.content, inline=False)
            temp_files = []
            if mess_to_delete.attachments != None and len(mess_to_delete.attachments) > 0:
                embed.add_field(name=f"Tin nhắn chứa {len(mess_to_delete.attachments)} attachments.", value="", inline=False)
                for index,attachment in enumerate(mess_to_delete.attachments):
                    embed.add_field(name="", value=f"{index+1}. {attachment.url}", inline=False)
                    file = await CustomFunctions.get_attachment_file_from_url(url=attachment.url, content_type=attachment.content_type)
                    if file != None: temp_files.append(file)
            
            embed.set_footer(text=f"Message Id: {mess}. User ID Invoke: {interaction.user.id}")  # Footer text
            await mess_to_delete.delete()
            await interaction.followup.send(f"Đã xoá tin nhắn ID: {mess}. Lý do xoá: {reason}", ephemeral=True)
            channel = bot.get_channel(1257150347017850990) #Log-text
            await channel.send(embed=embed, files=temp_files)
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} delete message of {mess_to_delete.author.display_name}.")
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} delete message of {mess_to_delete.author.display_name}.")
        except discord.NotFound:
                await interaction.followup.send(f"Không tìm được tin nhắn với ID {mess}. Vui lòng thử lại!", ephemeral=True)
                print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried to delete message id{mess} but not found.")
        except discord.Forbidden:
                await interaction.followup.send(f"Bot không có quyền xoá tin nhắn với ID {mess}. Vui lòng cấp quyền Manage Message!", ephemeral=True)
                print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried to delete message id{mess} but bot has insufficient permissions.")
        except Exception as e:
                await interaction.followup.send(f"<@315835396305059840> Bot gặp exception trong lúc xoá message ID {mess}. Exception: {str(e)}. Vui lòng liên hệ Darkie!")
                print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried to delete message id{mess} but got exception {str(e)}.")

@app_commands.context_menu(name="Delete Message")
async def delete_message_context(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True)
    req_roles = ['Supervisor', 'Server Master', 'Moderator', 'Ultimate Admins']
    has_required_role = any(role.name in req_roles for role in interaction.user.roles)
    if not has_required_role:
        await interaction.followup.send("Không đủ thẩm quyền để thực hiện lệnh.")
        return
    try:
            user_reported = message.author
            is_user_admin = False
            if user_reported != None:
                if isinstance(user_reported, discord.Member):
                    is_user_admin = any(role.name in req_roles for role in user_reported.roles)
                    if is_user_admin and interaction.user.id != 315835396305059840:        #Chỉ Darkie mới được quyền xoá tin nhắn của admin, moderator
                        await interaction.followup.send("Không thể xoá tin nhắn của admin/moderator. Vui lòng liên hệ <@315835396305059840>.")
                        return
            if len(message.content) > 1000:
                message.content = message.content[:1000] + "..."
            # Create embed object
            embed = discord.Embed(title="Một tin nhắn đã bị xoá", description=f"User {interaction.user.mention} đã xoá một tin nhắn của {user_reported.mention if user_reported != None else 'Người Dùng Đã Thoát Server'} đăng tại <#{message.channel.id}>!", color=0xFC0345)
            embed.add_field(name="Lý do xoá tin nhắn:", value="Không có. Hình thức xoá thông qua context menu", inline=False)
            embed.add_field(name="Nội dung tin nhắn bị xoá:", value=message.content, inline=False)
            temp_files = []
            if message.attachments != None and len(message.attachments) > 0:
                embed.add_field(name=f"Tin nhắn chứa {len(message.attachments)} attachments.", value="", inline=False)
                for index,attachment in enumerate(message.attachments):
                    embed.add_field(name="", value=f"{index+1}. {attachment.url}", inline=False)
                    file = await CustomFunctions.get_attachment_file_from_url(url=attachment.url, content_type=attachment.content_type)
                    if file != None: temp_files.append(file)
            
            embed.set_footer(text=f"Message Id: {message.id}. User ID Invoke: {interaction.user.id}")  # Footer text
            await message.delete()
            await interaction.followup.send(f"Đã xoá tin nhắn ID: {message.id}.", ephemeral=True)
            channel = bot.get_channel(1257150347017850990) #Log-text
            await channel.send(embed=embed, files=temp_files)
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} delete message of {user_reported.display_name if user_reported!=None else 'Out Server'}.")
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} delete message of {user_reported.display_name if user_reported!=None else 'Out Server'}.")
    except discord.NotFound:
            await interaction.followup.send(f"Không tìm được tin nhắn với ID {message.id}. Vui lòng thử lại!", ephemeral=True)
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried to delete message id{message.id} but not found.")
    except discord.Forbidden:
            await interaction.followup.send(f"Bot không có quyền xoá tin nhắn với ID {message.id}. Vui lòng cấp quyền Manage Message!", ephemeral=True)
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried to delete message id{message.id} but bot has insufficient permissions.")
    except Exception as e:
            await interaction.followup.send(f"<@315835396305059840> Bot gặp exception trong lúc xoá message ID {message.id}. Exception: {str(e)}. Vui lòng liên hệ Darkie!")
            print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried to delete message id{message.id} but got exception {str(e)}.")
#endregion

#region report command
@bot.tree.command(name="report", description="Báo cáo user vi phạm luật về cho admin và moderator xem xét.", guild=discord.Object(id=TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value))
@app_commands.describe(user="Chọn user đã phạm luật để báo cáo", reason="Lý do tại sao báo cáo", message_id= "Chuột phải vào message muốn xoá, vào bấm Copy Id rồi dán vào đây", image = "Chọn hình làm bằng chứng (sẽ xử lý nhanh hơn).")
async def report(interaction: discord.Interaction, user : discord.Member, reason: str, message_id: Optional[str] = None, image: Optional[discord.Attachment] = None):
    await interaction.response.defer(ephemeral=True)
    try:
        await interaction.followup.send(f"Đã thành công gửi báo cáo {user.mention} về cho dàn admin và moderator xem xét với lý do: {reason}.", ephemeral=True)
        channel = bot.get_channel(1257004337989943370) #great-hall
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
        else:
            await interaction.followup.send(f"<@315835396305059840> Bot không tìm được channel để gửi báo cáo!")
    except Exception as e:
        #Tag bản thân
        await interaction.followup.send(f"<@315835396305059840> Bot gặp exception trong lúc thực hiện lệnh. Exception: {str(e)}. Vui lòng liên hệ Darkie!", ephemeral=True)

# Task: Check jail expiry
@tasks.loop(seconds=30)
async def check_jail_expiry():
    now = datetime.now()
    jail_db = "jailed_user"
    #Lấy tất cả dữ liệu db jail user ra
    list_all_jailed_users = db.find_all_users(chosen_collection=jail_db)
    if list_all_jailed_users:
        guild = bot.get_guild(TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value)
        for jail_user in list_all_jailed_users:
                #Lấy thời hạn tù đày
                jailed_time = (jail_user.jail_until)
                if jailed_time > now: continue
                user = guild.get_member(jail_user.user_id)
                if user:
                    #Xoá role Đáy Xã Hội
                    jail_role = discord.utils.get(user.guild.roles, name="Đáy Xã Hội")
                    if jail_role == None: continue
                    await user.remove_roles(jail_role)
                    #Tìm xem user này đã có chưa, có thì xoá khỏi db jail_user
                    search_user = db.find_user_by_id(jail_user.user_id, jail_db)
                    if search_user == None: continue
                        #Restore lại roles cũ của user
                    for role in search_user.roles:
                            get_role_from_server = discord.utils.get(user.guild.roles, id = role["role_id"])
                            if get_role_from_server:
                                try:
                                    await user.add_roles(get_role_from_server)
                                except Exception as e:
                                    print(e)
                    #Xoá row khỏi database
                    db.delete_user_by_id(jail_user.user_id, chosen_collection= jail_db)
                    # Create embed object
                    mordern_date_time_format = datetime.now().strftime(f"%d/%m/%Y %H:%M")
                    embed = discord.Embed(title="Ân Xá Khỏi Đại Lao", description=f"Kẻ tội đồ {user.mention} đã hoàn thành hạn tù và ân xoá khỏi đại lao!", color=0x00FF00)  # Green color
                    embed.add_field(name="Lý do được ân xá:", value="Hoàn thành hạn tù", inline=False)  # Single-line field
                    embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
                    embed.add_field(name="Ghi chú", value="Nhớ đừng vi phạm để bị tống vài đại lao nữa nhé!", inline=False) 
                    embed.set_footer(text=f"Đã được ân xoá bởi: {bot.user}")  # Footer text
                    channel = guild.get_channel(1257012036718563380)
                    if channel:
                            await channel.send(embed=embed)
                    print(f"Bot {bot.user} automatically unjailed {user.display_name} for time is up.")

# Task: Nói chuyện tự động
@tasks.loop(hours=3, minutes= 30)
async def automatic_speak_randomly():
    guilds = bot.guilds
    for guild in guilds:
        guild_extra_info = db.find_guild_extra_info_by_id(guild.id)
        if guild_extra_info != None and guild_extra_info.list_channels_ai_talk != None and len(guild_extra_info.list_channels_ai_talk)>0:
            random_channel_id = random.choice(guild_extra_info.list_channels_ai_talk)
            actual_channel = guild.get_channel(random_channel_id)
            if actual_channel:
                model = genai.GenerativeModel(CustomFunctions.AI_MODEL, CustomFunctions.safety_settings)
                prompt = CustomFunctions.get_automatically_talk_prompt("Creation 1", guild, actual_channel)
                response = model.generate_content(f"{prompt}")
                print(f"{bot.user} started talking on its own at {guild_extra_info.guild_name}, channel {actual_channel.name}.")
                async with actual_channel.typing():
                    await actual_channel.send(f"{response.text}")
 
@tasks.loop(hours=12)
async def remove_old_conversation():
    #Kiểm tra các collections user_conversation_info_creation xem
    #có dữ liệu nào có last interaction cách đây 3 ngày không
    #Nếu có thì xoá luôn
    count = 0
    three_day_before = datetime.now() - timedelta(days=3)
    bot_name = "creation_1"
    list_all_user_convo_info = db.find_all_user_convo_info(bot_name)
    if list_all_user_convo_info:
        for data in list_all_user_convo_info:
            if data.last_time_interaction < three_day_before:
                db.delete_user_convo_info(data.user_id, bot_name)
                count+=1
    print(f"Found {count} old conversation in collection 'user_conversation_info_{bot_name}' and deleted them.")

@tasks.loop(hours=6)
async def check_true_heavens_role_expiracy():
    count = 0
    guild = bot.get_guild(TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value)
    if not guild:
        return
    donator_role = guild.get_role(TrueHeavenEnum.DONATOR.value)
    if not donator_role:
        return
    list_donator = DonatorMongoManager.find_all_donators()
    if list_donator:
        for donator in list_donator:
            if donator.date_donate is None or not donator.is_given_role: continue
            if donator.date_donate + timedelta(weeks=2) < datetime.now():
                member = guild.get_member(donator.user_id)
                if member and donator_role in member.roles:
                    try:
                        await member.remove_roles(donator_role, reason="Donator role expired after 2 weeks.")
                        DonatorMongoManager.update_is_given_role(user_id=member.id, value=False)
                        count += 1
                        print(f"Removed Donator role from {member.display_name}, username: {member.name}")
                    except Exception as e:
                        print(f"Error removing role from {member.display_name}, username: {member.name}: {e}")
    print(f"Donator role check completed. Removed role from {count} users.")

@tasks.loop(hours=12)
async def clear_up_data_task():
    guilds = bot.guilds
    for guild in guilds:
        #Kiểm tra quest cũ, xóa đi nếu cần
        all_quest_data = QuestMongoManager.find_all_profiles(guild_id=guild.id)
        count = 0
        if all_quest_data != None:
            for quest in all_quest_data:
                if datetime.now() > quest.reset_date: 
                    QuestMongoManager.delete_quest(guild_id=guild.id, user_id=quest.user_id)
                    count+=1
        print(f"clear_up_data_task started. Deleted {count} quest data in guild {guild.name}")
        all_mw_data = MwMongoManager.find_all_info_in_guild(guild_id=guild.id)
        count = 0
        if all_mw_data != None:
            for lang, mw_data in all_mw_data:
                if datetime.now() > mw_data.last_played + timedelta(weeks=4):
                    MwMongoManager.delete_data_info(channel_id=mw_data.channel_id, guild_id=guild.id, lang=lang)
                    count+=1
        print(f"clear_up_data_task started. Deleted {count} MatchWord data in guild {guild.name} for being inactive over 1 month")
        
        all_sw_data = SwMongoManager.find_all_info_in_guild(guild_id=guild.id)
        count = 0
        if all_sw_data != None:
            for lang, sw_data in all_sw_data:
                if datetime.now() > sw_data.last_played + timedelta(weeks=4):
                    SwMongoManager.delete_data_info(channel_id=sw_data.channel_id, guild_id=guild.id, lang=lang)
                    count+=1
            
        print(f"clear_up_data_task started. Deleted {count} SortWord data in guild {guild.name} for being inactive over 1 month")
        all_gn_data = GnMongoManager.find_all_info_in_guild(guild_id=guild.id)
        count = 0
        if all_gn_data != None:
            for data in all_gn_data:
                if datetime.now() > data.last_played + timedelta(weeks=4):
                    GnMongoManager.delete_data_info(channel_id=data.channel_id, guild_id=guild.id)
                    count+=1
            
        print(f"clear_up_data_task started. Deleted {count} Guess Number data in guild {guild.name} for being inactive over 1 month")
        #Drop quest collection nếu trống
        QuestMongoManager.drop_quest_collection_if_empty(guild_id=guild.id)
        MwMongoManager.drop_collections_if_empty(guild_id=guild.id)
        SwMongoManager.drop_collections_if_empty(guild_id=guild.id)
        GnMongoManager.drop_collection_if_empty(guild_id=guild.id)
        #Kiểm tra snipe message cũ, xóa đi nếu cần
        all_snipe_channels = db.find_all_snipe_channel_info(guild_id=guild.id)
        count = 0
        if all_snipe_channels != None:
            count = 0
            for snipe_channel in all_snipe_channels:
                if snipe_channel.snipe_messages != None and len(snipe_channel.snipe_messages) > 0:
                    #Xóa bớt message
                    snipe_messages = snipe_channel.snipe_messages
                    filtered_messages = [
                        msg for msg in snipe_messages 
                        if datetime.now() <= msg.deleted_date + timedelta(weeks=2)
                    ]
                    count += len(snipe_messages) - len(filtered_messages)
                    snipe_messages = filtered_messages
                    db.replace_snipe_message_info(guild_id=guild.id, channel_id=snipe_channel.channel_id, snipe_messages=snipe_messages)
                else:
                    #Xóa channel
                    db.delete_snipe_channel_info(guild_id=guild.id, channel_id=snipe_channel.channel_id)
        print(f"clear_up_data_task started. Deleted {count} snipe message in {guild.name}")
        #drop collection nếu trống
        db.drop_snipe_channel_info_collection_if_empty(guild_id=guild.id)


client = discord.Client(intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    check_jail_expiry.start()
    if CustomFunctions.check_if_dev_mode()==False:
        # Tạm tắt 
        # automatic_speak_randomly.start()
        
        check_true_heavens_role_expiracy.start()
        activity = discord.Activity(type=discord.ActivityType.watching, 
                                name="True Heavens",
                                state = "Dùng lệnh /help để biết thêm thông tin",
                                details = "Kiểm tra profile của từng người..",
                                )
        await bot.change_presence(status=discord.Status.online, activity=activity)
    remove_old_conversation.start()
    clear_up_data_task.start()
    #Load extension
    for ext in init_extension:
        await bot.load_extension(ext)
        
    

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    #Tạm thời không cần chạy trong server khác
    if before.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
    
    model = genai.GenerativeModel(CustomFunctions.AI_MODEL, CustomFunctions.safety_settings)
    channel = bot.get_channel(1259392446987632661)
    await CustomFunctions.thanking_for_boost(bot_name="creation 1", before=before, after=after, model=model, channel=channel)
    
    # Check for Nitro Boost loss
    if before.premium_since and after.premium_since is None:
        # List role to remove
        ROLE_IDS_TO_REMOVE_ON_BOOST_LOSS = [
            TrueHeavenEnum.ROLE_CYAN.value,
            TrueHeavenEnum.ROLE_BLUE.value,
            TrueHeavenEnum.ROLE_GREEN.value,
            TrueHeavenEnum.ROLE_PURPLE.value,
            TrueHeavenEnum.ROLE_RED.value,
            TrueHeavenEnum.ROLE_WHITE.value,
            TrueHeavenEnum.ROLE_YELLOW.value,
        ]
        roles_to_remove = [after.guild.get_role(role_id) for role_id in ROLE_IDS_TO_REMOVE_ON_BOOST_LOSS]
        roles_to_remove = [role for role in roles_to_remove if role in after.roles]  # Only remove if the user actually has the role
        if roles_to_remove:
            try:
                await after.remove_roles(*roles_to_remove, reason="User stopped boosting the server.")
                print(f"Removed boost-only roles from {after.display_name}")
            except Exception as e:
                print(f"Error removing roles from {after.name}: {e}")

    if before.timed_out_until != after.timed_out_until:
        channel = after.guild.get_channel(1257004337989943370) #Channel great hall
        if not channel: return
        if after.timed_out_until:
            embed = discord.Embed(title="Thông Tin Member Bị Timeout", description=f"{after.mention}, username {after.name}", color=0xeb0c0c)
            embed.add_field(name=f"", value=f"- ID: {after.id}", inline=False)
            unix_time = int(datetime.now().timestamp())
            embed.add_field(name=f"", value=f"- Thời gian bị timeout: <t:{unix_time}:f>", inline=False)
            unix_time_until = int(after.timed_out_until.timestamp())
            embed.add_field(name=f"", value=f"- Sẽ bị timeout cho đến lúc: <t:{unix_time_until}:f>", inline=False)
            embed.set_footer(text=f"Made by Darkie.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            view = RemoveTimeoutView(user=after)
            m = await channel.send(view=view, embed=embed)
            view.message = m

@bot.event
async def on_guild_remove(guild: discord.Guild):
    #drop collection sw guild and world matching database
    SwMongoManager.drop_sort_word_info_collection(guild_id=guild.id)
    MwMongoManager.drop_word_matching_info_collection(guild_id=guild.id)
    print(f"Bot {bot.user.display_name} removed from guild {guild.name}. Deleted all related collection")
    
#Khi có người bị banned
@bot.event
async def on_member_ban(guild: discord.Guild, user: discord.Member):
    #Tạm thời không cần chạy trong server khác
    if guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
    channel = guild.get_channel(1257004337989943370) #Channel great hall
    if not channel:
        return
    ban_entry = await guild.fetch_ban(user)
    reason = "Không có lý do."
    if ban_entry != None:
        reason = ban_entry.reason if ban_entry.reason else "Không có lý do."
    embed = discord.Embed(title="Thông Tin Member Bị Ban", description=f"{user.mention}, username {user.name}", color=0xeb0c0c)
    embed.add_field(name=f"", value=f"- ID: {user.id}", inline=False)
    embed.add_field(name=f"", value=f"- Lý do bị ban: **{reason}**", inline=False)
    unix_time = int(datetime.now().timestamp())
    embed.add_field(name=f"", value=f"- Thời gian bị ban: <t:{unix_time}:f>", inline=False)
    embed.set_footer(text=f"Made by Darkie.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
    view = UnbanView(user=user, guild=guild)
    m = await channel.send(view=view, embed=embed)
    view.message = m

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    speakFlag= True
    sort_word_game = SwHandling.SwHandlingFunction(message= message)
    sw_info, lan = await sort_word_game.check_if_message_inside_game(source=message)
    if sw_info != None:
        #Xử lý nối từ
        asyncio.create_task(sort_word_game.handling_game(message=message))
        speakFlag = False
        
    match_word_game = MwHandling.MwHandlingFunction(message= message)
    mw_info, lan = await match_word_game.check_if_message_inside_game(source=message)
    if mw_info != None:
        #Xử lý nối từ
        asyncio.create_task(match_word_game.handling_game(message=message))
        speakFlag = False
        
    guess_number_game = GnHandling.GnHandlingFunction(message= message)
    gn_info = await guess_number_game.check_if_message_inside_game(source=message)
    if gn_info != None:
        #Xử lý đoán số
        asyncio.create_task(guess_number_game.handling_game(message=message))
        speakFlag = False
    
    guild_extra_info = db.find_guild_extra_info_by_id(guild_id=message.guild.id)
    if guild_extra_info != None and message.channel.id == guild_extra_info.therapy_channel and message.author.bot == False:
        #Xử lý therapy
        model = genai.GenerativeModel(CustomFunctions.AI_MODEL, CustomFunctions.safety_settings)
        asyncio.create_task(TherapyHandling(bot=bot, model=model).handling_therapy_ai(message=message))
        speakFlag = False
    if guild_extra_info != None and guild_extra_info.custom_parameter_2 != None and message.channel.id == guild_extra_info.custom_parameter_2: #Hiện tại chỉ có true heaven có
        speakFlag = False
        #sticky message
        await StickyMessageHandling(bot=bot).handling_sticky_message(message=message)
    await anti_spam.handling_message(message)
    ai_handling_response = AIResponseHandling(bot=bot)
    await ai_handling_response.sub_function_ai_response(message=message, speakFlag=speakFlag)
    await bot.process_commands(message)

bot_token = os.getenv("BOT_TOKENN")
if CustomFunctions.check_if_dev_mode():
    bot_token = os.getenv("BOT_TOKEN_NO1_DEV")
english_words_dictionary = CustomFunctions.english_dict
vietnamese_dict = CustomFunctions.vietnamese_dict
message_tracker = CustomFunctions.MessageTracker()
anti_spam = AntiSpamHandling.AntiSpam()  
#Cog command
init_extension = [
                  "cogs.games.WordMiniGameCog",
                  "cogs.games.HintWordMiniGameCog",
                  "cogs.games.SkillWordMiniGameCog",
                  "cogs.games.LeaderboardWordMiniGameCog",
                  "cogs.games.TruthDareCog",
                  "cogs.misc.SnipeCog",
                  "cogs.misc.TherapyAICog",
                  "cogs.misc.TrueHeavenCustomCommandsCog",
                  "cogs.misc.HelpCog",
                  "cogs.misc.DonationCog",
                  "cogs.misc.DDCNCustomCommandsCog",
                  ]
bot.tree.add_command(delete_message_context)
bot.run(bot_token)