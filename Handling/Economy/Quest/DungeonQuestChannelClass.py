from typing import List, Optional
from datetime import datetime

class DungeonQuestChannel:
    def __init__(self, channel_id: int, channel_name: str, difficulty_level: int = 1):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.difficulty_level = difficulty_level
        
    
    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "difficulty_level": self.difficulty_level,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return DungeonQuestChannel(
                channel_id=data.get("channel_id", None),
                channel_name=data.get("channel_name", None),
                difficulty_level=data.get("difficulty_level", 1),
            )

