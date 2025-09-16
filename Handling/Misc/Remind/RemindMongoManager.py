import uuid
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Misc.Remind.RemindClass import Remind
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions


# Connect to the MongoDB server
if UtilitiesFunctions.USER_NAME_MONGODB != "" and UtilitiesFunctions.USER_NAME_MONGODB != None and UtilitiesFunctions.PASSWORD_MONGODB != "" and UtilitiesFunctions.PASSWORD_MONGODB != None:
    client = MongoClient(f"mongodb://{UtilitiesFunctions.USER_NAME_MONGODB}:{UtilitiesFunctions.PASSWORD_MONGODB}@localhost:27017/")
else:
    client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["creation_global_database"]


#region Global Item
def find_remind_by_id(remind_id: str):
    collection = db_specific['reminds']
    data = collection.find_one({"remind_id": remind_id})
    if data:
        return Remind.from_dict(data)
    return None

def find_due_reminds():
    collection = db_specific['reminds']
    now = datetime.now()
    cursor = collection.find({"date_remind": {"$lte": now}})
    return [Remind.from_dict(doc) for doc in cursor]

def find_all_reminds_by_user(user_id: int):
    collection = db_specific['reminds']
    cursor = collection.find({"user_id": user_id})
    return [Remind.from_dict(doc) for doc in cursor]

def count_reminds_by_user(user_id: int) -> int:
    collection = db_specific['reminds']
    return collection.count_documents({"user_id": user_id})

def find_all_reminds_by_user_and_guild(user_id: int, guild_id: int):
    collection = db_specific['reminds']
    cursor = collection.find({"user_id": user_id, "guild_id": guild_id})
    return [Remind.from_dict(doc) for doc in cursor]

def delete_remind_by_id(remind_id: str) -> bool:
    collection = db_specific['reminds']
    result = collection.delete_one({"remind_id": remind_id})
    return result.deleted_count > 0

def delete_old_reminds():
    """Delete all reminders older than 9 months from now."""
    collection = db_specific['reminds']
    cutoff_date = datetime.now() - timedelta(days=30 * 9)  # ~9 months
    collection.delete_many({"date_remind": {"$lte": cutoff_date}})

def create_or_update_remind(remind_id: str | None, user_id: int, user_name: str, user_display_name: str, guild_id: int, guild_name: str, channel_id: int, channel_name: str, message_content: str, date_remind: datetime):
    collection = db_specific["reminds"]
    if remind_id is None:
        # New remind
        remind_id = str(uuid.uuid4())
        new_data = Remind(
            user_id=user_id,
            user_name=user_name,
            user_display_name=user_display_name,
            guild_id=guild_id,
            guild_name=guild_name,
            channel_id=channel_id,
            channel_name=channel_name,
            message_content=message_content,
            date_remind=date_remind,
        )
        doc = new_data.to_dict()
        doc["remind_id"] = remind_id
        collection.insert_one(doc)
        return new_data

    # Update existing remind
    existing_raw = collection.find_one({"remind_id": remind_id})
    if not existing_raw:
        return None

    updated_fields = {
        "user_id": user_id,
        "user_name": user_name,
        "user_display_name": user_display_name,
        "guild_id": guild_id,
        "guild_name": guild_name,
        "channel_id": channel_id,
        "channel_name": channel_name,
        "message_content": message_content,
        "date_remind": date_remind,
    }
    collection.update_one(
        {"remind_id": remind_id},
        {"$set": updated_fields}
    )
    existing_raw.update(updated_fields)
    return Remind.from_dict(existing_raw)