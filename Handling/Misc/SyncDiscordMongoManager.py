from typing import Optional, List
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Misc.DonatorClass import Donator
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from bson.int64 import Int64
from datetime import datetime, timedelta

# Connect to the MongoDB server
if UtilitiesFunctions.USER_NAME_MONGODB != "" and UtilitiesFunctions.USER_NAME_MONGODB != None and UtilitiesFunctions.PASSWORD_MONGODB != "" and UtilitiesFunctions.PASSWORD_MONGODB != None:
    client = MongoClient(f"mongodb://{UtilitiesFunctions.USER_NAME_MONGODB}:{UtilitiesFunctions.PASSWORD_MONGODB}@localhost:27017/")
else:
    client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["misc_database"]
collection = db_specific["discord_chat"]

def insert_message(
    message_id: int,
    channel_id: int,
    guild_id: int,

    author_id: int,
    author_username: str,
    author_display_name: str,

    content: str,
    created_at: datetime,

    edited_at: Optional[datetime] = None,
    attachments: Optional[List[str]] = None,
    embeds: Optional[List[dict]] = None,
    author_image: Optional[str] = None,


    is_bot: bool = False,
    source: str = "discord"
):
    collection.insert_one({
        "message_id": Int64(message_id),
        "channel_id": Int64(channel_id),
        "guild_id": Int64(guild_id),

        "author_id": Int64(author_id),
        "author_username": author_username,
        "author_display_name": author_display_name,
        "author_image": author_image,

        "content": content,

        "created_at": created_at,
        "edited_at": edited_at,

        "attachments": attachments or [],
        "embeds": embeds or [],

        "is_bot": is_bot,
        "source": source,
    })
    
def get_messages(channel_id: int, page: int = 0, limit: int = 20):
    data = list(
        collection.find({"channel_id": Int64(channel_id)})
        .sort("created_at", -1)
        .skip(page * limit)
        .limit(limit)
    )
    return data


def cleanup_old_messages(days: int = 30):
    cutoff = datetime.utcnow() - timedelta(days=days)

    result = collection.delete_many({
        "created_at": {"$lt": cutoff}
    })

    return result.deleted_count