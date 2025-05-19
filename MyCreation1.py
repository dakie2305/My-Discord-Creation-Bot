import PIL.Image
import discord
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import CustomFunctions
import google.generativeai as genai
import time
import DailyLogger
from discord.ext import commands, tasks
from discord import app_commands
import db.DbMongoManager as db
from db.DbMongoManager import UserInfo
import db.Class.WordMatchingClass as WordMatchingClass
import random
import string
import CustomButton
from typing import Optional
import asyncio
import PIL
from Handling.MiniGame.SortWord import SwHandling as SwHandling
from Handling.Misc.Therapy import TherapyHandling
from Handling.Misc.StickyMessage import StickyMessageHandling
from discord.app_commands import Choice
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
import Handling.Economy.Couple.CoupleMongoManager as CoupleMongoManager
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

interaction_logger = DailyLogger.get_logger("Creation1_Interaction")
commands_logger = DailyLogger.get_logger("Creation1_Commands")


bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')
#region Bot Prefix Commands
@bot.command()
async def ping(ctx):
    await ctx.send(f"Online at {ctx.guild}")
    commands_logger.info("Someone use ping!")

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
        commands_logger.info(f"Synced commands for {ctx.guild}!")
    else:
        await ctx.send(f"Có phải là Darkie đâu mà dùng lệnh này?")
        
#region Nối Từ Commands
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def start_wm_en(ctx):
    message: discord.Message = ctx.message
    if message:
        #Kiểm tra xem đã tồn tại WordMatchingClass cho channel này chưa
        if db.find_word_matching_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, language='en'):
            #Xoá word matching info
            db.delete_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language='en')
            await ctx.send(f"Đã xoá trò chơi nối từ trong channel này.")
        else:
            data = db.WordMatchingInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="a", first_character="a",last_character="a",remaining_word=12300)
            result = db.create_word_matching_info(data=data, guild_id=message.guild.id, language='en')
            message_tu_hien_tai = f"\nTừ hiện tại là: `'{data.current_word}'`, và có **{data.remaining_word if data.remaining_word else 0}** bắt đầu bằng chữ cái `{data.last_character if data.last_character else 0}`"
            await ctx.send(f"Đã tạo trò chơi nối từ tiếng Anh cho channel này. Hãy bắt đầu nối từ đi. {message_tu_hien_tai}")
        return
    return

@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def start_wm_vn(ctx):
    message: discord.Message = ctx.message
    if message:
        #Kiểm tra xem đã tồn tại WordMatchingClass cho channel này chưa
        if db.find_word_matching_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, language='vn'):
            #Xoá word matching info
            db.delete_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language='vn')
            await ctx.send(f"Đã xoá trò chơi nối từ trong channel này.")
        else:
            data = db.WordMatchingInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="a", first_character="a",last_character="a",remaining_word=12300)
            result = db.create_word_matching_info(data=data, guild_id=message.guild.id, language='vn')
            message_tu_hien_tai = f"\nTừ hiện tại là: `'{data.current_word}'`, và có **{data.remaining_word if data.remaining_word else 0}** bắt đầu bằng chữ cái `{data.last_character if data.last_character else 0}`"
            await ctx.send(f"Đã tạo trò chơi nối từ tiếng Việt cho channel này. Hãy bắt đầu nối từ đi. {message_tu_hien_tai}")
        return
    return


#region Reset nối từ
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def reset_wm(ctx):
    message: discord.Message = ctx.message
    if message:
        if message.guild.id == 1256987900277690470:
            #Chỉ check trong True Heaven
            req_roles = ['Supervisor', 'Server Master', 'Moderator', 'Ultimate Admins']
            has_required_role = any(role.name in req_roles for role in message.author.roles)
            if not has_required_role:
                await ctx.send("Không đủ thẩm quyền để thực hiện lệnh.")
                return
        #Kiểm tra xem đã tồn tại WordMatchingClass cho channel này chưa
        word_matching_channel = db.find_word_matching_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, language='en')
        if word_matching_channel:
            await process_reset_word_matching(message=message, word_matching_channel=word_matching_channel, language='en')
        else:
            word_matching_channel = db.find_word_matching_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, language='vn')
            if word_matching_channel:
                await process_reset_word_matching(message=message, word_matching_channel=word_matching_channel, language='vn')
            else:
                await ctx.send(f"Chưa tồn tại thông tin Word Match Info cho channel này. Hãy dùng lệnh !bat_dau_noi_tu_english.")
        return
    return

async def process_reset_word_matching(message: discord.Message, word_matching_channel: db.WordMatchingInfo, language):
    embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Trò Chơi Nối Từ", color=0x03F8FC)
    embed.add_field(name=f"", value="___________________", inline=False)
    embed.add_field(name=f"", value=f"Round hiện tại: {word_matching_channel.current_round}", inline=False)
    count = 0
    if word_matching_channel.player_profiles:
        word_matching_channel.player_profiles.sort(key=lambda x: x.points, reverse=True)
        for index, profile in enumerate(word_matching_channel.player_profiles):
            user = message.guild.get_member(profile.user_id)
            if user != None and (profile.points!= 0 or len(profile.special_items)> 0):
                embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.points}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                count+=1
            if count >= 25: break
    text = "Chúc mừng các player top đầu!"
    if message.guild.id == 1256987900277690470:
        text+= " <@315835396305059840> sẽ trao role đặc biệt cho những Player thuộc top 3 nhé!"
    await message.channel.send(content=text, embed=embed)
    #Xoá đi tạo lại
    db.delete_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=language)
    data = db.WordMatchingInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="a", first_character="a",last_character="a",remaining_word=12300)
    result = db.create_word_matching_info(data=data, guild_id=message.guild.id, language=language)
    message_tu_hien_tai = f"\nTừ hiện tại là: `'{data.current_word}'`, và có **{data.remaining_word if data.remaining_word else 0}** bắt đầu bằng chữ cái `{data.last_character if data.last_character else 0}`"
    await message.channel.send(f"Đã reset toàn bộ từ trong trò nối từ trong channel này. {message_tu_hien_tai}")

#region Give skill
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def wm_give_skill(ctx, item_id: str = None, user: Optional[discord.Member] = None):
    message: discord.Message = ctx.message
    if message.guild.id == 1256987900277690470:
        req_roles = ['Cai Ngục', 'Server Master', 'Moderator']
        has_required_role = any(role.name in req_roles for role in message.author.roles)
        if not has_required_role and message.author.id != 315835396305059840:
            await ctx.send("Không đủ thẩm quyền để dùng lệnh.")
            return
    elif message.guild.owner_id != message.author.id:
        await ctx.send("Không đủ thẩm quyền để dùng lệnh. Chỉ Server Owner mới được dùng lệnh này")
        return
    called_channel = message.channel
    #Kiểm tra xem ở đây là bảng channel nối từ hay không
    word_matching_channel = db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'en')
    if word_matching_channel:
        if item_id is None or user is None:
            await ctx.send(f"Dùng sai câu lệnh. Vui lòng dùng câu lệnh đúng format sau.\n!give_skill skill_id @User")
            return
        #Lấy item theo item_id
        special_item = get_special_item_by_id(item_id=item_id)
        if special_item==None:
            await ctx.send(f"{message.author.mention} Kỹ năng **`{item_id}`** không hợp lệ")
            return
        #Add item vào inven của player
        db.update_player_special_item_word_matching_info(user_id=user.id, user_name=user.name, user_display_name=user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='en', special_item= special_item)
        await ctx.send(f"Đã thêm kỹ năng **`{special_item.item_name}`** cho player {user.mention}!")
        return
    else:
        word_matching_channel= db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'vn')
        if word_matching_channel:
            if item_id is None or user is None:
                await ctx.send(f"Dùng sai câu lệnh")
                return
            #Lấy item theo item_id
            special_item = get_special_item_by_id(item_id=item_id)
            if special_item==None:
                await ctx.send(f"{message.author.mention} Kỹ năng **`{message.content}`** không hợp lệ")
                return
            #Add item vào inven của player
            db.update_player_special_item_word_matching_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='vn', special_item= special_item)
            await ctx.send(f"Đã thêm kỹ năng **`{special_item.item_name}`** cho player {message.author.mention}!")
            return
        else:
            await ctx.send(f"Đây không phải là channel dùng để chơi nối từ. Chỉ dùng lệnh này trong channel chơi nối từ thôi!")
    return

#region Give ban skill
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def wm_give_ban(ctx, user: discord.Member, ban_amount: int):
    message: discord.Message = ctx.message
    if message.guild.id == 1256987900277690470:
        req_roles = ['Cai Ngục', 'Server Master', 'Moderator']
        has_required_role = any(role.name in req_roles for role in message.author.roles)
        if not has_required_role and message.author.id != 315835396305059840:
            await ctx.send("Không đủ thẩm quyền để dùng lệnh.")
            return
    elif message.guild.owner_id != message.author.id:
        await ctx.send("Không đủ thẩm quyền để dùng lệnh. Chỉ Server Owner mới được dùng lệnh này")
        return
    called_channel = message.channel
    if ban_amount is None or user is None:
            await ctx.send(f"Dùng sai câu lệnh. Vui lòng dùng câu lệnh đúng format sau.\n!give_ban @User 1")
            return
    #Kiểm tra xem ở đây là bảng channel nối từ hay không
    lan = 'en'
    word_matching_channel = db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'en')
    if word_matching_channel == None:
        word_matching_channel = db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'vn')
        if word_matching_channel == None:
            await ctx.send(f"Đây không phải là channel dùng để chơi nối từ. Chỉ dùng lệnh này trong channel chơi nối từ thôi!")
            return
        lan = 'vn'
    db.create_and_update_player_bans_word_matching_info(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= lan, user_id= user.id, user_name=user.name, ban_remaining=ban_amount)
    if ban_amount==0:
        await message.reply(content=f"Đã bỏ khoá mõm {user.name}.")
    else:
        await message.reply(content=f"Đã khoá mõm {user.name} trong vòng **{ban_amount}** lượt chơi tiếp theo!")
    return

#region remove skill
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def wm_remove_skill(ctx, item_id: str = None, user: Optional[discord.Member] = None):
    message: discord.Message = ctx.message
    called_channel = message.channel
    if message.guild.id == 1256987900277690470:
        #Chỉ check trong guild True Heaven
        req_roles = ['Cai Ngục', 'Moderator','Server Master']
        has_required_role = any(role.name in req_roles for role in message.author.roles)
        if not has_required_role:
            await ctx.send("Không đủ thẩm quyền để dùng lệnh.")
            return
    elif message.guild.owner_id != message.author.id:
        await ctx.send("Không đủ thẩm quyền để dùng lệnh.")
        return
        
    #Kiểm tra xem ở đây là bảng channel nối từ hay không
    word_matching_channel = db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'en')
    if word_matching_channel:
        if item_id is None or user is None:
            await ctx.send(f"Dùng sai câu lệnh. Vui lòng dùng câu lệnh đúng format sau.\n!remove_skill skill_id @User")
            return
        selected_player = None
        for player in word_matching_channel.player_profiles:
            if player.user_id == user.id:
                selected_player = player
                break
        if selected_player == None:
            await ctx.send(f"Không tìm được user này trong bảng xếp hạng.")
            return
        if selected_player.special_items == None or len(selected_player.special_items) == 0:
            await ctx.send(f"User không có bất kỳ kỹ năng đặc biệt nào cả.")
            return
        if item_id == "random":
            #Xoá ngẫu nhiên skill của user
            random_item = random.choice(selected_player.special_items)
            if random_item:
                db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=user.id, user_name=user.name, user_display_name=user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='en', special_item= random_item)
                await ctx.send(f"Đã xoá kỹ năng **`{random_item.item_name}`** khỏi kho kỹ năng của người chơi {user.mention}.")
            else:
                await ctx.send(f"User không có bất kỳ kỹ năng đặc biệt nào cả.")
            return
        elif item_id == "all":
            #Xoá toàn bộ skill của user
            for player_item in selected_player.special_items:
                db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=user.id, user_name=user.name, user_display_name=user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='en', special_item= player_item)
            await ctx.send(f"Đã xoá toàn bộ kỹ năng khỏi kho kỹ năng của người chơi {user.mention}.")
            return
        #Lấy item theo item_id
        special_item = get_special_item_by_id(item_id=item_id)
        if special_item==None:
            await ctx.send(f"{message.author.mention} Kỹ năng **`{item_id}`** không hợp lệ")
            return
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=user.id, user_name=user.name, user_display_name=user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='en', special_item= special_item)
        await ctx.send(f"Đã xoá kỹ năng **`{special_item.item_name}`** khỏi kho kỹ năng của người chơi {user.mention}!")
        return
    else:
        word_matching_channel= db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'vn')
        if word_matching_channel:
            if item_id is None or user is None:
                await ctx.send(f"Dùng sai câu lệnh. Vui lòng dùng câu lệnh đúng format sau.\n!remove_skill skill_id @User")
                return
            selected_player = None
            for player in word_matching_channel.player_profiles:
                if player.user_id == user.id:
                    selected_player = player
                    break
            if selected_player == None:
                await ctx.send(f"Không tìm được user này trong bảng xếp hạng.")
                return
            if selected_player.special_items == None:
                await ctx.send(f"User không có bất kỳ kỹ năng đặc biệt nào cả.")
                return
            if item_id == "random":
                #Xoá ngẫu nhiên skill của user
                random_item = random.choice(selected_player.special_items)
                if random_item:
                    db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=user.id, user_name=user.name, user_display_name=user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='vn', special_item= random_item)
                    await ctx.send(f"Đã xoá kỹ năng **`{random_item.item_name}`** khỏi kho kỹ năng của người chơi {user.mention}.")
                else:
                    await ctx.send(f"User không có bất kỳ kỹ năng đặc biệt nào cả.")
                return
            elif item_id == "all":
                #Xoá toàn bộ skill của user
                for player_item in selected_player.special_items:
                    db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=user.id, user_name=user.name, user_display_name=user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='vn', special_item= player_item)
                await ctx.send(f"Đã xoá toàn bộ kỹ năng khỏi kho kỹ năng của người chơi {user.mention}.")
                return
            #Lấy item theo item_id
            special_item = get_special_item_by_id(item_id=item_id)
            if special_item==None:
                await ctx.send(f"{message.author.mention} Kỹ năng **`{item_id}`** không hợp lệ")
                return
            #xoá khỏi inven của player
            db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=user.id, user_name=user.name, user_display_name=user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language='vn', special_item= special_item)
            await ctx.send(f"Đã xoá kỹ năng **`{special_item.item_name}`** khỏi kho kỹ năng của người chơi {user.mention}!")
            return
        else:
            await ctx.send(f"Đây không phải là channel dùng để chơi nối từ. Chỉ dùng lệnh này trong channel chơi nối từ thôi!")
    return

#region Use skill
@bot.command()
@app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
async def use_skill(ctx, item_id: str = None, user: Optional[discord.Member] = None):
    message: discord.Message = ctx.message
    called_channel = message.channel
    #Kiểm tra xem ở đây là bảng channel nối từ hay không
    word_matching_channel = db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'en')
    lan = 'en'
    if word_matching_channel == None:
        word_matching_channel = db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'vn')
        if word_matching_channel == None:
            await ctx.send(f"Đây không phải là channel dùng để chơi nối từ. Chỉ dùng lệnh này trong channel chơi nối từ thôi!")
            return
        lan = 'vn'
    if item_id is None and user is None:
        embed = danh_sach_ky_nang(word_matching_channel= word_matching_channel, user=message.author)
        await message.reply(embed=embed)
        return
    #Lấy item theo item_id
    special_item = get_special_item_by_id(item_id=item_id)
    if special_item==None:
        await message.reply(f"{message.author.mention} Kỹ năng **`{message.content}`** không hợp lệ")
        return
        #Kiểm xem kỹ năng có cần mục tiêu không
    elif special_item.required_target==True and user is None:
        await message.reply(f"{message.author.mention} Kỹ năng **`{special_item.item_name}`** yêu cầu phải có mục tiêu mới dùng được.")
        return
        #Kiểm xem user có kỹ năng đó không
    player = find_player_profile_by_user_id(user_id=message.author.id, word_matching_channel=word_matching_channel)
    if player == None:
        await message.reply(f"{message.author.mention} Bạn không nằm trong danh sách người chơi.")
        return
    elif player.special_items == None:
        await message.reply(f"{message.author.mention} Bạn không có bất kỳ kỹ năng nào để dùng.")
        return
    else:
        matched = False
        for user_item in player.special_items:
            if user_item.item_id == item_id:
                matched = True
                break
        if matched == False:
            await message.reply(f"{message.author.mention} Bạn không có kỹ năng này.")
            return
        #Sau khi bắt lỗi, bắt đầu thực hiện chức năng kỹ năng
    await process_special_item_functions(word_matching_channel=word_matching_channel, special_item=special_item, message=message, user_target=user, lan = lan)
    return


#region xử lý skill nối từ
async def process_special_item_functions(word_matching_channel: db.WordMatchingInfo, special_item: WordMatchingClass.SpecialItem, message: discord.Message, lan:str,user_target: discord.User = None):
    #Nếu có user_target thì lập tức kiểm tra xem user_target có effect đặc biệt không
    target_player_effect: db.PlayerEffect = None
    if user_target != None:
        for effect in word_matching_channel.player_effects:
            if effect.user_id == user_target.id:
                target_player_effect = effect
                break
    #Kỹ năng hint, gợi ý từ
    if special_item.item_id == "ct_hint":
        #Tìm từ hợp lệ, bắt đầu bằng chữ cái trong word_matching_channel
        suitable_word = None
        if lan == 'eng' or lan == 'en':
            for word in english_words_dictionary.keys():
                if len(word) > 1 and word.startswith(word_matching_channel.last_character) and word not in word_matching_channel.used_words:
                    suitable_word = word
        elif lan == 'vn':
            for word in vietnamese_dict.keys():
                if len(word) > 1 and word.startswith(word_matching_channel.last_character) and word not in word_matching_channel.used_words:
                    suitable_word = word
        if suitable_word == None:
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nRất tiếc là không có từ hợp lệ... lạ ta. <@315835396305059840>")
        half_length = (len(suitable_word) + 2) // 2
        suitable_word = suitable_word[:half_length] + "..."
        #Gợi ý nửa từ
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nGợi ý từ hợp lệ: **`{suitable_word}**`")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    elif special_item.item_id == "cc_hint":
        #Tìm từ hợp lệ, bắt đầu bằng chữ cái trong word_matching_channel
        suitable_word = None
        if lan == 'eng' or lan == 'en':
            for word in english_words_dictionary.keys():
                if word.startswith(word_matching_channel.last_character) and word not in word_matching_channel.used_words:
                    suitable_word = word
        elif lan == 'vn':
            for word in vietnamese_dict.keys():
                if word.startswith(word_matching_channel.last_character) and word not in word_matching_channel.used_words:
                    suitable_word = word
        if suitable_word == None:
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nRất tiếc là không có từ hợp lệ... lạ ta. <@315835396305059840>")
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nGợi ý từ hợp lệ: **`{suitable_word}**`")
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    elif special_item.item_id =="ct_curr_player":
        if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
            text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {user_target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
            #Vô hiệu hoá
            if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                #Phản lại kỹ năng
                db.update_current_player_id_word_matching_info(channel_id=message.channel.id,guild_id=message.guild.id, language=lan, user_id=message.author.id)
                text_reply += f"{message.author.mention} mất quyền nối từ trong lượt chơi hiện tại"
                if target_player_effect.effect_id.startswith("dc"):
                    #Cướp luôn kỹ năng
                    db.update_player_special_item_word_matching_info(user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                    text_reply += f" và đã bị **{user_target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
            await message.reply(text_reply)
            #xoá khỏi inven của player
            db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
            #Xoá hiệu ứng khỏi target user
            db.update_player_effects_word_matching_info(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=user_target.id, user_name=user_target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            return
        #Chuyển current_player_id sang user_target là được
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**. Người chơi {user_target.mention} sẽ mất quyền nối từ trong lượt chơi hiện tại.\n")
        db.update_current_player_id_word_matching_info(channel_id=message.channel.id,guild_id=message.guild.id, language=lan, user_id=user_target.id)
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    elif special_item.item_id =="ct_allow":
        #Chuyển current_player_id sang số 1 là được
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\n")
        db.update_current_player_id_word_matching_info(channel_id=message.channel.id,guild_id=message.guild.id, language=lan, user_id=1)
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    #Những kỹ năng có id tận cùng là minus_first hoặc minus_second
    #Đây là những kỹ năng trừ điểm của top 1 hoặc top 2
    elif special_item.item_id.endswith("minus_first") or special_item.item_id.endswith("minus_second"):
        #Tìm top player để trừ điểm
        sort = sorted(word_matching_channel.player_profiles, key=lambda x: x.points, reverse=True)
        top_number = "1"
        if special_item.item_id.endswith("minus_first"):
            top_profile = sort[0]
        else:
            top_number = "2"
            top_profile = sort[1]
        top_user = message.guild.get_member(top_profile.user_id)
        if top_user == None:
            await message.reply(f"Không tìm ra player top {top_number} để trừ điểm.\n")
            return
        for effect in word_matching_channel.player_effects:
            if effect.user_id == top_user.id:
                target_player_effect = effect
                break
        if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
            text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {top_user.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
            #Vô hiệu hoá
            if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                #Phản lại kỹ năng
                db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=-special_item.point)
                text_reply += f"{message.author.mention} bị trừ {special_item.point} điểm!"
                if target_player_effect.effect_id.startswith("dc"):
                    #Cướp luôn kỹ năng
                    db.update_player_special_item_word_matching_info(user_id=top_user.id, user_name=top_user.name, user_display_name=top_user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                    text_reply += f" và đã bị **{top_user.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
            await message.reply(text_reply)
            #xoá khỏi inven của player
            db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
            #Xoá hiệu ứng khỏi target user
            db.update_player_effects_word_matching_info(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=top_user.id, user_name=top_user.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            return
        db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= top_user.id, user_name=top_user.name,user_display_name=top_user.display_name, point=-special_item.point)
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để trừ {special_item.point} điểm của {top_user.mention}.\n")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return

    elif special_item.item_id.endswith("steal_skill") or special_item.item_id.endswith("del_skill"):
        #Lấy ra ngẫu nhiên skill trong bộ skils của đối thủ
        selected_player = None
        for player in word_matching_channel.player_profiles:
            if player.user_id == user_target.id:
                selected_player = player
                break
        if selected_player == None:
            await message.reply(f"Không tìm được user này trong bảng xếp hạng.")
            return
        elif selected_player.special_items == None or len(selected_player.special_items) == 0:
            await message.reply(f"Đối phương không có bất kỳ kỹ năng đặc biệt nào cả.")
            return
        if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
            text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {user_target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
            #Vô hiệu hoá
            if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                #Chỉ cướp kỹ năng
                db.update_player_special_item_word_matching_info(user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                text_reply += f" **{user_target.display_name}** đã cướp mất kỹ năng **`{special_item.item_name}`**!"
            await message.reply(text_reply)
            #xoá khỏi inven của player
            db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
            #Xoá hiệu ứng khỏi target user
            db.update_player_effects_word_matching_info(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=user_target.id, user_name=user_target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            return
        
        random_item = random.choice(selected_player.special_items)
        action = "xoá"
        if special_item.item_id.endswith("steal_skill"): 
            action = "cướp"
            #Thêm cái random item kia cho user
            db.update_player_special_item_word_matching_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= random_item)
        #xoá random item kia ra khỏi inven của user target
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= random_item)
        #xoá skill đã dùng khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để {action} kỹ năng **`{random_item.item_name}`** của {user_target.mention}.\n")
        return

    #Những kỹ năng có id chứa chữ "_random_skill_"
    #Đây là những kỹ năng đổi điểm lấy skill
    elif special_item.item_id.endswith("random_skill_dc") or special_item.item_id.endswith("random_skill_cc"):
        random_skill = None
        if special_item.item_id.endswith("dc"):
            random_skill = random.choice(WordMatchingClass.list_special_items_dang_cap)
        else:
            random_skill = random.choice(WordMatchingClass.list_special_items_cap_cao)
        #Thêm cái random item kia cho user
        db.update_player_special_item_word_matching_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= random_skill)
        #Skill này yêu cầu hy sinh điểm để đổi skill
        db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=-special_item.point)
        #xoá skill đã dùng khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để hy sinh {special_item.point} điểm, và nhận được kỹ năng **`{random_skill.item_name}`**.\n")
        return
    
    #Những kỹ năng có id tận cùng là _minus hoặc _add
    #Đây là những kỹ năng trừ điểm hoặc cộng điểm của đối thủ
    elif special_item.item_id.endswith("_minus") or special_item.item_id.endswith("_add"):
        is_minus = special_item.item_id.endswith("_minus")
        if user_target == None and is_minus:
            await message.reply(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
            return
        if is_minus:
            if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {user_target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=-special_item.point)
                    text_reply += f"{message.author.mention} bị trừ {special_item.point} điểm."
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        db.update_player_special_item_word_matching_info(user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                        text_reply += f" và đã bị **{user_target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await message.reply(text_reply)
                #xoá khỏi inven của player
                db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                #Xoá hiệu ứng khỏi target user
                db.update_player_effects_word_matching_info(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=user_target.id, user_name=user_target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
                return
            db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= user_target.id, user_name=user_target.name,user_display_name=user_target.display_name, point=-special_item.point)
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để trừ {special_item.point} điểm của {user_target.mention}.\n")
        else:
            db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=special_item.point)
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cộng {special_item.point} điểm cho bản thân mình.\n")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    #Những kỹ năng có id tận cùng là _add_user
    #Đây là những kỹ năng cộng điểm cho đối thủ
    elif special_item.item_id.endswith("_add_user"):
        if user_target == None:
            await message.reply(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
            return
        elif user_target.id == message.author.id:
            await message.reply(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn.\n")
            return
        db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= user_target.id, user_name=user_target.name,user_display_name=user_target.display_name, point=special_item.point)
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cộng {special_item.point} điểm của {user_target.mention}.\n")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    #Những kỹ năng có id tận cùng là steal_point
    #Đây là những kỹ năng ăn cắp điểm của đối thủ
    elif special_item.item_id.endswith("_steal_point"):
        if user_target == None:
            await message.reply(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
            return
        elif user_target.id == message.author.id:
            await message.reply(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn.\n")
            return
        
        if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {user_target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=-special_item.point)
                    db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= user_target.id, user_name=user_target.name,user_display_name=user_target.display_name, point=special_item.point)
                    text_reply += f"{message.author.mention} đã bị cướp mất {special_item.point} điểm!"
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        db.update_player_special_item_word_matching_info(user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                        text_reply += f" và đã bị **{user_target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await message.reply(text_reply)
                #xoá khỏi inven của player
                db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                #Xoá hiệu ứng khỏi target user
                db.update_player_effects_word_matching_info(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=user_target.id, user_name=user_target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
                return
        
        if special_item.item_id == "ct_steal_point":
            #50% thất bại
            ran = random.randint(1, 2)
            if ran == 2:
                await message.reply(f"{message.author.mention} định dùng kỹ năng **`{special_item.item_name}`** để cướp điểm {user_target.mention} nhưng đã thất bại!\n")
                #xoá khỏi inven của player
                db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                return
        #cộng điểm player
        db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=special_item.point)
        #trừ điểm đối thủ
        db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= user_target.id, user_name=user_target.name,user_display_name=user_target.display_name, point=-special_item.point)
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cướp {special_item.point} điểm của {user_target.mention}.\n")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    #Những kỹ năng có id tận cùng là minus_all
    #Đây là những kỹ năng trừ điểm toàn bộ đối thủ
    elif special_item.item_id.endswith("minus_all"):
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để trừ {special_item.point} điểm cho toàn bộ đấu thủ!\n")
        db.update_all_players_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, point=-special_item.point, immune_user_id=message.author.id)
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    #Những kỹ năng có id chứa chữ "_swap_"
    #Đây là những kỹ năng cộng điểm lên top
    elif "_swap_" in special_item.item_id:
        #Tìm top player để cộng điểm bản thân lên
        sort = sorted(word_matching_channel.player_profiles, key=lambda x: x.points, reverse=True)
        for player in word_matching_channel.player_profiles:
            if player.user_id == message.author.id:
                curr_player = player
                break
        top_profile = None
        if special_item.item_id.endswith("2"): 
            #Lấy profile top 2 ra
            top_profile = sort[1]
        else:
            #Lấy profile top 3 ra
            top_profile = sort[2]
        if top_profile == None:
            await message.reply(f"Không tìm ra profile player top để dùng kỹ năng này.\n")
            return
        top_user = message.guild.get_member(top_profile.user_id)
        if top_user == None:
            await message.reply(f"Không tìm ra user để dùng kỹ năng.\n")
            return
        for effect in word_matching_channel.player_effects:
            if effect.user_id == top_user.id:
                target_player_effect = effect
                break
            
        if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
            text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {top_user.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
            #Vô hiệu hoá
            if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                #Phản lại kỹ năng
                db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=-special_item.point)
                text_reply += f"{message.author.mention} bị trừ {special_item.point} điểm!"
                if target_player_effect.effect_id.startswith("dc"):
                    #Cướp luôn kỹ năng
                    db.update_player_special_item_word_matching_info(user_id=top_user.id, user_name=top_user.name, user_display_name=top_user.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                    text_reply += f" và đã bị **{top_user.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
            await message.reply(text_reply)
            #xoá khỏi inven của player
            db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
            #Xoá hiệu ứng khỏi target user
            db.update_player_effects_word_matching_info(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=top_user.id, user_name=top_user.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            return
        
        #Lấy điểm của user_target ra và trừ điểm hiện tại của người chơi, đó sẽ là điểm cần cộng cho người chơi
        calc_point = top_profile.points -curr_player.points
        db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=calc_point)
        #User target bị trừ năm điểm
        db.update_player_point_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= top_user.id, user_name=top_user.name,user_display_name=top_user.display_name, point=-special_item.point)
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để thế vị trí của {top_user.mention}, và đối phương đã bị trừ {special_item.point} điểm.\n")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    #Những kỹ năng có id chứa chữ "_protect"
    #Đây là những kỹ năng bảo hộ, thêm vào danh mục player effect
    elif "_protect" in special_item.item_id:
        #Thêm vào db player_effect
        if special_item.item_id.endswith("protect_user"):
            if user_target == None:
                await message.reply(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                return
            if user_target.id == message.author.id:
                await message.reply(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn.\n")
                return
            db.update_player_effects_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=user_target.id, user_name=user_target.name, effect_id= "ct_protect", effect_name= "Bảo Hộ")
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để bảo vệ player {user_target.mention}.\n")
        else:    
            db.update_player_effects_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=message.author.id, user_name=message.author.name, effect_id= special_item.item_id, effect_name= special_item.item_name)
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** lên bản thân\n")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    
    #Những kỹ năng có id chứa chữ "_ban"
    #Đây là những kỹ năng khoá mõm player
    elif "_ban" in special_item.item_id:
        if user_target == None:
            await message.reply(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
            return
        elif user_target.id == message.author.id:
            await message.reply(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn. Muốn tự khoá mõm mình à?\n")
            return
        if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {user_target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    db.create_and_update_player_bans_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name, ban_remaining=special_item.point)
                    text_reply += f"{message.author.mention} đã bị khoá mõm trong {special_item.point} vòng chơi tiếp theo!"
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        db.update_player_special_item_word_matching_info(user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                        text_reply += f" và đã bị **{user_target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await message.reply(text_reply)
                #xoá khỏi inven của player
                db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                #Xoá hiệu ứng khỏi target user
                db.update_player_effects_word_matching_info(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=user_target.id, user_name=user_target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
                return
        #khoá mõm đối thủ
        db.create_and_update_player_bans_word_matching_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= user_target.id, user_name=user_target.name, ban_remaining=special_item.point)
        await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để khoá mõm {user_target.mention} trong {special_item.point} lượt chơi tiếp theo.\n")
        #xoá khỏi inven của player
        db.update_player_special_item_word_matching_info(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
    await message.reply(f"Darkie chưa hoàn thành kỹ năng **`{special_item.item_name}`** đâu nhé. Vui lòng đợi Darkie hoàn thiện bộ kỹ năng.")
    return

async def process_players_effects_functions(word_matching_channel: db.WordMatchingInfo, special_item: WordMatchingClass.SpecialItem, message: discord.Message, lan:str,user_target: discord.User = None):
    #Lấy ra player effect đầu tiên của target
    flag = False
    selected_player_effect: db.PlayerEffect = None
    for effect in word_matching_channel.player_effects:
        if effect.user_id == user_target.id:
            selected_player_effect = effect
            break
    if selected_player_effect == None:
        return flag
    
    
    return flag
def get_special_item_by_id(item_id: str):
    for data in WordMatchingClass.list_special_items_cap_thap:
        if data.item_id == item_id:
            return data
    for data in WordMatchingClass.list_special_items_cap_cao:
        if data.item_id == item_id:
            return data
    for data in WordMatchingClass.list_special_items_dang_cap:
        if data.item_id == item_id:
            return data
    for data in WordMatchingClass.list_special_items_toi_thuong:
        if data.item_id == item_id:
            return data
    return None

def danh_sach_ky_nang(word_matching_channel: db.WordMatchingInfo, user = discord.Member):
    embed = discord.Embed(title=f"Danh sách kỹ năng", description= f"Player: {user.mention}", color=0xC3A757)  # Yellowish color
    if word_matching_channel.player_profiles:
        word_matching_channel.player_profiles.sort(key=lambda x: x.points, reverse=True)
        matched = False
        list_effect = []
        for player_effect in word_matching_channel.player_effects:
            if player_effect.user_id == user.id:
                list_effect.append(player_effect.effect_name)
        
        for profile in word_matching_channel.player_profiles:
            if profile.user_id == user.id:
                matched = True
                if len(list_effect) > 0:
                    comma_separated_string = ', '.join(list_effect)
                    embed.add_field(name=f"", value= f"Hiệu ứng đặc biệt: **`{comma_separated_string}`**", inline=False)
                    embed.add_field(name=f"________________", value= f"")
                if profile.special_items:
                    for index_item, item in enumerate(profile.special_items):
                        embed.add_field(name=f"Kỹ năng {index_item+1}", value= f"Tên kỹ năng: *{item.item_name}*\nRank: {item.level} \n\nMô tả kỹ năng: {item.item_description}", inline=False)  # Single-line field
                        embed.add_field(name=f"________________", value= f"")
                else:
                    embed.add_field(name="", value= "Bạn không có kỹ năng đặc biệt nào cả.", inline=False)
                break
        if matched == False:
            embed.add_field(name="", value= "Bạn hãy nối từ trước đi đã.", inline=False)
    else:
        embed.add_field(name="", value= "Chưa có danh sách Player Profile.", inline=False)
    return embed


def find_player_profile_by_user_id(word_matching_channel: db.WordMatchingInfo, user_id = int):
    if word_matching_channel.player_profiles:
        for profile in word_matching_channel.player_profiles:
            if profile.user_id == user_id:
                return profile
        return None
    else:
        return None
#endregion   
#endregion



#region Bot Slash Commands

#region say command
@bot.tree.command(name = "say", description="Nói gì đó ẩn danh thông qua bot, có thể gắn hình ảnh và nhắn vào Channel khác")
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

#region jail command
@bot.tree.command(name="jail", description="Tống ai đó vào đại lao trong khoảng thời gian nhất định.", guild=discord.Object(id=1256987900277690470))
@discord.app_commands.choices(time_format=[
        Choice(name="Giây", value="second"),
        Choice(name="Phút", value="minute"),
        Choice(name="Giờ", value="hour"),
        Choice(name="Ngày", value="day"),
        Choice(name="Tuần", value="week"),
        Choice(name="Tháng", value="month"),
    ])
@app_commands.describe(user= "Người cần tống giam", duration= "Thời gian tống giam (nhập số)", time_format = "Thời gian tống giam (second, minute, hour, day, week, month)", reason="Lý do tống giam")
async def first_command(interaction: discord.Interaction, user : discord.Member, duration: int, time_format : str, reason : str):
    await interaction.response.defer()  # Defer the interaction early
    req_roles = ['Cai Ngục', 'Supervisor', 'Server Master', 'Moderator']
    jail_db = "jailed_user"
    has_required_role = any(role.name in req_roles for role in interaction.user.roles)
    if not has_required_role:
        await interaction.followup.send("Không đủ thẩm quyền để tống giam.")
        return
    if time_format not in ['second', 'minute', 'hour', 'day', 'month']:
        await interaction.followup.send("Sai định dạng thời gian. Chỉ dùng những từ sau: second, minute, hour, day, month.", ephemeral=True)
        return
    
    #Nếu là Bot thì lật ngược vị thế:
    temp_author = interaction.user 
    if user.bot:
        interaction.user = user
        user = temp_author
    
    # Calculate the end time
    end_time = datetime.now() + CustomFunctions.get_timedelta(duration, time_format)
    mordern_date_time_format = end_time.strftime(f"%d/%m/%Y %H:%M")
    # Save user's roles
    original_roles = [role for role in user.roles if not role.is_default() and not role.is_premium_subscriber()]
    stored_original_roles = []
    for role in original_roles:
        old_role = {
                        "role_id": role.id,
                        "role_name": role.name
                    }
        stored_original_roles.append(old_role)
    
    # Remove all roles and add jail role
    jail_role = discord.utils.get(user.guild.roles, name="Đáy Xã Hội")
    if not jail_role:
        jail_role = await user.guild.create_role(name="Đáy Xã Hội")

    user_info = UserInfo(
    user_id=user.id,
    user_name=user.name,
    user_display_name=user.display_name,
    reason= reason,
    jail_until= end_time,
    roles=stored_original_roles
    )
    
    
    #Tìm xem user này đã có chưa, chưa có thì insert
    search_user = db.find_user_by_id(user_info.user_id, jail_db)
    if search_user == None:
        #Insert
        db.create_user(user_info= user_info, chosen_collection= jail_db)
    else:
        #Update lại jail_until và reason
        updated_data = {"jail_until": end_time.isoformat(), "reason" :user_info.reason }
        db.update_guild_extra_info(guild_id=user_info.user_id, update_data= updated_data)
    
    try:
        for ori_role in original_roles:
            try:
                await user.remove_roles(ori_role)
            except Exception:
                continue
        await user.add_roles(jail_role)
    except Exception as e:
        print(e)
    # Create embed object
    embed = discord.Embed(title="Đại Lao Thẳng Tiến", description=f"Kẻ tội đồ {user.mention} đã bị {interaction.user.mention} bắt giữ và tống vào đại lao!", color=0x00FF00)  # Green color
    embed.add_field(name="Lý do bị tù đày:", value=reason, inline=False)  # Single-line field
    embed.add_field(name="Sẽ được ân xoá sau khoảng thời gian:", value=f"{duration} {time_format}", inline=False)
    embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
    embed.add_field(name="Ghi chú", value="Nếu quá thời hạn phạt tù mà chưa được ra tù thì hãy la làng lên nhé!", inline=False) 
    embed.set_footer(text=f"Đã bị tống giam bởi: {interaction.user.name}")  # Footer text

    await interaction.followup.send(f"Kẻ tội độ {user.mention} đã bị {interaction.user.mention} bắt giữ và sẽ bị tống vào đại lao. Kẻ tội đồ này chỉ được thả ra xã hội sau {duration} {time_format}. Lý do tống giam: {reason}")
    channel = bot.get_channel(1257012036718563380)
    if channel:
        await channel.send(content=f"{user.mention}",embed=embed)
    print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} jailed {user.display_name} for {duration} {time_format}. Reason: {reason}")
    commands_logger.info(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} jailed {user.display_name} for {duration} {time_format}. Reason: {reason}")
#endregion

#region unjail command
@bot.tree.command(name="unjail", description="Ân xá tội đồ ra khỏi đại lao ngay lập tức.", guild=discord.Object(id=1256987900277690470))
@app_commands.describe(user= "Người cần ân xá", reason = "Lý do tại sao ân xá")
async def unjail(interaction: discord.Interaction, user : discord.Member, reason : str):
    await interaction.response.defer()
    req_roles = ['Cai Ngục', 'Supervisor', 'Server Master', 'Moderator']
    jail_db = "jailed_user"
    has_required_role = any(role.name in req_roles for role in interaction.user.roles)
    if not has_required_role:
        await interaction.followup.send("Không đủ thẩm quyền để ân xá tội đồ.")
        return
    
    #Xoá role Đáy Xã Hội
    jail_role = discord.utils.get(user.guild.roles, name="Đáy Xã Hội")
    if jail_role:
        await user.remove_roles(jail_role)
    
    #Tìm xem user này đã có chưa, có thì xoá khỏi db jail_user
    search_user = db.find_user_by_id(user.id, jail_db)
    if search_user:
        #Restore lại roles cũ của user
        for role in search_user.roles:
            get_role_from_server = discord.utils.get(user.guild.roles, id = role["role_id"])
            if get_role_from_server:
                try:
                    await user.add_roles(get_role_from_server)
                except Exception:
                    continue
        #Xoá row khỏi database
        db.delete_user_by_id(user_id= user.id, chosen_collection= jail_db)
        # Create embed object
        mordern_date_time_format = datetime.now().strftime(f"%d/%m/%Y %H:%M")
        embed = discord.Embed(title="Ân Xá Khỏi Đại Lao", description=f"Kẻ tội đồ {user.mention} đã được {interaction.user.mention} ân xoá khỏi đại lao!", color=0x00FF00)  # Green color
        embed.add_field(name="Lý do được ân xá:", value=reason, inline=False)  # Single-line field
        embed.add_field(name="Thời gian ra đại lao:", value=f"{mordern_date_time_format}", inline=True)
        embed.add_field(name="Ghi chú", value="Nhớ đừng vi phạm để bị tống vài đại lao nữa nhé!", inline=False) 
        embed.set_footer(text=f"Đã được ân xoá bởi: {interaction.user.name}")  # Footer text

        await interaction.followup.send(f"Kẻ tội độ {user.mention} đã được {interaction.user.mention} ân xá đại lao. Mong thần dân đừng vi phạm để thành kẻ tội đồ nữa. Lý do ân xá: {reason}")
        channel = bot.get_channel(1257012036718563380)
        if channel:
            await channel.send(embed=embed)
    else:
        await interaction.followup.send(f"Người này không ở trong tù.", ephemeral=True)
    print(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} unjailed {user.display_name}. Reason: {reason}")
    commands_logger.info(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} unjailed {user.display_name}. Reason: {reason}")
#endregion

#region delete_message command
@bot.tree.command(name="delete_message", description="Xoá một hoặc nhiều tin nhắn bất kỳ.", guild=discord.Object(id=1256987900277690470))
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
@bot.tree.command(name="report", description="Báo cáo user vi phạm luật về cho admin và moderator xem xét.", guild=discord.Object(id=1256987900277690470))
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
            commands_logger.info(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} report user id: {user.id} with Username {user.name}.")
        else:
            await interaction.followup.send(f"<@315835396305059840> Bot không tìm được channel để gửi báo cáo!")
    except Exception as e:
        #Tag bản thân
        await interaction.followup.send(f"<@315835396305059840> Bot gặp exception trong lúc thực hiện lệnh. Exception: {str(e)}. Vui lòng liên hệ Darkie!", ephemeral=True)
        commands_logger.info(f"Username {interaction.user.name}, Display user name {interaction.user.display_name} tried report user id {user.id} but got exception {str(e)}.")
#endregion


#region Snipe command
@bot.tree.command(name="snipe", description="Hiện lại message mới nhất vừa bị xoá trong channel này.")
async def snipe(interaction: discord.Interaction):
    await interaction.response.defer()
    called_channel = interaction.channel
    
    snipe_channel_info = db.find_snipe_channel_info_by_id(called_channel.id, interaction.guild.id)
    if snipe_channel_info:
        # list_snipe_message = []
        # for mess in snipe_channel_info.snipe_messages:
        #     list_snipe_message.append(mess.to_dict)
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
        message = await interaction.followup.send(embed=view.embed, view=view, files=temp_files)
        view.discord_message = message
        await view.countdown()
    else:
        await interaction.followup.send(f"Chưa có dữ liệu snipe cho channel {interaction.channel.mention}. Vui lòng thử lại sau.")
#endregion

#region Bảng Xếp Hạng Nối Từ
@bot.tree.command(name="bxh_noi_tu", description="Hiện bảng xếp hạng những người chơi nối từ trong channel này.")
@app_commands.describe(user="Chọn user cần muốn xem cụ thể xếp hạng")
async def bxh_noi_tu(interaction: discord.Interaction, user: Optional[discord.Member] = None):
    await interaction.response.defer()
    called_channel = interaction.channel
    #Kiểm tra xem ở đây là bảng channel nối từ hay không
    word_matching_channel = db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'en')
    if word_matching_channel:
        embed = get_bxh_noi_tu(interaction=interaction, lan='en',word_matching_channel=word_matching_channel, user_mention=user)
        await interaction.followup.send(embed= embed)
    else:
        word_matching_channel= db.find_word_matching_info_by_id(channel_id= called_channel.id, guild_id= called_channel.guild.id, language= 'vn')
        if word_matching_channel:
            embed = get_bxh_noi_tu(interaction=interaction, lan='vn',word_matching_channel=word_matching_channel, user_mention=user)
            await interaction.followup.send(embed= embed)
        else:
            await interaction.followup.send(f"Đây không phải là channel dùng để chơi nối từ. Chỉ dùng lệnh này trong channel chơi nối từ thôi!")


def get_bxh_noi_tu(interaction: discord.Interaction,lan: str, word_matching_channel: db.WordMatchingInfo, user_mention: Optional[discord.Member] = None):
    if lan == 'en' or lan == 'eng':
        lan = "Tiếng Anh"
    elif lan == 'vn':
        lan = "Tiếng Việt"
    embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Trò Chơi Nối Từ {lan}", color=0x03F8FC)
    embed.add_field(name=f"", value="___________________", inline=False)
    embed.add_field(name=f"", value=f"Round thứ: **{word_matching_channel.current_round}**", inline=False)
    count = 0
    if word_matching_channel.player_profiles:
        word_matching_channel.player_profiles.sort(key=lambda x: x.points, reverse=True)
        if user_mention == None:
            for index, profile in enumerate(word_matching_channel.player_profiles):
                user = interaction.guild.get_member(profile.user_id)
                if user != None and (profile.points!= 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.points}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 15: break
        else:
            matched = False
            for index, profile in enumerate(word_matching_channel.player_profiles):
                if profile.user_id == user_mention.id:
                    user = interaction.guild.get_member(profile.user_id)
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.points}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    #Show kỹ năng luôn
                    if profile.special_items:
                        embed.add_field(name=f"________________", value= f"")
                        for index_item, item in enumerate(profile.special_items):
                            target_require = "Có" if item.required_target else "Không"
                            embed.add_field(name=f"Kỹ năng {index_item+1}", value= f"Tên kỹ năng: *{item.item_name}*\nRank: {item.level} \n\nMô tả kỹ năng: {item.item_description}", inline=False)  # Single-line field
                            embed.add_field(name=f"________________", value= f"")
                    matched = True
                    break
            if matched == False:
                embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi này*", inline=False)     
    else:
        embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi*", inline=False)       
    embed.add_field(name=f"", value="___________________", inline=False)
    return embed     
#endregion


#endregion

#endregion


# Task: Check jail expiry
@tasks.loop(seconds=30)
async def check_jail_expiry():
    now = datetime.now()
    jail_db = "jailed_user"
    #Lấy tất cả dữ liệu db jail user ra
    list_all_jailed_users = db.find_all_users(chosen_collection=jail_db)
    guild = bot.get_guild(1256987900277690470)
    if list_all_jailed_users:
        for jail_user in list_all_jailed_users:
                #Lấy thời hạn tù đày
                jailed_time = (jail_user.jail_until)
                if jailed_time > now:
                    continue
                user = guild.get_member(jail_user.user_id)
                if user:
                    #Xoá role Đáy Xã Hội
                    jail_role = discord.utils.get(user.guild.roles, name="Đáy Xã Hội")
                    if jail_role == None: return
                    await user.remove_roles(jail_role)
                    #Tìm xem user này đã có chưa, có thì xoá khỏi db jail_user
                    search_user = db.find_user_by_id(jail_user.user_id, jail_db)
                    if search_user == None: return
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
                    commands_logger.info(f"Bot {bot.user} automatically unjailed {user.display_name} for time is up")
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
                model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
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


@tasks.loop(hours=12)
async def clear_up_data_task():
    guilds = bot.guilds
    for guild in guilds:
        #Kiểm tra quest cũ, xóa đi nếu cần
        all_quest_data = QuestMongoManager.find_all_profiles(guild_id=guild.id)
        if all_quest_data != None:
            count = 0
            for quest in all_quest_data:
                if datetime.now() > quest.reset_date: 
                    QuestMongoManager.delete_quest(guild_id=guild.id, user_id=quest.user_id)
                    count+=1
            print(f"clear_up_data_task started. Deleted {count} quest data in guild {guild.name}")
        #Drop quest collection nếu trống
        QuestMongoManager.drop_quest_collection_if_empty(guild_id=guild.id)
        #Kiểm tra snipe message cũ, xóa đi nếu cần
        all_snipe_channels = db.find_all_snipe_channel_info(guild_id=guild.id)
        if all_snipe_channels != None:
            count = 0
            for snipe_channel in all_snipe_channels:
                if snipe_channel.snipe_messages != None and len(snipe_channel.snipe_messages) > 0:
                    #Xóa bớt message
                    snipe_messages = snipe_channel.snipe_messages
                    for deleted_mess in snipe_messages:
                        date_deleted = deleted_mess.deleted_date
                        overdue_date = date_deleted + timedelta(weeks=2)
                        if datetime.now() > overdue_date:
                            snipe_messages.remove(deleted_mess)
                            count+=1
                    db.replace_snipe_message_info(guild_id=guild.id, channel_id=snipe_channel.channel_id, snipe_messages=snipe_messages)
                    print(f"clear_up_data_task started. Deleted {count} snipe message in {guild.name}")
                else:
                    #Xóa channell
                    db.delete_snipe_channel_info(guild_id=guild.id, channel_id=snipe_channel.channel_id)
        #drop collection nếu trống
        db.drop_snipe_channel_info_collection_if_empty(guild_id=guild.id)


#region Response AI
async def sub_function_ai_response(message: discord.Message, speakFlag = True):
    if speakFlag == False: return
    if message.channel.id == 1269029322950180977 or message.channel.id == 1259237810653626440 or message.channel.id == 1259242009290477618 or message.channel.id == 1287118424874684530: return #Không cho bot nói chuyện ở những channel sau
    bots_creation1_name = ["creation 1", "creation số 1", "creation no 1", "creation no. 1"]
    if message.reference is not None and message.reference.resolved is not None:
        if message.reference.resolved.author == bot.user or CustomFunctions.contains_substring(message.content.lower(), bots_creation1_name):
            if message.guild.id != 1256987900277690470 and message.guild.id != 1194106864582004849: #Chỉ True Heaven, học viện 2ten mới không bị dính
                if CustomFunctions.is_inside_working_time() == False:
                    await message.channel.send(f"Tính năng AI của Bot chỉ hoạt động đến 12h đêm, vui lòng đợi đến 8h sáng hôm sau.")
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
                prompt = await CustomFunctions.get_proper_prompt(message,"Creation 1", referenced_message)
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
                #Nếu là bot thì đương nhiên không reply, chỉ nhắn bình thường thôi
                if(message.author.id == CustomFunctions.user_cr_1["user_id"] or message.author.id == CustomFunctions.user_cr_2["user_id"] or message.author.id == CustomFunctions.user_cr_3["user_id"]):
                    await message.channel.send(f"{message.author.mention} {bot_response}")
                else:
                    await message.reply(f"{bot_response}")
                CustomFunctions.save_user_convo_data(message=message, bot_reponse= bot_response, bot_name= "Creation 1")
                print(f"Username {message.author.name}, Display user name {message.author.display_name} replied {bot.user}")
                interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} replied {bot.user}")
            
    elif CustomFunctions.contains_substring(message.content.lower(), bots_creation1_name):
        async with message.channel.typing():
            if message.guild.id != 1256987900277690470 and message.guild.id != 1194106864582004849: #Chỉ True Heaven, học viện 2ten mới không bị dính
                if CustomFunctions.is_inside_working_time() == False:
                    await message.channel.send(f"Tính năng AI của Bot chỉ hoạt động đến 12h đêm, vui lòng đợi đến 8h sáng hôm sau.")
                    return
            flag, mess = await CustomFunctions.check_message_nsfw(message, bot)
            if flag != 0:
                await message.channel.send(mess)
                interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} violated chat when talking to {bot.user}")
                interaction_logger.info(f"Username {message.author.name} violated chat {message.content} when talking to {bot.user}")
            else:
                model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
                prompt = await CustomFunctions.get_proper_prompt(message,"Creation 1")
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
                await message.channel.send(f"{message.author.mention} {bot_response}")
                CustomFunctions.save_user_convo_data(message=message, bot_reponse= bot_response, bot_name= "Creation 1")
                print(f"Username {message.author.name}, Display user name {message.author.display_name} directly call {bot.user}")
                interaction_logger.info(f"Username {message.author.name}, Display user name {message.author.display_name} directly call {bot.user}")
    return

#region Word Matching
async def word_matching(message: discord.Message):
    if str.isspace(message.content): return
    if message.author.bot: return
    word_matching_channel = db.find_word_matching_info_by_id(channel_id= message.channel.id, guild_id= message.guild.id, language= 'en')
    lan = 'en'
    if word_matching_channel == None:
        word_matching_channel = db.find_word_matching_info_by_id(channel_id= message.channel.id, guild_id= message.guild.id, language= 'vn')
        if word_matching_channel == None:
            return
        lan = 'vn'
    if lan == 'en' and len(message.content.split()) > 1: return
    if message.content[0] not in string.punctuation and message.content[0] != ":":
        #Kiểm xem nằm đúng channel không
        point = 1
        if word_matching_channel.special_point != None and word_matching_channel.special_point > 0:
            point = word_matching_channel.special_point
        selected_ban = None
        for player_ban in word_matching_channel.player_bans:
                if player_ban.user_id == message.author.id and player_ban.ban_remaining>0:
                    selected_ban = player_ban
                    break
        #Bắt đầu chơi
        message_tu_hien_tai = f"\nTừ hiện tại là: `'{word_matching_channel.current_word}'`, và có **{word_matching_channel.remaining_word if word_matching_channel.remaining_word else 0}** bắt đầu bằng chữ cái `{word_matching_channel.last_character if word_matching_channel.last_character else 0}`"
        if selected_ban:
            await message.reply(f"Bạn đã bị khoá mõm trong vòng **{selected_ban.ban_remaining}** lượt chơi tới. Vui lòng chờ đi.\nOwner server có thể dùng lệnh `!wm_give_ban {message.author.mention} 0` để mở khoá giam")
            return
        if word_matching_channel.current_player_id == message.author.id:
            await message.reply(f"Bạn đã nối từ rồi, vui lòng né qua để cho người khác chơi đi. {message_tu_hien_tai}")
            if message_tracker.add_message(user_id= message.author.id, channel_id= message.channel.id, content= "spam nối từ"): #Đánh dấu những đối tượng thích spam
                #Ban 5 vòng
                db.create_and_update_player_bans_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language= lan, user_id= message.author.id, user_name=message.author.name, ban_remaining=5)
                await message.reply(f"{message.author.mention} đã spam quá nhiều và bị khoá mõm trong vòng **5** lượt chơi tiếp theo!")
                print(f"Player {message.author.name} is banned 5 round from world matching game for spamming")
                message_tracker.clear_user_messages(user_id=message.author.id, channel_id=message.channel.id)
            return
        #Kiểm tra xem content có chứa first character là last character của current word không
        elif word_matching_channel.special_case == False and message.content.lower()[0] != word_matching_channel.last_character:
            await matching_words_fail(err= f"Từ mới phải bắt đầu bằng chữ cái `'{word_matching_channel.last_character}'` mới được nha.", message=message, word_matching_channel=word_matching_channel,lan=lan,point=point)
        #Kiểm tra xem content có chứa nguyên từ đầu là last character của current word không
        elif word_matching_channel.special_case == True and message.content.lower().split()[0] != word_matching_channel.last_character:
            await matching_words_fail(err= f"Từ mới phải bắt đầu bằng chữ cái `'{word_matching_channel.last_character}'` mới được nha.", message=message, word_matching_channel=word_matching_channel,lan=lan,point=point)
        #Kiểm xem content có nằm trong list từ đã nối rồi chưa
        elif message.content.lower() in word_matching_channel.used_words:
            await matching_words_fail(err= f"Từ `{message.content}` đã có người nối rồi bạn ơi.", message=message, word_matching_channel=word_matching_channel,lan=lan,point=point)
        #Kiểm tra xem từ này có tồn tại không
        elif lan == 'en' and message.content.lower() not in english_words_dictionary.keys():
            await matching_words_fail(err= f"Từ `{message.content}` không nằm trong từ điển.", message=message, word_matching_channel=word_matching_channel,lan=lan,point=point)
        elif lan == 'vn' and message.content.lower() not in vietnamese_dict.keys():
            await matching_words_fail(err= f"Từ `{message.content}` không nằm trong từ điển.", message=message, word_matching_channel=word_matching_channel,lan=lan,point=point)
        else:
            if word_matching_channel.current_round>=1200:
                #Reset
                await message.channel.send(f"Đã chơi được 1200 round rồi. Cảm ơn mọi người đã chơi nhé. Đến lúc reset lại rồi, nên mọi người bắt đầu lại nhé!")
                await process_reset_word_matching(message=message, word_matching_channel=word_matching_channel, language=lan)
                return
            #Coi như pass hết
            await message.add_reaction('👍')
            #Nếu trong game việt nam, gặp những từ có đuôi như sau thì đánh special case để xử lý tiếp
            special_words = ["à", "ả","ã", "ạ", "ẳ", "ẵ","ặ", "ẫ", "ẩ", "ậ", "õ", "ẽ", "ó", "ọ", "ờ","ớ", "ỡ", "ỗ", "ĩ", "ỉ","í", "ị", "ì", "ũ", "ỹ", "ỳ", "ỵ", "ử", "ự", "ộ","ẻ","è", "ể", "ề", "ễ", "ệ", "ẹ", "ợ", "ữ"]
            special_case = False
            if lan == 'vn' and message.content[-1].lower() in special_words:
                special_case = True
            #Cập nhật lại thông tin
            db.update_data_word_matching_info(language=lan,channel_id=message.channel.id, guild_id= message.guild.id, current_player_id=message.author.id, current_player_name=message.author.name,current_word=message.content.lower(), special_case_vn=special_case)
            db.update_player_point_word_matching_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan)
            word_matching_channel = db.find_word_matching_info_by_id(channel_id= message.channel.id, guild_id= message.guild.id, language=lan)
            ProfileMongoManager.update_level_progressing(guild_id=message.guild.id, user_id=message.author.id)
            if word_matching_channel.remaining_word>0:
                message_tu_hien_tai = f"\nTừ hiện tại là: `'{word_matching_channel.current_word}'`, và có **{word_matching_channel.remaining_word if word_matching_channel.remaining_word else 0}** từ bắt đầu bằng chữ cái `{word_matching_channel.last_character if word_matching_channel.last_character else 0}`"
                #Kiểm tra xem có special_item không, nếu có thì cộng cho player
                chuc_mung_item = ""
                if word_matching_channel.special_item:
                    db.update_player_special_item_word_matching_info(user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= point, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= word_matching_channel.special_item)
                    chuc_mung_item = f" và nhận được kỹ năng **{word_matching_channel.special_item.item_name}**. Nhớ đừng quên sử dụng nó nhé"
                #Trả lời đúng thì reset special_points và special_item lại từ đầu, cập nhật lại list player ban
                await message.channel.send(f"Hay lắm {message.author.mention}, bạn đã được cộng {point} điểm{chuc_mung_item}. Để kiểm tra điểm số của mình thì hãy dùng lệnh /bxh_noi_tu nhé. {message_tu_hien_tai}")
                db.update_special_point_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
                db.update_special_item_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
                db.reduce_player_bans_word_matching_info_after_round(channel_id= message.channel.id, guild_id= message.guild.id, language=lan)
            elif word_matching_channel.remaining_word==0:
                #reset lại
                await message.channel.send(f"Kinh nhờ, chơi hết từ khả dụng rồi. Cảm ơn mọi người đã chơi nhé. Đến lúc reset thông tin từ rồi. Mọi người bắt đầu lại nhé!")
                await process_reset_word_matching(message=message, word_matching_channel=word_matching_channel, language=lan)
            message_tracker.clear_user_messages(user_id=message.author.id, channel_id=message.channel.id)
        #Xổ số nếu chưa có special point
        so_xo = random.randint(4, 10)
        #Nếu sổ xố rơi trúng số 5 thì coi như cộng point lên x2, x3, x4 ngẫu nhiên
        if so_xo == 10:
            x_value = random.randint(2, 5)
            special_point_english = 1*x_value
            db.update_special_point_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= special_point_english)
            text_cong_point = f"\n**Cơ hội chỉ đến một lần duy nhất, nếu ai thắng nhận được {special_point_english} điểm nhaaa! Cơ hội duy nhất, duy nhất, suy nghĩ kỹ trước khi trả lời!**\n"
            await message.channel.send(f"{text_cong_point}")
        else:
            #Sổ xố xem trúng kỹ năng đặc biệt không
            so_xo = random.randint(3, 10)
            if so_xo == 10:
                text_cong_skill = f"\n**Cơ hội chỉ đến một lần duy nhất, nếu ai thắng nhận được kỹ năng đặc biệt bên dưới! Cơ hội duy nhất thôi!**\n"
                percent = random.randint(0, 100)
                item = None
                if percent >= 0 and percent < 55:
                    #Cấp thấp
                    item = random.choice(WordMatchingClass.list_special_items_cap_thap)
                elif percent >= 55 and percent < 80:
                    #Cấp cao
                    item = random.choice(WordMatchingClass.list_special_items_cap_cao)
                elif percent >= 80 and percent < 95:
                    #Đẳng cấp
                    item = random.choice(WordMatchingClass.list_special_items_dang_cap)
                else:
                    #tối thượng
                    item = random.choice(WordMatchingClass.list_special_items_toi_thuong)
                result = db.update_special_item_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item=item)
                embed = discord.Embed(title=f"Kỹ năng đặc biệt. Rank: {item.level}", description=f"", color=0x03F8FC)
                embed.add_field(name=f"", value=f"Mã kỹ năng: {item.item_id}", inline=False)
                embed.add_field(name=f"", value=f"Tên kỹ năng: {item.item_name}", inline=False)
                embed.add_field(name=f"", value=f"Mô tả kỹ năng: {item.item_description}", inline=False)
                await message.channel.send(content=text_cong_skill, embed=embed)
                return


async def matching_words_fail(message: discord.Message, err: str, word_matching_channel: db.WordMatchingInfo, lan: str, point: int):
    #Reset special point nếu trả lời sai, và nếu trước đó đã có
    message_tu_hien_tai = f"\nTừ hiện tại là: `'{word_matching_channel.current_word}'`, và có **{word_matching_channel.remaining_word if word_matching_channel.remaining_word else 0}** từ bắt đầu bằng chữ cái `{word_matching_channel.last_character if word_matching_channel.last_character else 0}`"
    if word_matching_channel.special_point:
        db.update_special_point_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_point= 0)
    if word_matching_channel.special_item:
        db.update_special_item_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language=lan, special_item= None)
    if message_tracker.add_message(user_id= message.author.id, channel_id= message.channel.id, content= "spam nối từ"): #Đánh dấu những đối tượng thích spam
        #Ban 5 vòng
        db.create_and_update_player_bans_word_matching_info(channel_id= message.channel.id, guild_id= message.guild.id, language= lan, user_id= message.author.id, user_name=message.author.name, ban_remaining=5)
        await message.reply(f"{message.author.mention} đã spam quá nhiều và bị khoá mõm trong vòng **5** lượt chơi tiếp theo!")
        print(f"Player {message.author.name} is banned 5 round from world matching game for spamming")
        message_tracker.clear_user_messages(user_id=message.author.id, channel_id=message.channel.id)
        return
    await message.add_reaction('❌')
    await message.reply(f"{err} {message_tu_hien_tai}")


client = discord.Client(intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    interaction_logger.info(f"Successfully logged in as {bot.user}")
    check_jail_expiry.start()
    if CustomFunctions.check_if_dev_mode()==False:
        automatic_speak_randomly.start()
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
    if before.guild.id != 1256987900277690470: return
    
    model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
    channel = bot.get_channel(1259392446987632661)
    await CustomFunctions.thanking_for_boost(bot_name="creation 1", before=before, after=after, model=model, channel=channel)
    
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
    db.drop_word_matching_info_collection(guild_id=guild.id)
    SwMongoManager.drop_word_matching_info_collection(guild_id=guild.id)
    print(f"Bot {bot.user.display_name} removed from guild {guild.name}. Deleted all related collection")
    
#Khi có người bị banned
@bot.event
async def on_member_ban(guild: discord.Guild, user: discord.Member):
    #Tạm thời không cần chạy trong server khác
    if guild.id != 1256987900277690470: return
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
    sort_word_game = SwHandling.SwHandlingFunction(message= message, message_tracker=message_tracker)
    sw_info, lan = await sort_word_game.check_if_message_inside_game(source=message)
    if sw_info != None:
        #Xử lý nối từ
        asyncio.create_task(sort_word_game.handling_game(message=message))
        speakFlag = False
    
    guild_extra_info = db.find_guild_extra_info_by_id(guild_id=message.guild.id)
    if guild_extra_info != None and message.channel.id == guild_extra_info.therapy_channel and message.author.bot == False:
        #Xử lý therapy
        model = genai.GenerativeModel('gemini-1.5-flash', CustomFunctions.safety_settings)
        asyncio.create_task(TherapyHandling(bot=bot, model=model).handling_therapy_ai(message=message))
        speakFlag = False
    if guild_extra_info != None and guild_extra_info.custom_parameter_2 != None and message.channel.id == guild_extra_info.custom_parameter_2: #Hiện tại chỉ có true heaven có
        speakFlag = False
        #sticky message
        await StickyMessageHandling(bot=bot).handling_sticky_message(message=message)
    asyncio.create_task(word_matching(message=message))
    
    word_matching_channel_en = db.find_word_matching_info_by_id(channel_id= message.channel.id, guild_id= message.guild.id, language= 'en')
    word_matching_channel_vn = db.find_word_matching_info_by_id(channel_id= message.channel.id, guild_id= message.guild.id, language= 'vn')
    if word_matching_channel_en != None or word_matching_channel_vn!= None:
        speakFlag = False
    
    ai_handling_response = AIResponseHandling(bot=bot)
    await ai_handling_response.sub_function_ai_response(message=message, speakFlag=speakFlag)
    
    await bot.process_commands(message)

bot_token = os.getenv("BOT_TOKENN")
english_words_dictionary = CustomFunctions.english_dict
vietnamese_dict = CustomFunctions.vietnamese_dict
message_tracker = CustomFunctions.MessageTracker()
#Cog command
init_extension = [
                  "cogs.games.SortWordCog",
                  "cogs.games.TruthDareCog",
                  "cogs.misc.TherapyAICog",
                  "cogs.misc.TrueHeavenCustomCommandsCog",
                  "cogs.misc.HelpCog",
                  "cogs.misc.DonationCog",
                  "cogs.misc.DDCNCustomCommandsCog",
                  ]
bot.tree.add_command(delete_message_context)
bot.run(bot_token)