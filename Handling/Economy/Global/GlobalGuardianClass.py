
from datetime import datetime
from typing import List, Optional
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel

class GlobalGuardian:
    def __init__(self, user_id: str, user_name: str, user_display_name: str, guild_name: str, guild_id: int, date_created: datetime = datetime.now(), date_updated: datetime = datetime.now(), guardian: GuardianAngel = None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.guild_name = guild_name
        self.guild_id = guild_id
        self.date_created = date_created
        self.date_updated = date_updated
        self.guardian = guardian
        

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "guild_name": self.guild_name,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
            "guardian": self.guardian,
        }

    @staticmethod
    def from_dict(data:dict) -> 'GlobalGuardian':
        return GlobalGuardian(
                user_id=data.get("user_id", None),
                user_name=data.get("user_name", None),
                user_display_name=data.get("user_display_name", None),
                guild_name=data.get("guild_name", None),
                date_created=data.get("date_created", datetime.now()),
                date_updated=data.get("date_updated", datetime.now()),
                guardian=data.get("guardian", None),
            )
