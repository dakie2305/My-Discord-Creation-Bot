
import discord
from discord.ext import commands
import CustomFunctions
import asyncio
import random
from Handling.Misc.SelfDestructView import SelfDestructView

class AutoresponderHandling():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def handling_auto_responder(self, message: discord.Message):
        coin_flip = ["tung đồng xu", "sấp ngửa", "sấp hay ngửa", "ngửa hay sấp", "ngửa sấp", "tung xu"]
        conversion_rate = ["quy đổi coin", "quy đổi gold", "quy đổi silver", "quy đổi copper", "darkium"]
        quote = ["quote"]
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
            view = SelfDestructView(timeout=20)
            _mess = await message.channel.send(embed=embed, view=view)
            view.message= _mess
            flag = True
        elif CustomFunctions.contains_substring(message.content.lower(), quote):
            flag = True
            embed = discord.Embed(title=f"", description=f"Để thay đổi **Quote** trong lệnh </profile:1294699979058970656> thì hãy dùng lệnh:\n!quote \"Ghi quote vào đây\"", color=0xc379e0)
            view = SelfDestructView(timeout=20)
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
        return