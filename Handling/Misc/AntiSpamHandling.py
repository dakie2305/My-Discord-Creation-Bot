import discord
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from collections import defaultdict, deque
from datetime import datetime, timedelta

class AntiSpam:
    def __init__(self):
        # {guild_id: {user_id: deque[(timestamp, channel_id, content)]}}
        self.user_messages = defaultdict(lambda: defaultdict(deque))
        self.spam_time_window = timedelta(minutes=1)
        self.spam_message_count = 5
        self.spam_channel_count = 5

    async def handling_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.guild.id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value:
            return

        # check only non-empty
        if not message.content.strip(): return

        user_id = message.author.id
        now = datetime.now()
        user_deque = self.user_messages[message.guild.id][user_id]

        user_deque.append((now, message.channel.id, message.content))

        # Remove old messages outside time window
        while user_deque and now - user_deque[0][0] > self.spam_time_window:
            user_deque.popleft()

        # Only consider messages with the **same content** as the latest
        same_content_messages = [m for m in user_deque if m[2] == message.content]
        channels = {m[1] for m in same_content_messages}

        # Ban if user spammed the same content in enough channels
        if len(same_content_messages) >= self.spam_message_count and len(channels) >= self.spam_channel_count:
            try:
                await message.guild.ban(
                    message.author,
                    delete_message_days=7,
                    reason="Spam detected: same text content across multiple channels"
                )
                print(f"Banned {message.author} for spamming the same text content")
                # Clear messages for this user
                self.user_messages[message.guild.id].pop(user_id, None)
            except Exception as e:
                print(f"Failed to ban {message.author}: {e}")
