
from datetime import datetime
import json
import os
from pymongo import MongoClient
import CustomFunctions
from Handling.MiniGame.MatchWord.MwClass import MatchWordInfo, PlayerBan, PlayerEffect, PlayerPenalty, SpecialItem, PlayerProfile
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from typing import List

# Connect to the MongoDB server
if UtilitiesFunctions.USER_NAME_MONGODB != "" and UtilitiesFunctions.USER_NAME_MONGODB != None and UtilitiesFunctions.PASSWORD_MONGODB != "" and UtilitiesFunctions.PASSWORD_MONGODB != None:
    client = MongoClient(f"mongodb://{UtilitiesFunctions.USER_NAME_MONGODB}:{UtilitiesFunctions.PASSWORD_MONGODB}@localhost:27017/")
else:
    client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["mw_database"]

#region MatchWordInfo
def find_match_word_info_by_id(lang: str, guild_id: int, channel_id: int):
    collection = db_specific[f'{lang}_mw_guild_{guild_id}']
    data = collection.find_one({"channel_id": channel_id})
    if data:
        return MatchWordInfo.from_dict(data)
    return None

def create_info(lang: str, guild_id: int, data: MatchWordInfo):
    #Mỗi channel là một collection riêng, chia theo channel id
    collection = db_specific[f'{lang}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": data.channel_id})
    if existing_data:
        return None
    result = collection.insert_one(data.to_dict())
    return result

def update_data_info(channel_id: int, guild_id: int, current_player_id: int, current_player_name: str, current_word: str, lang: str, existed_words: List[str] = None, special_case: bool = False, type: str = "A"):
    collection = db_specific[f'{lang}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    if not existing_info: return
    used_words = existing_info.used_words
    if existed_words is not None:
        used_words = existed_words
    used_words.append(current_word)
    #Cộng current round lên 1
    current_round = existing_info.current_round+ 1
    #Chuyển last play thành hiện tại
    last_played = datetime.now()
    if type == "A": #Nối Theo Từ Cuối
        special_case = True
    
    #Nếu là special case thì correct_start_word luôn là bằng current word
    if special_case:
        correct_start_word = current_word.strip().split()[-1].lower()
    else:
        #Không thì sẽ lấy từ cuối
        correct_start_word = current_word[-1]
    
    remaining_word = get_remaining_words_english(data=correct_start_word, used_words=used_words) if lang == "en" else get_remaining_words_vietnamese(data=correct_start_word, used_words=used_words, special_case=special_case)
    
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"current_player_id": current_player_id,
                                                                         "current_player_name": current_player_name,
                                                                         "current_word": current_word,
                                                                         "current_round": current_round,
                                                                         "special_case": special_case,
                                                                         "last_played": last_played,
                                                                         "remaining_word": remaining_word,
                                                                         "correct_start_word": correct_start_word,
                                                                         "used_words": [word for word in used_words], #chỉ dùng used_words
                                                                         }})
    return result



def delete_data_info(channel_id: int, guild_id: int, lang: str):
    collection = db_specific[f'{lang}_mw_guild_{guild_id}']
    result = collection.delete_one({"channel_id": channel_id})
    return result

def drop_word_matching_info_collection(guild_id: int):
    collection = db_specific[f'en_mw_guild_{guild_id}']
    if collection != None:
        collection.drop()
    collection = db_specific[f'vn_mw_guild_{guild_id}']
    if collection != None:
        collection.drop()

def update_special_point_data_info(channel_id: int, guild_id: int, language: str, special_point: int = 0):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    #Cập nhật special point của channel lại
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"special_point": special_point,
                                                                         }})
    return result

def update_special_item_data_info(channel_id: int, guild_id: int, language: str, special_item: SpecialItem = None):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    #Cập nhật special item của channel lại
    if special_item:
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"special_item": special_item.to_dict(),
                                                                         }})
    else:
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"special_item": None,
                                                                         }})
    return result


#region PlayerProfile
def update_player_point_data_info(channel_id: int, guild_id: int, language: str,user_id: int, user_name: str, user_display_name: str, point:int):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    list_player_profiles = existing_info.player_profiles
    #Tìm xem có user_id trong list player_profiles chưa
    selected_player = None
    for player in list_player_profiles:
        if player.user_id == user_id:
            selected_player = player
            break
    if selected_player == None:
        #Tạo mới player và thêm vào
        new_player = PlayerProfile(user_id=user_id, user_name=user_name, user_display_name=user_display_name, point=point)
        list_player_profiles.append(new_player)
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_profiles": [player.to_dict() for player in list_player_profiles],
                                                                         }})
        return result
    else:
        selected_player.point += point
        if selected_player.point < 0: selected_player.point = 0
        result = collection.update_one({"channel_id": channel_id, "player_profiles.user_id": user_id}, {"$set": {"player_profiles.$.point": selected_player.point,
                                                                                                                }})
        return result

def update_player_special_item(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, user_display_name: str, point:int, special_item: SpecialItem, remove_special_item = False):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    list_player_profiles = existing_info.player_profiles
    #Tìm xem có user_id trong list player_profiles chưa
    selected_player = None
    for player in list_player_profiles:
        if player.user_id == user_id:
            selected_player = player
            break
    if selected_player == None:
        #Tạo mới player và thêm vào
        temp = []
        temp.append(special_item)
        new_player = PlayerProfile(user_id=user_id, user_name=user_name, user_display_name=user_display_name, point=point, special_items=temp)
        list_player_profiles.append(new_player)
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_profiles": [player.to_dict() for player in list_player_profiles],
                                                                         }})
        return result
    else:
        #Thêm item đó vào list special_items của player
        existing_items = selected_player.special_items
        if remove_special_item == False:
            existing_items.append(special_item)
        else:
            #Tìm xem có item đó không, và remove luôn
            for item_in_list in existing_items:
                if item_in_list.item_id == special_item.item_id: 
                    existing_items.remove(item_in_list)
                    break
        #Chỉ cho phép tối đa 4 item
        if len(existing_items) > 4:
            existing_items.pop(0)
        result = collection.update_one({"channel_id": channel_id, "player_profiles.user_id": user_id}, {"$set": {"player_profiles.$.special_items": [data.to_dict() for data in existing_items],
                                                                                                                }})
        return result

def update_current_player_id(channel_id: int, guild_id: int, language: str,user_id: int):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    if existing_data:
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"current_player_id": user_id}})
        return result

def update_all_players_point(channel_id: int, guild_id: int, language: str, immune_user_id: int,point: int):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    if existing_info:
        list_player_profiles = existing_info.player_profiles
        for player_profile in list_player_profiles:
            if player_profile.user_id == immune_user_id: 
                continue
            player_profile.point += point
            if player_profile.point < 0: player_profile.point = 0
        
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_profiles": [player.to_dict() for player in list_player_profiles],
                                                                         }})
        return result

def update_player_effects(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, effect_id: str, effect_name: str, remove_special_effect = False):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    list_player_effect = existing_info.player_effects
    if remove_special_effect == False:
        #Tạo mới danh sách Player Effect
        data = PlayerEffect(user_id= user_id, username= user_name, effect_id= effect_id, effect_name= effect_name)
        list_player_effect.append(data)
    else:
        #Xoá effect id của user id khỏi danh sách
        for item in list_player_effect:
            if item.effect_id == effect_id and item.user_id == user_id:
                list_player_effect.remove(item)
                break
    list_temp_to_remove = []
    for player_effect in list_player_effect:
        if player_effect.user_id == user_id:
            list_temp_to_remove.append(player_effect)
            
    if list_temp_to_remove != None and len(list_temp_to_remove)>2:
        while len(list_temp_to_remove)>2:
            first_skill_to_remove = list_temp_to_remove[0]
            for item in list_player_effect:
                if item.effect_id == first_skill_to_remove.effect_id and item.user_id == first_skill_to_remove.user_id:
                    list_player_effect.remove(item)
                    break
            list_temp_to_remove.pop(0)
    #Cập nhật danh sách trong db
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_effects": [player_effects.to_dict() for player_effects in list_player_effect],
                                                                         }})
    return result


#region player ban
def create_and_update_player_bans_word_matching_info(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, ban_remaining: int):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    list_player_ban = existing_info.player_ban
    #Tìm xem có user_id trong list player_ban chưa
    selected_player: PlayerBan = None
    for player in list_player_ban:
        if player.user_id == user_id:
            selected_player = player
            player.ban_remain = ban_remaining
            break
    if selected_player == None:
        #Tạo mới player ban và thêm vào world matching
        new_player = PlayerBan(user_id=user_id, username=user_name, ban_remaining=ban_remaining)
        list_player_ban.append(new_player)
    elif selected_player.ban_remain <= 0:
        list_player_ban.remove(selected_player)
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_ban": [player.to_dict() for player in list_player_ban],
                                                                         }})
    return result
    
def reduce_player_bans_word_matching_info_after_round(channel_id: int, guild_id: int, language: str):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    list_player_ban = existing_info.player_ban
    if list_player_ban != None and len(list_player_ban) > 0:
        for player in list_player_ban:
            player.ban_remain += -1
        new_list_remove_0 = [item for item in list_player_ban if item.ban_remain > 0]    
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_ban": [player.to_dict() for player in new_list_remove_0],
                                                                            }})
        return result

def create_and_update_player_penalty(channel_id: int, guild_id: int, language: str,user_id: int, user_name: str, penalty_point = 1):
    """
    Cập nhật lại danh sách Player Bans của world matching info cụ thể.
    """
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = MatchWordInfo.from_dict(existing_data)
    list_penalty = existing_info.player_penalty
    #Tìm xem có user_id trong list player_ban chưa
    selected_player: PlayerPenalty = None
    for player in list_penalty:
        if player.user_id == user_id:
            selected_player = player
            player.penalty_point += penalty_point
            break
    if selected_player == None:
        #Tạo mới player ban và thêm vào world matching
        new_player = PlayerPenalty(user_id=user_id, user_name=user_name, timestamp=datetime.now(), penalty_point=penalty_point)
        list_penalty.append(new_player)
    elif selected_player.penalty_point <= 0:
        list_penalty.remove(selected_player)
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_penalty": [player.to_dict() for player in list_penalty],
                                                                         }})
    return result
    
def remove_player_penalty_after_round(channel_id: int, guild_id: int, language: str):
    collection = db_specific[f'{language}_mw_guild_{guild_id}']
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_penalty": [],
                                                                            }})
    return result


#region remaining words
def get_remaining_words_english(data: str, used_words: List[str]):
    """
    Kiểm tra với danh sách những từ đã tồn tại, đối chiếu vói dictionary để xem còn bao nhiêu từ khả dụng.
    """
    if data == None: return 0
    count = 0
    for word in english_words_dictionary.keys():
        if word == data: continue
        if word.startswith(data) and word not in used_words:
            count+= 1
    return count

def get_remaining_words_vietnamese(data: str, used_words: List[str], special_case: bool = False):
    """
    Đếm số lượng từ khả dụng trong từ điển tiếng Việt, loại bỏ những từ đã dùng.
    Nếu là special_case (nối theo từ đầu), thì chỉ so sánh phần đầu tiên của từ.
    Ngoài ra, nếu chính từ gốc đã bị dùng, loại trừ nó ra khỏi count.
    """
    if data is None:
        return 0

    count = 0
    used_words_set = set(used_words)  # Faster lookup

    for phrase in vietnamese_words_dictionary.keys():
        if phrase == data:
            continue
        if special_case:
            if phrase.split()[0] == data and phrase not in used_words_set:
                count += 1
        else:
            if phrase.startswith(data) and phrase not in used_words_set:
                count += 1

    # If the base word itself is already used (and it's not being counted above), subtract 1
    if data in used_words_set:
        count -= 1
    return count

english_words_dictionary = CustomFunctions.get_english_dict()
vietnamese_words_dictionary = CustomFunctions.get_vietnamese_dict()