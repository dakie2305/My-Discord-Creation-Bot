from datetime import datetime

class Donator:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, date_donate: datetime= None, total_time_donate: int = 0, total_amount_donate: int = 0, is_given_role = True):
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.date_donate = date_donate
        self.total_time_donate = total_time_donate
        self.total_amount_donate = total_amount_donate
        self.is_given_role = is_given_role

    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "date_donate": self.date_donate,
            "total_time_donate": self.total_time_donate,
            "total_amount_donate": self.total_amount_donate,
            "is_given_role": self.is_given_role,
        }

    @staticmethod
    def from_dict(data:dict):
        return Donator(
                user_id=data.get("user_id", None),
                user_name=data.get("user_name", None),
                user_display_name=data.get("user_display_name", None),
                date_donate=data.get("date_donate", None),
                total_time_donate=data.get("total_time_donate", None),
                total_amount_donate=data.get("total_amount_donate", None),
                is_given_role=data.get("is_given_role", True),
            )