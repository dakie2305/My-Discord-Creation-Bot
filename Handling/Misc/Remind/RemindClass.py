import uuid
from datetime import datetime

class Remind:
    def __init__(self, user_id: int, user_name: str, user_display_name: str, guild_id: int, guild_name: str, channel_id: int, channel_name: str, message_content: str, date_remind: datetime= None, remind_id: str = None):
        self.remind_id = remind_id or str(uuid.uuid4())
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.message_content = message_content
        self.date_remind = date_remind if date_remind else datetime.now()

    def to_dict(self):
        return {
            "remind_id": self.remind_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "guild_id": self.guild_id,
            "guild_name": self.guild_name,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "message_content": self.message_content,
            "date_remind": self.date_remind if self.date_remind else None,
        }

    @staticmethod
    def from_dict(data: dict):
        return Remind(
            remind_id=data.get("remind_id"),
            user_id=data.get("user_id"),
            user_name=data.get("user_name"),
            user_display_name=data.get("user_display_name"),
            guild_id=data.get("guild_id"),
            guild_name=data.get("guild_name"),
            channel_id=data.get("channel_id"),
            channel_name=data.get("channel_name"),
            message_content=data.get("message_content"),
            date_remind=data["date_remind"] if data.get("date_remind") else None,
        )