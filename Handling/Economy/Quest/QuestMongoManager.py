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
            # 5% 4, 20% 3, 30% 2
            quest_difficult_rate = get_value(lengend=10, hard=20, avarage=30)
        elif data_profile.level >= 15 and data_profile.level < 30:
            # 5% 4, 20% 3, 40% 2
            quest_difficult_rate = get_value(lengend=10, hard=30, avarage=40)
        elif data_profile.level >= 30 and data_profile.level < 50:
            # 5% 4, 35% 3, 35% 2
            quest_difficult_rate = get_value(lengend=10, hard=35, avarage=35)
        elif data_profile.level >= 50 and data_profile.level < 75:
            # 10% 4, 35% 3, 35% 2
            quest_difficult_rate = get_value(lengend=10, hard=35, avarage=35)
        elif data_profile.level >= 75 and data_profile.level < 99:
            quest_difficult_rate = get_value(lengend=10, hard=50, avarage=10)
        elif data_profile.level >= 99:
            quest_difficult_rate = get_value(lengend=20, hard=55, avarage=25)
    reward_type = "C"
    bonus_exp = 0
    emoji = EmojiCreation2.COPPER.value
    if quest_difficult_rate == 2 or quest_difficult_rate == 3:
        reward_type = "S"
        emoji = EmojiCreation2.SILVER.value
        bonus_exp = 15
    elif quest_difficult_rate == 4:
        reward_type = "G"
        emoji = EmojiCreation2.GOLD.value
        bonus_exp = 35
    base_amount = 1
    quest_title = ""
    quest_des = ""
    base_reward_amount = 2000
    if quest_type == "emoji_reaction_count":
        base_amount = quest_difficult_rate * 120
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 1800
        if reward_type == "C":
            base_reward_amount = 2000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 100 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1 * rand_reward_amount
        quest_title = f"Thả **{base_amount}** reactions bất kỳ tại kênh <#{channel_id}>"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "message_count":
        base_amount = quest_difficult_rate * 80
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3000
        if reward_type == "C":
            base_reward_amount = 3000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 200 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 5 * rand_reward_amount
        quest_title = f"Nhắn **{base_amount}** tin nhắn tại kênh <#{channel_id}>"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "attachments_count":
        base_amount = quest_difficult_rate * 10
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 500
        if reward_type == "C":
            base_reward_amount = 500 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1
        quest_title = f"Thả **{base_amount}** ảnh, video bất kỳ vào kênh <#{channel_id}>"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "truth_game_count" or quest_type == "dare_game_count":
        game_name = "Truth"
        if quest_type == "dare_game_count": game_name = "Dare"
        base_amount = quest_difficult_rate * 20
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 3000
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
        if reward_type == "C":
            base_reward_amount = 2000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1
        quest_title = f"Chơi **{base_amount}** trận game Kéo Búa Bao ({SlashCommand.KEO_BUA_BAO.value})"
        quest_des = f"**{base_reward_amount}**{emoji}"
    elif quest_type == "coin_flip_game_count":
        base_amount = quest_difficult_rate * 20
        rand_reward_amount = random.randint(1, 5)
        base_reward_amount = 1000
        if reward_type == "C":
            base_reward_amount = 1000 * rand_reward_amount
        elif reward_type == "S":
            base_reward_amount = 1 * rand_reward_amount
        elif reward_type == "G":
            base_reward_amount = 1
        quest_title = f"Chơi **{base_amount}** trận game Tung Xu ({SlashCommand.COIN_FLIP.value})"
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
    rand_num = random.randint(0, 100)
    if rand_num < lengend:  # % lengend chance
        return 4
    elif rand_num < hard:  # % hard chance
        return 3
    elif rand_num < avarage:  # 30% chance (25% + 30% = 55%)
        return 2
    else:  # % easy chance
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



list_quest_general_type = [
    "emoji_reaction_count", 
    "message_count", 
    "attachments_count", 
    "truth_game_count",
    "dare_game_count",
    "coin_flip_game_count",
    "rps_game_count",
    ]