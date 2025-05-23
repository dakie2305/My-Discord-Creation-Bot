import json
import os
from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from db.Class.CustomClass import UserInfo, GuildExtraInfo, UserConversationInfo, ConversationInfo, SnipeChannelInfo, SnipeMessage, SnipeMessageAttachments, PreDeleteAttachmentsInfo
from db.Class.WordMatchingClass import WordMatchingInfo, PlayerProfile, SpecialItem, PlayerEffect, PlayerBan
from db.Class.UserCountClass import UserCount
import CustomFunctions
from pathlib import Path
from Handling.Economy.Quest.DungeonQuestChannelClass import DungeonQuestChannel


#region User Info Database

def create_user(user_info, chosen_collection):
    """
    Insert a new user into the collection.

    Parameters:
    - user_info (UserInfo): A UserInfo object representing the user data to insert.

    Returns:
    - result: The result of the insert operation.
    """
    collection = db[chosen_collection]
    existing_user = collection.find_one({"user_id": user_info.user_id})
    if existing_user:
      return f"User with user_id {user_info.user_id} already exists."
    result = collection.insert_one(user_info.to_dict())
    return result
  
def find_user_by_id(user_id, chosen_collection):
    """
    Find a user by their user_id.

    Parameters:
    - user_id (int): The user_id of the user to find.

    Returns:
    - user_info (UserInfo): A UserInfo object if found, otherwise None.
    """
    collection = db[chosen_collection]
    user_data = collection.find_one({"user_id": user_id})
    if user_data:
        return UserInfo.from_dict(user_data)
    return None

def find_all_users(chosen_collection):
    """
    Find all users in the collection.

    Returns:
    - users (list): A list of UserInfo objects.
    """
    collection = db[chosen_collection]
    users_data = list(collection.find())
    return [UserInfo.from_dict(user_data) for user_data in users_data]


def update_guild_extra_info(user_id, update_data, chosen_collection):
    """
    Update a user's information.

    Parameters:
    - user_id (int): The user_id of the user to update.
    - update_data (dict): A dictionary of the fields to update.

    Returns:
    - result: The result of the update operation.
    """
    collection = db[chosen_collection]
    result = collection.update_one({"user_id": user_id}, {"$set": update_data})
    return result
  
def delete_user_by_id(user_id, chosen_collection):
    """
    Delete a user by their user_id.

    Parameters:
    - user_id (int): The user_id of the user to delete.

    Returns:
    - result: The result of the delete operation.
    """
    collection = db[chosen_collection]
    result = collection.delete_one({"user_id": user_id})
    return result

# Example user data
user_info = UserInfo(
    user_id=315835396305059840,
    user_name="darkiex_xx",
    user_display_name="Darkie",
    reason= "Test",
    jail_until= datetime.utcnow(),
    roles=[
        {
            "role_id": 1256989385744846989,
            "role_name": "Server Master"
        }
    ]
)
#endregion

#region Guild Info
def find_guild_extra_info_by_id(guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific['guild_extra_info']
    data = collection.find_one({"guild_id": guild_id})
    if data:
        return GuildExtraInfo.from_dict(data)
    return None

def delete_guild_extra_info_by_id(guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific['guild_extra_info']
    result = collection.delete_one({"guild_id": guild_id})
    return result

def find_all_guild_extra_info():
    db_specific = client['guild_database']
    collection = db_specific['guild_extra_info']
    data = list(collection.find())
    return [GuildExtraInfo.from_dict(guild) for guild in data]
    
def insert_guild_extra_info(guild_info: GuildExtraInfo):
    db_specific = client['guild_database']
    collection = db_specific['guild_extra_info']
    existing_data = collection.find_one({"guild_id": guild_info.guild_id})
    if existing_data:
      return f"Guild with guild_id {guild_info.guild_id} already exists."
    result = collection.insert_one(guild_info.to_dict())
    return result
    
def update_guild_extra_info(guild_id: int, update_data):
    db_specific = client['guild_database']
    collection = db_specific['guild_extra_info']
    result = collection.update_one({"guild_id": guild_id}, {"$set": update_data})
    return result

def update_guild_extra_info_list_channels_dungeon(guild_id: int, list_channels_dungeon: List[DungeonQuestChannel] = None):
    db_specific = client['guild_database']
    collection = db_specific['guild_extra_info']
    existing_data = find_guild_extra_info_by_id(guild_id=guild_id)
    if existing_data == None: return
    
    
    result = collection.update_one({"guild_id": guild_id}, {"$set": {"list_channels_dungeon": [data.to_dict() for data in list_channels_dungeon],}})
    return result


def delete_user_convo_info(guild_id:int):
    db_specific = client['guild_database']
    collection = db_specific['guild_extra_info']
    result = collection.delete_one({"guild_id": guild_id})
    return result
#endregion

#region UserConversationInfo
def find_user_convo_info_by_id(user_id: int, bot_name: str):
    collection = db[f'user_conversation_info_{bot_name}']
    data = collection.find_one({"user_id": user_id})
    if data:
        return UserConversationInfo.from_dict(data)
    return None

def find_all_user_convo_info(bot_name: str):
    collection = db[f'user_conversation_info_{bot_name}']
    data = list(collection.find())
    return [UserConversationInfo.from_dict(user) for user in data]

def create_user_convo_info(user_convo_info: UserConversationInfo, bot_name: str):
    collection = db[f'user_conversation_info_{bot_name}']
    existing_data = collection.find_one({"user_id": user_convo_info.user_id})
    if existing_data:
      return f"User with user_id {user_convo_info.user_id} already exists."
    result = collection.insert_one(user_convo_info.to_dict())
    return result

def update_or_insert_conversation_info(user_id: int, conversation: ConversationInfo, bot_name: str):
    collection = db[f'user_conversation_info_{bot_name}']
    #Tìm xem có thông tin về UserConversationInfo của id truyền vào không
    existing_data = collection.find_one({"user_id": user_id})
    existing_user_info = UserConversationInfo.from_dict(existing_data)
    if existing_data == None:
        #Không có thì tạo mới một UserConversationInfo rỗng
        new_user_info = UserConversationInfo(user_id= user_id, user_name="Uknown")
        create_user_convo_info(new_user_info)
        existing_user_info = new_user_info
    list_convo = existing_user_info.past_conversation
    #Thêm thông tin ConversationInfo vào list
    list_convo.append(conversation)
    #Chỉnh lại last time interaction là hiện tại
    last_time_interaction = datetime.now()
    #Chỉ cho phép tối đa 2 conversation tồn tại
    if len(list_convo) > 2:
        list_convo.pop(0)
    result = collection.update_one({"user_id": user_id}, {"$set": {"last_time_interaction":last_time_interaction,
                                                                   "past_conversation": [conv.to_dict() for conv in list_convo]}})
    return result



def delete_user_convo_info(user_id:int, bot_name: str):
    collection = db[f'user_conversation_info_{bot_name}']
    result = collection.delete_one({"user_id": user_id})
    return result

#endregion


#region SnipeChannelInfo
def find_snipe_channel_info_by_id(channel_id: int, guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific[f'snipe_info_guild_{guild_id}']
    data = collection.find_one({"channel_id": channel_id})
    if data:
        return SnipeChannelInfo.from_dict(data)
    return None

def find_all_snipe_channel_info(guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific[f'snipe_info_guild_{guild_id}']
    data = list(collection.find())
    return [SnipeChannelInfo.from_dict(snipe_channel) for snipe_channel in data]

def create_snipe_channel_info(snipe_channel_info: SnipeChannelInfo, guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific[f'snipe_info_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": snipe_channel_info.channel_id})
    if existing_data:
        return f"Channel with channel_id {snipe_channel_info.channel_id}, channel name {snipe_channel_info.channel_name} already exists."
    result = collection.insert_one(snipe_channel_info.to_dict())
    return result

def update_or_insert_snipe_message_info(guild_id: int, channel_id: int, snipe_message: SnipeMessage):
    db_specific = client['guild_database']
    collection = db_specific[f'snipe_info_guild_{guild_id}']
    #Tìm xem có đã tồn tại SnipeChannelInfo với channel_id truyền vào chưa cái đã
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SnipeChannelInfo.from_dict(existing_data)
    if existing_data == None:
        #Không có thì tạo mới một SnipeChannelInfo rỗng
        new_snipe_channel_info = SnipeChannelInfo(channel_id == channel_id, channel_name="Uknown")
        create_snipe_channel_info(snipe_channel_info=new_snipe_channel_info, guild_id=guild_id)
        existing_info = new_snipe_channel_info
    
    list_sniped_mess = existing_info.snipe_messages
    #Thêm thông tin vào list
    list_sniped_mess.append(snipe_message)
    #Chỉ cho phép tối đa 7 snipe message tồn tại trong channel
    if len(list_sniped_mess) > 7:
        list_sniped_mess.pop(0)
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"snipe_messages": [conv.to_dict() for conv in list_sniped_mess]}})
    return result

def replace_snipe_message_info(guild_id: int, channel_id: int, snipe_messages: List['SnipeMessage']):
    db_specific = client['guild_database']
    collection = db_specific[f'snipe_info_guild_{guild_id}']
    #Tìm xem có đã tồn tại SnipeChannelInfo với channel_id truyền vào chưa cái đã
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = SnipeChannelInfo.from_dict(existing_data)
    if existing_data == None: return
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"snipe_messages": [conv.to_dict() for conv in snipe_messages]}})
    return result

def drop_snipe_channel_info_collection_if_empty(guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific[f'snipe_info_guild_{guild_id}']
    if collection is not None and collection.estimated_document_count() == 0:
        collection.drop()
        print(f"Collection 'snipe_info_guild_{guild_id}' dropped because it was empty.")

def delete_snipe_channel_info(channel_id:int, guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific[f'snipe_info_guild_{guild_id}']
    result = collection.delete_one({"channel_id": channel_id})
    return result

#endregion

#region PreDeleteAttachmentsInfo
def find_predelete_attachment_info_by_id(channel_id: int, guild_id: int) -> PreDeleteAttachmentsInfo:
    db_specific = client['guild_database']
    collection = db_specific[f'pre_delete_attachments_info_guild_{guild_id}']
    data = collection.find_one({"channel_id": channel_id})
    if data:
        return PreDeleteAttachmentsInfo.from_dict(data)
    return None

def create_predelete_attachment_info(data: PreDeleteAttachmentsInfo, guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific[f'pre_delete_attachments_info_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": data.channel_id})
    if existing_data:
        return f"Channel with channel_id {data.channel_id}, channel name {data.channel_name} already exists."
    result = collection.insert_one(data.to_dict())
    return result

def update_or_insert_predelete_attachment_info(guild_id: int, channel_id: int, attachments: List[SnipeMessageAttachments]):
    db_specific = client['guild_database']
    collection = db_specific[f'pre_delete_attachments_info_guild_{guild_id}']
    #Tìm xem có đã tồn tại PreDeleteAttachmentsInfo với channel_id truyền vào chưa cái đã
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = PreDeleteAttachmentsInfo.from_dict(existing_data)
    if existing_data == None:
        #Không có thì tạo mới một PreDeleteAttachmentsInfo rỗng
        new_pre_delete_attachments_info = PreDeleteAttachmentsInfo(channel_id = channel_id, channel_name="Uknown")
        create_predelete_attachment_info(data=new_pre_delete_attachments_info, guild_id=guild_id)
        existing_info = new_pre_delete_attachments_info
    
    list_attachments = existing_info.user_attachments
    #Thêm thông tin vào list
    for att in attachments:
        list_attachments.append(att)
    #Chỉ cho phép tối đa 50 link attachments
    if len(list_attachments) > 50:
        while len(list_attachments) > 50:
            list_attachments.pop(0)
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"user_attachments": [attach.to_dict() for attach in list_attachments]}})
    return result

def delete_predelete_attachment_info(channel_id:int, guild_id: int):
    db_specific = client['guild_database']
    collection = db_specific[f'pre_delete_attachments_info_guild_{guild_id}']
    result = collection.delete_one({"channel_id": channel_id})
    return result

#endregion

#region WordMatchingClass
def find_word_matching_info_by_id(channel_id: int, guild_id: int, language: str):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    data = collection.find_one({"channel_id": channel_id})
    if data:
        return WordMatchingInfo.from_dict(data)
    return None

def create_word_matching_info(data: WordMatchingInfo, guild_id: int, language: str):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": data.channel_id})
    if existing_data:
        return f"Channel with channel_id {data.channel_id}, channel name {data.channel_name} already exists."
    result = collection.insert_one(data.to_dict())
    return result

def update_data_word_matching_info(channel_id: int, guild_id: int, current_player_id: int, current_player_name: str, current_word: str, language: str, existed_words: List[str] = None, special_case_vn: bool = False):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
    if existing_data == None:
        #Không có thì tạo mới một WorldMatchInfo rỗng
        new_data = WordMatchingInfo(channel_id = channel_id, channel_name="Uknown")
        create_word_matching_info(data=new_data, guild_id=guild_id)
        existing_info = new_data
    
    used_words = existing_info.used_words
    if existed_words != None:
        used_words = existed_words
    first_character = current_word[0]
    last_character = current_word[-1]
    if special_case_vn:
        splitted = get_first_and_last_word_special_case_vn(current_word)
        if splitted != None:
            first_character = splitted[0]
            last_character = splitted[1]
    #Để biết được còn bao nhiêu remaining words, ta sẽ đếm số lượng từ trong dictionary bắt đầu bằng first_character, và trừ đi số lượng từ bắt đầu bằng first_character trong used_words
    #Tuỳ vào language sẽ get remaining word khác nhau
    if language == 'en' or language == 'eng':
        existing_info.remaining_word = get_remaining_words_english(data=last_character, used_words= used_words)
    elif language == 'vn' or language == 'vietnam':
        existing_info.remaining_word = get_remaining_words_vietnamese(data=last_character, used_words= used_words, special_case=special_case_vn)
    used_words.append(current_word)
    #Cộng current round lên 1
    existing_info.current_round += 1
    
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"current_player_id": current_player_id,
                                                                         "current_player_name": current_player_name,
                                                                         "current_word": current_word,
                                                                         "first_character": first_character,
                                                                         "last_character": last_character,
                                                                         "remaining_word": existing_info.remaining_word,
                                                                         "special_case": special_case_vn,
                                                                         "current_round": existing_info.current_round,
                                                                         "used_words": [word for word in used_words], #chỉ dùng used_words
                                                                         }})
    return result

def delete_word_matching_info(channel_id: int, guild_id: int, language: str):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
    if existing_info:
        #Xoá đi
        result = collection.delete_one({"channel_id": channel_id})
        return result

def drop_word_matching_info_collection(guild_id: int):
    db_specific = client['word_matching_database']
    collection = db_specific[f'en_word_matching_guild_{guild_id}']
    if collection != None:
        collection.drop()
    collection = db_specific[f'vn_word_matching_guild_{guild_id}']
    if collection != None:
        collection.drop()

def update_special_point_word_matching_info(channel_id: int, guild_id: int, language: str, special_point: int):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    #Cập nhật special point của channel lại
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"special_point": special_point,
                                                                         }})
    return result

def update_special_item_word_matching_info(channel_id: int, guild_id: int, language: str, special_item: SpecialItem = None):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    #Cập nhật special point của channel lại
    item = None
    item = special_item
    if item:
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"special_item": special_item.to_dict(),
                                                                         }})
    else:
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"special_item": None,
                                                                         }})
    return result

def update_player_point_word_matching_info(channel_id: int, guild_id: int, language: str,user_id: int, user_name: str, user_display_name: str, point:int):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
    list_player_profiles = existing_info.player_profiles
    #Tìm xem có user_id trong list player_profiles chưa
    selected_player = None
    for player in list_player_profiles:
        if player.user_id == user_id:
            selected_player = player
            break
    if selected_player == None:
        #Tạo mới player và thêm vào
        new_player = PlayerProfile(user_id=user_id, username=user_name, user_display_name=user_display_name, points=point)
        list_player_profiles.append(new_player)
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_profiles": [player.to_dict() for player in list_player_profiles],
                                                                         }})
        return result
    else:
        selected_player.points += point
        if selected_player.points < 0: selected_player.points = 0
        result = collection.update_one({"channel_id": channel_id, "player_profiles.user_id": user_id}, {"$set": {"player_profiles.$.points": selected_player.points,
                                                                                                                }})
        return result



def update_player_special_item_word_matching_info(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, user_display_name: str, point:int, special_item: SpecialItem, remove_special_item = False):
    """
    Cập nhật lại danh sách các Special Items của player cụ thể.
    """
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
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
        new_player = PlayerProfile(user_id=user_id, username=user_name, user_display_name=user_display_name, points=point, special_items=temp)
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
    Kiểm tra với danh sách những từ đã tồn tại, đối chiếu vói dictionary để xem còn bao nhiêu từ khả dụng.
    """
    if data == None: return 0
    count = 0
    for phrase in vietnamese_words_dictionary.keys():
        if phrase == data: continue
        if special_case == True and phrase.split()[0] == data and phrase not in used_words:
            count += 1
        elif special_case == False and phrase.startswith(data) and phrase not in used_words:
            count += 1
    return count

#region Các functions về kỹ năng của nối từ
def update_current_player_id_word_matching_info(channel_id: int, guild_id: int, language: str,user_id: int):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    if existing_data:
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"current_player_id": user_id}})
        return result
    
def update_all_players_point_word_matching_info(channel_id: int, guild_id: int, language: str, immune_user_id: int,point: int):
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
    if existing_info:
        list_player_profiles = existing_info.player_profiles
        for player_profile in list_player_profiles:
            if player_profile.user_id == immune_user_id: 
                continue
            player_profile.points += point
            if player_profile.points < 0: player_profile.points = 0
            collection.update_one({"channel_id": channel_id, "player_profiles.user_id": player_profile.user_id}, {"$set": {"player_profiles.$.points": player_profile.points,
                                                                                                                                                                                        }})

def update_player_effects_word_matching_info(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, effect_id: str, effect_name: str, remove_special_effect = False):
    """
    Cập nhật lại danh sách Player Effects của player cụ thể.
    """
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
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

def create_and_update_player_bans_word_matching_info(channel_id: int, guild_id: int, language: str,user_id: int,user_name: str, ban_remaining: int):
    """
    Cập nhật lại danh sách Player Bans của world matching info cụ thể.
    """
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
    list_player_ban = existing_info.player_bans
    #Tìm xem có user_id trong list player_ban chưa
    selected_player: PlayerBan = None
    for player in list_player_ban:
        if player.user_id == user_id:
            selected_player = player
            player.ban_remaining = ban_remaining
            break
    if selected_player == None:
        #Tạo mới player ban và thêm vào world matching
        new_player = PlayerBan(user_id=user_id, username=user_name, ban_remaining=ban_remaining)
        list_player_ban.append(new_player)
    elif selected_player.ban_remaining <= 0:
        list_player_ban.remove(selected_player)
    result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_bans": [player.to_dict() for player in list_player_ban],
                                                                         }})
    return result
    
def reduce_player_bans_word_matching_info_after_round(channel_id: int, guild_id: int, language: str):
    """
    Trừ 1 điểm ban_remaining của tất cả dữ liệu trong danh sách Player Ban của world matching info cụ thể sau mỗi lượt chơi thành công.
    """
    db_specific = client['word_matching_database']
    collection = db_specific[f'{language}_word_matching_guild_{guild_id}']
    existing_data = collection.find_one({"channel_id": channel_id})
    existing_info = WordMatchingInfo.from_dict(existing_data)
    list_player_ban = existing_info.player_bans
    if list_player_ban != None and len(list_player_ban) > 0:
        for player in list_player_ban:
            player.ban_remaining += -1
        new_list_remove_0 = [item for item in list_player_ban if item.ban_remaining > 0]    
        result = collection.update_one({"channel_id": channel_id}, {"$set": {"player_bans": [player.to_dict() for player in new_list_remove_0],
                                                                            }})
        return result

def get_first_and_last_word_special_case_vn(input_string: str):
    words = input_string.split()
    if len(words) == 0:
        return None
    elif len(words) == 1:
        # Nếu chữ chỉ có một thì trả về nguyên chữ cái
        first_char = words[0]
        last_char = words[0]
        return [first_char, last_char]
    else:
        # Trả về nguyên từ đầu và từ cuối
        first_word = words[0]
        last_word = words[-1]
        return [first_word, last_word]

def find_user_count_by_id(guild_id: int, user_id: int):
    db_specific = client['misc_database']
    collection = db_specific[f'{guild_id}_user_count']
    existing_data = collection.find_one({"user_id": user_id})
    if existing_data:
        return UserCount.from_dict(existing_data)
    return None

def create_user_count(guild_id: int, data: UserCount):
    """
    Thêm mới lại thông tin count của user.
    """
    db_specific = client['misc_database']
    collection = db_specific[f'{guild_id}_user_count']
    existing_data = collection.find_one({"user_id": data.user_id})
    if existing_data:
        return f"Data user count for user {data.user_id} at {guild_id} already exists."
    result = collection.insert_one(data.to_dict())
    return result

def update_or_insert_user_count(guild_id: int, user_id: int, user_name: str, user_display_name: str, truth_game_index: int = None, dare_game_index: int = None, therapy_count: int = 0):
    """
    Cập nhật hoặc tạo mới thông tin count của user.
    """
    db_specific = client['misc_database']
    collection = db_specific[f'{guild_id}_user_count']
    existing_data = collection.find_one({"user_id": user_id})
    last_interaction = datetime.now()
    if existing_data == None:
        #Không có thì tạo mới
        new_data = UserCount(user_id = user_id, user_display_name=user_display_name, user_name=user_name, last_interaction=last_interaction)
        create_user_count(data=new_data, guild_id=guild_id)
        existing_info = new_data
    else:
        existing_info = UserCount.from_dict(existing_data)
    
    if dare_game_index != None:
        existing_info.dare_game_count.append(dare_game_index)
        if len(existing_info.dare_game_count) >= CustomFunctions.dare_count:
            existing_info.dare_game_count = []
            
    if truth_game_index != None:
        existing_info.truth_game_count.append(truth_game_index)
        if len(existing_info.truth_game_count) >= CustomFunctions.truth_count:
            existing_info.truth_game_count = []
            
    existing_info.therapy_count += therapy_count
    if existing_info.therapy_count>5:
        existing_info.therapy_count = 0
    
    result = collection.update_one({"user_id": user_id}, 
                                   {"$set": 
                                       {"dare_game_count": [index for index in existing_info.dare_game_count],
                                        "truth_game_count": [index for index in existing_info.truth_game_count],
                                        "therapy_count": existing_info.therapy_count,
                                        "last_interaction": last_interaction,
                                                                                }})
    return result

#endregion
def get_env_variable(variable_name):
  """
  Gets the value of an environment variable from the .env file in the base directory.

  Args:
    variable_name: The name of the environment variable.

  Returns:
    The value of the environment variable.
  """

  # Get the path to the base directory
  base_dir = Path(__file__).resolve().parent.parent
  # Construct the path to the .env file
  env_file_path = os.path.join(base_dir, ".env")

  # Load environment variables from the .env file
  if os.path.exists(env_file_path):
    with open(env_file_path) as f:
      for line in f:
        if line.startswith(variable_name):
          return line.strip().split("=")[1]

  # If the environment variable is not found in the .env file,
  # try to get it from the environment
  return os.getenv(variable_name)


#endregion

#Luôn set database nào cần dùng
#Không set thì mặc định vào misc_database hết
set_database = "misc_database"
# Connect to the MongoDB server
USER_NAME_MONGODB = get_env_variable('USER_NAME_MONGODB')
PASSWORD_MONGODB = get_env_variable('PASSWORD_MONGODB')
if USER_NAME_MONGODB != "" and USER_NAME_MONGODB != None and PASSWORD_MONGODB != "" and PASSWORD_MONGODB != None:
    client = MongoClient(f"mongodb://{USER_NAME_MONGODB}:{PASSWORD_MONGODB}@localhost:27017/")
else:
    client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db = client["user_database"]
db_specific = client[set_database]

def get_english_dict()->dict:
    filepath = os.path.join(os.path.dirname(__file__), "json", "english_dictionary.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data
    return None

def get_vietnamese_dict()->dict:
    filepath = os.path.join(os.path.dirname(__file__),"json", "vietnamese_dictionary.json")
    with open(filepath, 'r', encoding= 'utf-8') as f:
        data = json.load(f)
        return data
    return None

english_words_dictionary = get_english_dict()
vietnamese_words_dictionary = get_vietnamese_dict()