import discord
from discord.ext import commands
import PIL
import db.DbMongoManager as db
from db.Class.CustomClass import GuildExtraInfo

async def setup(bot: commands.Bot):
    await bot.add_cog(TherapyAI(bot=bot))
    print("Therapy AI is ready!")

class TherapyAI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #region keo_bua_bao command
    @discord.app_commands.command(name="therapy", description="Chọn channel hiện tại làm channel bot AI tâm lý học.")
    async def therapy(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user.id != 315835396305059840 and interaction.user.id != interaction.guild.owner_id:
            await interaction.followup.send(f"Chỉ chủ Server mới dùng lệnh này.", ephemeral= False)
            return
        check_exist = db.find_guild_extra_info_by_id(interaction.guild.id)
        if check_exist:
            if check_exist.therapy_channel != None and check_exist.therapy_channel == interaction.channel_id:
                #Xóa đi
                data_updated = {"therapy_channel": None}
                db.update_guild_extra_info(guild_id=interaction.guild.id, update_data= data_updated)
                await interaction.followup.send(f"Đã xóa channel bot AI tâm lý.", ephemeral= True)
            else:
                #Cập nhật
                data_updated = {"therapy_channel": interaction.channel_id}
                db.update_guild_extra_info(guild_id=interaction.guild.id, update_data= data_updated)
                await interaction.followup.send(f"Đã thiết lập channel này để làm channel bot AI tâm lý.", ephemeral= True)
        else:
            data = GuildExtraInfo(guild_id=interaction.guild.id, guild_name= interaction.guild.name, allowed_ai_bot=True, therapy_channel=interaction.channel_id )
            db.insert_guild_extra_info(data)
            await interaction.followup.send(f"Đã thiết lập channel này để làm channel bot AI tâm lý.", ephemeral= True)