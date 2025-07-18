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
from Handling.Economy.Global import GlobalMongoManager
import db.DbMongoManager as db
from db.DbMongoManager import UserInfo, GuildExtraInfo
import random
import CustomButton
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
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
import Handling.MiniGame.RockPaperScissor.RpsMongoManager as RpsMongoManager
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from Handling.Economy.GA.GaDugeonView import GaDugeonView
from Handling.Economy.Quest.DungeonQuestChannelClass import DungeonQuestChannel
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from Handling.Misc.AIResponse import AIResponseHandling

load_dotenv()
intents = discord.Intents.all()
intents.presences = False
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
                model = genai.GenerativeModel(CustomFunctions.AI_MODEL, CustomFunctions.safety_settings)
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
            embed.set_footer(text=f"Hộp quà sẽ xuất hiện ngẫu nhiên, và khi thấy thì nhớ nhanh tay nhé!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            print(f"Created random dropbox at channel {quest_channel.name} in guild {guild.name}.")
            view = RandomDropboxEconomyView()
            m = await quest_channel.send(embed=embed, view=view)
            view.old_message = m
            
@tasks.loop(hours=1, minutes = 10)
async def random_quizz_embed():
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
            embed.set_footer(text=f"Hỏi Nhanh Có Thưởng sẽ xuất hiện ngẫu nhiên, và khi thấy thì nhớ trả lời đúng nhé!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            print(f"Created random quizz at channel {quest_channel.name} in guild {guild.name}.")
            m = await quest_channel.send(embed=embed, view=view)
            view.old_message = m

@tasks.loop(hours=12)
async def love_point_rank_reducing_task():
    guilds = bot.guilds
    for guild in guilds:
        #Kiểm tra couple info của server, nếu có thì mới chọn
        couples_in_guild = CoupleMongoManager.find_all_couples(guild_id=guild.id)
        if couples_in_guild == None: continue
        for couple in couples_in_guild:
            if couple.love_point <= 0:
                old_love_progressing = couple.love_progressing
                calculated_love_progressing = old_love_progressing - 150
                if calculated_love_progressing <= 0: calculated_love_progressing =  0
                CoupleMongoManager.set_love_progressing_value(guild_id=guild.id, user_id=couple.first_user_id, love_progressing=calculated_love_progressing)
            elif couple.love_point <= 50:
                old_love_progressing = couple.love_progressing
                calculated_love_progressing = old_love_progressing - 100
                if calculated_love_progressing <= 0: calculated_love_progressing =  0
                CoupleMongoManager.set_love_progressing_value(guild_id=guild.id, user_id=couple.first_user_id, love_progressing=calculated_love_progressing)
            elif couple.love_point < 90:
                old_love_progressing = couple.love_progressing
                calculated_love_progressing = old_love_progressing - 50
                if calculated_love_progressing <= 0: calculated_love_progressing =  0
                CoupleMongoManager.set_love_progressing_value(guild_id=guild.id, user_id=couple.first_user_id, love_progressing=calculated_love_progressing)
            couple.love_point -= 10
            if couple.love_point <= 0: couple.love_point = 0
            CoupleMongoManager.set_love_point_value(guild_id=guild.id, user_id=couple.first_user_id, love_point=couple.love_point)
            if couple.love_rank == 20: continue
            two_weeks_ago = datetime.now() - timedelta(weeks=2)
            two_weeks_after = datetime.now() + timedelta(weeks=2)
            delete_check = 0
            if couple.last_fight_action == None and couple.last_love_action == None: delete_check +=1
            if couple.last_love_action != None and couple.last_love_action + timedelta(weeks=2) < datetime.now(): delete_check +=1
            if couple.last_fight_action != None and couple.last_fight_action + timedelta(weeks=2) < datetime.now(): delete_check +=1
            if couple.love_point == 0: delete_check +=1
            if couple.love_point == 0 and couple.love_progressing == 0: delete_check +=1
            #Mới tạo trong vòng 2 tuần không cần check
            if couple.date_created + timedelta(weeks=2) > datetime.now(): delete_check -=2
            if couple.love_rank == 20: delete_check = -99
            #Nếu đạt trên ba tiêu chí trên thì xoá
            if delete_check >= 3:
                CoupleMongoManager.delete_couple_by_id(guild_id=guild.id, user_id=couple.first_user_id)
                print(f"Check delete for couple id {couple.first_user_id} reached. Is deleted")

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
        #Drop quest collection
        QuestMongoManager.drop_quest_collection_if_empty(guild_id=guild.id)

        #Kiểm tra snipe message cũ, xóa đi nếu cần
        all_snipe_channels = db.find_all_snipe_channel_info(guild_id=guild.id)
        count = 0
        if all_snipe_channels != None:
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
                else:
                    #Xóa channell
                    db.delete_snipe_channel_info(guild_id=guild.id, channel_id=snipe_channel.channel_id)
        print(f"clear_up_data_task started. Deleted {count} snipe message in {guild.name}")
        #drop collection khi trống
        db.drop_snipe_channel_info_collection_if_empty(guild_id=guild.id)
        
        count = 0
        all_global_inventories = GlobalMongoManager.find_all_global_items()
        if all_global_inventories:
            for global_inventory in all_global_inventories:
                if global_inventory.date_updated + timedelta(weeks=24) < datetime.now():
                    #Xóa
                    GlobalMongoManager.delete_global_item_by_user_id(user_id=global_inventory.user_id)
                    count+=1
        print(f"clear_up_data_task started. Deleted {count} global inventory due to in-active")

@tasks.loop(minutes = 13)
async def dungeon_spawn_enemy_embed():
    guilds = bot.guilds
    for guild in guilds:
        is_inside_disable_time = UtilitiesFunctions.is_within_time_range()
        #Không chạy trong khoảng thời gian trên, trừ server True Heavens
        if is_inside_disable_time and guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
        if CustomFunctions.check_if_dev_mode()==True and guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value and guild.id != 1293554240593330241: continue
        #Kiểm tra quest channel của server, nếu có thì mới chọn
        guild_info = db.find_guild_extra_info_by_id(guild_id=guild.id)
        if guild_info == None: continue
        if guild_info.list_channels_dungeon == None or len(guild_info.list_channels_dungeon) <= 0: continue
        list_channels_dungeon = guild_info.list_channels_dungeon
        random_quest_channel_id = random.choice(list_channels_dungeon)
        if guild.id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            for quest_channel in list_channels_dungeon:
                await spawning_enemy_embed_in_dungeon(guild=guild, random_quest_channel_id=quest_channel, list_channels_dungeon=list_channels_dungeon)
                await asyncio.sleep(5)
        else:
            await spawning_enemy_embed_in_dungeon(guild=guild, random_quest_channel_id=random_quest_channel_id, list_channels_dungeon=list_channels_dungeon)

async def spawning_enemy_embed_in_dungeon(guild: discord.Guild, random_quest_channel_id: DungeonQuestChannel, list_channels_dungeon):
    quest_channel = guild.get_channel_or_thread(random_quest_channel_id.channel_id)
    if quest_channel == None:
        #Xoá channel_id lỗi
        list_channels_dungeon.remove(random_quest_channel_id)
        db.update_guild_extra_info_list_channels_dungeon(guild_id=guild.id, list_channels_dungeon=list_channels_dungeon)
        return
    if quest_channel != None:
        level = random.randint(10, 30)
        guardian_chance = 15
        double_enemy_chance = 0
        mysterious_stats = False
        bonus_percent = 10
        
        if random_quest_channel_id.difficulty_level == 2:
            level = random.randint(30, 50)
            guardian_chance = 15
            double_enemy_chance = 20
            bonus_percent = 15
        elif random_quest_channel_id.difficulty_level == 3:
            level = random.randint(50, 90)
            guardian_chance = 20
            double_enemy_chance = 20
            mysterious_stats = True
            bonus_percent = 25
        elif random_quest_channel_id.difficulty_level == 4:
            dice_harder = UtilitiesFunctions.get_chance(25)
            double_enemy_chance = 25
            bonus_percent = 45
            mysterious_stats = True
            if dice_harder:
                level = random.randint(95, 250)
            else:
                level = random.randint(90, 150)
            guardian_chance = 25
        embed = discord.Embed(title=f"", description=f"{EmojiCreation2.STUN_SKILL.value} **Hầm Ngục {UtilitiesFunctions.get_cap_do_quest(random_quest_channel_id.difficulty_level)}** {EmojiCreation2.STUN_SKILL.value}", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        
        double_enemy_dice = UtilitiesFunctions.get_chance(double_enemy_chance)
        enemy = ListGAAndSkills.get_random_ga_enemy_generic(level=level, guardian_chance=guardian_chance)
        enemy_2 = None
        
        if double_enemy_dice:
            enemy = ListGAAndSkills.get_random_ga_enemy_generic(level=int(level/2), guardian_chance=guardian_chance)
            text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {enemy.level})"
            if random_quest_channel_id.difficulty_level >= 3:
                text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {UtilitiesFunctions.replace_with_question_marks(enemy.level)})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{enemy.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.health, max_value=enemy.max_health, emoji=EmojiCreation2.HP.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.stamina, max_value=enemy.max_stamina, emoji=EmojiCreation2.STAMINA.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.mana, max_value=enemy.max_mana, emoji=EmojiCreation2.MP.value, mysterious_stats=mysterious_stats)}", inline=False)
            
            enemy_2 = ListGAAndSkills.get_random_ga_enemy_generic(level=int(level/3), guardian_chance=guardian_chance)
            text = f"Kẻ thù {enemy_2.ga_emoji} - **{enemy_2.ga_name}** (Cấp {enemy_2.level})"
            if random_quest_channel_id.difficulty_level > 3:
                text = f"Kẻ thù {enemy_2.ga_emoji} - **{enemy_2.ga_name}** (Cấp {UtilitiesFunctions.replace_with_question_marks(enemy_2.level)})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{enemy_2.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy_2.health, max_value=enemy_2.max_health, emoji=EmojiCreation2.HP.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy_2.stamina, max_value=enemy_2.max_stamina, emoji=EmojiCreation2.STAMINA.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy_2.mana, max_value=enemy_2.max_mana, emoji=EmojiCreation2.MP.value, mysterious_stats=mysterious_stats)}", inline=False)
        else:
            text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {enemy.level})"
            if random_quest_channel_id.difficulty_level >= 3:
                text = f"Kẻ thù {enemy.ga_emoji} - **{enemy.ga_name}** (Cấp {UtilitiesFunctions.replace_with_question_marks(enemy.level)})"
            embed.add_field(name=f"", value=text, inline=False)
            embed.add_field(name=f"", value=f"🦾: **{enemy.attack_power}**\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.health, max_value=enemy.max_health, emoji=EmojiCreation2.HP.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.stamina, max_value=enemy.max_stamina, emoji=EmojiCreation2.STAMINA.value, mysterious_stats=mysterious_stats)}\n{UtilitiesFunctions.progress_bar_stat(input_value=enemy.mana, max_value=enemy.max_mana, emoji=EmojiCreation2.MP.value, mysterious_stats=mysterious_stats)}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        footer_text = f"Ai chưa hiểu cách thức hoạt động của Hầm Ngục Hộ Vệ Thần thì cứ nhắn\ngd help"
        embed.set_footer(text=footer_text)
        print(f"Spawning enemy with base level around {level} at channel {quest_channel.name} in guild {guild.name}. Difficult dungeon: {random_quest_channel_id.difficulty_level}")
        view = GaDugeonView(guild_id=guild.id, enemy_ga=enemy, enemy_ga_2=enemy_2, title=f"{EmojiCreation2.STUN_SKILL.value} **Hầm Ngục {UtilitiesFunctions.get_cap_do_quest(random_quest_channel_id.difficulty_level)}** {EmojiCreation2.STUN_SKILL.value}", bonus_percent=bonus_percent, difficulty=random_quest_channel_id.difficulty_level, footer_text=footer_text, channel_name=quest_channel.name)
        m = await quest_channel.send(embed=embed, view=view)
        view.message = m
        await view.catch_random_player_profile()
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
        dungeon_spawn_enemy_embed.start()
        activity = discord.Activity(type=discord.ActivityType.watching, 
                                name="True Heavens",
                                state = "Dùng lệnh /help để biết thêm thông tin",
                                details = "Kiểm tra profile của từng người..",
                                assets={
                                            "large_image": "discord_ggtrue-heavens_1",
                                            "large_text": "True Heavens",  # Tooltip text when hovering over the image
                                            "small_image": "00107-3430954361-photoroom",
                                            "small_text": "Join My True Heaven",
                                        })
        await bot.change_presence(status=discord.Status.online, activity=activity)
    remove_old_conversation.start()
    love_point_rank_reducing_task.start()
    clear_up_data_task.start()
    #Load extension
    for ext in init_extension:
        await bot.load_extension(ext)
    

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    speakFlag = True
    auto_rep = AutoresponderHandling(bot=bot)
    if await auto_rep.handling_auto_responder(message=message):
        speakFlag = False
    
    ai_handling_response = AIResponseHandling(bot=bot)
    await ai_handling_response.sub_function_ai_response(message=message, speakFlag=speakFlag)
    # await sub_function_ai_response(message=message, speakFlag=speakFlag)
    
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
    if message.guild.id == TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value and message.attachments != None and len(message.attachments)>0:
        #Áp dụng log images cho server true Heavens
        temp_files = []
        true_heaven_server = bot.get_guild(TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value) 
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
            m = await message.channel.send(embed=quest_embed, view=view, content=f"{user.mention}")
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
async def on_guild_remove(guild: discord.Guild):
    #drop collection quest và profile
    ProfileMongoManager.drop_profile_collection(guild_id=guild.id)
    QuestMongoManager.drop_quest_collection_if_empty(guild_id=guild.id)
    #Drop extra info
    db.delete_guild_extra_info_by_id(guild_id=guild.id)
    #Drop snipe của guild
    db.drop_snipe_channel_info_collection_if_empty(guild_id=guild.id)
    #Drop rps
    RpsMongoManager.drop_rps_collection(guild_id=guild.id)
    print(f"Bot {bot.user.display_name} removed from guild {guild.name}. Deleted all related collection")
    

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    #Tạm thời không cần chạy trong server khác
    if before.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value: return
    
    model = genai.GenerativeModel(CustomFunctions.AI_MODEL, CustomFunctions.safety_settings)
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
                  "cogs.economy.GaCog",
                  "cogs.economy.GlobalProfileCog",
                  
                  "cogs.misc.HelpCog",
                  "cogs.misc.SnipeCog",
                  "cogs.misc.DonationCog",
                  ]

bot_token = os.getenv("BOT_TOKEN_NO2")
if CustomFunctions.check_if_dev_mode():
    bot_token = os.getenv("BOT_TOKEN_NO2_DEV")
bot.run(bot_token)