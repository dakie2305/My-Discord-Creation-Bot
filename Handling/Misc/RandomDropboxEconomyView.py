import discord
from discord.ui import Button, View
from Handling.Economy.Profile import ProfileMongoManager
from Handling.Economy.Profile.ProfileClass import Profile
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Misc.SelfDestructView import SelfDestructView
import random

class RandomDropboxEconomyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.old_message: discord.Message = None
        self.opened = False
        
    @discord.ui.button(label="Mở Hộp Quà 🎁", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: Button):
        if self.opened == True: return
        await interaction.response.defer(ephemeral=True)
        if self.old_message != None: await self.old_message.delete()
        self.opened = True
        
        #2% - trừ nhân phẩm. Còn lại gold 10%, silver 35%, exp 30%, dignity 35%, còn lại sẽ drop copper
        amount = random.randint(2500, 25000)
        emoji = EmojiCreation2.COPPER.value
        flag = False
        minus_dignity = self.get_chance(2)
        if minus_dignity and flag == False: 
            emoji = "Nhân Phẩm"
            amount = random.randint(-2, -15)
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, dignity_point=amount)
            flag = True
            
        gold_chance = self.get_chance(10)
        if gold_chance and flag == False: 
            emoji = EmojiCreation2.GOLD.value
            amount = random.randint(1, 8)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, gold=amount)
            flag = True
            
        silver_chance = self.get_chance(35)
        if silver_chance and flag == False: 
            emoji = EmojiCreation2.SILVER.value
            amount = random.randint(5, 35)
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, silver=amount)
            flag = True
            
        exp_chance = self.get_chance(35)
        if exp_chance and flag == False: 
            emoji = "Điểm Kinh Nghiệm"
            amount = random.randint(1, 30)
            flag = True
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=interaction.user.id, bonus_exp=amount)
            
            
        dignity_chance = self.get_chance(35)
        if dignity_chance and flag == False: 
            emoji = "Nhân Phẩm"
            amount = random.randint(5, 50)
            flag = True
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, dignity_point=amount)
        
        if flag == False:
            #Cộng copper
            ProfileMongoManager.update_profile_money(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=interaction.user.id, user_display_name=interaction.user.display_name, user_name=interaction.user.name, copper=amount)
        
        embed = discord.Embed(title=f"", description=f"{EmojiCreation2.GOLDEN_GIFT_BOX.value} **Hộp Quà Thần Bí** {EmojiCreation2.GOLDEN_GIFT_BOX.value}", color=0x0ce7f2)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Một hộp quà thần bí đã xuất hiện tại đúng channel này! {interaction.user.mention} đã nhanh tay chộp được hộp quà và mở nó và nhận được:", inline=False)
        embed.add_field(name=f"", value=f"> {EmojiCreation2.GOLDEN_GIFT_BOX.value}: **{amount}** {emoji}", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.set_footer(text=f"Hộp quà sẽ xuất hiện ngẫu nhiên, và khi thấy thì nhớ nhanh tay nhé!", icon_url="https://cdn.discordapp.com/icons/1256987900277690470/8fd7278827dbc92713e315ee03e0b502.webp?size=32")
        
        await interaction.followup.send(f"Bạn đã nhận hộp quà!",ephemeral=True)
        called_channel = interaction.channel
        await called_channel.send(embed=embed, view= None)
        return
    
    async def on_timeout(self):
        if self.opened == False:
            await self.old_message.delete()
    
    
    def get_chance(self, chance: int):
        rand_num = random.randint(0, 100)
        if rand_num < chance:
            return True
        else:
            return False