import discord
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from datetime import datetime, timedelta
from Handling.MiniGame.SortWord import SwClass, SwHandling, SwMongoManager, SwView

async def setup(bot: commands.Bot):
    await bot.add_cog(SortWords(bot=bot))
    print("Sort Word game is ready!")

class SortWords(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def check_if_message_inside_game(self, source: discord.Message = None, guild_id: int = None, channel_id: int = None):

        langs = ['en', 'vn']
        if source == None: 
            for lan in langs:
                check = SwMongoManager.find_sort_word_info_by_id(lang=lan, guild_id=guild_id, channel_id= channel_id)
                if check!=None:
                    return check, lan
        else:
            for lan in langs:
                check = SwMongoManager.find_sort_word_info_by_id(lang=lan, guild_id=source.guild.id, channel_id= source.channel.id)
                if check!=None:
                    return check, lan
        return None, None
    
    #region start sort word Commands
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def start_sw_en(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Kiểm tra xem đã tồn tại game trong channel này chưa
            if SwMongoManager.find_sort_word_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, lang='en'):
                #Xoá game
                SwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang='en')
                await ctx.send(f"Đã xoá trò chơi đoán chữ trong channel này.")
            #Không tạo trong channel đoán từ tiếng việt
            elif SwMongoManager.find_sort_word_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, lang='vn'):
                await ctx.send(f"Channel này đã dành cho game đoán từ Tiếng Việt rồi!")
            else:
                #Tạo mới
                data = SwClass.SortWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="hi", unsorted_word="ih")
                result = SwMongoManager.create_info(data=data, guild_id=message.guild.id, lang='en')
                message_tu_hien_tai = f"\nTừ hiện tại: `'{data.unsorted_word}'`."
                await ctx.send(f"Đã tạo trò chơi đoán chữ tiếng Anh cho channel này. Hãy bắt đầu đoán đi. {message_tu_hien_tai}")
            return
    
    #region start sort word Commands
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def start_sw_vn(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Kiểm tra xem đã tồn tại game trong channel này chưa
            if SwMongoManager.find_sort_word_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, lang='vn'):
                #Xoá game
                SwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang='vn')
                await ctx.send(f"Đã xoá trò chơi đoán chữ trong channel này.")
            #Không tạo trong channel đoán từ tiếng việt
            elif SwMongoManager.find_sort_word_info_by_id(channel_id=message.channel.id, guild_id=message.guild.id, lang='en'):
                await ctx.send(f"Channel này đã dành cho game đoán từ Tiếng Anh rồi!")
            else:
                #Tạo mới
                data = SwClass.SortWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="nha", unsorted_word="hna")
                result = SwMongoManager.create_info(data=data, guild_id=message.guild.id, lang='vn')
                message_tu_hien_tai = f"\nTừ hiện tại: `'{data.unsorted_word}'`."
                await ctx.send(f"Đã tạo trò chơi đoán chữ tiếng Việt cho channel này. Hãy bắt đầu đoán đi. {message_tu_hien_tai}")
            return
        
        
    #region reset
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def reset_sw(self, ctx):
        message: discord.Message = ctx.message
        if message:
            #Kiểm xem có game Sort Word ở đây không
            sw_info, lan = await self.check_if_message_inside_game(source=message)
            if sw_info == None:
                await message.channel.send(f"Không tìm được trò chơi sắp xếp từ để xoá trong channel này")
                return
            await self.process_reset(message=message, sw_info=sw_info, language=lan)
            return
        
    async def process_reset(self, message: discord.Message, sw_info: SwClass.SortWordInfo, language: str):
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Game Sắp Xếp Từ", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 0
        if sw_info.player_profiles:
            sw_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            for index, profile in enumerate(sw_info.player_profiles):
                user = message.guild.get_member(profile.user_id)
                if user != None and (profile.point!= 0 or len(profile.special_items)> 0):
                    embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                    count+=1
                if count >= 25: break
        await message.channel.send(content=f"Chúc mừng các player top đầu! <@315835396305059840> sẽ trao role đặc biệt cho những Player thuộc top 3 nhé!", embed=embed)
        #Xoá đi tạo lại
        SwMongoManager.delete_data_info(channel_id=message.channel.id, guild_id=message.guild.id, lang=language)
        
        #Tạo lại
        data = SwClass.SortWordInfo(channel_id=message.channel.id, channel_name=message.channel.name, current_word="hi", unsorted_word="ih")
        result = SwMongoManager.create_info(data=data, guild_id=message.guild.id, lang='en')
        message_tu_hien_tai = f"\nTừ hiện tại: `'{data.unsorted_word}'`."
        await message.channel.send(f"Đã reset trò chơi trong channel này. {message_tu_hien_tai}")
        

    #region Bảng xếp hạng
    @discord.app_commands.command(name="bxh_sw", description="Hiện bảng xếp hạng những người chơi đoán từ trong channel này.")
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    @discord.app_commands.describe(user="Chọn user cần muốn xem cụ thể xếp hạng")
    async def bxh_sw(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        await interaction.response.defer()
        called_channel = interaction.channel
        #Kiểm xem có game Sort Word ở đây không
        sw_info, lan = await self.check_if_message_inside_game(guild_id=interaction.guild_id, channel_id=interaction.channel_id)
        if sw_info:
            embed = self.get_bxh_noi_tu(interaction=interaction, lan=lan,sw_info=sw_info, user_mention=user)
            await interaction.followup.send(embed = embed)
        else:
            await interaction.followup.send(f"Đây không phải là channel dùng để chơi đoán từ. Chỉ dùng lệnh này trong channel chơi đoán từ thôi!")
    
    def get_bxh_noi_tu(self, interaction: discord.Interaction,lan: str, sw_info: SwClass.SortWordInfo, user_mention: Optional[discord.Member] = None):
        if lan == 'en' or lan == 'eng':
            lan = "Tiếng Anh"
        elif lan == 'vn':
            lan = "Tiếng Việt"
        embed = discord.Embed(title=f"Xếp hạng các player theo điểm.", description=f"Trò Chơi Đoán Từ {lan}", color=0x03F8FC)
        embed.add_field(name=f"", value="___________________", inline=False)
        count = 0
        if sw_info.player_profiles:
            sw_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            if user_mention == None:
                for index, profile in enumerate(sw_info.player_profiles):
                    user = interaction.guild.get_member(profile.user_id)
                    if user != None and (profile.point!= 0):
                        embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                        count+=1
                    if count >= 25: break
            else:
                matched = False
                for index, profile in enumerate(sw_info.player_profiles):
                    if profile.user_id == user_mention.id:
                        user = interaction.guild.get_member(profile.user_id)
                        embed.add_field(name=f"", value=f"**Hạng {index+1}.** {user.mention}. Tổng điểm: **{profile.point}**. Số lượng kỹ năng đặc biệt: **{len(profile.special_items)}**.", inline=False)
                        #Show kỹ năng luôn
                        if profile.special_items:
                            embed.add_field(name=f"________________", value= f"")
                            for index_item, item in enumerate(profile.special_items):
                                instruction = f"!sws {item.item_id}"
                                if item.required_target:
                                    instruction = f"!sws {item.item_id} <@315835396305059840>"
                                embed.add_field(name=f"Kỹ năng {index_item+1}", value= f"Tên kỹ năng: *{item.item_name}*\n\nMô tả kỹ năng: {item.item_description}\n\nCách dùng:\n**{instruction}**", inline=False)  # Single-line field
                                embed.add_field(name=f"________________", value= f"")
                        matched = True
                        break
                if matched == False:
                    embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi này*", inline=False)     
        else:
            embed.add_field(name=f"", value=f"*Chưa có dữ liệu về người chơi*", inline=False)       
        embed.add_field(name=f"", value="___________________", inline=False)
        return embed
    
    
    #region sws_give_skill
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def sws_give_skill(self, ctx, item_id: str = None, user: Optional[discord.Member] = None):
        message: discord.Message = ctx.message
        called_channel = message.channel
        req_roles = ['Cai Ngục', 'Server Master']
        has_required_role = any(role.name in req_roles for role in message.author.roles)
        if not has_required_role and message.author.id != 315835396305059840 and message.author.id != message.guild.owner_id:
            await ctx.send("Không đủ thẩm quyền để dùng lệnh.")
            return
        
        if item_id is None or user is None:
            await ctx.send(f"Dùng sai câu lệnh. Vui lòng dùng câu lệnh đúng format sau.\n!sws_give_skill skill_id @User")
            return
        #Kiểm tra xem ở đây là channel game hay không
        sw_info, lan = await self.check_if_message_inside_game(source=message)
        if sw_info == None:
            await message.channel.send(f"Không tìm được trò chơi sắp xếp từ trong channel này")
            return

        special_item = self.get_special_item_by_id(item_id=item_id)
        if special_item==None:
            await ctx.send(f"{message.author.mention} Kỹ năng **`{item_id}`** không hợp lệ")
            return
        #Add item vào inven của player
        SwMongoManager.update_player_special_item(user_id=user.id, user_name=user.name, user_display_name=user.display_name, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, point=0, special_item= special_item)
        await ctx.send(f"Đã thêm kỹ năng **`{special_item.item_name}`** cho player {user.mention}!")
        return
    
    #region sws
    @commands.command()
    @discord.app_commands.checks.cooldown(1, 5.0) #1 lần mỗi 5s
    async def sws(self, ctx, item_id = None, user: Optional[discord.Member] = None):
        message: discord.Message = ctx.message
        if message:
            #Kiểm xem có game Sort Word ở đây không
            sw_info, lan = await self.check_if_message_inside_game(source=message)
            if sw_info == None:
                await message.channel.send(f"Không tìm được trò chơi sắp xếp từ trong channel này")
                return
            
            if item_id is None and user is None:
                embed = self.danh_sach_ky_nang(sw_info= sw_info, user=message.author)
                await message.reply(embed=embed)
                return
            
            #Kiểm xem user có kỹ năng đó không
            player = self.find_player_profile_by_user_id(user_id=message.author.id, sw_info=sw_info)
            if player == None:
                await message.reply(f"{message.author.mention} Bạn không nằm trong danh sách người chơi.")
                return
            elif player.special_items == None:
                await message.reply(f"{message.author.mention} Bạn không có bất kỳ kỹ năng nào để dùng.")
                return
            
            #nếu item_id là số đếm được
            if str.isdigit(item_id):
                item_id_int = int(item_id)
                #Phải nằm trong player.special_item
                if item_id_int < 1 or item_id_int > len(player.special_items):
                    await message.reply(f"{message.author.mention} Thứ tự kỹ năng không hợp lệ rồi!")
                    return
                special_item = player.special_items[item_id_int-1]
            #Nếu item_id là string
            else:
                #Lấy item theo item_id
                special_item = self.get_special_item_by_id(item_id=item_id)
                if special_item==None:
                    await message.reply(f"{message.author.mention} Kỹ năng **`{message.content}`** không hợp lệ")
                    return
                #Kiểm xem kỹ năng có cần mục tiêu không
                elif special_item.required_target==True and user is None:
                    await message.reply(f"{message.author.mention} Kỹ năng **`{special_item.item_name}`** yêu cầu phải có mục tiêu mới dùng được.")
                    return
                #Kiểm xem player có không
                else:
                    matched = False
                    for user_item in player.special_items:
                        if user_item.item_id == item_id:
                            matched = True
                            break
                    # Nếu player không có kỹ năng hint thì có thể đổi 3 điểm để tạo hint 
                    if matched == False and item_id == "hint":
                        if player.point< 3:
                            await message.reply(f"{message.author.mention} Bạn phải có ít nhất 3 điểm mới dùng gợi ý được.")
                            return
                        # Get the current epoch time (in seconds)
                        start_time = datetime.now()
                        end_time = start_time + timedelta(seconds=30)  # 30 seconds from now
                        unix_time = int(end_time.timestamp())
                        # Tạo embed thông báo
                        embed = discord.Embed(title=f"", description= f"{message.author.mention} bạn có muốn đổi 3 điểm để gợi ý từ tiếp theo không?", color=0xC3A757)  # Yellowish color
                        embed.add_field(name="______________", value= f"Thời gian còn lại: <t:{unix_time}:R>", inline=False)
                        view = SwView.SwView(embed=embed, user=message.author, sw_info=sw_info, lan=lan)
                        message = await message.channel.send(embed=embed, view= view)
                        view.message = message
                        return
                    elif matched == False:
                        await message.reply(f"{message.author.mention} Bạn không có kỹ năng này.")
                        return
            #Sau khi bắt lỗi, bắt đầu thực hiện chức năng kỹ năng
            await self.process_special_item_functions(sw_info=sw_info, special_item=special_item, message=message, user_target=user, lan = lan)
        return
    
    #region xử lý skill đoán từ
    async def process_special_item_functions(self, sw_info: SwClass.SortWordInfo, special_item: SwClass.SwSpecialItem, message: discord.Message, lan:str,user_target: discord.User = None):
        #Nếu có user_target thì lập tức kiểm tra xem user_target có effect đặc biệt không
        target_player_effect: SwClass.SwPlayerEffect = None
        if user_target != None:
            for effect in sw_info.player_effects:
                if effect.user_id == user_target.id:
                    target_player_effect = effect
                    break
        #Kỹ năng gợi ý 
        if special_item.item_id.endswith("hint"):
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**.\nGợi ý từ hợp lệ: **`{sw_info.current_word}**`")
        #Kỹ năng cộng điểm bản thân
        elif special_item.item_id.endswith("+"):
            SwMongoManager.update_player_point_data_info(channel_id=message.channel.id, guild_id=message.guild.id, language= lan, user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point=special_item.point)
            await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để cộng {special_item.point} điểm cho bản thân mình.\n")
        #Kỹ năng cộng hoặc trừ đối phương
        elif special_item.item_id.endswith("+u") or special_item.item_id.endswith("-"):
            text = "cộng"
            is_minus = False
            if special_item.item_id.endswith("-"):
                text = "trừ"
                is_minus = True
            if user_target == None:
                await message.reply(f"Kỹ năng **`{special_item.item_name}`** cần phải tag tên của đối phương mới có hiệu nghiệm.\n")
                return
            #Nếu là trừ thì kiểm xem có hiệu ứng bảo hộ không
            if is_minus and target_player_effect!= None and target_player_effect.effect_id.endswith("protect"):
                text_reply = f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`**, nhưng người chơi {user_target.mention} có hiệu ứng **`{target_player_effect.effect_name}`** nên không hề hấn gì! "
                #Vô hiệu hoá
                if target_player_effect.effect_id.startswith("cc") or target_player_effect.effect_id.startswith("dc"):
                    #Phản lại kỹ năng
                    SwMongoManager.update_player_point_data_info(channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id= message.author.id, user_name=message.author.name,user_display_name=message.author.display_name, point=special_item.point)
                    text_reply += f"{message.author.mention} bị trừ {special_item.point} điểm."
                    if target_player_effect.effect_id.startswith("dc"):
                        #Cướp luôn kỹ năng
                        SwMongoManager.update_player_special_item(user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
                        text_reply += f" và đã bị **{user_target.display_name}** cướp mất kỹ năng **`{special_item.item_name}`**!"
                await message.reply(text_reply)
                #Xoá hiệu ứng khỏi target user
                SwMongoManager.update_player_effects(remove_special_effect= True,channel_id=message.channel.id, guild_id=message.guild.id, language=lan, user_id=user_target.id, user_name=user_target.name, effect_id= target_player_effect.effect_id, effect_name= target_player_effect.effect_name)
            else:
                #cộng trừ bình thường
                SwMongoManager.update_player_point_data_info(channel_id=message.channel.id, guild_id=message.guild.id, language= lan, user_id=user_target.id, user_name=user_target.name, user_display_name=user_target.display_name, point=special_item.point)
                await message.reply(f"{message.author.mention} đã dùng kỹ năng **`{special_item.item_name}`** để {text} cho {user_target.mention} {special_item.point} điểm.\n")
        #Kỹ năng không rõ
        else:
            await message.reply(f"Darkie chưa hoàn thành kỹ năng **`{special_item.item_name}`** đâu nhé. Vui lòng đợi Darkie hoàn thiện bộ kỹ năng.")
            return
        #xoá khỏi inven của author
        SwMongoManager.update_player_special_item(remove_special_item=True,user_id=message.author.id, user_name=message.author.name, user_display_name=message.author.display_name, point= 0, guild_id=message.guild.id, channel_id=message.channel.id,language=lan, special_item= special_item)
        return
        
    def get_special_item_by_id(self, item_id: str):
        for data in SwClass.list_special_items_cap_thap:
            if data.item_id == item_id:
                return data
        for data in SwClass.list_special_items_cap_cao:
            if data.item_id == item_id:
                return data
        for data in SwClass.list_special_items_dang_cap:
            if data.item_id == item_id:
                return data
        for data in SwClass.list_special_items_toi_thuong:
            if data.item_id == item_id:
                return data
        return None
    
    def find_player_profile_by_user_id(self, sw_info: SwClass.SortWordInfo, user_id = int):
        if sw_info.player_profiles:
            for profile in sw_info.player_profiles:
                if profile.user_id == user_id:
                    return profile
            return None
        else:
            return None
    
    def danh_sach_ky_nang(self, sw_info: SwClass.SortWordInfo, user = discord.Member):
        embed = discord.Embed(title=f"Danh sách kỹ năng", description= f"Player: {user.mention}", color=0xC3A757)  # Yellowish color
        if sw_info.player_profiles:
            sw_info.player_profiles.sort(key=lambda x: x.point, reverse=True)
            matched = False
            list_effect = []
            for player_effect in sw_info.player_effects:
                if player_effect.user_id == user.id:
                    list_effect.append(player_effect.effect_name)
            
            for profile in sw_info.player_profiles:
                if profile.user_id == user.id:
                    matched = True
                    if len(list_effect) > 0:
                        comma_separated_string = ', '.join(list_effect)
                        embed.add_field(name=f"", value= f"Hiệu ứng đặc biệt: **`{comma_separated_string}`**", inline=False)
                        embed.add_field(name=f"________________", value= f"")
                    if profile.special_items:
                        for index_item, item in enumerate(profile.special_items):
                            instruction = f"!sws {index_item+1}"
                            if item.required_target:
                                    instruction = f"!sws {index_item+1} <@315835396305059840>"
                            embed.add_field(name=f"Kỹ năng {index_item+1}", value= f"Tên kỹ năng: *{item.item_name}*\n\nMô tả kỹ năng: {item.item_description}\n\nCách dùng:\n**{instruction}**", inline=False)  # Single-line field
                            embed.add_field(name=f"________________", value= f"")
                    else:
                        embed.add_field(name="", value= "Bạn không có kỹ năng đặc biệt nào cả.", inline=False)
                    break
            if matched == False:
                embed.add_field(name="", value= "Bạn hãy chơi trước đi đã.", inline=False)
        else:
            embed.add_field(name="", value= "Chưa có danh sách Player Profile.", inline=False)
        return embed
