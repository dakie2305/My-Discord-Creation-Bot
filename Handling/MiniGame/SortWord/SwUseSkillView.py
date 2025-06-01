import discord

from Handling.MiniGame.SortWord import SwClass, SwMongoManager
class SwUseSkillView(discord.ui.View):
    def __init__(self, user: discord.Member, target: discord.Member, channel_id: int, lan: str, info: SwClass.SortWordInfo, all_skills: list[SwClass.SwSpecialItem], profile: SwClass.SwPlayerProfile, english_words_dictionary, vietnamese_dict):
        super().__init__(timeout=30)
        self.user = user
        self.target = target
        self.lan = lan
        self.channel_id = channel_id
        self.profile = profile
        self.all_skills = all_skills
        self.info = info
        self.message: discord.Message = None
        self.english_words_dictionary = english_words_dictionary
        self.vietnamese_dict = vietnamese_dict
        
    async def on_timeout(self):
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
    
    @discord.ui.button(label="Chọn Kỹ Năng", style=discord.ButtonStyle.blurple)
    async def choose(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user.id: return
        #Lấy ra list kỹ năng trong trang
        modal = UseSkillInputModal(
            user=self.user,
            target=self.target,
            channel_id=self.channel_id,
            lan=self.lan,
            list_skills=self.all_skills,
            english_words_dictionary=self.english_words_dictionary,
            vietnamese_dict=self.vietnamese_dict,
            info=self.info,
            profile=self.profile,
            message=self.message
        )
        await interaction.response.send_modal(modal)

#region use
class UseSkillInputModal(discord.ui.Modal):
    def __init__(self, user: discord.Member, target: discord.Member, channel_id: str, lan: str, list_skills: list[SwClass.SwSpecialItem], info: SwClass.SortWordInfo, profile: SwClass.SwPlayerProfile, english_words_dictionary, vietnamese_dict, message: discord.Message):
        super().__init__(title="Chọn kỹ năng")
        self.input_index_page_field = discord.ui.TextInput(
            label="Nhập số thứ tự kỹ năng bạn muốn dùng",
            placeholder="VD: 1, 2, 3, 4,...",
            required=True,
            default = "1",
            max_length=1
        )
        self.add_item(self.input_index_page_field)
        self.user = user
        self.target = target
        self.channel_id = channel_id
        self.lan = lan
        self.list_skills = list_skills
        self.info = info
        self.profile = profile
        self.english_words_dictionary: dict = english_words_dictionary
        self.vietnamese_dict: dict = vietnamese_dict
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        input_value = self.input_index_page_field.value
        try:
            index = int(input_value) - 1
            if not self.list_skills:
                await interaction.followup.send("Bạn không có kỹ năng nào để dùng!", ephemeral=True)
                return
            #Đảm bảo giá trị hợp lệ
            if index < 0:
                index = 0
            elif index >= len(self.list_skills):
                index = len(self.list_skills) - 1
            #Bóc ra kỹ năng để dùng
            chosen_skill = self.list_skills[index]
            if chosen_skill is None:
                await interaction.followup.send(f"Không tìm thấy kỹ năng đã chọn!", ephemeral=False)
                return
            #Logic xử lý dùng kỹ năng
            await self.process_special_item_functions(interaction=interaction, special_item=chosen_skill)
        except Exception as e:
            print(f"Exception on use skill MW: {e}")
            await interaction.followup.send(f"Chỉ nhập số hợp lệ!", ephemeral=True)
            return
        
        return
    
    async def process_special_item_functions(self, interaction: discord.Interaction, special_item: SwClass.SwSpecialItem):
        #Nếu có self.target thì lập tức kiểm tra xem self.target có effect đặc biệt không
        target_player_effect: SwClass.SwPlayerEffect = None
        for effect in self.info.player_effects:
            if effect.user_id == self.target.id:
                target_player_effect = effect
                break
        flag_remove_skill = True
        #Kỹ năng gợi ý 
        if special_item.item_id.endswith("hint"):
            await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nGợi ý từ hợp lệ: **`{self.info.current_word}**`")
        #Kỹ năng cộng điểm bản thân
        elif special_item.item_id.endswith("+"):
            SwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language= self.lan, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, point=special_item.point)
            await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cộng {special_item.point} điểm cho bản thân mình.\n")
        #Kỹ năng cộng hoặc trừ đối phương
        elif special_item.item_id.endswith("+u") or special_item.item_id.endswith("-"):
            text = "cộng"
            is_minus = False
            if special_item.item_id.endswith("-"):
                text = "trừ"
                is_minus = True
            if self.target == None:
                await interaction.followup.send(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                return
            #Nếu là trừ thì kiểm xem có hiệu ứng bảo hộ không
            if is_minus and target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {self.target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    SwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=special_item.point)
                    text_reply += f"{interaction.user.mention} bị trừ {special_item.point} điểm."
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        SwMongoManager.update_player_special_item(user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                        text_reply += f" và đã bị **{self.target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await interaction.followup.send(text_reply)
                #Xoá hiệu ứng khỏi target user
                SwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id, user_name=self.target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            else:
                #cộng trừ bình thường
                SwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language= self.lan, user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point=special_item.point)
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để {text} cho {self.target.mention} {special_item.point} điểm.\n")
        #Kỹ năng không rõ
        else:
            await interaction.followup.send(f"{interaction.user.mention}, Darkie vẫn chưa hoàn thành kỹ năng **`{special_item.item_name}`**.\nVui lòng đợi sau!")
            flag_remove_skill = False
        if flag_remove_skill:
            #xoá khỏi inven của player
            SwMongoManager.update_player_special_item(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, point=0, special_item=special_item, remove_special_item=True)
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
        return