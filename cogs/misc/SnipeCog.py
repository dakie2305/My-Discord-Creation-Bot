import CustomButton
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
from db import DbMongoManager

async def setup(bot: commands.Bot):
    await bot.add_cog(Snipe(bot=bot))
    print("Snipe command is ready!")

class Snipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @discord.app_commands.command(name="snipe", description="Hiện lại message vừa mới bị xoá trong channel này!")
    async def snipe_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        called_channel = interaction.channel
        
        snipe_channel_info = DbMongoManager.find_snipe_channel_info_by_id(called_channel.id, interaction.guild.id)
        if snipe_channel_info:
            list_snipe_message = snipe_channel_info.snipe_messages
            if list_snipe_message == None:
                await interaction.followup.send(f"Chưa thấy bất kỳ message nào bị xoá trong channel {interaction.channel.mention}. Vui lòng thử lại sau.")
                return
            list_snipe_message.reverse()
            temp_files = []
            first_message = list_snipe_message[0]
            if first_message != None and first_message.user_attachments!= None and len(first_message.user_attachments)>0:
                for att in first_message.user_attachments:
                    file = await CustomFunctions.get_attachment_file_from_url(url= att.url, content_type= att.content_type)
                    if file != None: temp_files.append(file)
                    
            view = CustomButton.PaginationView(bot=self.bot, interaction=interaction, items= list_snipe_message)
            message = await interaction.followup.send(embed=view.embed, view=view, files=temp_files)
            view.discord_message = message
            await view.countdown()
        else:
            await interaction.followup.send(f"Chưa có dữ liệu snipe cho channel {interaction.channel.mention}. Vui lòng thử lại sau.")