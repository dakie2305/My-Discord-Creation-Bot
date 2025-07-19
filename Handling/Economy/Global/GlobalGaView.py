import discord
from CustomEnum.TrueHeavenEnum import TrueHeavenEnum
import CustomFunctions
from Handling.Economy.Global import GlobalMongoManager
from Handling.Economy.Global.GlobalProfileClass import GlobalProfile
from Handling.Economy.Global.ToGlobalInventoryView import ToGlobalInventoryView
from Handling.Economy.Global.ToServerInventoryView import ToServerInventoryView
from Handling.Economy.Profile.ProfileClass import Profile
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.UtilitiesFunctionsEconomy import UtilitiesFunctions

class GlobalGaView(discord.ui.View):
    def __init__(self, user: discord.Member, user_profile: Profile, guild_id: int, global_profile: GlobalProfile = None):
        super().__init__(timeout=120)
        self.message: discord.Message = None
        self.user = user
        self.user_profile = user_profile
        self.guild_id = guild_id
        self.global_profile = global_profile
        if user_profile.guardian != None:
            self.button_transfer_to_global = discord.ui.Button(label="Profile -> Global", style=discord.ButtonStyle.primary)
            self.button_transfer_to_global.callback = self.button_transfer_to_global_function
            self.add_item(self.button_transfer_to_global)
            
        if global_profile != None and global_profile.guardian != None:
            self.button_transfer_to_profile = discord.ui.Button(label="Global -> Profile", style=discord.ButtonStyle.blurple)
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
            embed = discord.Embed(title=f"Server không đáp ứng điều kiện!", description="Cần phải đáp ứng một trong những điều kiện sau mới được phép chuyển Hộ Vệ Thần từ profile sang global!",color=discord.Color.blue())
            embed.add_field(name=f"", value="▬▬▬▬ι════════>", inline=False)
            embed.add_field(name=f"", value="- Server phải ít nhất 1500 thành viên", inline=False)
            embed.add_field(name=f"", value="- Dùng lệnh tại server True Heaven (https://discord.gg/kKzyJAuccr)", inline=False)
            footer_text = f"Những điều kiện trên có thể thay đổi bất kỳ lúc nào, và tồn tại nhằm tránh tình trạng lạm dụng chức năng liên thông server!"
            embed.set_footer(text=footer_text)
            mess = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
            view.message = mess
            return
        
        if self.user_profile.guardian == None:
            view = SelfDestructView(timeout=30)
            embed = discord.Embed(title=f"Không có Hộ Vệ Thần!", description="",color=discord.Color.blue())
            embed.add_field(name=f"", value="Bạn phải có Hộ Vệ Thần thì mới chuyển được", inline=False)
            mess = await interaction.followup.send(embed=embed, view=view)
            view.message = mess
            return
        
        #Chuyển sang global
        try:
            GlobalMongoManager.transfer_guardian_global(user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, guild_id=self.guild_id, guild_name=interaction.guild.name, guardian=self.user_profile.guardian, transfer_to_global = True)
            embed = discord.Embed(title=f"Đồng Bộ Thành Công", description="",color=discord.Color.blue())
            embed.add_field(name=f"", value="Các chỉ số sức mạnh và kỹ năng Hộ Vệ Thần của bạn đã được đồng bộ liên thông!", inline=False)
            embed.add_field(name=f"", value=f"Có thể kiểm tra bằng cách dùng lệnh {SlashCommand.PROFILE.value} và chọn Hộ Vệ Thần rồi bấm Hộ Vệ Thần Liên Thông", inline=False)
            await self.message.edit(embed=embed, view=None)
        except Exception:
            pass
        return
    
    async def button_transfer_to_profile_function(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id: return
        await interaction.response.defer(ephemeral=False)
        #Chuyển đồ từ global sang cá nhân
        try:
            GlobalMongoManager.transfer_guardian_global(user_id=self.user.id, user_name=self.user.name, user_display_name=self.user.display_name, guild_id=self.guild_id, guild_name=interaction.guild.name, guardian=self.global_profile.guardian, transfer_to_global = False)
            embed = discord.Embed(title=f"Đồng Bộ Thành Công", description="",color=discord.Color.blue())
            embed.add_field(name=f"", value="Bạn đã lấy dữ liệu Hộ Vệ Thần Liên Thông về server hiện tại thành công!", inline=False)
            embed.add_field(name=f"", value=f"Có thể kiểm tra bằng cách dùng lệnh {SlashCommand.PROFILE.value} và chọn Hộ Vệ Thần", inline=False)
            await self.message.edit(embed=embed, view=None)
        except Exception as e:
            print(f"Error in button_transfer_to_profile_function in Global Ga View: {e}")
            pass
        return
    