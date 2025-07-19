from pymongo import MongoClient
from datetime import datetime, timedelta
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel
from Handling.Economy.Global.GlobalProfileClass import GlobalProfile
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions
from Handling.Economy.Inventory_Shop.ItemClass import Item


# Connect to the MongoDB server
if UtilitiesFunctions.USER_NAME_MONGODB != "" and UtilitiesFunctions.USER_NAME_MONGODB != None and UtilitiesFunctions.PASSWORD_MONGODB != "" and UtilitiesFunctions.PASSWORD_MONGODB != None:
    client = MongoClient(f"mongodb://{UtilitiesFunctions.USER_NAME_MONGODB}:{UtilitiesFunctions.PASSWORD_MONGODB}@localhost:27017/")
else:
    client = MongoClient("mongodb://localhost:27017/")
# Create or switch to the database
db_specific = client["creation_global_database"]


#region Global Item
def find_global_profile_by_id(user_id: int):
    collection = db_specific['global_inventory']
    data = collection.find_one({"user_id": user_id})
    if data:
        return GlobalProfile.from_dict(data)
    return None

def find_all_global_items() -> list[GlobalProfile]:
    collection = db_specific['global_inventory']
    all_data = collection.find()
    return [GlobalProfile.from_dict(doc) for doc in all_data]

def delete_global_item_by_user_id(user_id: int) -> bool:
    collection = db_specific['global_inventory']
    result = collection.delete_one({"user_id": user_id})
    return result.deleted_count > 0


def create_or_update_global_item(user_id: int, user_name: str, user_display_name: str, guild_id: int, guild_name: str, item: Item, amount: int):
    collection = db_specific['global_inventory']
    existing_raw = collection.find_one({"user_id": user_id})
    item.item_worth_amount = 0 #Tránh lạm
    item.item_worth_type = "C" #Tránh lạm
    if existing_raw is None:
        # New record
        item.quantity = min(max(amount, 0), 99)
        if item.quantity <= 0: return None
        new_data = GlobalProfile(
            user_id=user_id,
            user_name=user_name,
            user_display_name=user_display_name,
            guild_id=guild_id,
            guild_name=guild_name,
            list_items=[item],
        )
        collection.insert_one(new_data.to_dict())
        return new_data

    existing_data = GlobalProfile.from_dict(existing_raw)
    # Update
    existing_data.user_name = user_name
    existing_data.user_display_name = user_display_name
    existing_data.guild_id = guild_id
    existing_data.guild_name = guild_name
    existing_data.date_updated = datetime.now()

    list_items = existing_data.list_items or []
    updated = False

    for profile_item in list_items:
        if profile_item.item_id == item.item_id:
            profile_item.quantity += amount
            profile_item.quantity = min(profile_item.quantity, 99)
            updated = True
            break

    if not updated:
        item.quantity = min(max(amount, 0), 99)
        if item.quantity > 0:
            list_items.append(item)

    list_items = [i for i in list_items if i.quantity > 0]
    # Limit max item count
    if len(list_items) > 5:
        list_items = list_items[-5:]

    # Save back to DB
    existing_data.list_items = list_items
    collection.update_one(
        {"user_id": user_id},
        {"$set": existing_data.to_dict()}
    )
    return existing_data

def transfer_item_global(user_id: int, user_name: str, user_display_name: str, guild_id: int, guild_name: str, item: Item, transfer_to_global: bool = False):
    collection = db_specific['global_inventory']
    existing_raw = collection.find_one({"user_id": user_id})
    if not existing_raw: return
    existing_data = GlobalProfile.from_dict(existing_raw)
    if not existing_data: return
    
    if transfer_to_global == False:
        #transfer_to_global false thì sẽ chuyển item từ database global sang database của server bình thường
        ProfileMongoManager.update_list_items_profile(guild_id=guild_id, guild_name=guild_name, user_id=user_id, user_name=user_name, user_display_name=user_display_name,item=item, amount = item.quantity)
        create_or_update_global_item(user_id=user_id, user_name=user_name, user_display_name=user_display_name, guild_id=guild_id, guild_name=guild_name, item=item, amount= - item.quantity)
    else:
        #transfer_to_global true thì sẽ chuyển item từ database của server bình thường sang database global
        ProfileMongoManager.update_list_items_profile(guild_id=guild_id, guild_name=guild_name, user_id=user_id, user_name=user_name, user_display_name=user_display_name,item=item, amount = - item.quantity)
        create_or_update_global_item(user_id=user_id, user_name=user_name, user_display_name=user_display_name, guild_id=guild_id, guild_name=guild_name, item=item, amount=item.quantity)
        
def update_enable_until(user_id: int, user_name: str, user_display_name: str, guild_id: int, guild_name: str):
    collection = db_specific['global_inventory']
    existing_raw = collection.find_one({"user_id": user_id})
    future = datetime.now() + timedelta(weeks=2)
    if existing_raw is None:
        # New record
        new_data = GlobalProfile(
            user_id=user_id,
            user_name=user_name,
            user_display_name=user_display_name,
            guild_id=guild_id,
            guild_name=guild_name,
            list_items=[],
            enable_until=future,
        )
        collection.insert_one(new_data.to_dict())
    else:
        collection.update_one({"user_id": user_id}, {"$set": {"enable_until": future,
                                                                                        }})

#region Global Guardian
def create_or_update_global_guardian(user_id: int, user_name: str, user_display_name: str, guild_id: int, guild_name: str, guardian: GuardianAngel):
    collection = db_specific['global_inventory']
    existing_raw = collection.find_one({"user_id": user_id})
    guardian.worth_amount = 0 #Tránh lạm
    guardian.worth_type = "C" #Tránh lạm
    if guardian.list_skills:
        for skill in guardian.list_skills:
            skill.item_worth_type = "C"
            skill.item_worth_amount = 0
    if existing_raw is None:
        # New record
        new_data = GlobalProfile(
            user_id=user_id,
            user_name=user_name,
            user_display_name=user_display_name,
            guild_id=guild_id,
            guild_name=guild_name,
            list_items=[],
            guardian=guardian,
        )
        collection.insert_one(new_data.to_dict())
        return new_data

    existing_data = GlobalProfile.from_dict(existing_raw)
    # Update
    existing_data.guardian = guardian
    existing_data.date_updated = datetime.now()
    
    collection.update_one(
        {"user_id": user_id},
        {"$set": existing_data.to_dict()}
    )
    return existing_data

def transfer_guardian_global(user_id: int, user_name: str, user_display_name: str, guild_id: int, guild_name: str, guardian: GuardianAngel, transfer_to_global: bool = False):
    collection = db_specific['global_inventory']
    existing_raw = collection.find_one({"user_id": user_id})
    if not existing_raw: return
    existing_data = GlobalProfile.from_dict(existing_raw)
    if not existing_data: return
    
    if transfer_to_global == False:
        #transfer_to_global false thì sẽ chuyển stats của database global sang database của server bình thường
        ProfileMongoManager.sync_with_global_guardian(guild_id=guild_id, user_id=user_id, guardian=guardian)
    else:
        #transfer_to_global true thì sẽ chuyển stats của database của server bình thường sang database global
        create_or_update_global_guardian(user_id=user_id, user_name=user_name, user_display_name=user_display_name, guild_id=guild_id, guild_name=guild_name, guardian = guardian)