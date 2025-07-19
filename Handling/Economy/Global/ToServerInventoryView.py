from typing import List
import discord
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
from Handling.Economy.Global import GlobalMongoManager
from Handling.Economy.Global.GlobalProfileClass import GlobalProfile
from Handling.Economy.Inventory_Shop.ItemClass import Item
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class ToServerInventoryView(discord.ui.View):
    def __init__(self, user: discord.Member, guild_id: int, global_inventory: GlobalProfile = None):
        super().__init__(timeout=30)
        self.message: discord.Message = None
        self.user = user
        self.guild_id = guild_id
        self.global_inventory = global_inventory
        self.button_transfer_to_global = discord.ui.Button(label="Chuyển Vào Kho Cá Nhân", style=discord.ButtonStyle.primary)
        self.button_transfer_to_global.callback = self.button_transfer_function
        self.add_item(ItemSelect(user, global_inventory.list_items, self))
        self.add_item(self.button_transfer_to_global)
        self.selected_item: Item = None
        
    async def on_timeout(self):
        if self.message != None:
            try:
                await self.message.delete()
            except Exception:
                return
            

    async def button_transfer_function(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        if self.selected_item == None: return
        await interaction.response.defer(ephemeral=False)
        #Kiểm tra xem item đó còn không
        global_inventory = GlobalMongoManager.find_global_profile_by_id(user_id=interaction.user.id)
        check_fail = True
        for player_item in global_inventory.list_items:
            if player_item.item_id == self.selected_item.item_id and player_item.quantity > 0:
                check_fail = False
                break
        if check_fail:
            await interaction.channel.send(f'{interaction.user.mention} Vật phẩm {self.selected_item.emoji} - **{self.selected_item.item_name}** đã không còn trong Kho Đồ Liên Thông của bạn!')
            return
        #Chuyển vào kho đồ server
        GlobalMongoManager.transfer_item_global(user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, guild_id=interaction.guild_id, guild_name=interaction.guild.name, item=self.selected_item, transfer_to_global=False)
        embed = discord.Embed(title=f"Chuyển thành công", description="",color=discord.Color.blue())
        embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
        embed.add_field(name=f"", value=f"Bạn đã chuyển thành công vật phẩm {self.selected_item.emoji} - **{self.selected_item.item_name}** và kho đồ cá nhân. Hãy kiểm tra bằng lệnh {SlashCommand.PROFILE.value} và chọn kho đồ", inline=False)
        footer_text = f"Kho đồ liên thông sẽ tự động xóa dữ liệu của bạn sau sáu tháng không hoạt động!"
        embed.set_footer(text=footer_text)
        mess = await interaction.followup.send(content=f"{interaction.user.mention}", embed=embed)
        return
    
class ItemSelect(discord.ui.Select):
    def __init__(self, user: discord.Member, list_item: List[Item], view: "ToServerInventoryView"):
        seen_item_ids = set()
        options = []

        for item in list_item:
            if item.item_id in seen_item_ids:
                continue
            seen_item_ids.add(item.item_id)
            options.append(
                discord.SelectOption(
                    label=f"{item.item_name} (x{item.quantity})",
                    description=(item.item_description[:97] + '...'),
                    value=item.item_id
                )
            )
        super().__init__(placeholder="Chọn vật phẩm muốn chuyển", options=options)
        self.list_item = list_item
        self.parent_view = view
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=True)
        selected_item_id = self.values[0]
        selected_item = next(item for item in self.list_item if item.item_id == selected_item_id)
        self.parent_view.selected_item = selected_item
        await interaction.followup.send(f'Bạn đã chọn vật phẩm {selected_item.emoji} - **{selected_item.item_name}**', ephemeral=True)

