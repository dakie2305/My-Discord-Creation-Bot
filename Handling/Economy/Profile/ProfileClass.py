from typing import List, Optional
from datetime import datetime

class Profile:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, guild_name: str, copper: int = 500, silver: int = 0, gold: int = 0, darkium: int = 0, is_authority: bool = False, last_attendance: datetime= None, last_work: datetime = None, level: int = 1, dignity_point: int = 50, quest_finished: int = 0, quote: str = None, level_progressing: int = 0, jail_time: datetime = None, last_crime: datetime = None):
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
        self.quest_finished = quest_finished
        self.quote = quote
        self.level_progressing = level_progressing
        self.jail_time = jail_time
        self.last_crime = last_crime
    
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
            "level": self.level,
            "dignity_point": self.dignity_point,
            "quest_finished": self.quest_finished,
            "quote": self.quote,
            "level_progressing": self.level_progressing,
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
                level=data.get("level", 1),
                dignity_point=data.get("dignity_point", 50),
                quest_finished=data.get("quest_finished", 0),
                level_progressing=data.get("level_progressing", 0),
                quote=data.get("quote", None),
            )
        