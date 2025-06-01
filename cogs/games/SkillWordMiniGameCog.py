import discord
from discord.ext import commands
from discord.app_commands import Choice
from CustomEnum import UserEnum
from CustomEnum.EmojiEnum import EmojiCreation1
import CustomFunctions
import random
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from Handling.MiniGame.MatchWord.MwGiveSkillView import MwGiveSkillView
from Handling.MiniGame.SortWord import SwClass, SwHandling, SwMongoManager, SwView
from Handling.MiniGame.MatchWord import ListSkills, MwClass, MwMongoManager
from Handling.MiniGame.SortWord.SwConfirmDeleteView import SwConfirmDeleteView
from Handling.MiniGame.SortWord.SwConfirmRestartView import SwConfirmRestartView
from Handling.MiniGame.SortWord.SwGiveSkillView import SwGiveSkillView
from Handling.Misc.SelfDestructView import SelfDestructView

async def setup(bot: commands.Bot):
    await bot.add_cog(SkillWordMiniGame(bot=bot))
    print("Skill Word Mini Game is ready!")

class SkillWordMiniGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def check_if_message_inside_sw_game(self, guild_id: int = None, channel_id: int = None):
        langs = ['en', 'vn']
        for lan in langs:
            check = SwMongoManager.find_sort_word_info_by_id(lang=lan, guild_id=guild_id, channel_id= channel_id)
            if check is not None:
                return check, lan
        return None, None
    
    def check_if_message_inside_mw_game(self, guild_id: int = None, channel_id: int = None):
        langs = ['en', 'vn']
        for lan in langs:
            check = MwMongoManager.find_match_word_info_by_id(lang=lan, guild_id=guild_id, channel_id= channel_id)
            if check is not None:
                return check, lan
        return None, None

    skill = discord.app_commands.Group(name="skill", description="Các lệnh liên quan đến Kỹ Năng đặc biệt trong Game Từ Vựng!")
    #region use skill
    @skill.command(name="use", description="Xem và sử dụng kỹ năng trong trò chơi Nối Từ, Đoán Từ!")
    @discord.app_commands.describe(target="Chọn người chơi khác ngoài bản thân")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def skills_slash_command(self, interaction: discord.Interaction, target: discord.Member):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Kiểm tra xem tồn tại mini game nối từ hay đoán từ chưa
        info, lan = self.check_if_message_inside_mw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            #Nối từ
            embed = self.get_list_skills_embed(interaction=interaction, lan= lan, mw_info=info)
            await interaction.followup.send(embed=embed)
            return
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            #Đoán từ
            embed = self.get_list_skills_embed(interaction=interaction, lan= lan, sw_info=info)
            await interaction.followup.send(embed=embed)
            return
        #Không có
        view = SelfDestructView(timeout=30)
        embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Chỉ dùng lệnh này trong kênh chơi Đoán Từ hoặc Nối Từ!",color=discord.Color.red())
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
        view.message = mess
        return
    
    @skills_slash_command.error
    async def skills_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    
    def get_list_skills_embed(self, interaction: discord.Interaction,lan: str, sw_info: SwClass.SortWordInfo = None, mw_info: MwClass.MatchWordInfo = None):
        if lan == 'en' or lan == 'eng':
            lan = "Tiếng Anh"
        elif lan == 'vn':
            lan = "Tiếng Việt"
        
        title = "Đoán Từ"
        game_info = None
        if sw_info is not None:
            game_info = sw_info
        elif mw_info is not None:
            game_info = mw_info
            title = "Nối Từ"
        embed = discord.Embed(title=f"Danh sách kỹ năng.", description=f"Trò Chơi {title} {lan}", color=0x03F8FC)
        embed.add_field(name=f"", value=f"Player: {interaction.user.mention}", inline=False)
        embed.add_field(name=f"", value="___________________", inline=False)
        list_effect = []
        for player_effect in game_info.player_effects:
            if player_effect.user_id == interaction.user.id:
                list_effect.append(player_effect.effect_name)

        if game_info.player_profiles:
            game_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for profile in game_info.player_profiles:
                if profile.user_id == interaction.user.id:
                    matched = True
                    if len(list_effect) > 0:
                        comma_separated_string = ', '.join(list_effect)
                        embed.add_field(name=f"", value= f"Hiệu ứng đặc biệt: **`{comma_separated_string}`**", inline=False)
                        embed.add_field(name=f"________________", value= f"")
                    if profile.special_items:
                        for index_item, item in enumerate(profile.special_items):
                            embed.add_field(name=f"Kỹ năng {index_item+1}", value= f"Tên kỹ năng: *{item.item_name}*\nRank: {item.level} \n\nMô tả kỹ năng: {item.item_description}", inline=False)  # Single-line field
                            embed.add_field(name=f"________________", value= f"")
                    else:
                        embed.add_field(name="", value= "Bạn không có kỹ năng đặc biệt nào cả.", inline=False)
                    break
            if matched == False:
                embed.add_field(name="", value= "Bạn hãy chơi trước đi đã.", inline=False)     
        else:
            embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi*", inline=False)       
        embed.add_field(name=f"", value="___________________", inline=False)
        return embed
    
    #region give skill
    @skill.command(name="give", description="Owner có thể cho kỹ năng cho người khác trong trò chơi Nối Từ, Đoán Từ!")
    @discord.app_commands.describe(target="Chọn người sẽ nhận kỹ năng")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def give_skill_slash_command(self, interaction: discord.Interaction, target: discord.Member):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        if interaction.user.id != interaction.guild.owner_id and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Đây là lệnh dành riêng cho chủ server để đưa kỹ năng đặc biệt cho người chơi khác!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        if target.bot:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Không được chọn bot!",color=discord.Color.red())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        #Kiểm tra xem tồn tại mini game nối từ hay đoán từ chưa
        info, lan = self.check_if_message_inside_mw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            #Nối từ
            list_embed = self.get_list_skill_embed_mw(user=interaction.user, target=target)
            first = list_embed[0]
            all_skills = []
            for item in ListSkills.list_special_items_cap_thap:
                all_skills.append(item)
            for item in ListSkills.list_special_items_cap_cao:
                all_skills.append(item)
            for item in ListSkills.list_special_items_dang_cap:
                all_skills.append(item)
            for item in ListSkills.list_special_items_toi_thuong:
                all_skills.append(item)

            #Paginate view
            view = MwGiveSkillView(user=interaction.user, target=target, channel_id=interaction.channel_id, lan=lan, list_embed=list_embed, all_skills= all_skills)
            mess = await interaction.followup.send(embed=first, view=view)
            view.message = mess
            return
        info, lan = self.check_if_message_inside_sw_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if info is not None:
            #Đoán từ
            list_embed = self.get_list_skill_embed_sw(user=interaction.user, target=target)
            first = list_embed[0]
            all_skills = []
            for item in SwClass.list_special_items_cap_thap:
                all_skills.append(item)
            for item in SwClass.list_special_items_cap_cao:
                all_skills.append(item)
            for item in SwClass.list_special_items_dang_cap:
                all_skills.append(item)
            for item in SwClass.list_special_items_toi_thuong:
                all_skills.append(item)

            #Paginate view
            view = SwGiveSkillView(user=interaction.user, target=target, channel_id=interaction.channel_id, lan=lan, list_embed=list_embed, all_skills= all_skills)
            mess = await interaction.followup.send(embed=first, view=view)
            view.message = mess
            return
        #Không có
        view = SelfDestructView(timeout=30)
        embed = discord.Embed(title="",description=f"{EmojiCreation1.CROSS.value} Chỉ dùng lệnh này trong kênh chơi Đoán Từ hoặc Nối Từ!",color=discord.Color.red())
        mess = await interaction.followup.send(embed=embed, view=view, ephemeral=False)
        view.message = mess
        return
        

    
    @give_skill_slash_command.error
    async def give_skill_slash_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(f"⏳ Lệnh đang cooldown, vui lòng thực hiện lại trong vòng {error.retry_after:.2f}s tới.", ephemeral=True)
        else:
            await interaction.response.send_message("Có lỗi khá bự đã xảy ra. Lập tức liên hệ Darkie ngay.", ephemeral=True)
    


    def get_list_skill_embed_mw(self, user: discord.Member, target: discord.Member):
        list_embed = []
        page_size = 5
        all_skills = []

        def add_skills_with_label(label, skill_list):
            for skill in skill_list:
                all_skills.append((label, skill))

        add_skills_with_label("Cấp Thấp", ListSkills.list_special_items_cap_thap)
        add_skills_with_label("Cấp Cao", ListSkills.list_special_items_cap_cao)
        add_skills_with_label("Đẳng Cấp", ListSkills.list_special_items_dang_cap)
        add_skills_with_label("Tối Thượng", ListSkills.list_special_items_toi_thuong)

        total_skills = len(all_skills)
        page_index = 0

        for i in range(0, total_skills, page_size):
            embed = discord.Embed(
                title="Danh sách kỹ năng Nối Từ",
                description=f"{user.mention} hãy chọn kỹ năng để cho {target.mention}",
                color=0x03F8FC
            )
            embed.add_field(name="", value="___________________", inline=False)

            for j in range(i, min(i + page_size, total_skills)):
                category, skill = all_skills[j]
                embed.add_field(
                    name=f"Kỹ năng `#{j- i + 1}`: **{skill.item_name}**",
                    value=(
                        f"ID: `{skill.item_id}`\n"
                        f"Rank: **{skill.level}**\n"
                        f"Mô tả kỹ năng: {skill.item_description}"
                    ),
                    inline=False
                )
                embed.add_field(name="________________", value="\u200b", inline=False)
            page_index += 1
            embed.set_footer(text=f"Trang {page_index}/{(total_skills + page_size - 1) // page_size}")
            list_embed.append(embed)
        return list_embed
    

    def get_list_skill_embed_sw(self, user: discord.Member, target: discord.Member):
        list_embed = []
        page_size = 5
        all_skills = []

        def add_skills_with_label(label, skill_list):
            for skill in skill_list:
                all_skills.append((label, skill))

        add_skills_with_label("Cấp Thấp", SwClass.list_special_items_cap_thap)
        add_skills_with_label("Cấp Cao", SwClass.list_special_items_cap_cao)
        add_skills_with_label("Đẳng Cấp", SwClass.list_special_items_dang_cap)
        add_skills_with_label("Tối Thượng", SwClass.list_special_items_toi_thuong)

        total_skills = len(all_skills)
        page_index = 0

        for i in range(0, total_skills, page_size):
            embed = discord.Embed(
                title="Danh sách kỹ năng Đoán Từ",
                description=f"{user.mention} hãy chọn kỹ năng để cho {target.mention}",
                color=0x03F8FC
            )
            embed.add_field(name="", value="___________________", inline=False)
            for j in range(i, min(i + page_size, total_skills)):
                category, skill = all_skills[j]
                embed.add_field(
                    name=f"Kỹ năng `#{j- i + 1}`: **{skill.item_name}**",
                    value=(
                        f"ID: `{skill.item_id}`\n"
                        f"Rank: **{skill.level}**\n"
                        f"Mô tả kỹ năng: {skill.item_description}"
                    ),
                    inline=False
                )
                embed.add_field(name="________________", value="\u200b", inline=False)
            page_index += 1
            embed.set_footer(text=f"Trang {page_index}/{(total_skills + page_size - 1) // page_size}")
            list_embed.append(embed)
        return list_embed

