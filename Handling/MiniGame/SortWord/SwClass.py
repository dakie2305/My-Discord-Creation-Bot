from datetime import datetime
from typing import List, Optional
#region SortWordInfo
class SortWordInfo:
    def __init__(self, channel_id: int, channel_name: str, current_player_id: int = None, current_player_name: str = None, unsorted_word: str = None, current_word: str = None, special_point: int = None, special_item: Optional['SwSpecialItem'] = None, used_words: List[str] = None, special_case: bool = False, player_profiles: Optional[List['SwPlayerProfile']] = None, player_effects : Optional[List['SwPlayerEffect']] = None, player_penalty : Optional[List['PlayerPenalty']] = None, current_round: int = 0, guild_name: str = None, last_played: datetime = datetime.now()):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.guild_name = guild_name
        self.current_player_id = current_player_id
        self.current_player_name = current_player_name
        self.unsorted_word = unsorted_word
        self.current_word = current_word
        self.special_point = special_point
        self.special_item = special_item if special_item else None
        self.special_case = special_case
        self.current_round = current_round
        self.last_played = last_played
        self.used_words: List[str] = used_words if used_words else []
        self.player_profiles: List[SwPlayerProfile] = player_profiles if player_profiles else []
        self.player_effects: List[SwPlayerEffect] = player_effects if player_effects else []
        self.player_penalty: List[PlayerPenalty] = player_penalty if player_penalty else []
        
    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "guild_name": self.guild_name,
            "current_player_id": self.current_player_id,
            "current_player_name": self.current_player_name,
            "unsorted_word": self.unsorted_word,
            "current_word": self.current_word,
            "special_point": self.special_point,
            "special_case": self.special_case,
            "current_round": self.current_round,
            "last_played": self.last_played,
            "special_item": self.special_item.to_dict() if self.special_item else None,
            "used_words": [data for data in self.used_words],
            "player_profiles": [data.to_dict() for data in self.player_profiles],
            "player_effects": [data.to_dict() for data in self.player_effects],
            "player_penalty": [data.to_dict() for data in self.player_penalty],
        }

    @staticmethod
    def from_dict(data:dict):
        return SortWordInfo(
            channel_id=data.get("channel_id", None),
            channel_name=data.get("channel_name", None),
            guild_name=data.get("guild_name", None),
            current_player_id=data.get("current_player_id", None),
            current_player_name=data.get("current_player_name", None),
            unsorted_word=data.get("unsorted_word", None),
            current_word=data.get("current_word", None),
            special_point=data.get("special_point", None),
            special_case=data.get("special_case", False),
            current_round=data.get("current_round", 0),
            last_played=data.get("last_played", None),
            special_item = SwSpecialItem.from_dict(data.get("special_item", None)) if data.get("special_item") else None,
            player_profiles = [SwPlayerProfile.from_dict(item) for item in data.get("player_profiles", [])],
            player_effects = [SwPlayerEffect.from_dict(item) for item in data.get("player_effects", [])],
            player_penalty = [PlayerPenalty.from_dict(item) for item in data.get("player_penalty", [])],
            used_words = [item for item in data.get("used_words", [])],
        )



#region SwPlayerProfile   
class SwPlayerProfile:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, point: int = 0, special_items: Optional[List['SwSpecialItem']] = None):
        self.user_id = user_id 
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.point = point
        self.special_items: List[SwSpecialItem] = special_items if special_items else []
        
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
        return SwPlayerProfile(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            user_display_name=data.get("user_display_name", None),
            point=data.get("point", 0),
            special_items = [SwSpecialItem.from_dict(item) for item in data.get("special_items", [])],
        )


#region SpecialItem
class SwSpecialItem:
    def __init__(self, item_id: str, item_name: str, item_description: str, level: str, quantity: int, point:int, required_target: bool):
        self.item_id = item_id 
        self.item_name = item_name
        self.item_description = item_description
        self.required_target = required_target
        self.quantity = quantity
        self.point = point
        self.level = level
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "item_description": self.item_description,
            "quantity": self.quantity,
            "point": self.point,
            "level": self.level,
            "required_target": self.required_target,
        }

    @staticmethod
    def from_dict(data:dict):
        return SwSpecialItem(
            item_id=data.get("item_id", None),
            item_name=data.get("item_name", None),
            item_description = data.get("item_description", None),
            quantity = data.get("quantity", None),
            point = data.get("point", None),
            level = data.get("level", None),
            required_target = data.get("required_target", None),
        )


#region Player Effect
class SwPlayerEffect:
    def __init__(self, user_id: int, user_name: str, effect_id: str, effect_name: str, effect_command: str):
        self.user_id = user_id 
        self.user_name = user_name
        self.effect_id = effect_id
        self.effect_name = effect_name
        self.effect_command = effect_command
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "effect_id": self.effect_id,
            "effect_name": self.effect_name,
            "effect_command": self.effect_command,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return SwPlayerEffect(
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
            penalty_point = data.get("penalty_point", 0),
        )

list_special_items_cap_thap = [
    SwSpecialItem(
        item_id="t-",
        item_name="Trừ Điểm Đối Phương",
        item_description="Kỹ năng này sẽ trừ đi 3 điểm của đối thủ trong trò chơi.",
        quantity = 1,
        point =-3,
        level="Cấp Thấp",
        required_target=True
    ),
    SwSpecialItem(
        item_id="t+u",
        item_name="Cộng Điểm Đối Phương",
        item_description="Kỹ năng này sẽ cộng 3 điểm cho đối thủ trong trò chơi.",
        quantity = 1,
        point =3,
        level="Cấp Thấp",
        required_target=True
    ),
    SwSpecialItem(
        item_id="t+",
        item_name="Cộng Điểm Bản Thân",
        item_description="Kỹ năng này sẽ cộng 3 điểm cho bản thân.",
        quantity = 1,
        point =3,
        level="Cấp Thấp",
        required_target=False
    ),
    SwSpecialItem(
        item_id="hint",
        item_name="Gợi ý",
        item_description="Kỹ năng này sẽ gợi tý từ đúng để hoàn thành lượt hiện tại.",
        quantity = 1,
        point =3,
        level="Cấp Thấp",
        required_target=False
    ),
]

list_special_items_cap_cao = [
    SwSpecialItem(
        item_id="c-",
        item_name="Trừ Điểm Đối Phương",
        item_description="Kỹ năng này sẽ trừ đi 5 điểm của đối thủ trong trò chơi.",
        quantity = 1,
        point =-5,
        level="Cấp Cao",
        required_target=True
    ),
    SwSpecialItem(
        item_id="c+",
        item_name="Cộng Điểm Bản Thân",
        item_description="Kỹ năng này sẽ cộng 5 điểm cho bản thân.",
        quantity = 1,
        point =5,
        level="Cấp Cao",
        required_target=False
    ),
    SwSpecialItem(
        item_id="hint",
        item_name="Gợi ý",
        item_description="Kỹ năng này sẽ gợi tý từ đúng để hoàn thành lượt hiện tại.",
        quantity = 1,
        point =3,
        level="Cấp Cao",
        required_target=False
    ),
]

list_special_items_dang_cap = [
    SwSpecialItem(
        item_id="d-",
        item_name="Trừ Điểm Đối Phương",
        item_description="Kỹ năng này sẽ trừ đi 8 điểm của đối thủ trong trò chơi.",
        quantity = 1,
        point =-8,
        level="Đẳng Cấp",
        required_target=True
    ),
    SwSpecialItem(
        item_id="d+",
        item_name="Cộng Điểm Bản Thân",
        item_description="Kỹ năng này sẽ cộng 8 điểm cho bản thân.",
        quantity = 1,
        point = 8,
        level="Đẳng Cấp",
        required_target=False
    ),
]

list_special_items_toi_thuong = [
    SwSpecialItem(
        item_id="tt-",
        item_name="Trừ Điểm Đối Phương",
        item_description="Kỹ năng này sẽ trừ đi 15 điểm của đối thủ trong trò chơi.",
        quantity = 1,
        point =-15,
        level="Tối Thượng",
        required_target=True
    ),
    SwSpecialItem(
        item_id="tt+",
        item_name="Cộng Điểm Bản Thân",
        item_description="Kỹ năng này sẽ cộng 15 điểm cho bản thân.",
        quantity = 1,
        point = 15,
        level="Tối Thượng",
        required_target=False
    ),
]