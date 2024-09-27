import os
from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from mini_game.RockPaperScissor.RpsClass import RpsInfo, RpsPlayerProfile, RpsBanInfo, ConsecutiveRpsPlayerProfile, RpsGameSession

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["rock_paper_scissor_database"]

#region RpsInfo
def find_rps_info_by_id(guild_id: int):
    collection = db_specific[f'rps_{guild_id}']
    data = collection.find_one({"id": "rps_info"})
    if data:
        return RpsInfo.from_dict(data)
    return None

def create_rps_info(guild_id: int, guild_name: str):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'rps_{guild_id}']
    existing_data = collection.find_one({"id": "rps_info"}) #Lấy ra RpsInfo
    if existing_data:
        return f"Rps Info for this guild {guild_id} already exists."
    data = RpsInfo(guild_id = guild_id, guild_name=guild_name)
    result = collection.insert_one(data.to_dict())
    return result

def create_update_consecutive_point_rps_info(guild_id: int,guild_name: str, user_id: int, user_name: str, con_win_time: int = 0, con_lose_time: int = 0):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'rps_{guild_id}']
    existing_rps_info = collection.find_one({"id": "rps_info"}) #Lấy ra RpsInfo
    if existing_rps_info == None:
        create_rps_info(guild_id=guild_id, guild_name=guild_name)
        data = RpsInfo(guild_id = guild_id, guild_name=guild_name)
        existing_info = data
    flag_existed = False
    con_player_profile = existing_info.con_player_profile
    for cons_player in con_player_profile:
        if cons_player.user_id == user_id:
            cons_player.con_win_time+=con_win_time
            cons_player.con_lose_time+=con_lose_time
            flag_existed = True
            break
    if flag_existed ==False:
        #Không tồn tại thì tạo mới danh sách con_player_profile
        new_cons_player = ConsecutiveRpsPlayerProfile(user_id=user_id, user_name=user_name, con_win_time=con_win_time,con_lose_time=con_lose_time)
        con_player_profile.append(new_cons_player)
    
    result = collection.update_one({"id": "rps_info"}, {"$set": {"con_player_profile": [data.to_dict() for data in con_player_profile],
                                                                         }})
    
    
    return result

def create_update_ban_list(guild_id: int,guild_name: str, user_id: int, user_name: str, ban_remaining: int):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'rps_{guild_id}']
    existing_rps_info = collection.find_one({"id": "rps_info"}) #Lấy ra RpsInfo
    if existing_rps_info == None:
        create_rps_info(guild_id=guild_id, guild_name=guild_name)
        data = RpsInfo(guild_id = guild_id, guild_name=guild_name)
        existing_info = data
    flag_existed = False
    ban_list = existing_info.ban_list
    for ban in ban_list:
        if ban.user_id == user_id:
            ban.ban_remaining+=ban_remaining
            flag_existed = True
            break
    if flag_existed ==False:
        #Không tồn tại thì tạo mới danh sách con_player_profile
        new_ban = RpsBanInfo(user_id=user_id, user_name=user_name, ban_remaining = ban_remaining)
        ban_list.append(new_ban)
    
    result = collection.update_one({"id": "rps_info"}, {"$set": {"ban_list": [data.to_dict() for data in ban_list],
                                                                         }})
    
    
    return result

def create_remove_game_session_list(guild_id: int,guild_name: str, player_1_id: int, player_1_username: str, player_2_id: int, player_2_username: str, message_id: int, channel_id: int, remove: bool = False):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'rps_{guild_id}']
    existing_rps_info = collection.find_one({"id": "rps_info"}) #Lấy ra RpsInfo
    if existing_rps_info == None:
        create_rps_info(guild_id=guild_id, guild_name=guild_name)
        data = RpsInfo(guild_id = guild_id, guild_name=guild_name)
        existing_info = data
    game_session = existing_info.game_session
    if remove:
        for game in game_session:
            if game.player_1_id == player_1_id and game.player_2_id == player_2_id:
                game_session.remove(game)
                break
    else:
        game = RpsGameSession(player_1_id = player_1_id, player_1_username = player_1_username, player_2_id = player_2_id, player_2_username = player_2_username, message_id= message_id, channel_id = channel_id)
        game_session.append(game)

    result = collection.update_one({"id": "rps_info"}, {"$set": {"game_session": [data.to_dict() for data in game_session],
                                                                         }})
    return result