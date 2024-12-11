from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager 
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.Quest.QuestClass import QuestProfile
import random
from CustomEnum.EmojiEnum import EmojiCreation2
from CustomEnum.SlashEnum import SlashCommand
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions


# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["economy_database"]

#region Quest
def find_quest_by_user_id(guild_id: int, user_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id})
    if data:
        return QuestProfile.from_dict(data)
    return None

def drop_quest_collection(guild_id: int):
    collection = db_specific[f'quest_{guild_id}']
    if collection:
        collection.drop()

def find_all_profiles(guild_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = list(collection.find())
    return [QuestProfile.from_dict(quest) for quest in data]

def create_new_random_quest(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, channel_id: int, channel_name: str, data_profile: Profile = None):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'quest_{guild_id}']
    existing_data = collection.find_one({"id": "quest", "user_id": user_id})
    if existing_data:
        return None
    quest_type = random.choice(list_quest_general_type)
    quest_difficult_rate = 1  #dễ, trung bình, khó, huyển thoại
    if data_profile != None and data_profile.level != None:
        if data_profile.level >= 1 and data_profile.level < 15:
            quest_difficult_rate = get_value(lengend=25, hard=35, avarage=35)
        elif data_profile.level >= 15 and data_profile.level < 30:
            quest_difficult_rate = get_value(lengend=25, hard=40, avarage=45)
        elif data_profile.level >= 30 and data_profile.level < 50:
            quest_difficult_rate = get_value(lengend=30, hard=45, avarage=45)
        elif data_profile.level >= 50 and data_profile.level < 75:
            quest_difficult_rate = get_value(lengend=40, hard=40, avarage=45)
        elif data_profile.level >= 75 and data_profile.level < 99:
            quest_difficult_rate = get_value(lengend=45, hard=45, avarage=45)
        elif data_profile.level >= 99:
            quest_difficult_rate = get_value(lengend=50, hard=50, avarage=45)
    reward_type = "C"
    emoji = EmojiCreation2.COPPER.value
    if quest_difficult_rate == 2 or quest_difficult_rate == 3:
        reward_type = "S"
        emoji = EmojiCreation2.SILVER.value
    elif quest_difficult_rate == 4:
        reward_type = "G"
        emoji = EmojiCreation2.GOLD.value
    base_amount = 1
    quest_title = ""
    quest_des = ""
    base_reward_amount = 4500
    bonus_exp = 100 * quest_difficult_rate
    if quest_type == "emoji_reaction_count":
        base_amount = quest_difficult_rate * 45
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 4500
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 4500 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 100 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 2 * rand_reward_amount
        quest_title = f"Thả **{base_amount}** reactions bất kỳ tại kênh <#{channel_id}>"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "message_count":
        base_amount = quest_difficult_rate * 40
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 4500
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 4500 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 200 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 5 * rand_reward_amount
        quest_title = f"Nhắn **{base_amount}** tin nhắn tại kênh <#{channel_id}>"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "attachments_count":
        base_amount = quest_difficult_rate * 10
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3000
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 3000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 2 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Thả **{base_amount}** ảnh, video bất kỳ vào kênh <#{channel_id}>"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "truth_game_count" or quest_type == "dare_game_count":
        game_name = "Truth"
        if quest_type == "dare_game_count": game_name = "Dare"
        base_amount = quest_difficult_rate * 15
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3000
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 3000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 5 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trò {game_name} trong game Truth Dare ({SlashCommand.TRUTH_DARE.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "rps_game_count":
        base_amount = quest_difficult_rate * 8
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 2500
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 2000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trận game Kéo Búa Bao ({SlashCommand.KEO_BUA_BAO.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "coin_flip_game_count":
        base_amount = quest_difficult_rate * 15
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 2000
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 1000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trận game Tung Xu ({SlashCommand.COIN_FLIP.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "sb_normal_count":
        base_amount = quest_difficult_rate * 20
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 1000
        if reward_type == "C":
            base_reward_amount = 1000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trận game Tài Xỉu bình thường ({SlashCommand.SB_NORMAL.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "sb_double_count":
        base_amount = quest_difficult_rate * 15
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 2000
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 2000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trận game Tài Xỉu Double ({SlashCommand.SB_DOUBLE.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "sb_triple_count":
        base_amount = quest_difficult_rate * 15
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 2000
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount = 2000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trận game Tài Xỉu Triple ({SlashCommand.SB_TRIPLE.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "sb_slot_machine_count":
        base_amount = quest_difficult_rate * 10
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3500
        bonus_exp += rand_reward_amount * 75
        if reward_type == "C":
            base_reward_amount = 3500 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trận game Nổ Hủ May Mắn ({SlashCommand.SB_SLOT_MACHINE.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "sb_bai_cao_count":
        base_amount = quest_difficult_rate * 5
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3000
        bonus_exp += rand_reward_amount * 75
        if reward_type == "C":
            base_reward_amount *= rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Chơi **{base_amount}** trận game Bài Cào ({SlashCommand.SB_BAI_CAO.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "work_fishing_count":
        base_amount = quest_difficult_rate * 3
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 2000
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount *= rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1
        quest_title = f"Câu cá **{base_amount}** lần ({SlashCommand.WORK_FISHING.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "work_planting_count":
        base_amount = quest_difficult_rate * 2
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3500
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount *= rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Trồng cây **{base_amount}** lần ({SlashCommand.WORK_PLANTING.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "work_normal_count":
        base_amount = quest_difficult_rate * 3
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3500
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount *= rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1
        quest_title = f"Làm việc **{base_amount}** lần ({SlashCommand.WORK.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "gift_count":
        base_amount = quest_difficult_rate * 1
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 1500
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount *= rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1
        quest_title = f"Tặng quà **{base_amount}** lần cho người khác ({SlashCommand.GIFT.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "crime_count":
        base_amount = quest_difficult_rate * 1
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 1500
        bonus_exp += rand_reward_amount * 50
        if reward_type == "C":
            base_reward_amount *= rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1
        quest_title = f"Phạm tội **{base_amount}** lần ({SlashCommand.CRIME.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"

    quest_profile = QuestProfile(user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name, quest_type= quest_type, quest_channel=channel_id, channel_name= channel_name, quest_title=quest_title, quest_description=quest_des, quest_difficult_rate=quest_difficult_rate, quest_total_progress=base_amount, bonus_exp=bonus_exp)
    if reward_type == "C":
        quest_profile.quest_reward_copper = base_reward_amount
    elif reward_type == "S":
        quest_profile.quest_reward_silver = base_reward_amount
    elif reward_type == "G":
        quest_profile.quest_reward_gold = base_reward_amount 
    quest_profile.reset_date = datetime.now() + timedelta(days=2)
    result = collection.insert_one(quest_profile.to_dict())
    return quest_profile

def get_value(lengend: int, hard: int, avarage: int):
    dice = UtilitiesFunctions.get_chance(lengend)
    if dice: return 4
    dice = UtilitiesFunctions.get_chance(hard)
    if dice: return 3
    dice = UtilitiesFunctions.get_chance(avarage)
    if dice: return 2
    return 1


def delete_quest(guild_id: int, user_id: int):
    collection = db_specific[f'quest_{guild_id}']
    result = collection.delete_one({"id": "quest", "user_id": user_id})
    return result

#region Quest truth dare
def increase_truth_dare_count(guild_id: int, user_id: int, is_truth: bool):
    collection = db_specific[f'quest_{guild_id}']
    quest_type = "truth_game_count"
    if is_truth == False:
        quest_type = "dare_game_count"
        
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": quest_type})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    if is_truth: 
        existing_data.truth_game_count += 1
        existing_data.quest_progress += 1
    else:
        existing_data.dare_game_count += 1
        existing_data.quest_progress += 1
    
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {"truth_game_count": existing_data.truth_game_count,
                                                                                    "quest_progress": existing_data.quest_progress,
                                                                                    "dare_game_count": existing_data.dare_game_count,
                                                                                    "is_completed": is_completed,
                                                                                    }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

#region Message Count
def increase_message_count(guild_id: int, user_id: int, channel_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "message_count", "quest_channel": channel_id})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

#region Attachment Count
def increase_attachment_count(guild_id: int, user_id: int, channel_id: int, count: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "attachments_count","quest_channel": channel_id})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += count
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

#region Coin Flip Count
def increase_coin_flip_count(guild_id: int, user_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "coin_flip_game_count"})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

#region sb Normal count
def increase_sb_normal_count(guild_id: int, user_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "sb_normal_count"})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

def increase_sb_double_count(guild_id: int, user_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "sb_double_count"})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

def increase_sb_triple_count(guild_id: int, user_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "sb_triple_count"})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed


#region Kéo Búa Bao Count
def increase_rps_count(guild_id: int, user_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "rps_game_count"})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

#region Emoji Count
def increase_emoji_count(guild_id: int, user_id: int, channel_id: int):
    collection = db_specific[f'quest_{guild_id}']
    data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": "emoji_reaction_count","quest_channel": channel_id})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed

#region Quest Objective Count
def increase_quest_objective_count(guild_id: int, user_id: int, quest_type: str, channel_id: int = None):
    collection = db_specific[f'quest_{guild_id}']
    if channel_id != None:
        data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": quest_type,"quest_channel": channel_id})
    else:
        data = collection.find_one({"id": "quest", "user_id": user_id, "quest_type": quest_type})
    if data == None: return False
    existing_data = QuestProfile.from_dict(data)
    if existing_data.quest_progress >= existing_data.quest_total_progress:
        return True
    existing_data.quest_progress += 1
    is_completed = False if existing_data.quest_progress < existing_data.quest_total_progress else True
    collection.update_one({"id": "quest", "user_id": user_id}, {"$set": {
                                                                            "quest_progress": existing_data.quest_progress,
                                                                            "is_completed": is_completed,
                                                                        }})
    if is_completed:
        ProfileMongoManager.increase_quest_finished(guild_id=guild_id, user_id=user_id)
    return is_completed




list_quest_general_type = [
    "emoji_reaction_count", 
    "message_count", 
    "attachments_count", 
    "truth_game_count",
    "dare_game_count",
    "coin_flip_game_count",
    "rps_game_count",
    "sb_normal_count",
    "sb_double_count",
    "sb_triple_count",
    "sb_slot_machine_count",
    "sb_bai_cao_count",
    "work_fishing_count",
    "work_planting_count",
    "work_normal_count",
    "gift_count",
    "crime_count",
    ]