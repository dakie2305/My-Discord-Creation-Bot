from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from Handling.Economy.Couple.CoupleClass import Couple

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["economy_database"]

#region couple
def find_couple_by_id(guild_id: int, user_id: int):
    collection = db_specific[f'couple_{guild_id}']
    data = collection.find_one({"$or": [
        {"first_user_id": user_id},
        {"second_user_id": user_id}
    ]})
    if data:
        return Couple.from_dict(data)
    return None

def find_all_couples(guild_id: int):
    collection = db_specific[f'couple_{guild_id}']
    data = list(collection.find())
    return [Couple.from_dict(couple) for couple in data]

def drop_couple_collection(guild_id: int):
    collection = db_specific[f'couple_{guild_id}']
    if collection:
        collection.drop()

def create_couple(guild_id: int, guild_name: str, first_user_id: int, first_user_name: str, first_user_display_name: str, second_user_id: int, second_user_name: str, second_user_display_name: str):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'couple_{guild_id}']
    existing_data = find_couple_by_id(guild_id=guild_id, user_id=first_user_id)
    if existing_data:
        return None
    data = Couple(guild_id=guild_id, guild_name=guild_name, first_user_id=first_user_id, first_user_name=first_user_name, first_user_display_name=first_user_display_name, second_user_id=second_user_id, second_user_display_name=second_user_display_name, second_user_name=second_user_name)
    result = collection.insert_one(data.to_dict())
    return data

#region love progressing
def update_love_progressing(guild_id:int, user_id: int, bonus_exp: int = 0):
    collection = db_specific[f'couple_{guild_id}']
    existing_data = find_couple_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    if existing_data.love_rank < 5:
        existing_data.love_progressing += 65
    elif existing_data.love_rank < 7:
        existing_data.love_progressing += 50
    elif existing_data.love_rank < 10:
        existing_data.love_progressing += 40
    elif existing_data.love_rank < 15:
        existing_data.love_progressing += 30
    elif existing_data.love_rank < 19:
        existing_data.love_progressing += 20
    elif existing_data.love_rank == 19:
        #Cực khó
        existing_data.love_progressing += 25
        bonus_exp = 0
    
    
    if bonus_exp < 0: bonus_exp = 0
    #Cộng thêm bonus nếu có
    existing_data.love_progressing += bonus_exp
    
    #Nếu rank 19 thì không tăng love_progressing, giữ nguyên love_progressing không cho tăng lên 20
    if existing_data.love_rank == 19 and existing_data.love_progressing > 995:
        existing_data.love_progressing = 995
        existing_data.is_ready_to_marry = True
    
    if existing_data.love_progressing >= 1000:
        lp = existing_data.love_progressing
        existing_data.love_progressing =  lp - 1000
        existing_data.love_rank += 1
    
    #Level 20 coi như đã đến chặng cuối, cho 100% progressing luôn
    if existing_data.love_rank >= 20:
        existing_data.love_rank = 20
        existing_data.love_progressing = 1000
    
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"love_progressing": existing_data.love_progressing,
                                                                                                                "love_rank": existing_data.love_rank,
                                                                                                                "is_ready_to_marry": existing_data.is_ready_to_marry,
                                                                                    }})
    return result

def set_love_progressing_value(guild_id:int, user_id: int, love_progressing: int):
    collection = db_specific[f'couple_{guild_id}']
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"love_progressing": love_progressing,
                                                                                    }})
    return result

def set_love_rank_value(guild_id:int, user_id: int, love_rank: int):
    collection = db_specific[f'couple_{guild_id}']
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"love_rank": love_rank,
                                                                                    }})
    return result

def set_love_point_value(guild_id:int, user_id: int, love_point: int):
    collection = db_specific[f'couple_{guild_id}']
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"love_point": love_point,
                                                                                    }})
    return result  

#region love point
def update_love_point(guild_id: int, user_id: int, love_point: int):
    collection = db_specific[f'couple_{guild_id}']
    existing_data = find_couple_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    existing_data.love_point += love_point
    if existing_data.love_point <= 0:
        existing_data.love_point = 0
    elif existing_data.love_point >= 100:
        existing_data.love_point = 100
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"love_point": existing_data.love_point,
                                                                                    }})
    return result



def update_auto_love_progressing(guild_id:int, user_id: int):
    collection = db_specific[f'couple_{guild_id}']
    existing_data = find_couple_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.love_rank >= 15: return
    #Sẽ cộng 20 exp mỗi lần
    existing_data.love_progressing += 20
    
    if existing_data.love_progressing >= 1000:
        lp = existing_data.love_progressing
        existing_data.love_progressing =  lp - 1000
        existing_data.love_rank += 1
    
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"love_progressing": existing_data.love_progressing,
                                                                                                                "love_rank": existing_data.love_rank,
                                                                                    }})
    return result

def delete_couple_by_id(guild_id:int, user_id: int):
    collection = db_specific[f'couple_{guild_id}']
    result = collection.delete_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]})
    return result

#region last date_time now
def update_last_date_time_now(guild_id:int, user_id: int, is_last_love_action = False, is_last_fight_action = False):
    collection = db_specific[f'couple_{guild_id}']
    existing_data = find_couple_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    now = datetime.now()
    if is_last_love_action == True:
        existing_data.last_love_action = now
    if is_last_fight_action == True:
        existing_data.last_fight_action = now
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"last_love_action": existing_data.last_love_action,
                                                                                                                "last_fight_action": existing_data.last_fight_action,
                                                                                                                }})
    return result

def update_married_time_now(guild_id:int, user_id: int):
    collection = db_specific[f'couple_{guild_id}']
    now = datetime.now()
    result = collection.update_one({"$or": [{"first_user_id": user_id},{"second_user_id": user_id}]}, {"$set": {"date_married": now,
                                                                                                                }})
    return result