from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["economy_database"]

#region Conversion Rate
def find_conversion_rate_by_id(guild_id: int):
    collection = db_specific[f'profile_{guild_id}']
    data = collection.find_one({"id": "conversion_rate"})
    if data:
        return ConversionRate.from_dict(data)
    return None


def create_update_conversion_rate(guild_id: int, rate: float):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_conversion_rate_by_id(guild_id=guild_id)
    if existing_data == None:
        existing_data = ConversionRate(rate=rate, last_reset=datetime.now())
        result = collection.insert_one(existing_data.to_dict())
    else:
        existing_data.rate = rate
        existing_data.last_reset = datetime.now()
        result = collection.update_one({"id": "conversion_rate"}, {"$set": existing_data.to_dict()})
    return result

def create_update_shop_rate(guild_id: int, rate: float):
    collection = db_specific[f'profile_{guild_id}']
    existing_data = find_conversion_rate_by_id(guild_id=guild_id)
    if existing_data == None:
        existing_data = ConversionRate(shop_rate=rate, last_reset=datetime.now())
        result = collection.insert_one(existing_data.to_dict())
    else:
        existing_data.shop_rate = rate
        existing_data.last_reset = datetime.now()
        result = collection.update_one({"id": "conversion_rate"}, {"$set": existing_data.to_dict()})
    return result