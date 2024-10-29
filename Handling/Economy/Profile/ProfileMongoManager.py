from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager 

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["economy_database"]

#region Profile
def find_profile_by_id(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    data = collection.find_one({"id": "profile", "user_id": user_id})
    if data:
        return Profile.from_dict(data)
    return None

def find_all_profiles(guild_id: int):
    collection = db_specific[f'profile_{guild_id}']
    data = list(collection.find())
    return [Profile.from_dict(profile) for profile in data]

def drop_profile_collection(guild_id: int):
    collection = db_specific[f'profile_{guild_id}']
    if collection:
        collection.drop()

def create_profile(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'profile_{guild_id}']
    existing_data = collection.find_one({"id": "profile", "user_id": user_id})
    if existing_data:
        return None
    data = Profile(user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
    result = collection.insert_one(data.to_dict())
    return data


def update_profile_money(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, gold: int= 0, silver: int = 0, copper:int = 0, darkium: int = 0):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None:
        existing_data = create_profile(guild_id=guild_id, user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
    
    existing_data.copper += copper
    existing_data.silver += silver
    existing_data.gold += gold
    existing_data.darkium += darkium
    
    #Tìm rate hiện tại
    rate = 1.0
    rate_bank = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=guild_id)
    if rate_bank!= None and rate_bank.rate != None:
        rate = rate_bank.rate
    
    #Nếu copper âm thì auto convert đồng khác qua copper nếu âm
    while existing_data.copper < 0:
        from_type = None
        if existing_data.silver > 0:
            from_type = "S"
            existing_data.silver -=1
        elif existing_data.gold > 0:
            from_type = "G"
            existing_data.gold -=1
        if from_type!= None:
            converted_money = convert_currency(amount=1, rate=rate, from_currency_type=from_type, to_currency_type="C")
            existing_data.copper += converted_money
        else: break
    
    #Nếu silver âm thì auto convert đồng khác qua
    while existing_data.silver < 0:
        from_type = None
        amount = 1
        #Có thể dùng copper cộng dồn lên để đổi
        copper_needed_for_silver = int(1 * 5000 * rate)
        if existing_data.gold > 0:
            from_type = "G"
            existing_data.gold -=1
            amount = 1
            converted_money = convert_currency(amount=amount, rate=rate, from_currency_type=from_type, to_currency_type="S")
            existing_data.silver += converted_money
        elif existing_data.darkium > 0:
            from_type = "D"
            existing_data.darkium -=1
            amount =1
            converted_money = convert_currency(amount=amount, rate=rate, from_currency_type=from_type, to_currency_type="S")
            existing_data.silver += converted_money
        elif existing_data.copper >= copper_needed_for_silver:
            from_type = "C"
            existing_data.copper -=copper_needed_for_silver
            amount = copper_needed_for_silver
            existing_data.silver += 1
        else: break
    
    #Nếu gold âm thì auto convert đồng khác qua
    while existing_data.gold < 0:
        from_type = None
        amount = 1
        #Có thể dùng copper hoặc silver cộng dồn lên để đổi
        copper_needed_for_one_gold = int(1 * (5000*rate) * (5000 * rate))
        silver_needed_for_one_gold  = int(1 * (5000*rate))
        if existing_data.darkium > 0:
            from_type = "D"
            existing_data.darkium -=1
            amount = 1
            converted_money = convert_currency(amount=amount, rate=rate, from_currency_type=from_type, to_currency_type="G")
            existing_data.gold += converted_money
        elif existing_data.silver >= silver_needed_for_one_gold:
            from_type = "S"
            existing_data.silver -=silver_needed_for_one_gold
            existing_data.gold += 1
        elif existing_data.copper >= copper_needed_for_one_gold:
            from_type = "C"
            existing_data.copper -=copper_needed_for_one_gold
            existing_data.gold += 1
        else: break
    
    #Nếu darkium âm thì chỉ có convert gold qua thôi, không convert mấy khác
    while existing_data.darkium < 0:
        gold_needed_for_one_darkium  = int(1 * 10000 * rate)
        if existing_data.gold >= gold_needed_for_one_darkium:
            existing_data.gold -=gold_needed_for_one_darkium
            existing_data.darkium += 1
        else: break
    
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"copper": existing_data.copper,
                                                                                    "gold": existing_data.gold,
                                                                                    "silver": existing_data.silver,
                                                                                    "darkium": existing_data.darkium,
                                                                                    
                                                                                    }})
    return result

def convert_currency(amount: int, rate: float, from_currency_type: str, to_currency_type: str):
        #Đổi darkium sang các đơn vị khác
        if from_currency_type == to_currency_type: return amount
        result = 0
        if from_currency_type == "D":
            if to_currency_type == "G": #Base 10000
                result = int(amount * 10000 * rate)
            elif to_currency_type == "S": #Base 10000 * 5000
                result = int(amount * 10000 * 5000 * rate)
            elif to_currency_type == "C": #Base 10000 * 5000 * 5000
                result = int(amount * 10000 * 5000 *  500 * rate)
        elif from_currency_type == "G":
            if to_currency_type == "D": #Base 1/10000
                result = int(amount / 10000 * rate)
            elif to_currency_type == "S": #Base 5000
                result = int(amount * 5000 * rate)
            elif to_currency_type == "C": #Base  5000 * 5000
                result = int(amount * 5000 *  5000 * rate)
        elif from_currency_type == "S":
            if to_currency_type == "D": #Base 1/5000/10000
                result = int(amount / 5000 / 10000 * rate)
            elif to_currency_type == "G": #Base 1/5000
                result = int(amount / 5000 * rate)
            elif to_currency_type == "C": #Base  5000
                result = int(amount * 5000 * rate)
        elif from_currency_type == "C":
            if to_currency_type == "D": #Base 1/5000/5000/10000
                result = int(amount /5000 / 5000 / 10000 * rate)
            elif to_currency_type == "G": #Base 1/5000/5000
                result = int(amount / 5000 / 5000 * rate)
            elif to_currency_type == "S": #Base  1/5000
                result = int(amount / 5000 * rate)
        return result

def update_profile_money_fast(guild_id:int, data: Profile):
    collection = db_specific[f'profile_{guild_id}']
    result = collection.update_one({"id": "profile", "user_id": data.user_id}, {"$set": {"copper": data.copper,
                                                                                    "gold": data.gold,
                                                                                    "silver": data.silver,
                                                                                    "darkium": data.darkium,
                                                                                    }})
    return result
#region daily
def update_last_attendance_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_attendance": today,
                                                                                    }})
    return result

#region quest finished
def increase_quest_finished(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    existing_data.quest_finished += 1
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"quest_finished": existing_data.quest_finished,
                                                                                    }})
    return result

#region level
def update_level_progressing(guild_id:int, user_id: int, bonus_exp: int = 0):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    if existing_data.level < 10:
        existing_data.level_progressing += 65
    elif existing_data.level >= 10 and existing_data.level < 25:
        existing_data.level_progressing += 50
    elif existing_data.level >= 25 and existing_data.level < 50:
        existing_data.level_progressing += 45
    elif existing_data.level >= 50 and existing_data.level < 75:
        existing_data.level_progressing += 35
    elif existing_data.level >= 75 and existing_data.level < 99:
        existing_data.level_progressing += 30
    elif existing_data.level == 99:
        #Cực khó sau level 99
        existing_data.level_progressing += 1
        bonus_exp = 0
    
    if bonus_exp < 0: bonus_exp = 0
    #Cộng thêm bonus nếu có
    existing_data.level_progressing += bonus_exp
    
    if existing_data.level_progressing >= 1000:
        lp = existing_data.level_progressing
        existing_data.level_progressing =  lp - 1000
        existing_data.level += 1
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"level_progressing": existing_data.level_progressing,
                                                                                    "level": existing_data.level,
                                                                                    }})
    return result

#region work
def update_last_work_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_work": today,
                                                                                    }})
    return result

def is_in_debt(data: Profile, darkium_threshold = 0, gold_threshold = 0, silver_threshold = 0, copper_threshold = 0):
    existing_data = data
    if existing_data == None:
        return False
    if existing_data.copper <= copper_threshold and existing_data.silver <= silver_threshold and existing_data.gold <= gold_threshold and existing_data.darkium <= darkium_threshold:
        return True
    else:
        return False

#region crime
def update_last_crime_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_crime": today,
                                                                                    }})
    return result

#region quote
def update_profile_quote(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, quote: str):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None:
        existing_data = create_profile(guild_id=guild_id, user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"quote": quote,
                                                                                    }})
    
def update_jail_time(guild_id:int, user_id: int, jail_time: datetime = None):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"jail_time": jail_time,
                                                                                    }})
    return result

def delete_profile(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    result = collection.delete_one({"id": "profile", "user_id": user_id})
    return result

#region dignity point
def update_dignity_point(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, dignity_point: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None:
        existing_data = create_profile(guild_id=guild_id, user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
    existing_data.dignity_point += dignity_point
    if existing_data.dignity_point <= 0:
        existing_data.dignity_point = 0
    elif existing_data.dignity_point >= 100:
        existing_data.dignity_point = 100
        
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"dignity_point": existing_data.dignity_point,
                                                                                    }})
    return result

#region Authority

def update_money_authority(guild_id: int, gold: int= 0, silver: int = 0, copper:int = 0, darkium: int = 0):
    collection = db_specific[f'profile_{guild_id}']
    data = collection.find_one({"id": "profile", "is_authority": True})
    if data == None: return None
    existing_data = Profile.from_dict(data)
    if existing_data == None: return None
    
    existing_data.copper += copper
    existing_data.silver += silver
    existing_data.gold += gold
    existing_data.darkium += darkium
    
    #Tìm rate hiện tại
    rate = 1.0
    rate_bank = ConversionRateMongoManager.find_conversion_rate_by_id(guild_id=guild_id)
    if rate_bank!= None and rate_bank.rate != None:
        rate = rate_bank.rate
    
    #Nếu copper âm thì auto convert đồng khác qua copper nếu âm
    while existing_data.copper < 0:
        from_type = None
        if existing_data.silver > 0:
            from_type = "S"
            existing_data.silver -=1
        elif existing_data.gold > 0:
            from_type = "G"
            existing_data.gold -=1
        if from_type!= None:
            converted_money = convert_currency(amount=1, rate=rate, from_currency_type=from_type, to_currency_type="C")
            existing_data.copper += converted_money
        else: break
    
    #Nếu silver âm thì auto convert đồng khác qua
    while existing_data.silver < 0:
        from_type = None
        amount = 1
        #Có thể dùng copper cộng dồn lên để đổi
        copper_needed_for_silver = int(1 * 5000 * rate)
        if existing_data.gold > 0:
            from_type = "G"
            existing_data.gold -=1
            amount = 1
            converted_money = convert_currency(amount=amount, rate=rate, from_currency_type=from_type, to_currency_type="S")
            existing_data.silver += converted_money
        elif existing_data.darkium > 0:
            from_type = "D"
            existing_data.darkium -=1
            amount =1
            converted_money = convert_currency(amount=amount, rate=rate, from_currency_type=from_type, to_currency_type="S")
            existing_data.silver += converted_money
        elif existing_data.copper >= copper_needed_for_silver:
            from_type = "C"
            existing_data.copper -=copper_needed_for_silver
            amount = copper_needed_for_silver
            existing_data.silver += 1
        else: break
    
    #Nếu gold âm thì auto convert đồng khác qua
    while existing_data.gold < 0:
        from_type = None
        amount = 1
        #Có thể dùng copper hoặc silver cộng dồn lên để đổi
        copper_needed_for_one_gold = int(1 * (5000*rate) * (5000 * rate))
        silver_needed_for_one_gold  = int(1 * (5000*rate))
        if existing_data.darkium > 0:
            from_type = "D"
            existing_data.darkium -=1
            amount = 1
            converted_money = convert_currency(amount=amount, rate=rate, from_currency_type=from_type, to_currency_type="G")
            existing_data.gold += converted_money
        elif existing_data.silver >= silver_needed_for_one_gold:
            from_type = "S"
            existing_data.silver -=silver_needed_for_one_gold
            existing_data.gold += 1
        elif existing_data.copper >= copper_needed_for_one_gold:
            from_type = "C"
            existing_data.copper -=copper_needed_for_one_gold
            existing_data.gold += 1
        else: break
    
    #Nếu darkium âm thì chỉ có convert gold qua thôi, không convert mấy khác
    while existing_data.darkium < 0:
        gold_needed_for_one_darkium  = int(1 * 10000 * rate)
        if existing_data.gold >= gold_needed_for_one_darkium:
            existing_data.gold -=gold_needed_for_one_darkium
            existing_data.darkium += 1
        else: break
    
    result = collection.update_one({"id": "profile", "user_id": existing_data.user_id}, {"$set": {"copper": existing_data.copper,
                                                                                        "gold": existing_data.gold,
                                                                                        "silver": existing_data.silver,
                                                                                        "darkium": existing_data.darkium,
                                                                                        }})
    return result

def get_authority(guild_id: int):
    collection = db_specific[f'profile_{guild_id}']
    data = collection.find_one({"id": "profile", "is_authority": True})
    if data:
        return Profile.from_dict(data)
    return None

def is_authority(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    data = collection.find_one({"id": "profile", "user_id": user_id, "is_authority": True})
    if data:
        return Profile.from_dict(data)
    return None

def set_authority(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None:
        existing_data = create_profile(guild_id=guild_id, user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
    #Update những người khác về false
    query = {}
    update = {"$set": {"is_authority": False}}
    res = collection.update_many(query, update)
    #Set lên authority
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"is_authority": True,
                                                                                    }})
    return result


def remove_authority_from_server(guild_id: int):
    collection = db_specific[f'profile_{guild_id}']
    query = {}
    update = {"$set": {"is_authority": False}}
    res = collection.update_many(query, update)

def update_last_authority(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    result = collection.update_one({"id": "conversion_rate"}, {"$set": {"last_authority":user_id}})
    
    
def update_last_riot_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_riot": today,
                                                                                    }})
    return result