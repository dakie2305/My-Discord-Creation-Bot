import discord
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from  Handling.Economy.ConversionRate.ConversionRateClass import ConversionRate
import Handling.Economy.ConversionRate.ConversionRateMongoManager as ConversionRateMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from typing import List
from Handling.Economy.Inventory_Shop.ItemClass import Item

class GiftView(discord.ui.View):
    def __init__(self, user_profile: Profile, target_profile: Profile, user: discord.Member, target_user: discord.Member):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.user_profile = user_profile
        self.target_profile = target_profile
        self.user = user
        self.target_user = target_user
        self.add_item(ItemSelect(user, user_profile.list_items, self))
        self.selected_item: Item = None
        self.gift_button = discord.ui.Button(label="🎁 Tặng Quà", style=discord.ButtonStyle.green)
        self.gift_button.callback = self.gift_button_callback
        self.add_item(self.gift_button)

    async def on_timeout(self):
        if self.message != None: 
            await self.message.delete()
            return
        
    async def gift_button_callback(self, interaction: discord.Interaction):
        if self.selected_item == None: return
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(f'Bạn đã tặng quà cho {self.target_user.mention}', ephemeral=True)
        if self.message != None: 
            await self.message.delete()
        channel = interaction.channel
        embed = discord.Embed(title=f"", description=f"**{interaction.user.mention} đã tặng quà {self.selected_item.emoji} cho {self.target_user.mention}**", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        embed.add_field(name=f"", value=f"- Nhờ món quà [{self.selected_item.emoji} - **{self.selected_item.item_name}**] nên {self.target_user.mention} đã được cộng:", inline=False)
        if self.selected_item.bonus_exp != 0:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} {self.selected_item.bonus_exp} EXP", inline=False)
            ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=self.target_user.id, bonus_exp=self.selected_item.bonus_exp)
        if self.selected_item.bonus_dignity != 0:
            embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} {self.selected_item.bonus_dignity} Nhân Phẩm", inline=False)
            ProfileMongoManager.update_dignity_point(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.target_user.id, user_name=self.target_user.name, user_display_name=self.target_user.display_name, dignity_point=self.selected_item.bonus_dignity)
        embed.add_field(name=f"", value="▬▬▬▬ι══════════>", inline=False)
        
        #Cộng cho người đã tặng luôn
        ProfileMongoManager.update_level_progressing(guild_id=interaction.guild_id, user_id=self.user.id)
        #Cập nhật thời gian gift
        ProfileMongoManager.update_last_gift_now(guild_id=interaction.guild_id, user_id= self.user.id)
        #-1 vật phẩm
        ProfileMongoManager.update_list_items_profile(guild_id=interaction.guild_id, guild_name=interaction.guild.name, user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, item=self.selected_item, amount=-1)
        await channel.send(embed=embed, content=f"{self.target_user.mention}")
        return
        


class ItemSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_item: List[Item], view: "GiftView"):
        options = [
            discord.SelectOption(label=f"{item.item_name} (x{item.quantity})", description=item.item_description[:97] + '...', value=item.item_id)
            for item in list_item
        ]
        super().__init__(placeholder="Chọn vật phẩm muốn tặng...", options=options)
        self.list_item = list_item
        self.parent_view  = view
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        selected_item_id = self.values[0]
        selected_item = next(item for item in self.list_item if item.item_id == selected_item_id)
        self.parent_view.selected_item = selected_item
        await interaction.followup.send(f'Bạn đã chọn tặng vật phẩm {selected_item.emoji} - **{selected_item.item_name}**', ephemeral=True)
        
        
        
        
