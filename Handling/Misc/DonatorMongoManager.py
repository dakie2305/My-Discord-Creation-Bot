from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Misc.DonatorClass import Donator
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from bson.int64 import Int64

# Connect to the MongoDB server
if UtilitiesFunctions.USER_NAME_MONGODB != "" and UtilitiesFunctions.USER_NAME_MONGODB != None and UtilitiesFunctions.PASSWORD_MONGODB != "" and UtilitiesFunctions.PASSWORD_MONGODB != None:
    client = MongoClient(f"mongodb://{UtilitiesFunctions.USER_NAME_MONGODB}:{UtilitiesFunctions.PASSWORD_MONGODB}@localhost:27017/")
else:
    client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["user_database"]

#region Donator
def find_donator_by_id(user_id: int):
    collection = db_specific['donator']
    data = collection.find_one({"user_id": Int64(user_id)})
    if data:
        return Donator.from_dict(data)
    return None

def find_all_donators():
    collection = db_specific['donator']
    data = list(collection.find())
    return [Donator.from_dict(profile) for profile in data]

def drop_profile_collection(guild_id: int):
    collection = db_specific['donator']
    if collection != None:
        collection.drop()

def create_profile(user_id: int, user_name: str, user_display_name: str, date_donate: datetime= datetime.now(), total_time_donate: int = 1, total_amount_donate: int = 0):
    collection = db_specific['donator']
    existing_data = collection.find_one({"user_id": Int64(user_id)})
    if existing_data:
        return None
    data = Donator(user_id=Int64(user_id), user_display_name=user_display_name, user_name=user_name, date_donate = date_donate, total_amount_donate=total_time_donate, total_amount_donate = total_amount_donate)
    collection.insert_one(data.to_dict())
    return data

def create_or_update_profile(user_id: int, user_name: str, user_display_name: str, date_donate: datetime = datetime.now(), donation_amount: int = 0):
    collection = db_specific['donator']

    collection.update_one(
        {"user_id": Int64(user_id)},
        {
            "$set": {
                "user_name": user_name,
                "user_display_name": user_display_name,
                "date_donate": date_donate,
                "is_given_role": True,
            },
            "$setOnInsert": {
                "total_time_donate": 0,
                "total_amount_donate": 0
            },
            "$inc": {
                "total_time_donate": 1,
                "total_amount_donate": donation_amount
            }
        },
        upsert=True
    )

    # Return the updated object (fetch latest from DB)
    updated = collection.find_one({"user_id": Int64(user_id)})
    return Donator.from_dict(updated)

def update_is_given_role(user_id: int, value: bool = False):
    collection = db_specific['donator']
    result = collection.update_one(
        {"user_id": Int64(user_id)},
        {"$set": {"is_given_role": value}}
    )
    return result.modified_count