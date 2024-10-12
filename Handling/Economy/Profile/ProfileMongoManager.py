from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Economy.Profile.ProfileClass import Profile

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
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"copper": existing_data.copper,
                                                                                    "gold": existing_data.gold,
                                                                                    "silver": existing_data.silver,
                                                                                    "darkium": existing_data.darkium,
                                                                                    
                                                                                    }})
    return result

def update_profile_quote(guild_id: int, guild_name: str, user_id: int, user_name: str, user_display_name: str, quote: str):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_profile_by_id(guild_id=guild_id, user_id=user_id)
    if existing_data == None:
        existing_data = create_profile(guild_id=guild_id, user_id=user_id, user_display_name=user_display_name, user_name=user_name, guild_name= guild_name)
    
    result = collection.update_one({"id": "profile", "user_id": user_id}, {"$set": {"quote": quote,
                                                                                    }})

def delete_profile(guild_id: int, user_id: int):
    collection = db_specific[f'profile_{guild_id}']
    result = collection.delete_one({"id": "profile", "user_id": user_id})
    return result

#region Authority

def is_authority_existed(guild_id: int):
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