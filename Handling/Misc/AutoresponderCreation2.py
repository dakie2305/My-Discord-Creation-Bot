
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
from db.DbMongoManager import GuildExtraInfo
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
        
        
        sb_help = ["sb help","cách chơi tài xỉu", "tài xỉu?", "tx help"]
        legend_weapon = ["thất truyền huyền khí"]
        ga_help = ["ga help", "guardian help", "hộ vệ thần?", "guardian help"]
        gd_help = ["gd help", "dungeon help"]
        global_help = ["global help", "global?"]
        gc_help = ["gc help", "challenge help", "ga challenge"]

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

        elif CustomFunctions.contains_substring(message.content.lower(), gd_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn Hầm Ngục Hộ Vệ Thần", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"- Dùng lệnh {SlashCommand.QUEST_DUNGEON.value} để xem danh sách hầm ngục trong Server. Nếu là Server Owner thì sẽ chọn một kênh làm Hầm Ngục (Chỉ Dành Cho Owner Server).", inline=False)
            embed.add_field(name="", value=f"- Ở kênh này, mỗi 15 phút thì sẽ tạo ra một con quái có cấp độ tương ứng với độ khó của Hầm Ngục!", inline=False)
            embed.add_field(name="", value=f"- Bất kỳ ai có Hộ Vệ Thần đều có thể chiến đấu, giống như {SlashCommand.GA_BATTLE.value}!", inline=False)
            embed.add_field(name="", value=f"- Quái từ Hầm Ngục có độ khó **Khó** và **Huyền Thoại** sẽ có cấp độ mạnh tương đương với Hộ Vệ Thần!", inline=False)
            embed.add_field(name="", value=f"- Quái từ Hầm Ngục có độ khó **Khó** và **Huyền Thoại** sẽ có thể bắt ngẫu nhiên bất kỳ ai trong channel!", inline=False)
            embed.add_field(name="", value=f"- Phần thưởng trong chiến đấu Hầm Ngục sẽ cao hơn {SlashCommand.GA_BATTLE.value}!", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.set_footer(text=f"Đừng quên mỗi Hộ Vệ Thần có tỉ lệ chết vĩnh viễn nếu để trọng thương khi đánh với quái nhé! Tỉ lệ rất thấp, nhưng đừng khinh suất!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
        
        elif CustomFunctions.contains_substring(message.content.lower(), gc_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn Thách Đấu Hộ Vệ Thần", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"- Dùng lệnh {SlashCommand.GA_CHALLENGE.value} để thách đấu Hộ Vệ Thần của đối phương (PVP).", inline=False)
            embed.add_field(name="", value=f"- Ở Thách Đấu không có giới hạn thời gian chiến đấu, nhưng cũng sẽ không hưởng bất kỳ phần thưởng nào hết!", inline=False)
            embed.add_field(name="", value=f"- Khi thách đấu, có thể đặt cược tiền, người thắng sẽ nhận được 95% số tiền cược của kẻ thua cuộc!", inline=False)
            embed.add_field(name="", value=f"- Khi thách đấu, có thể chọn hình thức chiến đấu khác nhau nếu muốn!", inline=False)
            embed.add_field(name="", value=f"- Mọi chỉ số Hộ Vệ Thần đều sẽ lưu lại sau mỗi trận chiến! Chỉ một bên ngã xuống thì mới dừng lại!", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.set_footer(text=f"Đừng quên mỗi Hộ Vệ Thần có tỉ lệ chết vĩnh viễn nếu để trọng thương khi Thách Đấu nhé! Tỉ lệ rất thấp, nhưng đừng khinh suất!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
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
            
        elif CustomFunctions.contains_substring(message.content.lower(), global_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Giải thích và hướng dẫn chức năng **Liên Thông**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Kho Đồ Liên Thông tức là kho đồ chung, bạn có thể truy cập từ bất kỳ server nào! Khi đủ điều kiện liên thông thì bạn có thể bỏ vào tối đa **10** vật phẩm từ kho đồ cá nhân để đem sang server khác", inline=False)
            embed.add_field(name="", value=f"- {EmojiCreation2.SHINY_POINT.value} Cần mua Thẻ Liên Thông trong lệnh {SlashCommand.SHOP_GLOBAL.value} để mở khóa chức năng Liên Thông trong vòng **hai tuần.**", inline=False)
            embed.add_field(name="", value=f"- {EmojiCreation2.SHINY_POINT.value} Sau **6** tháng không sử dụng chức năng Liên Thông thì Kho Đồ Liên Thông sẽ bị xóa!", inline=False)
            embed.add_field(name="", value=f"- {EmojiCreation2.SHINY_POINT.value} Để được phép bỏ vật phẩm từ kho đồ server vào Kho Đồ Liên Thông, cần phải đáp ứng điều kiện: server trên 1000 người, hoặc dùng lệnh trong server True Heavens!", inline=False)
            embed.add_field(name="", value=f"- {EmojiCreation2.SHINY_POINT.value} Yêu cầu như thế là để tránh tình trạng đưa bot vào server cá nhân và lạm dụng chức năng Liên Thông!", inline=False)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.set_footer(text=f"{EmojiCreation2.SHINY_POINT.value} Lưu ý, vật phẩm đã liên thông sẽ mất tất cả giá trị bán ra, nên tốt nhất đừng mơ đến chuyện đem ra server khác bán!", icon_url=f"{EmojiCreation2.TRUE_HEAVEN_LINK_MINI.value}")
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