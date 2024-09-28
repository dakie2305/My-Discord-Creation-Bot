from typing import List, Optional
from datetime import datetime, timedelta

#region RPS Info Class
class RpsInfo:
    def __init__(self, guild_id: int, guild_name: str, ban_list: Optional[List['RpsBanInfo']] = None):
        self.id = "rps_info"
        self.guild_id = guild_id 
        self.guild_name = guild_name
        self.ban_list: List[RpsBanInfo] = ban_list if ban_list else []
    
    def to_dict(self):
        return {
            "id": self.id,
            "guild_id": self.guild_id,
            "guild_name": self.guild_name,
            "ban_list": [data.to_dict() for data in self.ban_list],
        }

    @staticmethod
    def from_dict(data:dict):
        return RpsInfo(
            id = "rps_info",
            guild_id=data.get("guild_id", None),
            guild_name=data.get("guild_name", None),
            ban_list = [RpsBanInfo.from_dict(item) for item in data.get("ban_list", [])],
        )
        
#region RpsPlayerProfile   
class RpsPlayerProfile:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, win_point: int, lose_point: int, draw_point: int, legendary_point: int, humiliated_point: int, game_consecutive_round_win: int, game_consecutive_round_lose: int):
        self.id = "player_profile"
        self.user_id = user_id 
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.win_point = win_point
        self.lose_point = lose_point
        self.draw_point = draw_point
        self.game_consecutive_round_win = game_consecutive_round_win
        self.game_consecutive_round_lose = game_consecutive_round_lose
        self.humiliated_point = humiliated_point    #Thua 5 lần liên tiếp
        self.legendary_point = legendary_point      #Thắng 5 lần liên tiếp
        
    def to_dict(self):
        return {
            "id": "player_profile",
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "win_point": self.win_point,
            "lose_point": self.lose_point,
            "draw_point": self.draw_point,
            "humiliated_point": self.humiliated_point,
            "legendary_point": self.legendary_point,
            "game_consecutive_round_win": self.game_consecutive_round_win,
            "game_consecutive_round_lose": self.game_consecutive_round_lose,
        }

    @staticmethod
    def from_dict(data:dict):
        return RpsPlayerProfile(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            user_display_name=data.get("user_display_name", None),
            win_point=data.get("win_point", 0),
            lose_point=data.get("lose_point", 0),
            draw_point=data.get("draw_point", 0),
            humiliated_point=data.get("humiliated_point", 0),
            legendary_point=data.get("legendary_point", 0),
            game_consecutive_round_win=data.get("game_consecutive_round_win", 0),
            game_consecutive_round_lose=data.get("game_consecutive_round_lose", 0),
        )
        
#region ConsecutiveRpsPlayerProfile   
class ConsecutiveRpsPlayerProfile:
    def __init__(self, user_id: int, user_name: str, con_win_time: int = 0, con_lose_time: int = 0):
        self.user_id = user_id 
        self.user_name = user_name
        self.con_win_time = con_win_time
        self.con_lose_time = con_lose_time
        
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "con_win_time": self.con_win_time,
            "con_lose_time": self.con_lose_time,
        }
    @staticmethod
    def from_dict(data:dict):
        return ConsecutiveRpsPlayerProfile(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            con_win_time=data.get("con_win_time", None),
            con_lose_time=data.get("con_lose_time", None),
        )

#region RpsBanInfo
class RpsBanInfo:
    def __init__(self, user_id: int, user_name: str, ban_remaining: int):
        self.user_id = user_id 
        self.user_name = user_name
        self.ban_remaining = ban_remaining
        
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "ban_remaining": self.ban_remaining,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return RpsBanInfo(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            ban_remaining=data.get("ban_remaining", None),
        )
#region RpsGameSession        
class RpsGameSession:
    def __init__(self, player_1_id: int, player_1_username: str, player_1_choice: str, player_2_id: int, player_2_choice: str, player_2_username: str, message_id: int, channel_id: int):
        self.id = "game_session"
        self.player_1_id = player_1_id
        self.player_1_username = player_1_username
        self.player_1_choice = player_1_choice
        self.player_2_id = player_2_id
        self.player_2_username = player_2_username
        self.player_2_choice = player_2_choice
        self.message_id = message_id
        self.channel_id = channel_id
        
    def to_dict(self):
        return {
            "id": "game_session",
            "player_1_id": self.player_1_id,
            "player_1_username": self.player_1_username,
            "player_1_choice": self.player_1_choice,
            "player_2_id": self.player_2_id,
            "player_2_username": self.player_2_username,
            "player_2_choice": self.player_2_choice,
            "message_id": self.message_id,
            "channel_id": self.channel_id,
        }

    @staticmethod
    def from_dict(data:dict):
        return RpsGameSession(
            id = "game_session",
            player_1_id=data.get("player_1_id", None),
            player_1_username=data.get("player_1_username", None),
            player_1_choice=data.get("player_1_choice", None),
            player_2_id=data.get("player_2_id", None),
            player_2_username=data.get("player_2_username", None),
            player_2_choice=data.get("player_2_choice", None),
            message_id=data.get("message_id", None),
            channel_id=data.get("channel_id", None),
        )