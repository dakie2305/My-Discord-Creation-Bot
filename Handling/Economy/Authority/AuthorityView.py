import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager

class AuthorityView(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__(timeout=60)
        self.message: discord.Message = None
        self.embed: discord.Embed = None
        self.target_user = user
        self.vote_concluded = False
        self.yes_votes = set() 
        self.no_votes = set() 

    @discord.ui.button(label="👍 Có", style=discord.ButtonStyle.success)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.target_user.id:
            #Nếu tự bầu thì phải tự counter bản thân
            self.no_votes.add(1)
        user = interaction.user
        # Nếu user đã bầu Không thì xoá khỏi list No votes
        if user.id in self.no_votes:
            self.no_votes.remove(user.id)
        self.yes_votes.add(user.id)

        await interaction.response.send_message(f"Bạn đã đồng ý bầu cho {self.target_user.mention}!", ephemeral=True)
        # Kiểm tra xem đủ 10 vote chưa
        if len(self.yes_votes) >= 10:
            self.vote_concluded = True
            await self.conclude_vote(interaction)

    @discord.ui.button(label="🖕 Không", style=discord.ButtonStyle.danger)
    async def no_button(self, interaction: discord.Interaction, button: Button):
        user = interaction.user
        # Nếu user đã bầu Có thì xoá khỏi list Yes votes
        if user.id in self.yes_votes:
            self.yes_votes.remove(user.id)
        self.no_votes.add(user.id)

        await interaction.response.send_message(f"Bạn đã không đồng ý bầu cho {self.target_user.mention}!", ephemeral=True)
        # Kiểm tra xem đủ 10 vote chưa
        if len(self.no_votes) >= 10:
            self.vote_concluded = True
            await self.conclude_vote(interaction)

    async def conclude_vote(self, interaction: discord.Interaction=None):
        await self.message.edit(embed=self.embed, view= None)
        if len(self.yes_votes) > len(self.no_votes):
            result_message = f"**{self.target_user.display_name}** đã thắng bầu cử và trở thành Chính Quyền! Có **{len(self.yes_votes)}** người đã bầu ủng hộ! Đã cộng thêm tiền và của cải cho tân Chính Quyền đương nhiệm!"
            ProfileMongoManager.set_authority(guild_id=self.target_user.guild.id, guild_name=self.target_user.guild.name, user_id=self.target_user.id,user_name=self.target_user.name,user_display_name= self.target_user.display_name)
            ProfileMongoManager.update_profile_money(guild_id=self.target_user.guild.id, guild_name=self.target_user.guild.name, user_id=self.target_user.id,user_name=self.target_user.name,user_display_name= self.target_user.display_name,darkium=1,copper=5000, gold=10,silver=3)
        else:
            result_message = f"**{self.target_user.display_name}** đã thua bầu cử! Đáng tiếc là chỉ có {len(self.yes_votes)} người bầu ủng hộ bạn! Đừng quên bạn cũng vừa bị trừ **500** <a:copper:1294615524918956052>!"
            ProfileMongoManager.update_profile_money(guild_id=self.target_user.guild.id, guild_name=self.target_user.guild.name, user_id=self.target_user.id,user_name=self.target_user.name,user_display_name= self.target_user.display_name,copper=-500)
        if interaction:
            await interaction.followup.send(result_message, ephemeral=False)
        else:
            await self.message.channel.send(result_message)
        

    async def on_timeout(self):
        # Nếu vẫn chưa đủ 10 votes thì kết luận luôn
        if not self.vote_concluded:
            await self.conclude_vote()
