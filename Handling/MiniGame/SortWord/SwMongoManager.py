import os
from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from mini_game.SortWord.SwClass import SortWordInfo, SwPlayerProfile, SwSpecialItem, SwPlayerBan, SwPlayerEffect
import random
import string

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["sw_database"]

#region SortWordInfo
def find_sort_word_info_by_id(lang: str, guild_id: int, channel_id: int):
    collection = db_specific[f'{lang}_sw_guild_{guild_id}']
    data = collection.find_one({"channel_id": channel_id})
    if data:
        return SortWordInfo.from_dict(data)
    return None

def create_info(lang: str, guild_id: int, data: SortWordInfo):
    #Mỗi channel là một collection riêng, chia theo channel id
    collection = db_specific[f'{lang}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": data.channel_id})
    if existing_data:
        return f"Sort Word Info for this guild {guild_id}, channel {data.channel_id}, language {lang} already exists."
    result = collection.insert_one(data.to_dict())
    return result

def update_data_info(channel_id: int, guild_id: int, current_player_id: int, current_player_name: str, current_word: str, lang: str, existed_words: List[str] = None, special_case: bool = False):
    collection = db_specific[f'{lang}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
    if existing_data == None:
        #Không có thì tạo mới một SortWordInfo rỗng
        new_data = SortWordInfo(channel_id = channel_id, channel_name="Uknown")
        create_info(data=new_data, guild_id=guild_id)
        existing_info = new_data
    
    used_words = existing_info.used_words
    if existed_words != None:
        used_words = existed_words
    used_words.append(current_word)
    
    #Đảo lại current_word
    unsorted_word = get_unsorted_string(input_string= current_word)
        
    #Cộng current round lên 1
    current_round = existing_info.current_round+ 1
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"current_player_id": current_player_id,
                                                                         "current_player_name": current_player_name,
                                                                         "current_word": current_word,
                                                                         "unsorted_word": unsorted_word,
                                                                         "special_case": special_case,
                                                                         "current_round": current_round,
                                                                         "used_words": [word for word in used_words], #chỉ dùng used_words
                                                                         }})
    return result

def delete_data_info(channel_id: int, guild_id: int, lang: str):
    collection = db_specific[f'{lang}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
    if existing_info:
        #Xoá đi
        result = collection.delete_one({"channel_id": channel_id})
        return result
    
def update_special_point_data_info(channel_id: int, guild_id: int, language: str, special_point: int = 0):
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    #Cập nhật special point của channel lại
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"special_point": special_point,
                                                                         }})
    return result

def update_special_item_data_info(channel_id: int, guild_id: int, language: str, special_item: SwSpecialItem = None):
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
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
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
    list_player_profiles = existing_info.player_profiles
    #Tìm xem có user_id trong list player_profiles chưa
    selected_player = None
    for player in list_player_profiles:
        if player.user_id == user_id:
            selected_player = player
            break
    if selected_player == None:
        #Tạo mới player và thêm vào
        new_player = SwPlayerProfile(user_id=user_id, user_name=user_name, user_display_name=user_display_name, point=point)
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


def update_player_special_item(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, user_display_name: str, point:int, special_item: SwSpecialItem, remove_special_item = False):
    """
    Cập nhật lại danh sách các Special Items của player cụ thể.
    """
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
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
        new_player = SwPlayerProfile(user_id=user_id, user_name=user_name, user_display_name=user_display_name, point=point, special_items=temp)
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
        #Chỉ cho phép tối đa 3 item
        if len(existing_items) > 3:
            existing_items.pop(0)
        result = collection.update_one({"channel_id": channel_id, "player_profiles.user_id": user_id}, {"$set": {"player_profiles.$.special_items": [data.to_dict() for data in existing_items],
                                                                                                                }})
        return result
    
def randomize_word(input_string: str) -> str:
    if len(input_string) > 8:
        # Để ba từ đầu và ba từ cuối yên, random ở giữa
        middle_chars = list(input_string[3:-3])
        random.shuffle(middle_chars)
        return input_string[:3] + ''.join(middle_chars) + input_string[-3:]
    elif len(input_string) > 5:
        # Để hai từ đầu và hai từ cuối yên, random ở giữa
        middle_chars = list(input_string[2:-2])
        random.shuffle(middle_chars)
        return input_string[:2] + ''.join(middle_chars) + input_string[-2:]
    else:
        char_list = list(input_string)
        random.shuffle(char_list)
        unsorted_word = ''.join(char_list)
        return unsorted_word

def get_unsorted_string(input_string: str) -> str:
    # Xoá dấu khỏi string
    translator = str.maketrans('', '', string.punctuation)
    cleaned_string = input_string.translate(translator)
    
    phrase = cleaned_string.split()
    if len(phrase) == 1:
      #Một từ
      return randomize_word(input_string)
    else:
      #Cụm từ
      randomized_words = [randomize_word(word) for word in phrase]
      return ' '.join(randomized_words)

#region Các functions về kỹ năng
def update_current_player_id(channel_id: int, guild_id: int, language: str,user_id: int):
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    if existing_data:
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"current_player_id": user_id}})
        return result
    
def update_all_players_point(channel_id: int, guild_id: int, language: str, immune_user_id: int,point: int):
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
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
    """
    Cập nhật lại danh sách Player Effects của player cụ thể.
    """
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
    list_player_effect = existing_info.player_effects
    if remove_special_effect == False:
        #Tạo mới danh sách Player Effect
        data = SwPlayerEffect(user_id= user_id, user_name= user_name, effect_id= effect_id, effect_name= effect_name)
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

def create_and_update_player_bans(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, ban_remaining: int):
    """
    Cập nhật lại danh sách Player Bans của world matching info cụ thể.
    """
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
    list_player_ban = existing_info.player_bans
    #Tìm xem có user_id trong list player_ban chưa
    selected_player: SwPlayerBan = None
    for player in list_player_ban:
        if player.user_id == user_id:
            selected_player = player
            player.ban_remaining = ban_remaining
            break
    if selected_player == None:
        #Tạo mới player ban và thêm vào world matching
        new_player = SwPlayerBan(user_id=user_id, user_name=user_name, ban_remaining=ban_remaining)
        list_player_ban.append(new_player)
    elif selected_player.ban_remaining <= 0:
        list_player_ban.remove(selected_player)
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_bans": [player.to_dict() for player in list_player_ban],
                                                                         }})
    return result
    
def reduce_player_bans_after_round(channel_id: int, guild_id: int, language: str):
    """
    Trừ 1 điểm ban_remaining của tất cả dữ liệu trong danh sách Player Ban cụ thể sau mỗi lượt chơi thành công.
    """
    collection = db_specific[f'{language}_sw_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SortWordInfo.from_dict(existing_data)
    list_player_ban = existing_info.player_bans
    if list_player_ban != None and len(list_player_ban) > 0:
        for player in list_player_ban:
            player.ban_remaining += -1
        new_list_remove_0 = [item for item in list_player_ban if item.ban_remaining > 0]    
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_bans": [player.to_dict() for player in new_list_remove_0],
                                                                            }})
        return result