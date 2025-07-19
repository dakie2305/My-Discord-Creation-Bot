
from datetime import datetime, timedelta
from typing import List, Optional
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel
from Handling.Economy.Inventory_Shop.ItemClass import Item

class GlobalProfile:
    def __init__(self, user_id: str, user_name: str, user_display_name: str, guild_name: str, guild_id: int, date_created: datetime = None, date_updated: datetime = None, list_items : Optional[List['Item']] = None, guardian: GuardianAngel = None, enable_until: datetime = datetime.now()):
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.guild_name = guild_name
        self.guild_id = guild_id
        self.date_created = date_created if date_created else datetime.now()
        self.date_updated = date_updated if date_updated else datetime.now()
        self.enable_until = enable_until
        self.guardian = guardian
        
        self.list_items: List[Item] = list_items if list_items else []

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "guild_id": self.guild_id,
            "guild_name": self.guild_name,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "enable_until": self.enable_until,
            "guardian": self.guardian.to_dict() if self.guardian else None,
            "list_items": [data.to_dict() for data in self.list_items],
        }

    @staticmethod
    def from_dict(data:dict) -> 'GlobalProfile':
        return GlobalProfile(
                user_id=data.get("user_id", None),
                user_name=data.get("user_name", None),
                user_display_name=data.get("user_display_name", None),
                guild_id=data.get("guild_id", None),
                guild_name=data.get("guild_name", None),
                date_created=data.get("date_created", datetime.now()),
                date_updated=data.get("date_updated", datetime.now()),
                enable_until=data.get("enable_until", datetime.now()),
                
                guardian = GuardianAngel.from_dict(data.get("guardian", None)) if data.get("guardian") else None,
                list_items = [Item.from_dict(item) for item in data.get("list_items", [])],
            )
