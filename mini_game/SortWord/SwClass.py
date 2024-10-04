from typing import List, Optional
#region SortWordInfo
class SortWordInfo:
    def __init__(self, channel_id: int, channel_name: str, current_player_id: int = None, current_player_name: str = None, unsorted_word: str = None, current_word: str = None, special_point: int = None, special_item: Optional['SwSpecialItem'] = None, used_words: List[str] = None, special_case: bool = False, player_profiles: Optional[List['SwPlayerProfile']] = None, player_effects : Optional[List['SwPlayerEffect']] = None, player_bans : Optional[List['SwPlayerBan']] = None):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.current_player_id = current_player_id
        self.current_player_name = current_player_name
        self.unsorted_word = unsorted_word
        self.current_word = current_word
        self.special_point = special_point
        self.special_item = special_item if special_item else None
        self.special_case = special_case
        self.used_words: List[str] = used_words if used_words else []
        self.player_profiles: List[SwPlayerProfile] = player_profiles if player_profiles else []
        self.player_effects: List[SwPlayerEffect] = player_effects if player_effects else []
        self.player_bans: List[SwPlayerBan] = player_bans if player_bans else []
    
    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "current_player_id": self.current_player_id,
            "current_player_name": self.current_player_name,
            "unsorted_word": self.unsorted_word,
            "current_word": self.current_word,
            "special_point": self.special_point,
            "special_case": self.special_case,
            "special_item": self.special_item.to_dict() if self.special_item else None,
            "used_words": [data for data in self.used_words],
            "player_profiles": [data.to_dict() for data in self.player_profiles],
            "player_effects": [data.to_dict() for data in self.player_effects],
            "player_bans": [data.to_dict() for data in self.player_bans],
        }

    @staticmethod
    def from_dict(data:dict):
        return SortWordInfo(
            channel_id=data.get("channel_id", None),
            channel_name=data.get("channel_name", None),
            current_player_id=data.get("current_player_id", None),
            current_player_name=data.get("current_player_name", None),
            unsorted_word=data.get("unsorted_word", None),
            current_word=data.get("current_word", None),
            special_point=data.get("special_point", None),
            special_case=data.get("special_case", False),
            special_item = SwSpecialItem.from_dict(data.get("special_item", None)) if data.get("special_item") else None,
            player_profiles = [SwPlayerProfile.from_dict(item) for item in data.get("player_profiles", [])],
            player_effects = [SwPlayerEffect.from_dict(item) for item in data.get("player_effects", [])],
            player_bans = [SwPlayerBan.from_dict(item) for item in data.get("player_bans", [])],
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
    def __init__(self, item_id: str, item_name: str, item_description: str, level: str, quantity: int, point:int, required_target: bool, item_command):
        self.item_id = item_id 
        self.item_name = item_name
        self.item_description = item_description
        self.required_target = required_target
        self.quantity = quantity
        self.point = point
        self.level = level
        self.item_command =item_command
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "item_description": self.item_description,
            "quantity": self.quantity,
            "point": self.point,
            "level": self.level,
            "required_target": self.required_target,
            "item_command": self.item_command
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
            item_command = data.get("item_command", None),
        )


#region Player Effect
class SwPlayerEffect:
    def __init__(self, user_id: int, username: str, effect_id: str, effect_name: str, effect_command: str):
        self.user_id = user_id 
        self.username = username
        self.effect_id = effect_id
        self.effect_name = effect_name
        self.effect_command = effect_command
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "effect_id": self.effect_id,
            "effect_name": self.effect_name,
            "effect_command": self.effect_command,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return SwPlayerEffect(
            user_id=data.get("user_id", None),
            username=data.get("username", None),
            effect_id = data.get("effect_id", None),
            effect_name = data.get("effect_name", None),
        )


#region Player Ban
class SwPlayerBan:
    def __init__(self, user_id: int, username: str, ban_remaining: int):
        self.user_id = user_id 
        self.username = username
        self.ban_remaining = ban_remaining
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "ban_remaining": self.ban_remaining,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return SwPlayerBan(
            user_id=data.get("user_id", None),
            username=data.get("username", None),
            ban_remaining = data.get("ban_remaining", 0),
        )