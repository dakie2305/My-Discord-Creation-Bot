
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
        coin_flip = ["tung đồng xu", "sấp ngửa", "sấp hay ngửa", "ngửa hay sấp", "ngửa sấp", "tung xu"]
        conversion_rate = ["quy đổi coin", "quy đổi gold", "quy đổi silver", "quy đổi copper", "quy đổi darkium", "quy đổi tiền tệ"]
        quote = ["quote"]
        bank_help = ["bank help", "bank sao", "bank?"]
        
        dignity_help = ["tăng nhân phẩm", "điểm nhân phẩm", "nhân phẩm là gì", "nhân phẩm?"]
        dia_vi_help = ["tăng địa vị", "điểm địa vị", "địa vị là gì", "địa vị?"]
        
        bbb_warning = ["bbb", "BBB"]
        
        flag = False
        if message.author.bot: return flag
        
        if CustomFunctions.contains_substring(message.content.lower(), coin_flip):
            #Tung đồng xu
            embed = discord.Embed(title=f"", description=f"{message.author.mention} đã tung đồng xu. Đồng xu đang quay <a:doge_coin:1287452452827697276> ...", color=0x03F8FC)
            mess_coin = await message.reply(embed=embed)
            if mess_coin:
                await self.edit_embed_coin_flip(message=mess_coin, user=message.author)
            flag = True
            
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
        elif CustomFunctions.contains_substring(message.content.lower(), quote):
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
            embed.set_footer(text=f"Tỉ lệ quy đổi sẽ thay đổi theo mỗi ngày hoặc do Chính Quyền ép thay đổi nha!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
            view = SelfDestructView(timeout=180)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
        
        elif CustomFunctions.contains_substring(message.content.lower(), dignity_help):
            flag = True
            embed = discord.Embed(title=f"", description=f"Hướng dẫn **Diểm nhân phẩm**", color=0xc379e0)
            embed.add_field(name="", value="-------------------------------------", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Điểm nhân phẩm sẽ quyết định rất nhiều điều, về số tiền bạn kiếm được, về kinh nghiệm bạn kiếm được... và sẽ tác động đến những lệnh khác mà cần tốn tiền.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Điểm nhân phẩm càng thấp thì nhân phẩm bạn sẽ thấp và có thể gặp bất lợi, nhưng đồng thời cũng có lợi ở đôi chỗ khác như {SlashCommand.WORK.value} thì có thể trốn thuế nhiều hơn.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Để tăng nhân phẩm thì chỉ cần dùng những lệnh cơ bản như {SlashCommand.WORK.value}, {SlashCommand.DAILY.value} là được.", inline=False)
            embed.add_field(name="", value=f"{EmojiCreation2.SHINY_POINT.value} Nhân phẩm sẽ giảm khi bạn bạo động, hoặc khi chơi các mini game cờ bạc nhưng để bị thua.", inline=False)
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
            
        elif CustomFunctions.contains_substring(message.content.lower(), bbb_warning) and message.channel.id != 1297787832986767381 and message.guild.id == 1256987900277690470:
            flag = True
            view = SelfDestructView(timeout=5)
            _mess = await message.channel.send(content=f"Shhhhh... We do not talk about this topic here.", view=view)
            view.message= _mess
            await message.delete()
        
        elif message.guild.id == 1256987900277690470 and len(message.author.roles) == 1 and message.author.roles[0].is_default():
            flag = True
            view = SelfDestructView(timeout=30)
            _mess = await message.reply(content=f"Hey, <#1257002970529267774> <- ?", view=view)
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