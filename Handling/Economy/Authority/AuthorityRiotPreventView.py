import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import CurrencyEmoji
from datetime import datetime, timedelta
from Handling.Misc.SelfDestructView import SelfDestructView

class AuthorityRiotPreventView(discord.ui.View):
    def __init__(self, user: discord.Member, rioting_user: discord.Member):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.user = user
        self.rioting_user = rioting_user
        self.old_riot_message: discord.Message = None
        self.yes_votes = set() 
        self.no_votes = set()
        
    @discord.ui.button(label="🚨 Giải Quyết Bạo Động 🚨", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user.id:
            return
        await interaction.response.defer(ephemeral=False)
        #Lấy profile của chính quyền (user)
        authority_profile = ProfileMongoManager.is_authority(guild_id=interaction.guild_id, user_id=self.user.id)
        if authority_profile.silver < 1000:
            embed = discord.Embed(title=f"", description=f"Để bắt giữ tất cả thành phần bạo động thì Chính Quyền cần **1000**{CurrencyEmoji.SILVER.value}!", color=0xc379e0)
            view = SelfDestructView(20)
            mes = await interaction.followup.send(embed=embed, view=view)
            view.message = mes
            return
        #Xoá message cũ
        if self.old_riot_message != None:
            self.old_riot_message.delete()
        #Trừ tiền chính quyền
        authority_profile.silver -= 1000
        ProfileMongoManager.update_profile_money_fast(guild_id=interaction.guild_id, data= authority_profile)
        result_message = f"Thành phần phản động **{self.rioting_user.display_name}** đã tổ chức khủng bố Chính Quyền nhưng đã bị dập tắt bạo động ngay lập tức! Thủ phạm **{self.rioting_user.display_name}** bị phạt **100K**{CurrencyEmoji.COPPER.value} và cùng **{len(self.yes_votes)}** thành phần phản động khác bị tống giam trong 3 tiếng!"
        
        #Trừ tiền của phản động
        ProfileMongoManager.update_profile_money(guild_id=self.rioting_user.guild.id, guild_name=self.rioting_user.guild.name, user_id=self.rioting_user.id, user_display_name= self.rioting_user.display_name, user_name=self.rioting_user.name, copper=-100000)
        
        embed = discord.Embed(title=f"Kết Quả Bạo Động",description=f"{result_message}",color=discord.Color.blue())
        embed.set_thumbnail(url="https://miro.medium.com/v2/resize:fit:640/format:webp/1*svtb7AdUWnBGfuZfCJc8Og.gif")
        embed.add_field(name=f"", value="▬▬▬▬▬ι═════════>", inline=False)
        list_mention_yes = []
        for id in self.yes_votes:
            text = f"<@{id}>"
            list_mention_yes.append(text)
            time_window = timedelta(hours=3)
            jail_time = datetime.now() + time_window
            ProfileMongoManager.update_jail_time(guild_id=self.rioting_user.guild.id, user_id= id, jail_time=jail_time)
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
            
    
    async def on_timeout(self):
        #Delete
        if self.message != None:
            await self.message.delete()

        
        