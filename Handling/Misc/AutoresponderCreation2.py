
import discord
from discord.ext import commands
import CustomFunctions
import asyncio
import random
from Handling.Misc.SelfDestructView import SelfDestructView
from enum import Enum
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from CustomEnum.EmojiEnum import EmojiCreation2 
import string
from Handling.Economy.Inventory_Shop.ItemClass import Item, list_gift_items, list_protection_items, list_support_items, list_attack_items, list_fishing_rod, list_legend_weapon_1, list_legend_weapon_2
import db.DbMongoManager as db
from db.DbMongoManager import UserInfo, GuildExtraInfo
from datetime import datetime, timedelta

class CurrencyEmoji(Enum):
        DARKIUM = "<a:darkium:1294615481701105734>"
        GOLD = "<a:gold:1294615502588608563>"
        SILVER = "<a:silver:1294615512919048224>"
        COPPER = "<a:copper:1294615524918956052>"
    
class CurrencySlashCommand(Enum):
        PROFILE = "</profile:1294699979058970656>"
        VOTE_AUTHORITY = "</vote_authority:1294754901988999240>"
        BANK = "</bank:1295012466417205368>"

class AutoresponderHandling():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def handling_auto_responder(self, message: discord.Message):
        conversion_rate = ["quy đổi coin", "quy đổi gold", "quy đổi silver", "quy đổi copper", "quy đổi darkium", "quy đổi tiền tệ"]
        quote = ["quote"]
        bank_help = ["bank help", "bank sao", "bank?"]
        
        dignity_help = ["tăng nhân phẩm", "điểm nhân phẩm", "nhân phẩm là gì", "nhân phẩm?"]
        dia_vi_help = ["tăng địa vị", "điểm địa vị", "địa vị là gì", "địa vị?"]
        
        bbb_warning = ["bbb", "BBB", "bảo baby", "bảo babi"]
        
        donate = ["donate"]
        donate_disable = ["!disable donation", "!disable donation text"]
        sb_help = ["sb help","cách chơi tài xỉu", "tài xỉu?", "tx help"]
        legend_weapon = ["thất truyền huyền khí"]
        ga_help = ["ga help", "guardian help", "hộ vệ thần?", "guardian help"]

        chosen_item: Item = None
        
        for item in list_legend_weapon_1:
            if item.item_name.lower() in message.content.lower():
                chosen_item = item
                break
        for item in list_legend_weapon_2:
            if item.item_name.lower() in message.content.lower():
                chosen_item = item
                break
                
        flag = False
        if message.author.bot: return flag
        
        elif CustomFunctions.contains_substring(message.content.lower(), conversion_rate):
            embed = discord.Embed(title=f"", description=f"**Đơn vị quy đổi chuẩn của Creation 2 rất đơn giản thôi!**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f">>> 1 <a:darkium:1294615481701105734> = **10.000** <a:gold:1294615502588608563>\n1 <a:gold:1294615502588608563> = **5.000** <a:silver:1294615512919048224>\n1 <a:silver:1294615512919048224> = **5.000** <a:copper:1294615524918956052>\n", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value="Đương nhiên là chưa tính tỷ lệ quy đổi ngẫu nhiên tuỳ theo ngày nha. Hãy dùng lệnh </profile:1294699979058970656> để xem profile", inline=False)
            view = SelfDestructView(timeout=120)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
            flag = True
        
        elif message.content and message.content[0] == "=" and message.content != "=":
            flag = True
            options = [item.strip() for item in message.content[1:].split(",") if item.strip()]
            if len(options) >1:
                random_choice = random.choice(options)
                await message.reply(content=f"{random_choice}")
        
        elif CustomFunctions.contains_substring(message.content.lower(), quote) and message.content[0] not in string.punctuation and message.content[0] != ":":
            flag = True
            embed = discord.Embed(title=f"", description=f"Để thay đổi **Quote** trong lệnh </profile:1294699979058970656> thì hãy dùng lệnh:\n!quote \"Ghi quote vào đây\"", color=0xc379e0)
            view = SelfDestructView(timeout=60)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
        
        elif CustomFunctions.contains_substring(message.content.lower(), bank_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn lệnh {CurrencySlashCommand.BANK.value}", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value="- Đầu tiên, nếu muốn đổi sang tiền gì, ta chọn vào ô xổ xuống, chọn loại tiền ta đang cần.", inline=False)
            embed.add_field(name="", value="- Nhìn vào tỉ lệ quy đổi, làm chút toán để biết ta sẽ cần đổi bao nhiêu.", inline=False)
            embed.add_field(name="", value=f"- Ví dụ, muốn đổi **1** {CurrencyEmoji.SILVER.value} sang {CurrencyEmoji.COPPER.value}, thì ta sẽ chọn ô xổ xuống là Quy Đổi Sang Copper, rồi trong ô nhập t ghi là 1S là sẽ đổi từ **1** {CurrencyEmoji.SILVER.value} sang số {CurrencyEmoji.COPPER.value} như trên tỷ lệ quy đổi", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.set_footer(text=f"Tỉ lệ quy đổi sẽ thay đổi theo mỗi ngày hoặc do Chính Quyền ép thay đổi nha!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
            
        elif CustomFunctions.contains_substring(message.content.lower(), ga_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn Hộ Vệ Thần", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"- Bạn có thể mua một Hộ Vệ Thần trong lệnh {SlashCommand.SHOP_GUARDIAN.value}!", inline=False)
            embed.add_field(name="", value=f"- Ngoài ra còn có thể mua kỹ năng cho Hộ Vệ Thần trong lệnh {SlashCommand.SHOP_GUARDIAN_SKILL.value}!", inline=False)
            embed.add_field(name="", value=f"- Mỗi hộ vệ thần có các chỉ số chính: Máu, Thể Lực, Mana và Sức Tấn Công", inline=False)
            embed.add_field(name="", value=f"- Máu cao sẽ trụ được lâu, Thể Lực cao sẽ né được nhiều đòn, Mana cao sẽ tung được kỹ năng nhiều lần!", inline=False)
            embed.add_field(name="", value=f"- Đừng quên dùng lệnh {SlashCommand.GA_FEED.value}, {SlashCommand.GA_MEDITATE.value} hoặc mua bình hồi phục!", inline=False)
            embed.add_field(name="", value=f"- Lệnh {SlashCommand.GA_BATTLE.value} nếu chọn `target` là sẽ đánh với người chơi khác! Đây coi như giao hữu, nên sẽ không mất chỉ số hay chết vĩnh viễn nếu thua!", inline=False)
            embed.add_field(name="", value=f"- Lệnh {SlashCommand.GA_BATTLE.value} nếu không chọn `target` là sẽ đánh với quái! Mọi chỉ số đã mất sẽ lưu lại, và có khả năng chết vĩnh viễn nếu thua!", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.set_footer(text=f"Đừng quên mỗi Hộ Vệ Thần có tỉ lệ chết vĩnh viễn nếu để trọng thương khi đánh với quái nhé! Tỉ lệ rất thấp, nhưng đừng khinh suất!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess

        
        elif CustomFunctions.contains_substring(message.content.lower(), dignity_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn **Điểm nhân phẩm**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Điểm nhân phẩm sẽ quyết định rất nhiều điều, về số tiền bạn kiếm được, về kinh nghiệm bạn kiếm được... và sẽ tác động đến những lệnh khác mà cần tốn tiền.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Điểm nhân phẩm càng thấp thì nhân phẩm bạn sẽ thấp và có thể gặp bất lợi, nhưng đồng thời cũng có lợi ở đôi chỗ khác như {SlashCommand.WORK.value} thì có thể trốn thuế nhiều hơn.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Để tăng nhân phẩm thì chỉ cần dùng những lệnh cơ bản như {SlashCommand.WORK.value}, {SlashCommand.DAILY.value} là được.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Nhân phẩm sẽ giảm khi bạn bạo động, hoặc khi chơi các mini game cờ bạc nhưng để bị thua.", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
        
        elif CustomFunctions.contains_substring(message.content.lower(), sb_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn chơi **tài xỉu**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"- Tài xỉu bình thường ({SlashCommand.SB_NORMAL.value}) có tỷ lệ ăn 1:1 nếu thắng (tức đặt 1 {EmojiCreation2.GOLD.value} sẽ ăn 1 {EmojiCreation2.GOLD.value}), và cách tính thắng thua như sau:", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} **Thắng**: nếu chọn **tài** và ba xúc xắc cộng lại bằng 11 -> 17, hoặc chọn **xỉu** và tổng ba xúc xắc bằng 4 -> 10.", inline=False)
            embed.add_field(name="", value=f"- Tài xỉu double ({SlashCommand.SB_DOUBLE.value}) có tỷ lệ ăn 1:2, hoặc 1:4 nếu đoán số (tức đặt 1 {EmojiCreation2.GOLD.value} sẽ ăn 2 hoặc 4 {EmojiCreation2.GOLD.value}), và cách tính thắng thua như sau:", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} **Thắng**: nếu không đoán số, và hai trên ba xúc xắc ra giống nhau sẽ thắng. Nếu đoán trúng hai số nào sẽ ra giống nhau sẽ thắng x6 lần số tiền đặt cược.", inline=False)
            embed.add_field(name="", value=f"- Tài xỉu triple ({SlashCommand.SB_TRIPLE.value}) có tỷ lệ ăn 1:6, hoặc 1:8 nếu đoán số (tức đặt 1 {EmojiCreation2.GOLD.value} sẽ ăn 6 hoặc 8 {EmojiCreation2.GOLD.value}), và cách tính thắng thua như sau:", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} **Thắng**: nếu không đoán số, và cả ba xúc xắc ra giống nhau sẽ thắng. Nếu đoán trúng số nào sẽ ra giống nhau sẽ thắng x8 lần số tiền đặt cược.", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
            
        elif CustomFunctions.contains_substring(message.content.lower(), dia_vi_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn **Địa Vị**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Địa vị chính là tổng số tài sản của bạn cộng lại mà ra. Tổng tài sản càng nhiều thì địa vị sẽ tăng lên, và ngược lại.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Để kiếm được tiền thì bạn có thể dùng những lệnh như {SlashCommand.WORK.value}, {SlashCommand.DAILY.value}, hoặc đi bạo động chính quyền, hoặc chơi các lệnh cờ bạc! Vô vàn lựa chọn cho bạn chọn!", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
            
        elif chosen_item!= None:
            flag = True
            embed = discord.Embed(title=f"", description=f"**Thất Truyền Huyền Khí**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Vũ khí: [{chosen_item.emoji} - **{chosen_item.item_name}**]", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Mô tả: {chosen_item.item_description}", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
            
        elif CustomFunctions.contains_substring(message.content.lower(), legend_weapon):
            flag = True
            embed = discord.Embed(title=f"", description=f"**Thất Truyền Huyền Khí**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Chúng là tập hợp các vũ khí huyền thoại từng làm điên đảo thế gian, và đã thất lạc đến ngàn đời sau.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Mỗi vũ khí đều là vũ khí độc nhất với kỹ năng tối thượng cực mạnh và xuyên phá tất cả giáp mà kẻ địch đang mang", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Một số vũ khí có thể nhắm vào tất cả vật phẩm của kẻ địch", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Có thể câu được chúng bằng các cần câu cùi, tỉ lệ 5%", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Có thể mua được chúng trong {SlashCommand.SHOP_GLOBAL.value} vào đúng duy nhất **00:00** đêm hoặc **12:00**", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
            
        elif CustomFunctions.contains_substring(message.content.lower(), bbb_warning) and message.channel.id != 1297787832986767381 and message.guild.id == 1256987900277690470:
            flag = True
            view = SelfDestructView(timeout=5)
            _mess = await message.channel.send(content=f"Shhhhh... We do not talk about this topic here.", view=view)
            view.message= _mess
            await message.delete()
        
        elif message.guild.id != 1194106864582004849 and CustomFunctions.contains_substring(message.content.lower(), donate):
            check_exist = db.find_guild_extra_info_by_id(message.guild.id)
            if check_exist != None and check_exist.disable_donation_text_until != None and datetime.now() > check_exist.disable_donation_text_until:
                flag = True
                embed = discord.Embed(title=f"**Donate Darkie**", description=f"Xin lỗi vì đã làm phiền nhé! Tin nhắn này sẽ biến mất chỉ sau 1-2 phút thôi nhé!", color=0xc379e0)
                embed.set_image(url="https://i.imgur.com/Zsoel4d.png")
                embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
                embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Nếu mọi người có chút lòng thành để ủng hộ và tạo động lực cho Darkie làm thêm chức năng mới, mini-game hoặc cải thiện bot, hoặc đẩy nhanh tiến độ dịch truyện, đăng truyện thì có thể donate một ít cafe nhé! Darkie **xin chân thành cảm ơn** rất rất nhiều!", inline=False)
                embed.add_field(name="", value=f"> ACB: 9799317", inline=False)
                embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
                embed.set_footer(text=f"Cảm ơn chân thành vì đã đọc, nếu tin nhắn này làm phiền mọi người thì xin hãy dùng lệnh\n!disable donation text.", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
                view = SelfDestructView(timeout=15)
                _mess = await message.channel.send(embed=embed, view=view)
                view.message= _mess
            
        elif message.guild.id != 1194106864582004849 and CustomFunctions.contains_substring(message.content.lower(), donate_disable):
            flag = True
            check_exist = db.find_guild_extra_info_by_id(message.guild.id)
            if check_exist:
                one_week_later = datetime.now() + timedelta(weeks=1)
                check_exist.disable_donation_text_until = one_week_later
                data_updated = {"disable_donation_text_until": check_exist.disable_donation_text_until}
                db.update_guild_extra_info(guild_id=message.guild.id, update_data= data_updated)
            else:
                one_week_later = datetime.now() + timedelta(weeks=2)
                data = GuildExtraInfo(guild_id=message.guild.id, guild_name= message.guild.name, allowed_ai_bot=True, disable_donation_text_until=one_week_later)
                db.insert_guild_extra_info(data)
            view = SelfDestructView(timeout=30)
            _mess = await message.channel.send(content=f"Xin lỗi vì đã làm phiền. Bot sẽ không tự động gửi embed kêu gọi donate trong vòng hai tuần tới. Nếu muốn ủng hộ thì đừng quên dùng lệnh `!donation` nhé", view=view)
            view.message= _mess
            
        return flag
    
    async def edit_embed_coin_flip(self, message: discord.Message, user: discord.Member):
        await asyncio.sleep(3)
        choice = random.randint(0,10)
        emoji_state = '<:coin_ngua:1287452465733570684>'
        state = 'ngửa'
        if choice > 0 and choice <=5:
            state = 'sấp'
            emoji_state = '<:coin_sap:1287452474952777750>'
        elif choice == 10:
            #Troll player
            response = CustomFunctions.get_random_response("OnCoinFlip.txt")
            embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã tung đồng xu. {response}", color=0x03F8FC)
            await message.edit(embed=embed_updated)
            return
        embed_updated = discord.Embed(title=f"", description=f"{user.mention} đã tung đồng xu. Đồng xu đã quay ra **`{state}`** {emoji_state}!", color=0x03F8FC)
        await message.edit(embed=embed_updated)
        if choice == 0:
            await asyncio.sleep(2)
            #Troll tập 2
            if state == 'ngửa':
                state = 'sấp'
                emoji_state = '<:coin_sap:1287452474952777750>'
            else:
                state = 'ngửa'
                emoji_state = '<:coin_ngua:1287452465733570684>'
            embed_updated = discord.Embed(title=f"", description=f"Đùa thôi. Đồng xu đã quay ra **`{state}`** {emoji_state}!", color=0x03F8FC)
            await message.edit(embed=embed_updated)
        
        check_quest_message = QuestMongoManager.increase_coin_flip_count(guild_id=message.guild.id, user_id=message.author.id)
        if check_quest_message == True:
            quest_embed = discord.Embed(title=f"", description=f"Bạn đã hoàn thành nhiệm vụ của mình và được nhận thưởng! Hãy dùng lại lệnh {SlashCommand.QUEST.value} để kiểm tra quest mới nha!", color=0xc379e0)
            await message.channel.send(embed=quest_embed, content=f"{message.author.mention}")
        return