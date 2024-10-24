import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import EmojiCreation2
from datetime import datetime, timedelta
from Handling.Misc.SelfDestructView import SelfDestructView
from db.Class.CustomClass import UserInfo
import db.DbMongoManager as db 

class AuthorityInterceptView(discord.ui.View):
    def __init__(self, user: discord.Member, user_profile: Profile, crime_type: str, target_profile: Profile = None,target_user: discord.Member = None, authority_user: Profile = None):
        super().__init__(timeout=30)
        self.old_message: discord.Message = None
        self.crime_type = crime_type
        self.user = user
        self.target_user = target_user
        self.user_profile = user_profile
        self.target_profile = target_profile
        self.target_profile = target_profile
        self.authority_user = authority_user
        
    @discord.ui.button(label="🚨 Chính Quyền Vào Cuộc 🚨", style=discord.ButtonStyle.red)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        if self.authority_user == None:
            await interaction.followup.send(f"Server này không có chính quyền để giải quyết!", ephemeral=True)
            return
        elif interaction.user.id != self.authority_user.id:
            await interaction.followup.send(f"Chỉ Chính Quyền <@{self.authority_user.user_id}> mới có thể giải quyết, vui lòng gọi Chính Quyền!", ephemeral=True)
            return
        return