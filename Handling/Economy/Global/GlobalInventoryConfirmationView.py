import discord
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import CustomFunctions
from Handling.Economy.Global.GlobalProfileClass import GlobalProfile
from Handling.Economy.Global.ToGlobalInventoryView import ToGlobalInventoryView
from Handling.Economy.Global.ToServerInventoryView import ToServerInventoryView
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class GlobalInventoryConfirmationView(discord.ui.View):
    def __init__(self, user: discord.Member, user_profile: Profile, guild_id: int, global_inventory: GlobalProfile = None):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.user = user
        self.user_profile = user_profile
        self.guild_id = guild_id
        self.global_inventory = global_inventory
        if user_profile.list_items != None and len(user_profile.list_items) > 0:
            self.button_transfer_to_global = discord.ui.Button(label="Cá Nhân -> Liên Thông", style=discord.ButtonStyle.primary)
            self.button_transfer_to_global.callback = self.button_transfer_to_global_function
            self.add_item(self.button_transfer_to_global)
            
        if global_inventory != None and len(global_inventory.list_items) > 0:
            self.button_transfer_to_profile = discord.ui.Button(label="Liên Thông -> Cá Nhân", style=discord.ButtonStyle.blurple)
            self.button_transfer_to_profile.callback = self.button_transfer_to_profile_function
            self.add_item(self.button_transfer_to_profile)
        
    async def on_timeout(self):
        if self.message != None:
            try:
                await self.message.delete()
            except Exception:
                return

    async def button_transfer_to_global_function(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        #Phải xét đủ điều kiện mới cho phép đổi từ cá nhân sang global
        if interaction.guild.member_count < 1000 and interaction.guild_id != TrueHeavenEnum.TRUE_HEAVENS_SERVER_ID.value and not CustomFunctions.check_if_dev_mode():
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Server không đáp ứng điều kiện!", description="Cần phải đáp ứng một trong những điều kiện sau mới được phép chuyển từ profile sang liên thông server!",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            embed.add_field(name=f"", value="- Server phải ít nhất 1500 thành viên", inline=False)
            embed.add_field(name=f"", value="- Dùng lệnh tại server True Heaven ([Ấn Đây]( https://discord.gg/kKzyJAuccr))", inline=False)
            footer_text = f"Những điều kiện trên có thể thay đổi bất kỳ lúc nào, và tồn tại nhằm tránh tình trạng lạm dụng chức năng liên thông server!"
            embed.set_footer(text=footer_text)
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if self.user_profile.list_items == None or len(self.user_profile.list_items) == 0:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Kho đồ trống!", description="",color=discord.Color.blue())
            embed.add_field(name=f"", value="Bạn phải có vật phẩm trong kho đồ thì mới chuyển được", inline=False)
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        #Bật view chuyển sang global
        try:
            embed = discord.Embed(title=f"Chuyển Vào Kho Đồ Liên Thông!", description="Hãy chọn vật phẩm hiện tại mà bạn muốn chuyển vào Kho Đồ Liên Thông! ",color=discord.Color.blue())
            view = ToGlobalInventoryView(user=self.user, user_profile=self.user_profile, guild_id=self.guild_id, global_inventory=self.global_inventory)
            await self.message.edit(embed=embed, view=view)
        except Exception:
            pass
        return
    
    async def button_transfer_to_profile_function(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        #Chuyển đồ từ global sang cá nhân
        try:
            embed = discord.Embed(title=f"Chuyển Vào Kho Đồ Bình Thường!", description="Hãy chọn vật phẩm trong Kho Đồ Liên Thông mà bạn muốn chuyển vào server này! ",color=discord.Color.blue())
            view = ToServerInventoryView(user=self.user, guild_id=self.guild_id, global_inventory=self.global_inventory)
            await self.message.edit(embed=embed, view=view)
        except Exception as e:
            print(f"Error in button_transfer_to_profile_function: {e}")
            pass
        
        return
    