from datetime import date, datetime
from typing import List, Optional
#region MatchWordInfo
class MatchWordInfo:
    def __init__(self, channel_id: int, channel_name: str, guild_name: str, current_player_id: int = None, current_player_name: str = None, current_word: str = None, correct_start_word: str = None, remaining_word: int = 0, special_point: int = None, used_words: List[str] = None, current_round: int = 0, special_case = False, type: str = "A", player_profiles: Optional[List['PlayerProfile']] = None, player_effects : Optional[List['PlayerEffect']] = None, player_penalty : Optional[List['PlayerPenalty']] = None, player_ban : Optional[List['PlayerBan']] = None, last_played = datetime.now()):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.guild_name = guild_name
        self.current_player_id = current_player_id
        self.current_player_name = current_player_name
        self.current_word = current_word
        self.correct_start_word = correct_start_word
        self.remaining_word = remaining_word
        self.special_point = special_point
        self.current_round = current_round
        self.special_case = special_case
        self.type = type
        self.last_played = last_played
        self.used_words: List[str] = used_words if used_words else []
        self.player_profiles: List[PlayerProfile] = player_profiles if player_profiles else []
        self.player_effects: List[PlayerEffect] = player_effects if player_effects else []
        self.player_penalty: List[PlayerPenalty] = player_penalty if player_penalty else []
        self.player_ban: List[PlayerBan] = player_ban if player_ban else []
    
    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "guild_name": self.guild_name,
            "current_player_id": self.current_player_id,
            "current_player_name": self.current_player_name,
            "current_word": self.current_word,
            "correct_start_word": self.correct_start_word,
            "remaining_word": self.remaining_word,
            "special_point": self.special_point,
            "current_round": self.current_round,
            "last_played": self.last_played,
            "special_case": self.special_case,
            "type": self.type,
            "used_words": [data for data in self.used_words],
            "player_profiles": [data.to_dict() for data in self.player_profiles],
            "player_effects": [data.to_dict() for data in self.player_effects],
            "player_penalty": [data.to_dict() for data in self.player_penalty],
            "player_ban": [data.to_dict() for data in self.player_ban],

        }

    @staticmethod
    def from_dict(data:dict):
        return MatchWordInfo(
            channel_id=data.get("channel_id", None),
            channel_name=data.get("channel_name", None),
            guild_name=data.get("guild_name", None),
            current_player_id=data.get("current_player_id", None),
            current_player_name=data.get("current_player_name", None),
            current_word=data.get("current_word", None),
            correct_start_word=data.get("correct_start_word", None),
            remaining_word=data.get("remaining_word", None),
            special_point=data.get("special_point", None),
            current_round=data.get("current_round", 0),
            last_played=data.get("last_played", datetime.now()),
            used_words = [item for item in data.get("used_words", [])],
            player_profiles = [PlayerProfile.from_dict(item) for item in data.get("player_profiles", [])],
            player_effects = [PlayerEffect.from_dict(item) for item in data.get("player_effects", [])],
            player_penalty = [PlayerPenalty.from_dict(item) for item in data.get("player_penalty", [])],
            player_ban = [PlayerBan.from_dict(item) for item in data.get("player_ban", [])],
        )

#region SwPlayerProfile   
class PlayerProfile:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, point: int = 0, special_items: Optional[List['SpecialItem']] = None):
        self.user_id = user_id 
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.point = point
        self.special_items: List[SpecialItem] = special_items if special_items else []
        
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "point": self.point,
            "special_items": [data.to_dict() for data in self.special_items],
        }

    @staticmethod
    def from_dict(data:dict):
        return PlayerProfile(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            user_display_name=data.get("user_display_name", None),
            point=data.get("point", 0),
            special_items = [SpecialItem.from_dict(item) for item in data.get("special_items", [])],
        )


#region SpecialItem
class SpecialItem:
    def __init__(
        self,
        item_id: str,
        item_name: str,
        item_description: str,
        level: str,
        quantity: int = 1,
        point: int = 0,
        required_target: bool = False
    ):
        self.item_id = item_id
        self.item_name = item_name
        self.item_description = item_description
        self.level = level
        self.quantity = quantity
        self.point = point
        self.required_target = required_target

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "item_description": self.item_description,
            "level": self.level,
            "quantity": self.quantity,
            "point": self.point,
            "required_target": self.required_target
        }

    @staticmethod
    def from_dict(data: dict) -> "SpecialItem":
        return SpecialItem(
            item_id=data.get("item_id", ""),
            item_name=data.get("item_name", ""),
            item_description=data.get("item_description", ""),
            level=data.get("level", None),
            quantity=data.get("quantity", 1),
            point=data.get("point", 0),
            required_target=data.get("required_target", False)
        )

#region Player Effect
class PlayerEffect:
    def __init__(self, user_id: int, user_name: str, effect_id: str, effect_name: str):
        self.user_id = user_id 
        self.user_name = user_name
        self.effect_id = effect_id
        self.effect_name = effect_name
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "effect_id": self.effect_id,
            "effect_name": self.effect_name,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return PlayerEffect(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            effect_id = data.get("effect_id", None),
            effect_name = data.get("effect_name", None),
        )

#region PlayerPenalty
class PlayerPenalty:
    def __init__(self, user_id: int, user_name: str, timestamp: datetime = datetime.now(), penalty_point: int = 0):
        self.user_id = user_id 
        self.user_name = user_name
        self.timestamp = timestamp
        self.penalty_point = penalty_point
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "timestamp": self.timestamp,
            "penalty_point": self.penalty_point,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return PlayerPenalty(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            timestamp = data.get("timestamp", None),
            penalty_point = data.get("timestamp", 0),
        )
        
#region Player Ban
class PlayerBan:
    def __init__(self, user_id: int, user_name: str, ban_remain: int = 0):
        self.user_id = user_id 
        self.user_name = user_name
        self.ban_remain = ban_remain
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "ban_remain": self.ban_remain,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return PlayerPenalty(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            ban_remain = data.get("ban_remain", None),
        )