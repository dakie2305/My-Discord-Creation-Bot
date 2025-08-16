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

def get_top_donators(limit=20):
    collection = db_specific['donator']
    pipeline = [
        {
            "$addFields": {
                "donate_score": {
                    "$add": ["$total_amount_donate", "$total_time_donate"]
                }
            }
        },
        {
            "$sort": {"donate_score": -1}
        },
        {
            "$limit": limit
        }
    ]
    data = list(collection.aggregate(pipeline))
    return [Donator.from_dict(profile) for profile in data]

def get_donator_rank_and_profile(user_id: int):
    collection = db_specific['donator']
    pipeline = [
        {
            "$addFields": {
                "donate_score": {
                    "$add": ["$total_amount_donate", "$total_time_donate"]
                }
            }
        },
        {
            "$sort": {"donate_score": -1}
        },
        {
            "$group": {
                "_id": None,
                "docs": {"$push": "$$ROOT"}
            }
        },
        {
            "$unwind": {
                "path": "$docs",
                "includeArrayIndex": "rank"
            }
        },
        {
            "$match": {
                "docs.user_id": Int64(user_id)
            }
        },
        {
            "$project": {
                "rank": {"$add": ["$rank", 1]},
                "docs": 1
            }
        }
    ]

    result = list(collection.aggregate(pipeline))
    if not result:
        return None
    doc = result[0]
    return doc['rank'], Donator.from_dict(doc['docs'])



def drop_profile_collection(guild_id: int):
    collection = db_specific['donator']
    if collection != None:
        collection.drop()

def create_or_update_profile(user_id: int, user_name: str, user_display_name: str, date_donate: datetime = None, donation_amount: int = 0):
    collection = db_specific['donator']
    existing_raw = collection.find_one({"user_id": Int64(user_id)})

    if date_donate is None:
        date_donate = datetime.now()
        
    if existing_raw is None:
        # New donor profile
        new_data = Donator(
            user_id=user_id,
            user_name=user_name,
            user_display_name=user_display_name,
            date_donate=date_donate,
            total_time_donate=1,
            total_amount_donate=donation_amount,
            is_given_role=True
        )
        collection.insert_one(new_data.to_dict())
        return new_data
    else:
        # Existing donor profile
        existing_data = Donator.from_dict(existing_raw)
        existing_data.user_name = user_name
        existing_data.user_display_name = user_display_name
        existing_data.date_donate = date_donate
        existing_data.is_given_role = True
        existing_data.total_time_donate += 1
        existing_data.total_amount_donate += donation_amount
        collection.update_one(
            {"user_id": Int64(user_id)},
            {"$set": existing_data.to_dict()}
        )
        return existing_data

def update_is_given_role(user_id: int, value: bool = False):
    collection = db_specific['donator']
    result = collection.update_one(
        {"user_id": Int64(user_id)},
        {"$set": {"is_given_role": value}}
    )
    return result.modified_count