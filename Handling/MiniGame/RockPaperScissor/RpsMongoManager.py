import os
from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.MiniGame.RockPaperScissor.RpsClass import RpsInfo, RpsPlayerProfile, RpsBanInfo, ConsecutiveRpsPlayerProfile, RpsGameSession
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
# Connect to the MongoDB server
client = MongoClient(f"mongodb://{UtilitiesFunctions.USER_NAME_MONGODB}:{UtilitiesFunctions.PASSWORD_MONGODB}@localhost:27017/") if UtilitiesFunctions.USER_NAME_MONGODB != "" and UtilitiesFunctions.PASSWORD_MONGODB != "" else MongoClient(f"mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["rock_paper_scissor_database"]

#region RpsInfo
def find_rps_info_by_id(guild_id: int):
    collection = db_specific[f'rps_{guild_id}']
    data = collection.find_one({"id": "rps_info"})
    if data:
        return RpsInfo.from_dict(data)
    return None

def drop_rps_collection(guild_id: int):
    collection = db_specific[f'rps_{guild_id}']
    if collection != None:
        collection.drop()
        
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

#region Player Profile
def find_player_profile_by_id(guild_id: int, user_id: int):
    collection = db_specific[f'rps_{guild_id}']
    data = collection.find_one({"id": "player_profile", "user_id": user_id}) #Lấy ra Player Profile
    if data:
        return RpsPlayerProfile.from_dict(data)
    return None


def find_all_player_profile(guild_id: int):
    collection = db_specific[f'rps_{guild_id}']
    data = collection.find({"id": "player_profile"}) #Lấy ra tất cả Player Profile
    player_profiles = []
    if data:
        player_profiles = [RpsPlayerProfile.from_dict(player_data) for player_data in data]
    if len(player_profiles) > 0:
        return player_profiles
    return None




def player_profile_on_draw(guild_id: int, player_1_id: int, player_1_display_name: str, player_1_user_name: str, player_2_id:int, player_2_display_name: str, player_2_user_name: str):
    create_update_player_profile(guild_id=guild_id, user_id=player_1_id, user_display_name=player_1_display_name, user_name= player_1_user_name, draw_point=1)
    create_update_player_profile(guild_id=guild_id, user_id=player_2_id, user_display_name=player_2_display_name, user_name= player_2_user_name, draw_point=1)

def create_update_player_profile(guild_id: int, user_id: int, user_name: str, user_display_name: str, win_point: int = 0, lose_point: int = 0, draw_point: int = 0, legendary_point: int = 0, humiliated_point: int = 0, game_consecutive_round_win: int = 0, game_consecutive_round_lose: int = 0):
    #Mỗi server là một collection, chia theo server id
    collection = db_specific[f'rps_{guild_id}']
    existing_player_info = collection.find_one({"id": "player_profile", "user_id": user_id}) #Lấy ra Player Profile
    if existing_player_info == None:
        data = RpsPlayerProfile(user_id=user_id, user_name=user_name, user_display_name=user_display_name, win_point=win_point, lose_point=lose_point, draw_point=draw_point, legendary_point=0, humiliated_point=0, game_consecutive_round_win=game_consecutive_round_win, game_consecutive_round_lose=game_consecutive_round_lose)
        result = collection.insert_one(data.to_dict())
    else:
        data = RpsPlayerProfile.from_dict(existing_player_info)
        data.win_point += win_point
        data.lose_point += lose_point
        data.draw_point += draw_point
        data.legendary_point += legendary_point
        data.humiliated_point += humiliated_point
        data.game_consecutive_round_win += game_consecutive_round_win
        data.game_consecutive_round_lose += game_consecutive_round_lose
        if data.game_consecutive_round_win >= 5:
            #Cộng 1 điểm vào legend point và reset
            data.legendary_point+= 1
            data.game_consecutive_round_win = 0
            data.game_consecutive_round_lose = 0
        if data.game_consecutive_round_lose >= 5:
            #Cộng 1 điểm vào humi point và reset
            data.humiliated_point+= 1
            data.game_consecutive_round_lose = 0
            data.game_consecutive_round_win = 0
        result = collection.update_one({"id": "player_profile", "user_id": user_id}, {"$set": data.to_dict()})
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