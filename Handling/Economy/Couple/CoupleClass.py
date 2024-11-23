from typing import List, Optional
from datetime import datetime

class Couple:
    def __init__(self, guild_id: int, guild_name: str, first_user_id: int, first_user_name: str, first_user_display_name: str, second_user_id: int, second_user_name: str, second_user_display_name: str, date_created: datetime = datetime.now(), love_rank:int = 1, love_point: int = 0, love_progressing: int = 0, last_love_action: datetime = None, last_fight_action: datetime = None, is_ready_to_marry: bool = False, date_married: datetime= None):
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.first_user_id = first_user_id
        self.first_user_name = first_user_name
        self.first_user_display_name = first_user_display_name
        self.second_user_id = second_user_id
        self.second_user_name = second_user_name
        self.second_user_display_name = second_user_display_name
        self.date_created = date_created
        self.love_rank = love_rank
        self.love_point = love_point
        self.love_progressing = love_progressing
        self.is_ready_to_marry = is_ready_to_marry
        self.last_love_action = last_love_action if last_love_action else None
        self.last_fight_action = last_fight_action if last_fight_action else None
        self.date_married = date_married if date_married else None
        
        
    def to_dict(self):
        return {
            "guild_id": self.guild_id,
            "guild_name": self.guild_name,
            "first_user_id": self.first_user_id,
            "first_user_name": self.first_user_name,
            "first_user_display_name": self.first_user_display_name,
            "second_user_id": self.second_user_id,
            "second_user_name": self.second_user_name,
            "second_user_display_name": self.second_user_display_name,
            "date_created": self.date_created if self.date_created else None,
            "love_rank": self.love_rank,
            "love_point": self.love_point,
            "love_progressing": self.love_progressing,
            "is_ready_to_marry": self.is_ready_to_marry,
            "last_love_action": self.last_love_action if self.last_love_action else None,
            "last_fight_action": self.last_fight_action if self.last_fight_action else None,
            "date_married": self.date_married if self.date_married else None,
        }

    @staticmethod
    def from_dict(data:dict):
        return Couple(
                guild_id=data.get("guild_id", None),
                guild_name=data.get("guild_name", None),
                first_user_id=data.get("first_user_id", None),
                first_user_name=data.get("first_user_name", None),
                first_user_display_name=data.get("first_user_display_name", None),
                second_user_id=data.get("second_user_id", None),
                second_user_name=data.get("second_user_name", None),
                second_user_display_name=data.get("second_user_display_name", None),
                date_created=data.get("date_created", datetime.now()),
                love_rank=data.get("love_rank", 1),
                love_point=data.get("love_point", 0),
                love_progressing=data.get("love_progressing", 0),
                is_ready_to_marry=data.get("is_ready_to_marry", False),
                last_love_action=data.get("last_love_action", None),
                last_fight_action=data.get("last_fight_action", None),
                date_married=data.get("date_married", None),
            )
        