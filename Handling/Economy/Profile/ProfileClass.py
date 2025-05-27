from typing import List, Optional
from datetime import datetime
from Handling.Economy.Inventory_Shop.ItemClass import Item, PlantItem
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel

class Profile:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, guild_name: str, copper: int = 500, silver: int = 0, gold: int = 0, darkium: int = 0, is_authority: bool = False, last_attendance: datetime= None, last_work: datetime = None, level: int = 1, dignity_point: int = 50, quest_finished: int = 0, quote: str = None, level_progressing: int = 0, jail_time: datetime = None, last_crime: datetime = None, last_riot: datetime = None, last_gift: datetime = None, last_attack_item_used: datetime = None, gift_given: int = 0, list_items : Optional[List['Item']] = None, protection_item: Item = None, daily_streak_count: int = 0, last_breakup: datetime = None, attack_item: Item = None, last_fishing: datetime = None, plant: PlantItem = None, guardian: GuardianAngel = None, profile_color: int = None):
        self.id = "profile"
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.guild_name = guild_name
        self.copper = copper
        self.silver = silver
        self.gold = gold
        self.darkium = darkium
        self.is_authority = is_authority
        self.last_attendance = last_attendance
        self.last_work = last_work
        self.level = level
        self.dignity_point = dignity_point
        self.daily_streak_count = daily_streak_count
        self.quest_finished = quest_finished
        self.quote = quote
        self.level_progressing = level_progressing
        self.gift_given = gift_given
        self.jail_time = jail_time
        self.last_crime = last_crime
        self.last_riot = last_riot
        self.last_gift = last_gift
        self.last_attack_item_used = last_attack_item_used
        self.last_breakup = last_breakup
        self.last_fishing = last_fishing
        self.profile_color = profile_color
        
        self.protection_item = protection_item if protection_item else None
        self.attack_item = attack_item if attack_item else None
        self.plant = plant if plant else None
        self.guardian = guardian if guardian else None
        
        self.list_items: List[Item] = list_items if list_items else []
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "guild_name": self.guild_name,
            "copper": self.copper,
            "silver": self.silver,
            "gold": self.gold,
            "darkium": self.darkium,
            "is_authority": self.is_authority,
            "last_attendance": self.last_attendance if self.last_attendance else None,  # Convert to ISO format
            "last_work": self.last_work if self.last_work else None,
            "jail_time": self.jail_time if self.jail_time else None,
            "last_crime": self.last_crime if self.last_crime else None,
            "last_riot": self.last_riot if self.last_riot else None,
            "last_gift": self.last_gift if self.last_gift else None,
            "last_attack_item_used": self.last_attack_item_used if self.last_attack_item_used else None,
            "last_breakup": self.last_breakup if self.last_breakup else None,
            "last_fishing": self.last_fishing if self.last_fishing else None,
            "level": self.level,
            "dignity_point": self.dignity_point,
            "quest_finished": self.quest_finished,
            "quote": self.quote,
            "level_progressing": self.level_progressing,
            "gift_given": self.gift_given,
            "daily_streak_count": self.daily_streak_count,
            "profile_color": self.profile_color,
            
            "protection_item": self.protection_item.to_dict() if self.protection_item else None,
            "attack_item": self.attack_item.to_dict() if self.attack_item else None,
            "plant": self.plant.to_dict() if self.plant else None,
            "guardian": self.guardian.to_dict() if self.guardian else None,
            
            "list_items": [data.to_dict() for data in self.list_items],
        }

    @staticmethod
    def from_dict(data:dict):
        return Profile(
                user_id=data.get("user_id", None),
                user_name=data.get("user_name", None),
                user_display_name=data.get("user_display_name", None),
                guild_name=data.get("guild_name", None),
                copper=data.get("copper", 0),
                silver=data.get("silver", 0),
                gold=data.get("gold", 0),
                darkium=data.get("darkium", 0),
                is_authority=data.get("is_authority", False),
                last_attendance=data.get("last_attendance", None),  
                last_work=data.get("last_work", None),             
                jail_time=data.get("jail_time", None),             
                last_crime=data.get("last_crime", None),             
                last_riot=data.get("last_riot", None),
                last_gift=data.get("last_gift", None),
                last_attack_item_used=data.get("last_attack_item_used", None),
                last_breakup=data.get("last_breakup", None),
                last_fishing=data.get("last_fishing", None),
                level=data.get("level", 1),
                dignity_point=data.get("dignity_point", 50),
                quest_finished=data.get("quest_finished", 0),
                level_progressing=data.get("level_progressing", 0),
                gift_given=data.get("gift_given", 0),
                daily_streak_count=data.get("daily_streak_count", 0),
                quote=data.get("quote", None),
                profile_color=data.get("profile_color", None),
                
                protection_item = Item.from_dict(data.get("protection_item", None)) if data.get("protection_item") else None,
                attack_item = Item.from_dict(data.get("attack_item", None)) if data.get("attack_item") else None,
                plant = PlantItem.from_dict(data.get("plant", None)) if data.get("plant") else None,
                guardian = GuardianAngel.from_dict(data.get("guardian", None)) if data.get("guardian") else None,
                
                list_items = [Item.from_dict(item) for item in data.get("list_items", [])],
            )
        