from typing import List, Optional
from datetime import datetime, timedelta
from Handling.Economy.Quest.DungeonQuestChannelClass import DungeonQuestChannel
#region User Info Database
class UserInfo:
    def __init__(self, user_id, user_name, user_display_name, jailer_id=None, jailer_user_name=None, jailer_display_name=None, channel_id=None, channel_name=None, roles=None, reason=None, jail_until: datetime =None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.jailer_id = jailer_id
        self.jailer_user_name = jailer_user_name
        self.jailer_display_name = jailer_display_name
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.roles = roles or []
        self.reason = reason
        self.jail_until: datetime = jail_until

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_display_name": self.user_display_name,
            "jailer_id": self.jailer_id,
            "jailer_user_name": self.jailer_user_name,
            "jailer_display_name": self.jailer_display_name,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "roles": self.roles,
            "reason": self.reason,
            "jail_until": self.jail_until
        }

    @staticmethod
    def from_dict(data: dict):
        return UserInfo(
            user_id=data.get("user_id"),
            user_name=data.get("user_name"),
            user_display_name=data.get("user_display_name"),
            jailer_id=data.get("jailer_id"),
            jailer_user_name=data.get("jailer_user_name"),
            jailer_display_name=data.get("jailer_display_name"),
            channel_id=data.get("channel_id"),
            channel_name=data.get("channel_name"),
            roles=data.get("roles", []),
            reason=data.get("reason"),
            jail_until=data.get("jail_until", None)
        )
#region Guild Info

class GuildExtraInfo:
    def __init__(self, guild_id: int, guild_name :str, allowed_ai_bot: bool, list_channels_ai_talk: List[int] = None, enabled_ai_until: datetime = None, therapy_channel: int = None, list_channels_quests: List[int] = None, custom_parameter_1 = None, custom_parameter_2 = None, disable_donation_text_until: datetime = None, list_channels_dungeon : Optional[List['DungeonQuestChannel']] = None, list_li_xi: List[int] = None):
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.allowed_ai_bot = allowed_ai_bot
        self.therapy_channel = therapy_channel
        self.list_channels_ai_talk: List[int] = list_channels_ai_talk if list_channels_ai_talk else []
        self.list_channels_quests: List[int] = list_channels_quests if list_channels_quests else []
        self.enabled_ai_until = enabled_ai_until
        self.custom_parameter_1 = custom_parameter_1
        self.custom_parameter_2 = custom_parameter_2
        self.disable_donation_text_until = disable_donation_text_until if disable_donation_text_until else datetime.now()

        self.list_channels_dungeon: List[DungeonQuestChannel] = list_channels_dungeon if list_channels_dungeon else []
        self.list_li_xi: List[int] = list_li_xi if list_li_xi else []

    def to_dict(self):
        return {
            "guild_id": self.guild_id,
            "guild_name": self.guild_name,
            "allowed_ai_bot": self.allowed_ai_bot,
            "therapy_channel": self.therapy_channel,
            "custom_parameter_1": self.custom_parameter_1,
            "custom_parameter_2": self.custom_parameter_2,
            "list_channels_quests": [data for data in self.list_channels_quests],
            "list_channels_ai_talk": [data for data in self.list_channels_ai_talk],
            "list_li_xi": [data for data in self.list_li_xi],
            "enabled_ai_until": self.enabled_ai_until.isoformat() if self.enabled_ai_until else None,
            "disable_donation_text_until": self.disable_donation_text_until if self.disable_donation_text_until else None,

            "list_channels_dungeon": [data.to_dict() for data in self.list_channels_dungeon],
        }

    @staticmethod
    def from_dict(data:dict):
        return GuildExtraInfo(
            guild_id=data["guild_id"],
            guild_name=data["guild_name"],
            allowed_ai_bot=data["allowed_ai_bot"],
            therapy_channel=data.get("therapy_channel", None),
            custom_parameter_1=data.get("custom_parameter_1", None),
            custom_parameter_2=data.get("custom_parameter_2", None),
            disable_donation_text_until=data.get("disable_donation_text_until", None),
            list_channels_quests = [item for item in data.get("list_channels_quests", [])],
            list_channels_ai_talk = [item for item in data.get("list_channels_ai_talk", [])],
            list_li_xi = [item for item in data.get("list_li_xi", [])],
            enabled_ai_until=datetime.fromisoformat(data["enabled_ai_until"]) if data["enabled_ai_until"] else None,

            list_channels_dungeon = [DungeonQuestChannel.from_dict(item) for item in data.get("list_channels_dungeon", [])],
        )
        
#region User Conversation Info
class UserConversationInfo:
    def __init__(self, user_id: int, user_name: str, last_time_interaction: datetime = None, past_conversation: Optional[List['ConversationInfo']] = None):
        self.user_id = user_id
        self.user_name = user_name
        self.last_time_interaction = last_time_interaction
        self.past_conversation: List[ConversationInfo] = past_conversation if past_conversation else []

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "last_time_interaction": self.last_time_interaction,
            "past_conversation": [conv.to_dict() for conv in self.past_conversation],
        }

    @staticmethod
    def from_dict(data:dict):
        return UserConversationInfo(
            user_id=data["user_id"],
            user_name=data["user_name"],
            last_time_interaction= data["last_time_interaction"],
            past_conversation=[ConversationInfo.from_dict(conv) for conv in data.get("past_conversation", [])]
        )
        
class ConversationInfo:
    def __init__(self, user_message_id: int, user_message_content: str, bot_message_content: str):
        self.message_id = user_message_id
        self.message_content = user_message_content
        self.bot_message_content = bot_message_content

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "message_content": self.message_content,
            "bot_message_content": self.bot_message_content,
        }

    @staticmethod
    def from_dict(data):
        return ConversationInfo(
            user_message_id=data["message_id"],
            user_message_content=data["message_content"],
            bot_message_content=data["bot_message_content"],
        )
        
#region Snipe Info
class SnipeChannelInfo:
    def __init__(self, channel_id: int, channel_name: str, snipe_messages: Optional[List['SnipeMessage']] = None):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.snipe_messages: List[SnipeMessage] = snipe_messages if snipe_messages else []

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "snipe_messages": [conv.to_dict() for conv in self.snipe_messages],
        }

    @staticmethod
    def from_dict(data:dict):
        return SnipeChannelInfo(
            channel_id=data["channel_id"],
            channel_name=data["channel_name"],
            snipe_messages=[SnipeMessage.from_dict(conv) for conv in data.get("snipe_messages", [])]
        )
        
class SnipeMessage:
    def __init__(self, author_id: int, author_username: str, author_display_name: str, user_message_content: str, deleted_date: datetime, user_attachments: Optional[List['SnipeMessageAttachments']] = None):
        self.author_id = author_id
        self.author_username = author_username
        self.author_display_name = author_display_name
        self.user_message_content = user_message_content
        self.deleted_date = deleted_date
        self.user_attachments: List[SnipeMessageAttachments] = user_attachments if user_attachments else []
    def to_dict(self):
        return {
            "author_id": self.author_id,
            "author_username": self.author_username,
            "author_display_name": self.author_display_name,
            "deleted_date": self.deleted_date,
            "user_message_content": self.user_message_content,
            "user_attachments": [data.to_dict() for data in self.user_attachments],
        }
    @staticmethod
    def from_dict(data):
        return SnipeMessage(
            author_id=data["author_id"],
            author_username=data["author_username"],
            author_display_name=data["author_display_name"],
            deleted_date=data["deleted_date"],
            user_message_content=data["user_message_content"],
            user_attachments=[SnipeMessageAttachments.from_dict(conv) for conv in data.get("user_attachments", [])]
        )
        
class SnipeMessageAttachments:
    def __init__(self, filename: str, url: str, content_type, size):
        self.filename = filename
        self.url = url
        self.content_type = content_type
        self.size = size
    
    def to_dict(self):
        return {
            "filename": self.filename,
            "url": self.url,
            "content_type": self.content_type,
            "size": self.size,
        }

    @staticmethod
    def from_dict(data):
        return SnipeMessageAttachments(
            filename=data["filename"],
            url=data["url"],
            content_type=data["content_type"],
            size=data["size"],
        )
        
#region Pre Delete Attachments
class PreDeleteAttachmentsInfo:
    def __init__(self, channel_id: int, channel_name: str, user_attachments: Optional[List['SnipeMessageAttachments']] = None):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.user_attachments: List[SnipeMessageAttachments] = user_attachments if user_attachments else []

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "user_attachments": [data.to_dict() for data in self.user_attachments],
        }

    @staticmethod
    def from_dict(data:dict):
        return PreDeleteAttachmentsInfo(
            channel_id=data["channel_id"],
            channel_name=data["channel_name"],
            user_attachments=[SnipeMessageAttachments.from_dict(att) for att in data.get("user_attachments", [])]
        )

