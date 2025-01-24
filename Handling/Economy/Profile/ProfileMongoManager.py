from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items, PlantItem
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from bson.int64 import Int64

# Connect to the MongoDB server
if UtilitiesFunctions.USER_NAME_MONGODB != "" and UtilitiesFunctions.USER_NAME_MONGODB != None and UtilitiesFunctions.PASSWORD_MONGODB != "" and UtilitiesFunctions.PASSWORD_MONGODB != None:
    client = MongoClient(f"mongodb://{UtilitiesFunctions.USER_NAME_MONGODB}:{UtilitiesFunctions.PASSWORD_MONGODB}@localhost:27017/")
else:
    client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["economy_database"]

#region Profile
def find_profile_by_id(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    data = collection.find_one({"id": "profile", "user_id": Int64(user_id)})
    if data:
        return Profile.from_dict(data)
    return None

def find_all_profiles(guild_id: int):
    collection = db_specific[f'profile_{guild_id}']
    data = list(collection.find())
    return [Profile.from_dict(profile) for profile in data]

def drop_profile_collection(guild_id: int):
    collection = db_specific[f'profile_{guild_id}']
    if collection != None:
        collection.drop()

def create_profile(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str):
    if guild_name == "" or guild_name == None: return
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'profile_{guild_id}']
    existing_data = collection.find_one({"id": "profile", "user_id": Int64(user_id)})
    if existing_data:
        return None
    data = Profile(user_id=Int64(user_id), user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
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
    
    if existing_data.copper > 9999999999999: existing_data.copper = 9999999999999
    if existing_data.silver > 9999999999999: existing_data.silver = 9999999999999
    if existing_data.gold > 9999999999999: existing_data.gold = 9999999999999
    if existing_data.darkium > 9999999999999: existing_data.darkium = 9999999999999
    
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
    if data.copper > 9999999999999: data.copper = 9999999999999
    if data.silver > 9999999999999: data.silver = 9999999999999
    if data.gold > 9999999999999: data.gold = 9999999999999
    if data.darkium > 9999999999999: data.darkium = 9999999999999
    result = collection.update_one({"id": "profile", "user_id": data.user_id}, {"$set": {"copper": data.copper,
                                                                                    "gold": data.gold,
                                                                                    "silver": data.silver,
                                                                                    "darkium": data.darkium,
                                                                                    }})
    return result
#region daily
def update_last_attendance_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    if existing_data.last_attendance != None and yesterday.date() == existing_data.last_attendance.date():
        existing_data.daily_streak_count += 1
    else:
        existing_data.daily_streak_count = 0 

    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_attendance": today,
                                                                                    "daily_streak_count": existing_data.daily_streak_count
                                                                                    }})
    return result

#region gift
def update_last_gift_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    today = datetime.now()
    existing_data.gift_given += 1
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_gift": today,
                                                                                    "gift_given": existing_data.gift_given,
                                                                                    }})
    return result

def update_last_attack_item_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_attack_item_used": today,
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
    elif existing_data.level >= 99:
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

def reduce_level_progressing(guild_id:int, user_id: int, level_progressing: int, level_reduction_point: int = 0):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    existing_data.level -= level_reduction_point
    
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"level_progressing": level_progressing,
                                                                                    "level": existing_data.level,
                                                                                    }})
    return result


def update_auto_level_progressing(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.level >= 50: return
    
    #Sẽ cộng 20 exp mỗi lần
    existing_data.level_progressing += 20
    
    if existing_data.level_progressing >= 1000:
        lp = existing_data.level_progressing
        existing_data.level_progressing =  lp - 1000
        existing_data.level += 1
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"level_progressing": existing_data.level_progressing,
                                                                                    "level": existing_data.level,
                                                                                    }})
    return result

def add_one_level_and_reset_progress(guild_id:int, user_id: int, level: int = 1):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    existing_data.level += level
    existing_data.level_progressing = 0
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
    if data.is_authority == True:
        if UtilitiesFunctions.get_dia_vi(data) == "Trung Lưu" or UtilitiesFunctions.get_dia_vi(data) == "Hạ Lưu" or UtilitiesFunctions.get_dia_vi(data) == "Hạ Đẳng": return True
        total_wealth = int(data.darkium*10000*5000*5000 + data.gold*5000*5000 + data.silver*5000 + data.copper)
        if total_wealth < 85002505500:
            return True
        else:
            return False
    if existing_data.copper <= copper_threshold and existing_data.silver <= silver_threshold and existing_data.gold <= gold_threshold and existing_data.darkium <= darkium_threshold:
        return True
    else:
        return False

#region crime
def update_last_crime(guild_id:int, user_id: int, last_crime: datetime = None, flag_remove= True):
    collection = db_specific[f'profile_{guild_id}']
    value = datetime.now()
    if last_crime != None:
        value = last_crime
    if flag_remove:
        value = None
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_crime": value,
                                                                                    }})
    return result

#region plant
def update_plant(guild_id:int, user_id: int, plant: PlantItem = None):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if plant != None:
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"plant": plant.to_dict(),
                                                                                    }})
    else:
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"plant": None,
                                                                                    }})
    return result

def update_plant_date(guild_id:int, user_id: int, plant_date: datetime = None):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None or existing_data.plant == None: return
    value = datetime.now()
    if plant_date != None:
        value = plant_date
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"plant.plant_date": value,
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

def update_breakup_time(guild_id:int, user_id: int, last_breakup: datetime = None):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_breakup": last_breakup,
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

#region Item
def update_list_items_profile(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, item: Item, amount: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None:
        existing_data = create_profile(guild_id=guild_id, user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
    
    list_items = existing_data.list_items
    if list_items == None: list_items = []
    
    exist_flag = False
    #Nếu đã có items trong list thì chỉnh quantity lại theo amount
    if len(list_items)>0:
        for profile_item in list_items:
            if profile_item.item_id == item.item_id:
                profile_item.quantity += amount
                if profile_item.quantity > 99: profile_item.quantity = 99
                if profile_item.quantity <= 0: list_items.remove(profile_item)
                exist_flag = True
                break
            if profile_item.quantity <= 0:
                list_items.remove(profile_item)
    #Nếu chưa có item trong list thì append, và chỉnh quantity lại theo amount
    if exist_flag == False:
        item.quantity = amount
        if item.quantity > 99: item.quantity = 99
        if item.quantity > 0: list_items.append(item)
    
    if len(list_items) > 20:
        list_items.pop(0)
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"list_items": [data.to_dict() for data in list_items],
                                                                                    }})
    return result
    

def equip_protection_item_profile(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, item: Item, unequip: bool = False):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    if unequip == False:
        #Thêm thì sẽ gắn vào profile, và xoá một cái đi khỏi list item
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"protection_item": item.to_dict(),
                                                                                    }})
        update_list_items_profile(guild_id=guild_id, guild_name=guild_name, user_id=user_id, user_name=user_name, user_display_name= user_display_name, item=item, amount=-1)
    else:
        #Gỡ ra thì sẽ trả lại vào list item trong profile
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"protection_item": None,
                                                                                    }})
        update_list_items_profile(guild_id=guild_id, guild_name=guild_name, user_id=user_id, user_name=user_name, user_display_name= user_display_name, item=item, amount=1)
    return result
    
def remove_current_protection_item_profile(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"protection_item": None,
                                                                                    }})
    return result
    

def equip_attack_item_profile(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, item: Item, unequip: bool = False):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    if unequip == False:
        #Thêm thì sẽ gắn vào profile, và xoá một cái đi khỏi list item
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"attack_item": item.to_dict(),
                                                                                    }})
        update_list_items_profile(guild_id=guild_id, guild_name=guild_name, user_id=user_id, user_name=user_name, user_display_name= user_display_name, item=item, amount=-1)
    else:
        #Gỡ ra thì sẽ trả lại vào list item trong profile
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"attack_item": None,
                                                                                    }})
        update_list_items_profile(guild_id=guild_id, guild_name=guild_name, user_id=user_id, user_name=user_name, user_display_name= user_display_name, item=item, amount=1)
    return result
    
def remove_current_attack_item_profile(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"attack_item": None,
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
        
    if existing_data.copper > 9999999999999: existing_data.copper = 9999999999999
    if existing_data.silver > 9999999999999: existing_data.silver = 9999999999999
    if existing_data.gold > 9999999999999: existing_data.gold = 9999999999999
    if existing_data.darkium > 9999999999999: existing_data.darkium = 9999999999999
    
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
    today = datetime.now()
    result = collection.update_one({"id": "conversion_rate"}, {"$set": {"last_authority":user_id,
                                                                        "last_authority_date":today
                                                                        
                                                                        }})
    
    
def update_last_riot_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_riot": today,
                                                                                    }})
    return result

def update_last_breakup_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_breakup": today,
                                                                                    }})
    return result

def update_last_fishing_now(guild_id:int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    today = datetime.now()
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"last_fishing": today,
                                                                                    }})
    return result

#region guardian
def set_main_guardian_profile(guild_id: int, user_id: int, guardian: GuardianAngel = None):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if guardian:
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian": guardian.to_dict(),
                                                                                    }})
    else:
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian": None,
                                                                                    }})
    return result


def update_main_guardian_level_progressing(guild_id:int, user_id: int, bonus_exp: int = 0):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.guardian == None: return
    
    if existing_data.guardian.level < 10:
        existing_data.guardian.level_progressing += 50
    elif existing_data.guardian.level >= 10 and existing_data.guardian.level < 25:
        existing_data.guardian.level_progressing += 45
    elif existing_data.guardian.level >= 25 and existing_data.guardian.level < 50:
        existing_data.guardian.level_progressing += 45
    elif existing_data.guardian.level >= 50 and existing_data.guardian.level < 75:
        existing_data.guardian.level_progressing += 35
    elif existing_data.guardian.level >= 75 and existing_data.guardian.level < 99:
        existing_data.guardian.level_progressing += 30
    elif existing_data.guardian.level >= 99:
        #Cực khó sau level 99
        existing_data.guardian.level_progressing += 50
        bonus_exp = 0
    
    if bonus_exp < 0: bonus_exp = 0
    if bonus_exp > 500: bonus_exp = 500
    #Cộng thêm bonus nếu có
    existing_data.guardian.level_progressing += bonus_exp
    
    if existing_data.guardian.level_progressing >= 1000:
        while existing_data.guardian.level_progressing >= 1000:
            lp = existing_data.guardian.level_progressing
            existing_data.guardian.level_progressing =  lp - 1000
            existing_data.guardian.level += 1
            existing_data.guardian.stats_point += 1
    
    max_skills = 1
    if existing_data.guardian.level >= 25 and existing_data.guardian.level <50: max_skills = 2
    if existing_data.guardian.level >= 50 and existing_data.guardian.level <75: max_skills = 3
    if existing_data.guardian.level >= 75 and existing_data.guardian.level <100: max_skills = 4
    if existing_data.guardian.level >= 100: max_skills = 5

    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.level_progressing": existing_data.guardian.level_progressing,
                                                                                    "guardian.level": existing_data.guardian.level,
                                                                                    "guardian.stats_point": existing_data.guardian.stats_point,
                                                                                    "guardian.max_skills": max_skills,
                                                                                    }})
    return result

def update_main_guardian_profile_time(guild_id: int, user_id: int, data_type: str, date_value: datetime = None):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    
    if data_type == "time_to_recover":
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.time_to_recover": date_value,
                                                                                    }})
    elif data_type == "last_feed":
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.last_feed": date_value,
                                                                                    }})
    elif data_type == "last_meditation":
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.last_meditation": date_value,
                                                                                    }})
    elif data_type == "last_battle":
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.last_battle": date_value,
                                                                                    }})
    elif data_type == "last_dungeon":
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.last_dungeon": date_value,
                                                                                    }})
    elif data_type == "last_joined_battle":
        result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.last_joined_battle": date_value,
                                                                                    }})
        
    return

def update_guardian_stats(guild_id:int, user_id: int, health: int = 0, max_health: int = 0, mana: int = 0, max_mana = 0, stamina: int = 0, max_stamina: int = 0, attack_power: int = 0):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.guardian == None: return
    
    is_injured = False
    time_to_recover = None
    existing_data.guardian.health += health
    if existing_data.guardian.health <= 0: 
        existing_data.guardian.health = 0
        #Coi như bị thương
        is_injured = True
        time_to_recover = datetime.now() + timedelta(hours=3)
        
    existing_data.guardian.max_health += max_health
    if existing_data.guardian.max_health <= 0: 
        existing_data.guardian.max_health = 0
    
    existing_data.guardian.mana += mana
    if existing_data.guardian.mana <= 0: existing_data.guardian.mana = 0
    existing_data.guardian.max_mana += max_mana
    if existing_data.guardian.max_mana <= 0: existing_data.guardian.max_mana = 0
    
    existing_data.guardian.stamina += stamina
    if existing_data.guardian.stamina <= 0: existing_data.guardian.stamina = 0
    existing_data.guardian.max_stamina += max_stamina
    if existing_data.guardian.max_stamina <= 0: existing_data.guardian.max_stamina = 0
    
    existing_data.guardian.attack_power += attack_power
    if existing_data.guardian.attack_power <= 0: existing_data.guardian.attack_power = 10
    
    if existing_data.guardian.health > existing_data.guardian.max_health: existing_data.guardian.health = existing_data.guardian.max_health
    if existing_data.guardian.mana > existing_data.guardian.max_mana: existing_data.guardian.mana = existing_data.guardian.max_mana
    if existing_data.guardian.stamina > existing_data.guardian.max_stamina: existing_data.guardian.stamina = existing_data.guardian.max_stamina
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.health": existing_data.guardian.health,
                                                                                    "guardian.max_health": existing_data.guardian.max_health,
                                                                                    "guardian.mana": existing_data.guardian.mana,
                                                                                    "guardian.max_mana": existing_data.guardian.max_mana,
                                                                                    "guardian.stamina": existing_data.guardian.stamina,
                                                                                    "guardian.max_stamina": existing_data.guardian.max_stamina,
                                                                                    "guardian.attack_power": existing_data.guardian.attack_power,
                                                                                    "guardian.is_injured": is_injured,
                                                                                    "guardian.time_to_recover": time_to_recover,
                                                                                    }})
    return result

def set_guardian_current_stats(guild_id:int, user_id: int, health: int, mana: int, stamina: int, is_dead = False):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.guardian == None: return
    
    is_injured = False
    time_to_recover = None
    existing_data.guardian.health = health
    if existing_data.guardian.health <= 0: 
        existing_data.guardian.health = 0
        #Coi như bị thương
        is_injured = True
        time_to_recover = datetime.now() + timedelta(hours=3)
    
    if existing_data.guardian.health >= existing_data.guardian.max_health: existing_data.guardian.health = existing_data.guardian.max_health

    existing_data.guardian.mana = mana
    if existing_data.guardian.mana <= 0: existing_data.guardian.mana = 0
    if existing_data.guardian.mana >= existing_data.guardian.max_mana: existing_data.guardian.mana = existing_data.guardian.max_mana
    
    existing_data.guardian.stamina = stamina
    if existing_data.guardian.stamina <= 0: existing_data.guardian.stamina = 0
    if existing_data.guardian.stamina >= existing_data.guardian.max_stamina: existing_data.guardian.stamina = existing_data.guardian.max_stamina
    
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.health": existing_data.guardian.health,
                                                                                    "guardian.mana": existing_data.guardian.mana,
                                                                                    "guardian.stamina": existing_data.guardian.stamina,
                                                                                    "guardian.is_injured": is_injured,
                                                                                    "guardian.time_to_recover": time_to_recover,
                                                                                    "guardian.is_dead": is_dead,
                                                                                    }})
    return result

def set_guardian_stats_points(guild_id: int, user_id: int, stats_point: int = 0):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.guardian == None: return
    
    existing_data.guardian.stats_point += stats_point
    if existing_data.guardian.stats_point <= 0: existing_data.guardian.stats_point = 0
    
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.stats_point": existing_data.guardian.stats_point,
                                                                                    }})
    return result

def set_guardian_dead_status(guild_id: int, user_id: int, is_dead = False):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.guardian == None: return
    
    existing_data.guardian.is_dead = is_dead
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.is_dead": existing_data.guardian.is_dead,
                                                                                    }})
    return result

def update_list_skills_guardian(guild_id: int, user_id: int, skill: GuardianAngelSkill, is_remove: bool = False):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None: return
    if existing_data.guardian == None: return
    
    list_skills = existing_data.guardian.list_skills
    if list_skills == None: list_skills = []
    
    if is_remove == False:
        #Thêm thì sẽ gắn vào list skill của guardian
        list_skills.append(skill)
    else:
        #Gỡ ra thì sẽ trả lại vào list item trong profile
        for profile_skill in list_skills:
            if profile_skill.skill_id == skill.skill_id:
                list_skills.remove(profile_skill)
                break
    
    #Nếu list skill quá giới hạn thì xoá cái đầu tiên
    if len(list_skills) > existing_data.guardian.max_skills:
        list_skills.pop(0)
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"guardian.list_skills": [data.to_dict() for data in list_skills],}})
    return result
