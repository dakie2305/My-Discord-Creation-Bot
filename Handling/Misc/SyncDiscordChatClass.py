from datetime import datetime
from typing import Optional, List

class DiscordMessage:
    def __init__(
        self,
        message_id: int,
        channel_id: int,
        guild_id: int,

        author_id: int,
        author_username: str,
        author_display_name: str,

        content: str,
        created_at: datetime,

        edited_at: Optional[datetime] = None,
        attachments: Optional[List[str]] = None,
        embeds: Optional[List[dict]] = None,
        author_image: Optional[str] = None,

        is_bot: bool = False,
        source: str = "discord"
    ):
        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id

        self.author_id = author_id
        self.author_username = author_username
        self.author_display_name = author_display_name
        self.author_image = author_image

        self.content = content
        self.created_at = created_at
        self.edited_at = edited_at

        self.attachments = attachments or []
        self.embeds = embeds or []

        self.is_bot = is_bot
        self.source = source

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "channel_id": self.channel_id,
            "guild_id": self.guild_id,

            "author_id": self.author_id,
            "author_username": self.author_username,
            "author_display_name": self.author_display_name,

            "content": self.content,
            "author_image": self.author_image,
            "created_at": self.created_at.isoformat(),
            "edited_at": self.edited_at.isoformat() if self.edited_at else None,

            "attachments": self.attachments,
            "embeds": self.embeds,

            "is_bot": self.is_bot,
            "source": self.source,
        }

    @staticmethod
    def from_dict(data: dict):
        return DiscordMessage(
            message_id=data["message_id"],
            channel_id=data["channel_id"],
            guild_id=data["guild_id"],

            author_id=data["author_id"],
            author_username=data["author_username"],
            author_display_name=data["author_display_name"],
            author_image=data["author_image"],

            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            edited_at=datetime.fromisoformat(data["edited_at"]) if data.get("edited_at") else None,

            attachments=data.get("attachments", []),
            embeds=data.get("embeds", []),

            is_bot=data.get("is_bot", False),
            source=data.get("source", "discord"),
        )