import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import EmojiCreation2
from datetime import datetime, timedelta
from Handling.Economy.Authority.AuthorityRiotPreventView import AuthorityRiotPreventView

class AuthorityRiotView(discord.ui.View):
    def __init__(self, user: discord.Member, user_authority: Profile):
        super().__init__(timeout=80)
        self.message: discord.Message = None
        self.embed: discord.Embed = None
        self.target_user = user
        self.user_authority: Profile = user_authority
        self.vote_concluded = False
        self.yes_votes = set() 
        self.no_votes = set()
        
    @discord.ui.button(label="💀 Tham Gia Bạo Động", style=discord.ButtonStyle.success)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id == self.target_user.id:
            #Nếu tự bầu thì phải tự counter bản thân
            self.no_votes.add(1257713292445618239)
        user = interaction.user
        # Nếu user đã bầu Không thì xoá khỏi list No votes
        if user.id in self.no_votes:
            self.no_votes.remove(user.id)
        self.yes_votes.add(user.id)

        await interaction.response.send_message(f"Bạn đã tham gia đội ngũ bạo động chống lại Chính Quyền <@{self.user_authority.user_id}> server!", ephemeral=True)
        # Kiểm tra xem đủ 10 vote chưa
        if len(self.yes_votes) >= 10:
            self.vote_concluded = True
            await self.conclude_vote(interaction)

    @discord.ui.button(label="🤐 Phản Đối Bạo Động", style=discord.ButtonStyle.danger)
    async def no_button(self, interaction: discord.Interaction, button: Button):
        user = interaction.user
        # Nếu user đã bầu Có thì xoá khỏi list Yes votes
        if user.id in self.yes_votes:
            self.yes_votes.remove(user.id)
        self.no_votes.add(user.id)
                
        if(interaction.user.id == self.user_authority.user_id):
            #Tạo một View AuthorityRiotPrevent
            new_embed = discord.Embed(title=f"Chính Quyền Vào Cuộc",description=f"Chính Quyền <@{self.user_authority.user_id}> có chấp nhận tốn **500**{EmojiCreation2.SILVER.value} để phòng chống bạo động không?",color=discord.Color.green())
            new_view = AuthorityRiotPreventView(user=interaction.user, rioting_user=self.target_user)
            new_view.old_riot_message = self.message
            new_view.yes_votes = self.yes_votes
            new_view.no_votes = self.no_votes
            mes = await interaction.response.send_message(embed=new_embed, view=new_view, ephemeral=False)
            new_view.message = mes
        else:
            await interaction.response.send_message(f"Bạn đã phản đối bạo động!", ephemeral=True)

        # Kiểm tra xem đủ 10 vote chưa
        if len(self.no_votes) >= 10:
            self.vote_concluded = True
            await self.conclude_vote(interaction)

    async def conclude_vote(self, interaction: discord.Interaction=None):
        if self.message != None:
            await self.message.edit(embed=self.embed, view= None)
        riot_win = False
        if len(self.yes_votes) > len(self.no_votes):
            result_message = f"Anh hùng **{self.target_user.display_name}** đã bạo động thành công khiến Chính Quyền mất **1000**{EmojiCreation2.SILVER.value} và nhận được **500**{EmojiCreation2.SILVER.value}! Đã có **{len(self.yes_votes)}** người đứng ra ủng hộ bạo động chính quyền!"
            riot_win = True
        else:
            result_message = f"Thành phần phản động **{self.target_user.display_name}** đã tổ chức khủng bố Chính Quyền nhưng đã bị dập tắt bạo động ngay lập tức! Thủ phạm **{self.target_user.display_name}** bị phạt **100K**{EmojiCreation2.COPPER.value} và cùng **{len(self.yes_votes)}** thành phần phản động khác bị tống giam trong 3 tiếng!"
            riot_win = False
        embed = discord.Embed(title=f"Kết Quả Bạo Động",description=f"{result_message}",color=discord.Color.blue())
        if riot_win == False:
            embed.set_thumbnail(url="https://miro.medium.com/v2/resize:fit:640/format:webp/1*svtb7AdUWnBGfuZfCJc8Og.gif")
            #Trừ tiền của phản động
            ProfileMongoManager.update_profile_money(guild_id=self.target_user.guild.id, guild_name=self.target_user.guild.name, user_id=self.target_user.id, user_display_name= self.target_user.display_name, user_name=self.target_user.name, copper=-100000)
            #Cộng nhân phẩm cho chính quyền
            ProfileMongoManager.update_dignity_point(guild_id=self.target_user.guild.id, guild_name=self.target_user.guild.name, user_id=self.user_authority.user_id, user_name= self.user_authority.user_name, user_display_name=self.user_authority.user_display_name, dignity_point=15)
            ProfileMongoManager.update_level_progressing(guild_id=self.target_user.guild.id, user_id=self.user_authority.user_id, bonus_exp=10)
        else:
            #Cộng tiền cho phản động
            ProfileMongoManager.update_profile_money(guild_id=self.target_user.guild.id, guild_name=self.target_user.guild.name, user_id=self.target_user.id, user_display_name= self.target_user.display_name, user_name=self.target_user.name, silver=500)
            #Trừ tiền của chính quyền
            ProfileMongoManager.update_profile_money(guild_id=self.target_user.guild.id, guild_name=self.target_user.guild.name, user_id=self.user_authority.user_id, user_display_name= self.user_authority.user_display_name, user_name=self.user_authority.user_name, silver=-1000)
            embed.set_thumbnail(url="https://img.freepik.com/premium-photo/violent-riot-street-fight-criminal-gangs-extremists-faces-shadows-black-clothes-hoods-fire-flames-background-looting_884546-10051.jpg")
        embed.add_field(name=f"", value="▬▬▬▬▬ι═════════>", inline=False)
        list_mention_yes = []
        for id in self.yes_votes:
            text = f"<@{id}>"
            list_mention_yes.append(text)
            #Nếu thua thì cập nhật jail_time của từng người trong list yes vote
            if riot_win == False:
                time_window = timedelta(hours=3)
                jail_time = datetime.now() + time_window
                ProfileMongoManager.update_jail_time(guild_id=self.target_user.guild.id, user_id= id, jail_time=jail_time)
            
        result_y = ", ".join(list_mention_yes)
        list_mention_no = []
        for id in self.no_votes:
            text = f"<@{id}>"
            list_mention_no.append(text)
        result_n = ", ".join(list_mention_no)
        embed.add_field(name=f"Danh sách thành phần bạo động", value=f"{result_y}", inline=False)
        embed.add_field(name=f"Danh sách ủng hộ chính quyền", value=f"{result_n}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬▬ι═════════>", inline=False)
        if interaction:
            await interaction.followup.send(embed=embed, ephemeral=False)
        else:
            if self.message != None:
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
