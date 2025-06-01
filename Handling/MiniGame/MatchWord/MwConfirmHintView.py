import discord
from Handling.MiniGame.MatchWord import MwClass, MwMongoManager
class MwConfirmHintView(discord.ui.View):
    def __init__(self, user: discord.Member, info: MwClass.MatchWordInfo, lan: str, english_words_dictionary, vietnamese_dict):
        super().__init__(timeout=30)
        self.user = user
        self.info = info
        self.message: discord.Message = None
        self.is_confirmed = False
        self.english_words_dictionary = english_words_dictionary
        self.vietnamese_dict = vietnamese_dict
        self.lan = lan
        
    async def on_timeout(self):
        if self.is_confirmed: return
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
        
    @discord.ui.button(label="Xác Nhận", style=discord.ButtonStyle.blurple)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        #Tìm từ hợp lệ, bắt đầu bằng chữ cái trong self.info
        suitable_word = None
        message = f"{interaction.user.mention} Bạn đã chấp nhận đổi 3 điểm!"
        if self.lan == 'eng' or self.lan == 'en':
            for word in self.english_words_dictionary.keys():
                if len(word) > 1 and word.startswith(self.info.correct_start_word) and word not in self.info.used_words:
                    suitable_word = word
                    break
        elif self.lan == 'vn':
            for word in self.vietnamese_dict.keys():
                if len(word) > 1 and word.startswith(self.info.correct_start_word) and word not in self.info.used_words:
                    suitable_word = word
                    break
        if suitable_word == None:
            message += f"\nRất tiếc là không có từ hợp lệ... lạ ta. Liên hệ <@315835396305059840> gấp"
        await interaction.followup.send(content=f"{message}", ephemeral=True)
        try:
            await self.message.edit(content=f"{interaction.user.mention} đã chấp nhận đánh đổi 3 điểm.\nGợi ý từ hợp lệ: **`{suitable_word}**`", view=None, embed= None)
        except Exception as e:
            print(f"Exception at hint MW: {e}")
        MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name= interaction.user.display_name, point=-3)
        self.is_confirmed = True