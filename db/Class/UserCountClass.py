from datetime import datetime
class UserCount:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, last_interaction: datetime, truth_game_count: int = 0, dare_game_count: int = 0, therapy_count: int = 0):
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.truth_game_count = truth_game_count
        self.dare_game_count = dare_game_count
        self.therapy_count = therapy_count
        self.last_interaction = last_interaction if last_interaction else None
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "truth_game_count": self.truth_game_count,
            "dare_game_count": self.dare_game_count,
            "therapy_count": self.therapy_count,
            "last_interaction": self.last_interaction,
        }

    @staticmethod
    def from_dict(data:dict):
        return UserCount(
            user_id=data.get("user_id", None),
            user_name=data.get("user_name", None),
            user_display_name=data.get("user_display_name", None),
            last_interaction=data.get("last_interaction", None),
            dare_game_count=data.get("dare_game_count", 0),
            truth_game_count=data.get("truth_game_count", 0),
            therapy_count=data.get("therapy_count", 0),
        )