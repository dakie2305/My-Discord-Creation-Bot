import discord
class SelfDestructView(discord.ui.View):
    def __init__(self, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.message: discord.Message = None
        
    async def on_timeout(self):
        #Xoá message
        await self.message.delete()