import discord
from discord.ext import commands
from typing import Optional
from Handling.Economy.Quest.QuestClass import QuestProfile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from Handling.Misc.SelfDestructView import SelfDestructView
from enum import Enum
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
import CustomFunctions
import CustomEnum.UserEnum as UserEnum
import db.DbMongoManager as DbMongoManager
import random
from db.Class.CustomClass import GuildExtraInfo
from datetime import datetime, timedelta
from discord.app_commands import Choice
from Handling.Economy.Quest.DungeonQuestChannelClass import DungeonQuestChannel

async def setup(bot: commands.Bot):
    await bot.add_cog(QuestEconomy(bot=bot))
    print("Quest Economy is ready!")

class QuestEconomy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #region quest
    @discord.app_commands.command(name="quest", description="Hiển thị nhiệm vụ trong server")
    @discord.app_commands.describe(user="Chọn user để xem nhiệm vụ của người đó.")
    async def show_quest_profile(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        await interaction.response.defer(ephemeral=False)
        
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if user!= None and user.bot:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không được dùng cho bot!",color=discord.Color.blue())
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if user == None:
            embed = await self.procress_quest_embed(user=interaction.user)
        else:
            embed = await self.procress_quest_embed(user=user)
        await interaction.followup.send(embed=embed)
        return
    
    @commands.command()
    async def quest(self, ctx, user: Optional[discord.Member] = None):
        if user != None and user.bot: return
        message: discord.Message = ctx.message
        if message:
            #Không cho dùng bot nếu không phải user
            if CustomFunctions.check_if_dev_mode() == True and message.author.id != UserEnum.UserId.DARKIE.value:
                view = SelfDestructView(timeout=30)
                embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
                mess = await message.reply(embed=embed, view=view)
                view.message = mess
                return
            
            if user == None:
                embed = await self.procress_quest_embed(user=message.author)
            else:
                embed = await self.procress_quest_embed(user=user)
            await message.reply(embed=embed)
    
    async def procress_quest_embed(self, user: discord.Member):
        data = ProfileMongoManager.find_profile_by_id(guild_id=user.guild.id, user_id=user.id)
        if data == None:
            data = ProfileMongoManager.create_profile(guild_id=user.guild.id, user_id=user.id, guild_name=user.guild.name, user_name=user.name, user_display_name=user.display_name)
        quest = QuestMongoManager.find_quest_by_user_id(guild_id=user.guild.id, user_id=user.id)
        
        #Tìm xem channel có list chanel dành cho quest chưa
        guild_extra_info = DbMongoManager.find_guild_extra_info_by_id(guild_id=user.guild.id)
        if guild_extra_info == None or guild_extra_info.list_channels_quests == None or len(guild_extra_info.list_channels_quests) == 0:
            embed = discord.Embed(title=f"Owner Server vui lòng dùng lệnh {SlashCommand.QUEST_CHANNELS.value} để thêm channel cho Hệ Thống Nhiệm Vụ chọn!",color=discord.Color.red())
            return embed
        
        #Kiểm tra xem nếu today đã lố quest.reset_date thì xoá quest làm lại
        if quest != None and quest.reset_date != None and quest.reset_date.date() <= datetime.now().date():
            QuestMongoManager.delete_quest(guild_id=user.guild.id, user_id=user.id)
            quest = None
        
        
        #Kiểm xem quest cũ đã hoàn thành chưa
        if quest != None and quest.quest_progress!= None and quest.quest_total_progress != None and quest.quest_progress >= quest.quest_total_progress and quest.quest_title != None:
            #Hoàn thành
            new_embed = discord.Embed(title=f"", description=f"Chúc mừng **{user.name}** đã hoàn thành nhiệm vụ: {quest.quest_title}!",color=discord.Color.blue())
            new_embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            new_embed.add_field(name=f"", value=f"Bạn đã được nhận thưởng sau:", inline=False)
            new_embed.add_field(name=f"", value=f"{EmojiCreation2.GOLDEN_GIFT_BOX.value}: {quest.quest_description}", inline=False)
            if quest.bonus_exp != None and quest.bonus_exp != 0:
                new_embed.add_field(name=f"", value=f"{EmojiCreation2.GOLDEN_GIFT_BOX.value}: {quest.bonus_exp} Điểm Kinh Nghiệm", inline=False)
            new_embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
            new_embed.add_field(name=f"", value=f"> Đừng quên dùng lệnh {SlashCommand.QUEST.value} để nhận nhiệm vụ trong server nhé", inline=False)
            new_embed.set_footer(text=f"Quest {user.name}", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            #Cộng tiền
            ProfileMongoManager.update_profile_money(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name= user.display_name, gold=quest.quest_reward_gold, silver=quest.quest_reward_silver, copper=quest.quest_reward_copper)
            #Cộng kinh nghiệm
            ProfileMongoManager.update_level_progressing(guild_id=user.guild.id, user_id=user.id, bonus_exp= quest.bonus_exp)
            #Xoá quest hiện tại
            QuestMongoManager.delete_quest(guild_id=user.guild.id, user_id=user.id)
            return new_embed
        
        list_channels_quests = guild_extra_info.list_channels_quests.copy()
        if not list_channels_quests:
            embed = discord.Embed(title=f"Owner Server vui lòng dùng lệnh {SlashCommand.QUEST_CHANNELS.value} để thêm channel cho Hệ Thống Nhiệm Vụ chọn!",color=discord.Color.red())
            return embed
        quest_channel = None
        random_quest_channel_id = random.choice(list_channels_quests)
        quest_channel = user.guild.get_channel(random_quest_channel_id)
        if quest_channel is None:
            #Xoá channel_id lỗi
            list_channels_quests.remove(random_quest_channel_id)
            data_updated = {"list_channels_quests": list_channels_quests}
            DbMongoManager.update_guild_extra_info(guild_id=user.guild.id, update_data= data_updated)
            #Chọn lại channel khác
            if list_channels_quests == None or len(list_channels_quests) <= 0:
                embed = discord.Embed(title=f"Owner Server vui lòng dùng lệnh {SlashCommand.QUEST_CHANNELS.value} để thêm channel cho Hệ Thống Nhiệm Vụ chọn!",color=discord.Color.red())
                return embed
            if quest_channel is None and list_channels_quests:
                random_quest_channel_id = random.choice(list_channels_quests)
                quest_channel = user.guild.get_channel(random_quest_channel_id)
        
        if quest_channel is None:
                embed = discord.Embed(title=f"Owner Server vui lòng dùng lệnh {SlashCommand.QUEST_CHANNELS.value} để thêm channel cho Hệ Thống Nhiệm Vụ chọn!",color=discord.Color.red())
                return embed
        
        if quest == None:
            #Tạo random quest
            quest = QuestMongoManager.create_new_random_quest(guild_id=user.guild.id, guild_name=user.guild.name, user_id=user.id, user_name=user.name, user_display_name=user.display_name, channel_id=quest_channel.id, channel_name=quest_channel.name, data_profile=data)
        embed = discord.Embed(title=f"", description=f"**Nhiệm vụ dành cho {user.mention}**", color=0xe9f5ec)
        if user.avatar!=None:
            embed.set_thumbnail(url=user.avatar.url)
        if quest.reset_date != None:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Thời gian reset nhiệm vụ: <t:{int(quest.reset_date.timestamp())}:D> ", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cấp độ nhiệm vụ: **{self.get_cap_do_quest(quest.quest_difficult_rate)}**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Tổng nhiệm vụ hoàn thành: **{data.quest_finished}**", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"**Mô tả nhiệm vụ**: {quest.quest_title}", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} `Tiến độ`: {quest.quest_progress}/{quest.quest_total_progress}", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.GOLDEN_GIFT_BOX.value} Phần Thường: {quest.quest_description}", inline=False)
        if quest.bonus_exp != None and quest.bonus_exp != 0:
            embed.add_field(name=f"", value=f"{EmojiCreation2.GOLDEN_GIFT_BOX.value} Điểm thưởng: +**{quest.bonus_exp}** Kinh Nghiệm", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Nhớ đừng quên tuân theo đúng luật server khi làm quest! Khó quá thì dùng lệnh /quests reset!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
        return embed
    
    quest_group = discord.app_commands.Group(name="quests", description="Các lệnh liên quan đến Nhiệm Vụ của server!")
    #region quest channels
    @quest_group.command(name="channels", description="Thêm/xoá channel ra khỏi hệ thống Nhiệm Vụ Server")
    async def quest_channel_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        #Lệnh dành riêng cho server owner
        if interaction.user.id != interaction.guild.owner_id and interaction.user.id != UserEnum.UserId.DARKIE.value:
            await interaction.followup.send(content="Lệnh chỉ dành riêng cho Owner Server thôi!", ephemeral=True)
            return

        check_exist = DbMongoManager.find_guild_extra_info_by_id(interaction.guild.id)
        if check_exist:
            list_channels_quests = check_exist.list_channels_quests
            add = True
            if interaction.channel.id not in list_channels_quests:
                #thêm
                list_channels_quests.append(interaction.channel.id)
            else:
                add = False
                list_channels_quests.remove(interaction.channel.id)
            data_updated = {"list_channels_quests": list_channels_quests}
            DbMongoManager.update_guild_extra_info(guild_id=interaction.guild.id, update_data= data_updated)
            if add:
                await interaction.followup.send(f"Đã thêm channel này vào trong hệ thống nhiệm vụ của server này.", ephemeral= True)
            else:
                await interaction.followup.send(f"Đã xoá channel này khỏi hệ thống nhiệm vụ của server này.", ephemeral= True)
        else:
            list_channels_quests= []
            list_channels_quests.append(interaction.channel.id)
            data = GuildExtraInfo(guild_id=interaction.guild.id, guild_name= interaction.guild.name, allowed_ai_bot=True, list_channels_quests= list_channels_quests)
            DbMongoManager.insert_guild_extra_info(data)
            await interaction.followup.send(f"Đã tạo Guild Extra Info và thêm channel này vào trong hệ thống nhiệm vụ của server này.", ephemeral= True)
    
    #region quest reset
    @quest_group.command(name="reset", description="Reset nhiệm vụ của bản thân. Tốn tiền để reset")
    async def quest_reset_slash(self, interaction: discord.Interaction):
        await interaction.response.defer()
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        #Kiểm xem có quest không
        quest = QuestMongoManager.find_quest_by_user_id(guild_id=interaction.guild_id, user_id=interaction.user.id)        
        if quest == None:
            embed = discord.Embed(title=f"Bạn làm gì có quest để mà reset?! Vui lòng dùng lệnh {SlashCommand.QUEST.value} trước đã!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        #Kiểm tra xem đủ 10 silver không
        profile = ProfileMongoManager.find_profile_by_id(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if profile == None:
            embed = discord.Embed(title=f"Vui lòng dùng lệnh {SlashCommand.QUEST.value} hoặc {SlashCommand.PROFILE.value} trước đã!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        #Dựa vào quest reward_type để xác định loại tiền cần tốn
        cost_money = 10
        money_type = EmojiCreation2.SILVER.value
        if quest.quest_reward_gold > 0:
            cost_money = quest.quest_reward_gold
            money_type = EmojiCreation2.GOLD.value
        elif quest.quest_reward_silver > 10:
            cost_money = quest.quest_reward_silver
            money_type = EmojiCreation2.SILVER.value
        
        if money_type == EmojiCreation2.SILVER.value and profile.silver < cost_money:
            embed = discord.Embed(title=f"Bạn không có đủ **{cost_money}** {EmojiCreation2.SILVER.value} để reset quest hiện tại!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        elif money_type == EmojiCreation2.GOLD.value and profile.gold < cost_money:
            embed = discord.Embed(title=f"Bạn không có đủ **{cost_money}** {EmojiCreation2.GOLD.value} để reset quest hiện tại!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        QuestMongoManager.delete_quest(guild_id=interaction.guild_id, user_id=interaction.user.id)
        if money_type == EmojiCreation2.SILVER.value:
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, silver=-cost_money)
        if money_type == EmojiCreation2.GOLD.value:
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name="", user_id=interaction.user.id, user_name=interaction.user.name, user_display_name=interaction.user.display_name, gold=-cost_money)
        embed = discord.Embed(title=f"Bạn đã bị trừ {cost_money} {money_type} để reset nhiệm vụ hiện tại! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để nhận Nhiệm Vụ mới.",color=discord.Color.blue())
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
        
    def get_cap_do_quest(self, input: int):
        text = "Dễ"
        if input == 1:
            text = "Dễ"
        elif input == 2:
            text = "Vừa Phải"
        elif input == 3:
            text = "Khó"
        elif input == 4:
            text = "Huyền Thoại"
        return text
    
    #region quest channels
    @quest_group.command(name="dungeon_channels", description="Thêm/xoá channel Hầm Ngục Hộ Vệ Thần trong hệ thống Hầm Ngục Server")
    @discord.app_commands.choices(level=[
        Choice(name="Độ khó: Dễ", value="1"),
        Choice(name="Độ khó: Vừa Phải", value="2"),
        Choice(name="Độ khó: Khó", value="3"),
        Choice(name="Độ khó: Huyền Thoại", value="4"),
    ])
    async def quest_dungeon_channels_slash(self, interaction: discord.Interaction, level: str = None):
        await interaction.response.defer(ephemeral=False)
        #Không cho dùng bot nếu không phải user
        if CustomFunctions.check_if_dev_mode() == True and interaction.user.id != UserEnum.UserId.DARKIE.value:
            embed = discord.Embed(title=f"Darkie đang nghiên cứu, cập nhật và sửa chữa bot! Vui lòng đợi nhé!",color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        if level == None: level = "1"
        level_as_int = int(level)

        check_exist = DbMongoManager.find_guild_extra_info_by_id(interaction.guild.id)
        if check_exist:
            list_channels_dungeon = check_exist.list_channels_dungeon
            if (list_channels_dungeon == None or len(list_channels_dungeon) == 0) and (interaction.user.id != interaction.guild.owner_id and interaction.user.id != UserEnum.UserId.DARKIE.value):
                await interaction.followup.send(content="Vui lòng nhờ Owner Server dùng lệnh này để thêm channel này vào danh sách Hầm Ngục Hộ Vệ Thần!", ephemeral=True)
                return
            is_remove = False
            text = ""
            if interaction.user.id == interaction.guild.owner_id or interaction.user.id == UserEnum.UserId.DARKIE.value:
                for dungeon in list_channels_dungeon:
                    if dungeon.channel_id == interaction.channel_id:
                        #Xóa
                        is_remove = True
                        list_channels_dungeon.remove(dungeon)
                        break
                if is_remove == False:
                    data = DungeonQuestChannel(channel_id=interaction.channel_id, channel_name=interaction.channel.name, difficulty_level=level_as_int)
                    list_channels_dungeon.append(data)
                    text = f"Đã chọn channel này vào Hệ Thống Hầm Ngục Hộ Vệ Thần trong server này. Độ khó: **{self.get_cap_do_quest(input=level_as_int)}**"
                else:
                    text = f"Đã xóa channel này khỏi Hệ Thống Hầm Ngục Hộ Vệ Thần trong server này."
                DbMongoManager.update_guild_extra_info_list_channels_dungeon(guild_id=interaction.guild.id, list_channels_dungeon=list_channels_dungeon)
            
            embed = discord.Embed(title="Danh sách hầm ngục", description=f"Có tổng cộng **{len(list_channels_dungeon)} hầm ngục**", color=0xddede7)
            count = 0
            for value in list_channels_dungeon:
                count+=1
                embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Hầm Ngục: <#{value.channel_id}>. Độ khó: **{self.get_cap_do_quest(input=value.difficulty_level)}**", inline=False)
                if count > 19:
                    embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Và còn nhiều hầm ngục khác nữa!", inline=False)
                    break
                
            await interaction.followup.send(content=text, embed=embed)
        else:
            #nếu không phải là server owner thì làm như dưới
            if interaction.user.id != interaction.guild.owner_id and interaction.user.id != UserEnum.UserId.DARKIE.value:
                await interaction.followup.send(content="Vui lòng nhờ Owner Server dùng lệnh này để thêm channel này vào danh sách Hầm Ngục Hộ Vệ Thần!", ephemeral=True)
                return
            list_channels_dungeon= []
            data = DungeonQuestChannel(channel_id=interaction.channel_id, channel_name=interaction.channel.name, difficulty_level=level_as_int)
            list_channels_dungeon.append(data)
            data = GuildExtraInfo(guild_id=interaction.guild.id, guild_name= interaction.guild.name, allowed_ai_bot=True, list_channels_dungeon=list_channels_dungeon)
            DbMongoManager.insert_guild_extra_info(data)
            await interaction.followup.send(f"Đã chọn thêm channel này vào Hệ Thống Hầm Ngục Hộ Vệ Thần trong server này. Độ khó: **{self.get_cap_do_quest(input=level_as_int)}**", ephemeral= True)