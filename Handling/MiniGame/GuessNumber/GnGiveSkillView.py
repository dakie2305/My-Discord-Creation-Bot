import discord

from Handling.MiniGame.GuessNumber import GnMongoManager
from Handling.MiniGame.MatchWord.MwClass import SpecialItem

class GnGiveSkillView(discord.ui.View):
    def __init__(self, user: discord.Member, target: discord.Member, channel_id: str, list_embed: list[discord.Embed], all_skills: list[SpecialItem]):
        super().__init__(timeout=30)
        self.user = user
        self.target = target
        self.channel_id = channel_id
        self.list_embed = list_embed
        self.all_skills = all_skills
        self.current_page = 0
        self.page_size = 5
        self.total_pages = len(self.list_embed)
        self.message: discord.Message = None
        
    async def on_timeout(self):
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
    
    def create_embed(self):
        embed = self.list_embed[self.current_page]
        embed.set_footer(text=f"Trang {self.current_page + 1}/{self.total_pages}")
        return embed

    @discord.ui.button(label="Trước", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % self.total_pages
        await interaction.response.edit_message(embed=self.create_embed(), view=self)
    
    @discord.ui.button(label="Chọn Kỹ Năng", style=discord.ButtonStyle.red)
    async def chooose(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        #Lấy ra list kỹ năng trong trang
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(self.all_skills))
        list_current_skills = self.all_skills[start_index:end_index]
        modal = GiveSkillInputModal(
            user=self.user,
            target=self.target,
            channel_id=self.channel_id,
            list_skills=list_current_skills  # 5 kỹ năng trong trang hiện tại
        )
        await interaction.response.send_modal(modal)


    @discord.ui.button(label="Sau", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % self.total_pages
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

class GiveSkillInputModal(discord.ui.Modal):
    def __init__(self, user: discord.Member, target: discord.Member, channel_id: str, list_skills: list[SpecialItem]):
        super().__init__(title="Chọn kỹ năng")
        self.input_index_page_field = discord.ui.TextInput(
            label="Nhập số thứ tự kỹ năng bạn muốn cho",
            placeholder="VD: 1, 2, 3, 4,...",
            required=True,
            default = "1",
            max_length=1
        )
        self.add_item(self.input_index_page_field)
        self.user = user
        self.target = target
        self.channel_id = channel_id
        self.list_skills = list_skills
        self.submitted = False

    async def on_submit(self, interaction: discord.Interaction):
        if self.submitted:
            await interaction.response.send_message("Đang xử lý, vui lòng đợi...", ephemeral=True)
            return
        self.submitted = True
        await interaction.response.defer(ephemeral=False)
        input_value = self.input_index_page_field.value
        try:
            index = int(input_value) - 1
            #Đảm bảo giá trị hợp lệ
            if index < 0:
                index = 0
            elif index >= len(self.list_skills):
                index = len(self.list_skills) - 1
            #Bóc ra kỹ năng, và đưa cho target
            chosen_skill = self.list_skills[index]
            if chosen_skill is None:
                await interaction.followup.send(f"Không tìm thấy kỹ năng đã chọn!", ephemeral=False)
                self.submitted = False
                return
            GnMongoManager.update_player_special_item(channel_id=self.channel_id, guild_id=interaction.guild_id, user_id=self.target.id, user_display_name=self.target.display_name, user_name=self.target.name, point=0, special_item=chosen_skill)
            await interaction.followup.send(f"{interaction.user.mention} đã cho {self.target.mention} kỹ năng **{chosen_skill.item_name}** thuộc rank **{chosen_skill.level}**!", ephemeral=False)
        except Exception:
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
            return
        self.submitted = False
        return