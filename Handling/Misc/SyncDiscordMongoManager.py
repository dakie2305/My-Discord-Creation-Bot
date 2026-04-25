from typing import Optional, List
import discord
from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Misc.DonatorClass import Donator
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from bson.int64 import Int64
from datetime import datetime, timedelta
import requests
import re

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
    message: discord.Message,

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
    clean_content = resolve_mentions(content, message)
    result = collection.insert_one({
        "message_id": Int64(message_id),
        "channel_id": Int64(channel_id),
        "guild_id": Int64(guild_id),

        "author_id": Int64(author_id),
        "author_username": author_username,
        "author_display_name": author_display_name,
        "author_image": author_image,

        "content": clean_content,

        "created_at": created_at,
        "edited_at": edited_at,

        "attachments": attachments or [],
        "embeds": embeds or [],

        "is_bot": is_bot,
        "source": source,
    })
    if result.inserted_id:
        notify_laravel_broadcast(str(result.inserted_id))

def resolve_mentions(content: str, message: discord.Message):
    if not message:
        return content
    def replace(match):
        raw = match.group(1)  # e.g. @123, @!123, @&123, #123
        # USER
        if raw.startswith("@") and not raw.startswith("@&"):
            user_id = int(raw.replace("@", "").replace("!", ""))
            user = next((u for u in message.mentions if u.id == user_id), None)
            if not user and message.guild:
                user = message.guild.get_member(user_id)
            return f"@{user.display_name}" if user else match.group(0)

        # CHANNEL
        if raw.startswith("#"):
            channel_id = int(raw[1:])
            channel = next((c for c in message.channel_mentions if c.id == channel_id), None)
            if not channel and message.guild:
                channel = message.guild.get_channel(channel_id)
            return f"#{channel.name}" if channel else match.group(0)

        # ROLE
        if raw.startswith("@&"):
            role_id = int(raw[2:])
            role = message.guild.get_role(role_id) if message.guild else None
            return f"@{role.name}" if role else match.group(0)
        return match.group(0)
    return re.sub(r"<(@!?\d+|@&\d+|#\d+)>", replace, content)


def notify_laravel_broadcast(mongo_id: str):
    targets = [
        "https://asura.com.vn/api/discord/message-sync"
    ]
    payload = {"id": mongo_id}
    for url in targets:
        try:
            response = requests.post(url, json=payload, timeout=3) 
            if response.status_code == 200:
                print(f"[{url}] Successfully signaled: {mongo_id}")
            else:
                print(f"[{url}] Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"[{url}] Failed to connect: {e}")
    
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