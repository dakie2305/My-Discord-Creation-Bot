import discord
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from collections import defaultdict, deque
from datetime import datetime, timedelta

class AntiSpam:
    def __init__(self):
        # {guild_id: {user_id: deque[(timestamp, channel_id, content, attachments_hash)]}}
        self.user_messages = defaultdict(lambda: defaultdict(deque))
        self.spam_time_window = timedelta(minutes=1)
        self.spam_message_count = 4
        self.spam_channel_count = 4

    async def handling_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            return

        user_id = message.author.id
        now = datetime.now()
        user_deque = self.user_messages[message.guild.id][user_id]
        # Generate a simple hash for attachments (if any)
        attachments_hash = tuple(att.url for att in message.attachments) if message.attachments else None
        # Ignore empty content AND no attachments
        if not message.content.strip() and not attachments_hash:
            return

        # Append current message
        user_deque.append((now, message.channel.id, message.content.strip(), attachments_hash))

        # Remove old messages outside the time window
        while user_deque and now - user_deque[0][0] > self.spam_time_window:
            user_deque.popleft()

        # ---- Text spam check ----
        if message.content.strip():
            same_text_messages = [m for m in user_deque if m[2] == message.content.strip()]
            text_channels = {m[1] for m in same_text_messages}
            if len(same_text_messages) >= self.spam_message_count and len(text_channels) >= self.spam_channel_count:
                try:
                    await message.guild.ban(
                        message.author,
                        delete_message_days=7,
                        reason="Spam detected: same text content across multiple channels"
                    )
                    print(f"Banned {message.author} for text spam")
                    self.user_messages[message.guild.id].pop(user_id, None)
                    return
                except Exception as e:
                    print(f"Failed to ban {message.author}: {e}")

        # ---- Attachment spam check ----
        if attachments_hash:
            same_attachment_messages = [m for m in user_deque if m[3] == attachments_hash]
            attach_channels = {m[1] for m in same_attachment_messages}
            if len(same_attachment_messages) >= self.spam_message_count and len(attach_channels) >= self.spam_channel_count:
                try:
                    await message.guild.ban(
                        message.author,
                        delete_message_days=7,
                        reason="Spam detected: same attachments across multiple channels"
                    )
                    print(f"Banned {message.author} for attachment spam")
                    self.user_messages[message.guild.id].pop(user_id, None)
                    return
                except Exception as e:
                    print(f"Failed to ban {message.author}: {e}")
