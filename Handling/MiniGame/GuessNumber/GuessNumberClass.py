from datetime import date, datetime
from typing import List, Optional
from Handling.MiniGame.MatchWord.MwClass import PlayerBan, PlayerEffect, PlayerPenalty, PlayerProfile, SpecialItem

#region GuessNumberInfo
#Tận dụng lại Match Word
class GuessNumberInfo:
    def __init__(self, channel_id: int, channel_name: str, guild_name: str, current_player_id: int = None, current_player_name: str = None, range_from: int = None, range_to: int = None, correct_number: int = None, special_point: int = None, current_round: int = 0, player_profiles: Optional[List['PlayerProfile']] = None, player_effects : Optional[List['PlayerEffect']] = None, player_penalty : Optional[List['PlayerPenalty']] = None, player_ban : Optional[List['PlayerBan']] = None, special_item: Optional['SpecialItem'] = None, last_played = datetime.now()):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.guild_name = guild_name
        self.current_player_id = current_player_id
        self.current_player_name = current_player_name
        self.correct_number = correct_number
        self.range_from = range_from
        self.range_to = range_to
        self.special_point = special_point
        self.current_round = current_round
        self.last_played = last_played
        self.special_item = special_item if special_item else None
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
            "range_from": self.range_from,
            "range_to": self.range_to,
            "correct_number": self.correct_number,
            "special_point": self.special_point,
            "current_round": self.current_round,
            "last_played": self.last_played.isoformat() if self.last_played else None,
            "special_item": self.special_item.to_dict() if self.special_item else None,
            "player_profiles": [p.to_dict() for p in self.player_profiles],
            "player_effects": [e.to_dict() for e in self.player_effects],
            "player_penalty": [p.to_dict() for p in self.player_penalty],
            "player_ban": [b.to_dict() for b in self.player_ban],
        }

    @staticmethod
    def from_dict(data: dict):
        return GuessNumberInfo(
            channel_id=data.get("channel_id"),
            channel_name=data.get("channel_name"),
            guild_name=data.get("guild_name"),
            current_player_id=data.get("current_player_id"),
            current_player_name=data.get("current_player_name"),
            range_from=data.get("range_from"),
            range_to=data.get("range_to"),
            correct_number=data.get("correct_number"),
            special_point=data.get("special_point"),
            current_round=data.get("current_round", 0),
            last_played=datetime.fromisoformat(data["last_played"]) if data.get("last_played") else datetime.now(),
            special_item=SpecialItem.from_dict(data["special_item"]) if data.get("special_item") else None,
            player_profiles=[PlayerProfile.from_dict(p) for p in data.get("player_profiles", [])],
            player_effects=[PlayerEffect.from_dict(e) for e in data.get("player_effects", [])],
            player_penalty=[PlayerPenalty.from_dict(p) for p in data.get("player_penalty", [])],
            player_ban=[PlayerBan.from_dict(b) for b in data.get("player_ban", [])],
        )