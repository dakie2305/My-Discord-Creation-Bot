import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile

class AuthorityView(discord.ui.View):
    def __init__(self, user: discord.Member, data: Profile):
        super().__init__(timeout=5)
        self.message: discord.Message = None
        self.embed: discord.Embed = None
        self.target_user = user
        self.data: Profile = data
        self.vote_concluded = False
        self.yes_votes = set() 
        self.no_votes = set() 

    @discord.ui.button(label="👍 Có", style=discord.ButtonStyle.success)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.target_user.id:
            #Nếu tự bầu thì phải tự counter bản thân
            self.no_votes.add(1257713292445618239)
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
        
        embed = discord.Embed(title=f"Chính Quyền Đương Cử",description=f"{result_message}",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬▬ι═══════════>", inline=False)
        embed.add_field(name=f"", value="\n", inline=False)
        list_mention_yes = []
        for id in self.yes_votes:
            text = f"<@{id}>"
            list_mention_yes.append(text)
        result_y = ", ".join(list_mention_yes)
        list_mention_no = []
        for id in self.no_votes:
            text = f"<@{id}>"
            list_mention_no.append(text)
        result_n = ", ".join(list_mention_no)
        embed.add_field(name=f"Danh sách người bầu chọn", value=f"{result_y}", inline=False)
        embed.add_field(name=f"Danh sách người phản đối", value=f"{result_n}", inline=False)
        
        if interaction:
            await interaction.followup.send(embed=embed, ephemeral=False)
        else:
            await self.message.channel.send(embed=embed)
        
    def get_nhan_pham(self, number):
        text = "Người Thường"
        if number >= 100:
            text = "Thánh Nhân"
        elif number >= 75:
            text = "Người Tốt"
        elif number >= 60:
            text = "Lành tính"
        elif number >= 50:
            text = "Người Thường"
        elif number >= 40:
            text = "Tiểu Nhân"
        elif number >= 30:
            text = "Quỷ Quyệt"
        elif number >= 20:
            text = "Tội Phạm"
        else:
            text = "Gian Thương Tà Đạo"
        return text
    
    async def on_timeout(self):
        # Nếu vẫn chưa đủ 10 votes thì kết luận luôn
        if not self.vote_concluded:
            await self.conclude_vote()
