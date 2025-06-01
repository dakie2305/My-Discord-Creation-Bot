import random
import discord
from Handling.MiniGame.MatchWord import ListSkills, MwClass, MwMongoManager
class MwUseSkillView(discord.ui.View):
    def __init__(self, user: discord.Member, target: discord.Member, channel_id: int, lan: str, info: MwClass.MatchWordInfo, all_skills: list[MwClass.SpecialItem], profile: MwClass.PlayerProfile, english_words_dictionary, vietnamese_dict):
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
    
    @discord.ui.button(label="Chọn Kỹ Năng", style=discord.ButtonStyle.red)
    async def chooose(self, interaction: discord.Interaction, button: discord.ui.Button):
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
    def __init__(self, user: discord.Member, target: discord.Member, channel_id: str, lan: str, list_skills: list[MwClass.SpecialItem], info: MwClass.MatchWordInfo, profile: MwClass.PlayerProfile, english_words_dictionary, vietnamese_dict, message: discord.Message):
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
    
    async def process_special_item_functions(self, interaction: discord.Interaction, special_item: MwClass.SpecialItem):
        #Nếu có self.target thì lập tức kiểm tra xem self.target có effect đặc biệt không
        target_player_effect: MwClass.PlayerEffect = None
        for effect in self.info.player_effects:
            if effect.user_id == self.target.id:
                target_player_effect = effect
                break
        flag_remove_skill = True
        #Kỹ năng hint, gợi ý từ
        if special_item.item_id == "ct_hint":
            #Tìm từ hợp lệ, bắt đầu bằng chữ cái trong
            suitable_word = None
            if self.lan == 'eng' or self.lan == 'en':
                for word in self.english_words_dictionary.keys():
                    if len(word) > 1 and word.startswith(self.info.correct_start_word) and word not in self.info.used_words:
                        suitable_word = word
            elif self.lan == 'vn':
                for word in self.vietnamese_dict.keys():
                    if len(word) > 1 and word.startswith(self.info.correct_start_word) and word not in self.info.used_words:
                        suitable_word = word
            if suitable_word == None:
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nRất tiếc là không có từ hợp lệ... lạ ta. <@315835396305059840>", ephemeral=False)
                flag_remove_skill = False
            else:
                half_length = (len(suitable_word) + 2) // 2
                suitable_word = suitable_word[:half_length] + "..."
                #Gợi ý nửa từ
                await interaction.followup.send(f"{interaction.user.mention} đã sử dụng kỹ năng **`{special_item.item_name}`**.\nGợi ý từ hợp lệ: **`{suitable_word}**`")
        elif special_item.item_id == "cc_hint":
            #Tìm từ hợp lệ, bắt đầu bằng chữ cái trong self.info
            suitable_word = None
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
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nRất tiếc là không có từ hợp lệ... lạ ta. <@315835396305059840>", ephemeral=False)
                flag_remove_skill = False
            else:
                await interaction.followup.send(f"{interaction.user.mention} đã sử dụng kỹ năng **`{special_item.item_name}`**.\nGợi ý từ hợp lệ: **`{suitable_word}**`")
        
        elif special_item.item_id =="ct_curr_player":
            if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {self.target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    MwMongoManager.update_current_player_id(channel_id=interaction.channel_id,guild_id=interaction.guild_id, language=self.lan, user_id=interaction.user.id)
                    text_reply += f"{interaction.user.mention} mất quyền nối từ trong lượt chơi hiện tại"
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        MwMongoManager.update_player_special_item(user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                        text_reply += f" và đã bị **{self.target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await interaction.followup.send(text_reply)
                #Xoá hiệu ứng khỏi target user
                MwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id, user_name=self.target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            else:
                #Chuyển current_player_id sang self.target là được
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nNgười chơi {self.target.mention} sẽ mất quyền nối từ trong lượt chơi hiện tại.\n")
                MwMongoManager.update_current_player_id(channel_id=interaction.channel_id,guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id)

        elif special_item.item_id =="ct_allow":
            #Chuyển current_player_id sang số 1 là được
            await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\n")
            MwMongoManager.update_current_player_id(channel_id=interaction.channel_id,guild_id=interaction.guild_id, language=self.lan, user_id=1)

        #Những kỹ năng có id tận cùng là minus_first hoặc minus_second
        #Đây là những kỹ năng trừ điểm của top 1 hoặc top 2
        elif special_item.item_id.endswith("minus_first") or special_item.item_id.endswith("minus_second"):
            #Tìm top player để trừ điểm
            sort = sorted(self.info.player_profiles, key=lambda x: x.point, reverse=True)
            top_number = "1"
            top_profile= None
            if special_item.item_id.endswith("minus_first"):
                if len(sort) >= 1:
                    top_profile = sort[0]
            else:
                top_number = "2"
                if len(sort) >= 2:
                    top_profile = sort[1]
            if top_profile is None:
                await interaction.followup.send(f"{interaction.user.mention} Không tìm được người chơi thuộc top {top_number} để trừ điểm")
                return
            for effect in self.info.player_effects:
                if effect.user_id == top_profile.user_id:
                    target_player_effect = effect
                    break
            if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi <@{top_profile.user_id}> có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=-special_item.point)
                    text_reply += f"{interaction.user.mention} bị trừ {special_item.point} điểm!"
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        MwMongoManager.update_player_special_item(user_id=top_profile.user_id, user_name=top_profile.user_name, user_display_name=top_profile.user_display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                        text_reply += f" và đã bị **<@{top_profile.user_id}>** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await interaction.followup.send(text_reply)
                #Xoá hiệu ứng khỏi top profile
                MwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=top_profile.user_id, user_name=top_profile.user_name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            else:
                MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= top_profile.user_id, user_name=top_profile.user_name,user_display_name=top_profile.user_display_name, point=-special_item.point)
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để trừ {special_item.point} điểm của <@{top_profile.user_id}>.\n")

        elif special_item.item_id.endswith("steal_skill") or special_item.item_id.endswith("del_skill"):
            #Lấy ra ngẫu nhiên skill trong bộ skils của đối thủ
            selected_player = None
            for player in self.info.player_profiles:
                if player.user_id == self.target.id:
                    selected_player = player
                    break
            if selected_player == None:
                await interaction.followup.send(f"Không tìm được user này trong bảng xếp hạng.")
                return
            elif selected_player.special_items == None or len(selected_player.special_items) == 0:
                await interaction.followup.send(f"Đối phương không có bất kỳ kỹ năng đặc biệt nào cả.")
                return
            if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {self.target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Chỉ cướp kỹ năng
                    MwMongoManager.update_player_special_item(user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                    text_reply += f" **{self.target.display_name}** đã cướp mất kỹ năng **`{special_item.item_name}`**!"
                await interaction.followup.send(text_reply)
                #Xoá hiệu ứng khỏi target user
                MwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id, user_name=self.target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            else:            
                random_item = random.choice(selected_player.special_items)
                action = "xoá"
                if special_item.item_id.endswith("steal_skill"): 
                    action = "cướp"
                    #Thêm cái random item kia cho user
                    MwMongoManager.update_player_special_item(user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= random_item)
                #xoá random item kia ra khỏi inven của user target
                MwMongoManager.update_player_special_item(remove_special_item=True,user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= random_item)
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để {action} kỹ năng **`{random_item.item_name}`** của {self.target.mention}.\n")

        #Những kỹ năng có id chứa chữ "_random_skill_"
        #Đây là những kỹ năng đổi điểm lấy skill
        elif special_item.item_id.endswith("random_skill_dc") or special_item.item_id.endswith("random_skill_cc"):
            random_skill = None
            if special_item.item_id.endswith("dc"):
                random_skill = random.choice(ListSkills.list_special_items_dang_cap)
            else:
                random_skill = random.choice(ListSkills.list_special_items_cap_cao)
            #Thêm cái random item kia cho user
            MwMongoManager.update_player_special_item(user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= random_skill)
            #Skill này yêu cầu hy sinh điểm để đổi skill
            MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=-special_item.point)
            await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để hy sinh {special_item.point} điểm, và nhận được kỹ năng **`{random_skill.item_name}`**.\n")

        #Những kỹ năng có id tận cùng là _minus hoặc _add
        #Đây là những kỹ năng trừ điểm hoặc cộng điểm của đối thủ
        elif special_item.item_id.endswith("_minus") or special_item.item_id.endswith("_add"):
            is_minus = special_item.item_id.endswith("_minus")
            if self.target == None and is_minus:
                await interaction.followup.send(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                return
            if is_minus:
                if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                    text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {self.target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                    #Vô hiệu hoá
                    if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                        #Phản lại kỹ năng
                        MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=-special_item.point)
                        text_reply += f"{interaction.user.mention} bị trừ {special_item.point} điểm."
                        if target_player_effect.effect_id.startswith("dc"):
                            #Cướp luôn kỹ năng
                            MwMongoManager.update_player_special_item(user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                            text_reply += f" và đã bị **{self.target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                    await interaction.followup.send(text_reply)
                    #Xoá hiệu ứng khỏi target user
                    MwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id, user_name=self.target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
                else:
                    MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= self.target.id, user_name=self.target.name,user_display_name=self.target.display_name, point=-special_item.point)
                    await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để trừ {special_item.point} điểm của {self.target.mention}.\n")
            else:
                MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=special_item.point)
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cộng {special_item.point} điểm cho bản thân mình.\n")

        #Những kỹ năng có id tận cùng là _add_user
        #Đây là những kỹ năng cộng điểm cho đối thủ
        elif special_item.item_id.endswith("_add_user"):
            if self.target == None:
                await interaction.followup.send(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                return
            elif self.target.id == interaction.user.id:
                await interaction.followup.send(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn.\n")
                return
            MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= self.target.id, user_name=self.target.name,user_display_name=self.target.display_name, point=special_item.point)
            await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cộng {special_item.point} điểm cho {self.target.mention}.\n")

        #Những kỹ năng có id tận cùng là steal_point
        #Đây là những kỹ năng ăn cắp điểm của đối thủ
        elif special_item.item_id.endswith("_steal_point"):
            if self.target == None:
                await interaction.followup.send(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                return
            elif self.target.id == interaction.user.id:
                await interaction.followup.send(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn.\n")
                return
            
            if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                    text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {self.target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                    #Vô hiệu hoá
                    if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                        #Phản lại kỹ năng
                        MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=-special_item.point)
                        MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= self.target.id, user_name=self.target.name,user_display_name=self.target.display_name, point=special_item.point)
                        text_reply += f"{interaction.user.mention} đã bị cướp mất {special_item.point} điểm!"
                        if target_player_effect.effect_id.startswith("dc"):
                            #Cướp luôn kỹ năng
                            MwMongoManager.update_player_special_item(user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                            text_reply += f" và đã bị **{self.target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                    await interaction.followup.send(text_reply)
                    #Xoá hiệu ứng khỏi target user
                    MwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id, user_name=self.target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
                    return
            
            if special_item.item_id == "ct_steal_point":
                #50% thất bại
                ran = random.randint(1, 2)
                if ran == 2:
                    await interaction.followup.send(f"{interaction.user.mention} định dùng kỹ năng **`{special_item.item_name}`** để cướp điểm {self.target.mention} nhưng đã thất bại!\n")
                    #xoá khỏi inven của player
                    MwMongoManager.update_player_special_item(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, point=0, special_item=special_item, remove_special_item=True)
                    return
            #cộng điểm player
            MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=special_item.point)
            #trừ điểm đối thủ
            MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= self.target.id, user_name=self.target.name,user_display_name=self.target.display_name, point=-special_item.point)
            await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cướp {special_item.point} điểm của {self.target.mention}.\n")
        
        #Những kỹ năng có id tận cùng là minus_all
        #Đây là những kỹ năng trừ điểm toàn bộ đối thủ
        elif special_item.item_id.endswith("minus_all"):
            await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để trừ {special_item.point} điểm cho toàn bộ đấu thủ!\n")
            MwMongoManager.update_all_players_point(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, point=-special_item.point, immune_user_id=interaction.user.id)
        
        #Những kỹ năng có id chứa chữ "_swap_"
        #Đây là những kỹ năng cộng điểm lên top
        elif "_swap_" in special_item.item_id:
            #Tìm top player để cộng điểm bản thân lên
            sort = sorted(self.info.player_profiles, key=lambda x: x.point, reverse=True)
            for player in self.info.player_profiles:
                if player.user_id == interaction.user.id:
                    curr_player = player
                    break
            top_profile = None
            if special_item.item_id.endswith("2"):
                #Lấy profile top 2 ra
                if len(sort) >= 2:
                    top_profile = sort[1]
            else:
                #Lấy profile top 3 ra
                if len(sort) >= 3:
                    top_profile = sort[2]
            if top_profile == None:
                await interaction.followup.send(f"Không tìm ra profile player top để dùng kỹ năng này.\n")
                return
            for effect in self.info.player_effects:
                if effect.user_id == top_profile.id:
                    target_player_effect = effect
                    break
                
            if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi <@{top_profile.user_id} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=-special_item.point)
                    text_reply += f"{interaction.user.mention} bị trừ {special_item.point} điểm!"
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        MwMongoManager.update_player_special_item(user_id=top_profile.user_id, user_name=top_profile.user_name, user_display_name=top_profile.user_display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                        text_reply += f" và đã bị **<@{top_profile.user_id}>** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await interaction.followup.send(text_reply)
                #Xoá hiệu ứng khỏi target user
                MwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=top_profile.user_id, user_name=top_profile.user_name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            else:
                #Lấy điểm của self.target ra và trừ điểm hiện tại của người chơi, đó sẽ là điểm cần cộng cho người chơi
                calc_point = top_profile.point -curr_player.point
                MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name,user_display_name=interaction.user.display_name, point=calc_point)
                #User target bị trừ năm điểm
                MwMongoManager.update_player_point_data_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= top_profile.id, user_name=top_profile.user_name,user_display_name=top_profile.user_display_name, point=-special_item.point)
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để thế vị trí của <@{top_profile.user_id}>, và đối phương đã bị trừ {special_item.point} điểm.\n")
        
        #Những kỹ năng có id chứa chữ "_protect"
        #Đây là những kỹ năng bảo hộ, thêm vào danh mục player effect
        elif "_protect" in special_item.item_id:
            #Thêm vào db player_effect
            if special_item.item_id.endswith("protect_user"):
                if self.target == None:
                    await interaction.followup.send(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                    return
                if self.target.id == interaction.user.id:
                    await interaction.followup.send(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn.\n")
                    return
                MwMongoManager.update_player_effects(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id, user_name=self.target.name, effect_id= "ct_protect", effect_name= "Bảo Hộ")
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để bảo vệ player {self.target.mention}.\n")
            else:    
                MwMongoManager.update_player_effects(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=interaction.user.id, user_name=interaction.user.name, effect_id= special_item.item_id, effect_name= special_item.item_name)
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** lên bản thân\n")
        
        #Những kỹ năng có id chứa chữ "_ban"
        #Đây là những kỹ năng khoá mõm player
        elif "_ban" in special_item.item_id:
            if self.target == None:
                await interaction.followup.send(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                return
            elif self.target.id == interaction.user.id:
                await interaction.followup.send(f"Ôi bạn ơi, kỹ năng **`{special_item.item_name}`** chỉ dành cho người khác chứ không phải dành cho bạn. Muốn tự khoá mõm mình à?\n")
                return
            if target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                    text_reply = f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {self.target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                    #Vô hiệu hoá
                    if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                        #Phản lại kỹ năng
                        MwMongoManager.create_and_update_player_bans_word_matching_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= interaction.user.id, user_name=interaction.user.name, ban_remaining=special_item.point)
                        text_reply += f"{interaction.user.mention} đã bị khoá mõm trong {special_item.point} vòng chơi tiếp theo"
                        if target_player_effect.effect_id.startswith("dc"):
                            #Cướp luôn kỹ năng
                            MwMongoManager.update_player_special_item(user_id=self.target.id, user_name=self.target.name, user_display_name=self.target.display_name, point= 0, guild_id=interaction.guild_id, channel_id=interaction.channel_id,language=self.lan, special_item= special_item)
                            text_reply += f" và đã bị **{self.target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                    await interaction.followup.send(text_reply)
                    #Xoá hiệu ứng khỏi target user
                    MwMongoManager.update_player_effects(remove_special_effect= True,channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=self.target.id, user_name=self.target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            else:
                #khoá mõm đối thủ
                MwMongoManager.create_and_update_player_bans_word_matching_info(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id= self.target.id, user_name=self.target.name, ban_remaining=special_item.point)
                await interaction.followup.send(f"{interaction.user.mention} đã dùng kỹ năng **`{special_item.item_name}`** để khoá mõm {self.target.mention} trong {special_item.point} lượt chơi tiếp theo.\n")
        else:
            await interaction.followup.send(f"{interaction.user.mention}, Darkie vẫn chưa hoàn thành kỹ năng **`{special_item.item_name}`**.\nVui lòng đợi sau!")
            flag_remove_skill = False
        
        if flag_remove_skill:
            #xoá khỏi inven của player
            MwMongoManager.update_player_special_item(channel_id=interaction.channel_id, guild_id=interaction.guild_id, language=self.lan, user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, point=0, special_item=special_item, remove_special_item=True)
        #Xoá luôn message
        try:
            await self.message.delete()
        except Exception:
            pass
        return