from typing import List, Optional
from datetime import datetime

class QuestProfile:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, guild_name: str, quest_type: str, quest_channel: int, channel_name: str, quest_title: str, quest_description: str, quest_total_progress: int, quest_progress:int = 0, truth_game_count: int = 0, dare_game_count: int = 0, coin_flip_count = 0, rps_count = 0, quest_reward_copper:int = 0, quest_reward_silver:int = 0, quest_reward_gold : int = 0, quest_difficult_rate: int = 0, bonus_exp: int = 0, reset_date: datetime = None):
        self.id = "quest"
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.guild_name = guild_name
        self.quest_type = quest_type
        self.quest_channel = quest_channel
        self.channel_name = channel_name
        self.quest_title = quest_title
        self.quest_description = quest_description
        self.quest_progress = quest_progress
        self.quest_total_progress = quest_total_progress
        self.truth_game_count = truth_game_count
        self.dare_game_count = dare_game_count
        self.coin_flip_count = coin_flip_count
        self.rps_count = rps_count
        self.quest_reward_copper = quest_reward_copper
        self.quest_reward_silver = quest_reward_silver
        self.quest_reward_gold = quest_reward_gold
        self.quest_difficult_rate = quest_difficult_rate
        self.bonus_exp = bonus_exp
        self.reset_date = reset_date if reset_date else None
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "guild_name": self.guild_name,
            "quest_type": self.quest_type,
            "quest_channel": self.quest_channel,
            "channel_name": self.channel_name,
            "quest_title": self.quest_title,
            "quest_description": self.quest_description,
            "quest_progress": self.quest_progress,
            "quest_total_progress": self.quest_total_progress,
            "truth_game_count": self.truth_game_count,
            "dare_game_count": self.dare_game_count,
            "coin_flip_count": self.coin_flip_count,
            "rps_count": self.rps_count,
            "quest_reward_copper": self.quest_reward_copper,
            "quest_reward_silver": self.quest_reward_silver,
            "quest_reward_gold": self.quest_reward_gold,
            "quest_difficult_rate": self.quest_difficult_rate,
            "bonus_exp": self.bonus_exp,
            "reset_date": self.reset_date,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return QuestProfile(
                user_id=data.get("user_id", None),
                user_name=data.get("user_name", None),
                user_display_name=data.get("user_display_name", None),
                guild_name=data.get("guild_name", None),
                quest_type=data.get("quest_type", None),
                quest_channel=data.get("quest_channel", None),
                channel_name=data.get("channel_name", None),
                quest_title=data.get("quest_title", None),
                quest_description=data.get("quest_description", None),
                quest_progress=data.get("quest_progress", None),
                quest_total_progress=data.get("quest_total_progress", None),
                truth_game_count=data.get("truth_game_count", None),
                dare_game_count=data.get("dare_game_count", None),
                coin_flip_count=data.get("coin_flip_count", None),
                rps_count=data.get("rps_count", None),
                quest_reward_copper=data.get("quest_reward_copper", None),
                quest_reward_silver=data.get("quest_reward_silver", None),
                quest_reward_gold=data.get("quest_reward_gold", None),
                quest_difficult_rate=data.get("quest_difficult_rate", None),
                bonus_exp=data.get("bonus_exp", None),
                reset_date=data.get("reset_date", None),
            )

list_quest_general_type = [
    "emoji_reaction_count", 
    "message_count", 
    "attachments_count", 
    "truth_game_count",
    "dare_game_count",
    "coin_flip_game_count",
    "rps_game_count",
    ]