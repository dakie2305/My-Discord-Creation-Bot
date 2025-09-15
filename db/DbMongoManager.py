import json
import os
from typing import List
from pymongo import MongoClient
from datetime import datetime, timedelta
from db.Class.CustomClass import UserInfo, GuildExtraInfo, UserConversationInfo, ConversationInfo, SnipeChannelInfo, SnipeMessage, SnipeMessageAttachments, PreDeleteAttachmentsInfo
from db.Class.UserCountClass import UserCount
import CustomFunctions
from pathlib import Path
from Handling.Economy.Quest.DungeonQuestChannelClass import DungeonQuestChannel


#region User Info Database

def create_user(user_info, chosen_collection):
    collection = db[chosen_collection]
    existing_user = collection.find_one({"user_id": user_info.user_id})
    if existing_user:
      return f"User with user_id {user_info.user_id} already exists."
    result = collection.insert_one(user_info.to_dict())
    return result

def update_user_jail_time(user_id: int, jailer_id: int, jailer_user_name: str, jailer_display_name: str, reason: str, jail_until: datetime):
    collection = db['jailed_user']
    existing_user = collection.find_one({"user_id": user_id})
    if existing_user:
        collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "jailer_id": jailer_id,
                    "jailer_user_name": jailer_user_name,
                    "jailer_display_name": jailer_display_name,
                    "reason": reason,
                    "jail_until": jail_until
                }
            }
        )
  
def find_user_by_id(user_id, chosen_collection):
    collection = db[chosen_collection]
    user_data = collection.find_one({"user_id": user_id})
    if user_data:
        return UserInfo.from_dict(user_data)
    return None

def find_all_users(chosen_collection):
    collection = db[chosen_collection]
    users_data = list(collection.find())
    return [UserInfo.from_dict(user_data) for user_data in users_data]


def update_guild_extra_info(user_id, update_data, chosen_collection):
    collection = db[chosen_collection]
    result = collection.update_one({"user_id": user_id}, {"$set": update_data})
    return result
  
def delete_user_by_id(user_id, chosen_collection):
    collection = db[chosen_collection]
    result = collection.delete_one({"user_id": user_id})
    return result

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

def get_all_snipe_guild_ids() -> List[int]:
    """Return a list of guild IDs that have Snipe Info collections."""
    db_specific = client['guild_database']
    guild_ids: List[int] = []
    for collection_name in db_specific.list_collection_names():
        if not collection_name.startswith("snipe_info_guild_"):
            continue  # skip malformed names
        try:
            guild_id = int(collection_name.split("snipe_info_guild_")[1])
            if guild_id not in guild_ids:
                guild_ids.append(guild_id)
        except ValueError:
            continue
    return guild_ids

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



def find_user_count_by_id(guild_id: int, user_id: int):
    db_specific = client['misc_database']
    collection = db_specific[f'{guild_id}_user_count']
    existing_data = collection.find_one({"user_id": user_id})
    if existing_data:
        return UserCount.from_dict(existing_data)
    return None

def find_all_user_count_by_guild(guild_id: int):
    db_specific = client['misc_database']
    collection = db_specific[f'{guild_id}_user_count']
    data = list(collection.find())
    return [UserCount.from_dict(user) for user in data]

def get_all_user_count_guild_ids() -> List[int]:
    """Return a list of guild IDs that have user_count collections."""
    db_specific = client['misc_database']
    guild_ids: List[int] = []
    for collection_name in db_specific.list_collection_names():
        if not collection_name.endswith("_user_count"):
            continue  # skip unrelated collections
        try:
            guild_id_str = collection_name.replace("_user_count", "")
            guild_id = int(guild_id_str)
            if guild_id not in guild_ids:
                guild_ids.append(guild_id)
        except ValueError:
            continue  # skip malformed collection names
    return guild_ids


def delete_user_count(guild_id: int, user_id: int):
    collection = db_specific[f'{guild_id}_user_count']
    result = collection.delete_one({"user_id": user_id})
    return result

def drop_user_count_info_collection_if_empty(guild_id: int):
    db_specific = client['misc_database']
    collection = db_specific[f'{guild_id}_user_count']
    if collection is not None and collection.estimated_document_count() == 0:
        collection.drop()
        print(f"Collection '{guild_id}_user_count' dropped because it was empty.")

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