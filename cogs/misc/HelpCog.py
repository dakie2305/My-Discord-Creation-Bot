from CustomEnum.SlashEnum import SlashCommand
from CustomEnum.EmojiEnum import EmojiCreation2, EmojiCreation1
from CustomEnum.RoleEnum import TrueHeavenRoleId
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import CustomFunctions
from Handling.Misc.SelfDestructView import SelfDestructView
from Handling.Misc.HelpPageView import HelpPageView
from typing import List, Optional, Dict
import random

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot=bot))
    print("Help command is ready!")

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.list_all_embed: list[discord.Embed] = []
        if bot.user.id == 1257305865124581416: # cr 1
            self.list_all_embed = self.get_list_help_creation_1()
        else: #cr 2
            self.list_all_embed = self.get_list_help_creation_2()
    
    #region keo_bua_bao command
    @discord.app_commands.command(name="help", description="Hiện danh sách lệnh của Bot!")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        first_embed = self.list_all_embed[0]
        first_embed.set_footer(text=f"Trang 1/{len(self.list_all_embed)}")
        view = HelpPageView(list_all_embed=self.list_all_embed)
        mess = await interaction.followup.send(embed=first_embed, view=view, ephemeral=False)
        view.message = mess
    
    #region creation 1
    def get_list_help_creation_1(self):
        list_embed = []
        
        #Menu
        embed = discord.Embed(title=f"Tổng Hợp Lệnh Creation 1", description=f"", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        count = 2
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp lệnh game nối từ.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp lệnh game đoán từ.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp lệnh lặt vặt.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Những thông tin hữu ích về bot Creation 1", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        #Game nối từ
        embed = discord.Embed(title=f"Lệnh Game Nối Từ", description=f"Áp dụng cho mini game Nối Từ", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!start_wm_en:` Bắt đầu một game nối từ tiếng Anh trong channel hiện tại. Dùng thêm một lần nữa để xoá trò chơi nối từ khỏi channel đó", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!start_wm_vn:` Bắt đầu một game nối từ tiếng Việt trong channel hiện tại. Dùng thêm một lần nữa để xoá.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!reset_wm:` reset channel nối từ để bắt đầu lại từ đầu.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!wm_give_skill <id_skill> <@user>` chỉ dành cho chủ Server. Lệnh dùng để đưa kỹ năng đặc biệt cho player trong channel nối từ.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!wm_remove_skill <id_skill|all|random> <@user>`: chỉ dành cho chủ Server. Lệnh dùng để xoá kỹ năng đặc biệt cho user trong channel nối từ. (Có thể dùng all, random để xoá tất cả hoặc xoá ngẫu nhiên kỹ năng của player)", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!wm_use_skill`: Lệnh dùng để hiển thị bảng kỹ năng đặc biệt của player trong channel nối từ và cách dùng kỹ năng đó.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!wm_give_ban <@user> 1`: Lệnh dùng để cấm một player không được chơi trong một round.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`/bxh_noi_tu`: Lệnh dùng để hiển thị bảng xếp hạng điểm của các player trong channel nối từ.", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        #Game đoán từ
        embed = discord.Embed(title=f"Lệnh Game Đoán Từ", description=f"Áp dụng cho mini game Đoán Từ", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!start_sw_en:` bắt đầu một game đoán từ tiếng Anh trong channel hiện tại. Dùng thêm một lần nữa để xoá.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!start_sw_vn:` bắt đầu một game đoán từ tiếng Việt trong channel hiện tại. Dùng thêm một lần nữa để xoá.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!reset_sw:`: reset channel game đoán từ hiện tại để bắt đầu lại từ đầu.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!sws_give_skill <id_skill> <@user>`: chỉ dành cho chủ Server. Lệnh dùng để đưa kỹ năng đặc biệt cho player trong channel đoán từ.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`!sws`: Lệnh dùng để hiển thị bảng kỹ năng đặc biệt của player trong channel đoán từ và cách dùng kỹ năng đó.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`/bxh_sw`: Lệnh dùng để hiển thị bảng xếp hạng điểm của các player trong channel game đoán từ.", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        #Misc
        embed = discord.Embed(title=f"Lệnh Lặt Vặt Khác", description=f"Những lệnh nhỏ lẻ, hữu ích của Bot!", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`/say`: Lệnh dùng để gửi tin nhắn, hình ảnh ẩn danh.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`/truth_dare`: Lệnh dùng để gửi tạo mới trò chơi Truth Or Dare.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`/snipe`: Lệnh dùng để hiển thị lại 7 tin nhắn bị xoá gần nhất trong channel dùng lệnh. Chỉ dùng được nếu có bot Creation 2 trong server!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value}`/therapy`: Lệnh dùng để thiết lập channel dùng để tâm sự cùng bot.", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        #Information
        embed = discord.Embed(title=f"Thông tin Khác", description=f"Thông tin về bot Creation 1!", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Creation 1 là một dự án Bot cá nhân do **Darkie** (darkiex_xx) phát triển cho vui. Nó có gắn kèm theo **chức năng AI** nhỏ vui vui, với tính cách khá ngang một xíu.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Kích hoạt AI của Creation 1 rất dễ, cứ gọi tên \"Creation 1\" trong tin nhắn, hoặc reply tin nhắn của bot là nó sẽ tự động trả lời bạn.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Bot Creation 1 có thể hoạt động độc lập, nhưng chỉ phát huy tốt tác dụng khi dùng kèm với bot Creation 2, em gái của nó.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation1.SHINY_POINT.value} Dự án bot Creations sẽ luôn được phát triển theo thời gian, và sẽ luôn có feature mới, và đảm bảo fix bug phát sinh!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        return list_embed
    
    #region creation 2
    def get_list_help_creation_2(self):
        
        list_embed = []
        #Menu
        embed = discord.Embed(title=f"Tổng Hợp Lệnh Creation 2", description=f"", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        count = 2
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp lệnh game cờ bạc.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp thông tin về Profile và cách kiếm tiền.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp thông tin về Bank.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp thông tin về Shop và Kho Đồ.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp lệnh Chính Quyền.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp thông tin về Chính Quyền.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp thông tin về Hộ Vệ Thần (Guardian Angel)", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp thông tin chiến đấu Hộ Vệ Thần (Guardian Angel Battle)", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Tổng hợp thông tin về hệ thống Cặp Đôi.", inline=False)
        count+=1
        embed.add_field(name=f"", value=f"- **Trang {count}**: Những thông tin hữu ích về bot Creation 2", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        #Game cờ bạc
        embed = discord.Embed(title=f"Lệnh Game Cờ Bạc", description=f"Các lệnh mini game cá độ bằng tiền Creation 2", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"**Những lệnh dưới đây đều có thể dùng tiền {EmojiCreation2.COPPER.value} | {EmojiCreation2.SILVER.value} | {EmojiCreation2.GOLD.value} để đặt cược để kiếm thêm tiền!**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/cf`: chơi game tung xu sấp hoặc ngửa.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/sb normal`: chơi game tài xỉu bình thường.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/sb double`: chơi game tài xỉu double để nhận phần thưởng to. Liều thì ăn nhiều!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/sb triple`: chơi game tài xỉu triple để nhận phần thưởng to hơn. Liều thì ăn nhiều!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/sb slot_machine`: chơi game Nổ Hũ để nhận phần thưởng.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/sb bai_cao`: tạo sòng bài cào để cùng người khác chơi một ván bài cào.", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"*Ai không biết chơi tài xỉu cứ nhắn câu \"tx help\" là bot sẽ hướng dẫn chơi nhé!*", inline=False)
        list_embed.append(embed)
        
        #Profile
        embed = discord.Embed(title=f"Lệnh kiếm tiền", description=f"Các lệnh về profile, work, daily...", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"**Những lệnh dưới đây đều dùng để kiếm thêm tiền {EmojiCreation2.COPPER.value} | {EmojiCreation2.SILVER.value} | {EmojiCreation2.GOLD.value} | {EmojiCreation2.DARKIUM.value} cho Profile bản thân!**", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/profile`: Kiểm tra profile, kho đồ của bản thân.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/work`: làm việc để kiếm tiền và nhân phẩm. Mỗi một tiếng được dùng lệnh một lần.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/daily`: điểm danh server để kiếm tiền và nhân phẩm. Mỗi một ngày được dùng lệnh một lần.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/crime`: làm việc xấu để kiếm tiền, nhưng sẽ mất điểm nhân phẩm. Mỗi một tiếng được dùng lệnh một lần.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/quest`: làm nhiệm vụ server để kiếm tiền. Hai ngày sẽ reset quest nếu không hoàn thành.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority riot`: bạo động chính quyền. Nếu thành công sẽ nhận được rất nhiều tiền! Mỗi một ngày được bạo động một lần.", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"*Cẩn thận đừng để Chính Quyền bắt khi dùng lệnh `/crime` hoặc `/authority riot` nhé!*", inline=False)
        list_embed.append(embed)
        
        #Bank
        embed = discord.Embed(title=f"Lệnh đổi tiền", description=f"", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/bank`: dùng để quy đổi tiền {EmojiCreation2.COPPER.value} | {EmojiCreation2.SILVER.value} | {EmojiCreation2.GOLD.value} | {EmojiCreation2.DARKIUM.value} theo tỷ giá hằng ngày!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}Tỷ giá bank sẽ thay đổi hằng ngày, hoặc được chính quyền reset!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"*Nếu không hiểu cơ chế bank hoạt động thì nhắn câu \"bank help\" nhé!*", inline=False)
        list_embed.append(embed)
        
        #Shop
        embed = discord.Embed(title=f"Lệnh mua đồ và dùng đồ", description=f"Các lệnh về shop, inventory...", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/shop global`: dùng tiền {EmojiCreation2.COPPER.value} | {EmojiCreation2.SILVER.value} | {EmojiCreation2.GOLD.value} | {EmojiCreation2.DARKIUM.value} để mua vật phẩm đặc biệt, với giá thay đổi hằng ngày!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}Tỷ giá shop sẽ thay đổi hằng ngày, hoặc được chính quyền reset!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/inventory use`: chọn vật phẩm cần dùng sau khi mua từ shop!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/inventory sell`: bán các vật phẩm để kiếm tiền!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        #Authority
        embed = discord.Embed(title=f"Lệnh Chính Quyền", description=f"Các lệnh dành cho Chính Quyền", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority vote`: bỏ tiền để bầu bản thân làm Chính Quyền server nếu server chưa tồn tại Chính Quyền!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority unjai`: huỷ giam lệnh của bất kỳ user nào!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority reset_rate`: cho phép Chính Quyền bỏ 10% tiền để reset lại tỷ giá của Shop, Bank!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority drop_random`: cho phép Chính Quyền bỏ chút tiền để tạo Hộp Quà Bí Ẩn, hoặc Hỏi Nhanh Có Thưởng!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority overthrow`: lật đổ Chính Quyền hiện tại! Chỉ dành cho chủ server hoặc Chính Quyền hiện tại! Phạt tiền cực nặng!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority investigate`: điều tra hành vi phạm tội của user khác! Nếu user đó đã dùng lệnh `/crime` trong một tiếng đổ lại thì người đó coi như sẽ bị bắt!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`/authority resign`: cho phép bỏ 10% tiền để từ chức trong yên bình sau khi nhậm chức hai tuần, vẫn sẽ giữ được mọi của cải!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value}`!um`: Lệnh dành riêng cho server owner. Cho phép cộng trừ tiền cho bất kỳ ai tuỳ thích!", inline=False)
        list_embed.append(embed)
        
        #Authority
        embed = discord.Embed(title=f"Thông tin về Chính Quyền", description=f"Đặc quyền cực mạnh dành cho Chính Quyền", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"**Ưu điểm:**", inline=False)
        embed.add_field(name=f"", value=f"- Chính Quyền sẽ hưởng 10% tiền thuế từ nhiều lệnh khác, tất cả tiền đều đổ vào túi Chính Quyền", inline=False)
        embed.add_field(name=f"", value=f"- Chính Quyền được miễn không phải đóng bất kỳ thuế gì", inline=False)
        embed.add_field(name=f"", value=f"- Chính Quyền được phép bắt giam tất cả user nếu phát hiện đang phạm tội", inline=False)
        embed.add_field(name=f"", value=f"- Chính Quyền được phép dùng các lệnh độc quyền dành riêng cho Chính Quyền", inline=False)
        embed.add_field(name=f"", value=f"- Chính Quyền sẽ được cộng rất nhiều tiền khi nhậm chức!", inline=False)
        embed.add_field(name=f"", value=f"**Nhược điểm:**", inline=False)
        embed.add_field(name=f"", value=f"- Hầu hết số tiền do user kiếm được đều lấy từ túi Chính Quyền!", inline=False)
        embed.add_field(name=f"", value=f"- Tỉ lệ `/crime` thành công tối đa chỉ dưới 40%!", inline=False)
        embed.add_field(name=f"", value=f"- Sẽ tự động sụp đổ khi Địa Vị xuống Trung Cấp, và phạt tiền cực nặng!", inline=False)
        embed.add_field(name=f"", value=f"- Chơi cờ bạc nếu thua sẽ mất trắng tiền!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        #Guardian
        embed = discord.Embed(title=f"Thông tin về Hộ Vệ Thần", description=f"Thông tin cơ bản về hệ thống Guardian Angel", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name="", value=f"- Bạn có thể mua một Hộ Vệ Thần trong lệnh {SlashCommand.SHOP_GUARDIAN.value}!", inline=False)
        embed.add_field(name="", value=f"- Ngoài ra còn có thể mua kỹ năng cho Hộ Vệ Thần trong lệnh {SlashCommand.SHOP_GUARDIAN_SKILL.value}!", inline=False)
        embed.add_field(name="", value=f"- Mỗi hộ vệ thần có các chỉ số chính: Máu, Thể Lực, Mana và Sức Tấn Công", inline=False)
        embed.add_field(name="", value=f"- Máu cao sẽ trụ được lâu, Thể Lực cao sẽ né được nhiều đòn, Mana cao sẽ tung được kỹ năng nhiều lần!", inline=False)
        embed.add_field(name="", value=f"- Đừng quên dùng lệnh {SlashCommand.GA_FEED.value}, {SlashCommand.GA_MEDITATE.value} hoặc mua bình hồi phục trong {SlashCommand.SHOP_GLOBAL.value} để hồi phục chỉ số!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        embed = discord.Embed(title=f"Cách chiến đấu Hộ Vệ Thần", description=f"Hướng dẫn dùng lệnh {SlashCommand.GA_BATTLE.value}", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name="", value=f"- Chiến đấu Hộ Vệ Thần là chiến đấu theo lượt, mỗi lượt thì hai bên sẽ tung đòn, né đòn hoặc sử dụng kỹ năng nếu có.", inline=False)
        embed.add_field(name="", value=f"- Ngoài ra, người khác có thể gia nhập cuộc chiến để đánh phụ với nhau, giúp nhau chiến thắng.", inline=False)
        embed.add_field(name="", value=f"- Nếu trong Kho Đồ của bạn có bình phục hồi máu, thể lực, mana thì Hộ Vệ Thần sẽ sử dụng trong lúc giao chiến.", inline=False)
        embed.add_field(name="", value=f"- Khi chọn thêm `target` tức là Hộ Vệ Thần của bạn sẽ đánh giao hữu với Hộ Vệ Thần của mục tiêu. Cả hai sẽ **không mất chỉ số, sẽ không chết vĩnh viễn** nếu thua. Coi như đánh vui thôi", inline=False)
        embed.add_field(name="", value=f"- Khi không chọn `target` tức là đánh với quái. Phần thưởng cao hơn, có khả năng lụm phần thưởng tốt, nhưng mọi chỉ số đã mất sẽ lưu lại, và tồn tại khả năng rất thấp là sẽ chết vĩnh viễn. Liều thì ăn nhiều", inline=False)
        embed.add_field(name="", value=f"- Chọn `max_players` để set mặc định bao nhiêu người đánh với nhau được, tối đa là 3 vs 3.", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        #Couple
        embed = discord.Embed(title=f"Thông tin về Couple", description=f"", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Cặp đôi có ba thông số cần quan tâm là **Điểm thân mật**, **Tình trạng cặp đôi**, **Tỉ lệ thăng hoa cảm xúc**!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **Điểm thân mật** và **Tỉ lệ thăng hoa cảm xúc** có thể tăng bằng lệnh `/couple fight` hoặc `/couple intimate` hoặc dùng lệnh `/gift` để tặng!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Khi **Tỉ lệ thăng hoa cảm xúc** đặt 100% thì sẽ tăng cấp của Tình trạng cặp đôi", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Khi **Tình trạng cặp đôi** đạt lên cấp 19 có thể dùng lệnh `/couple marry` để cưới nhau!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **Điểm thân mật**, **Tỉ lệ thăng hoa cảm xúc** sẽ trừ sau mỗi 12 tiếng!", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} **Quan trọng**: sẽ xoá cặp đôi nếu không tương tác, tăng điểm thân mật hoặc điểm tỉ lệ thăng hoa cảm xúc trong vòng 2 tuần!", inline=False)
        list_embed.append(embed)
        
        #Information
        embed = discord.Embed(title=f"Thông tin Khác", description=f"Thông tin về bot Creation 2!", color=0xddede7)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Creation 2 là một dự án Bot cá nhân do **Darkie** (darkiex_xx) phát triển. Nó có gắn kèm theo **chức năng AI** nhỏ vui vui, với tính cách nhỏ nhẹ, dễ thương một xíu.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Kích hoạt AI của Creation 2 rất dễ, cứ gọi tên \"Creation 2\" trong tin nhắn, hoặc reply tin nhắn của bot là nó sẽ tự động trả lời bạn.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Bot Creation 2 có thể hoạt động độc lập, nhưng chỉ phát huy tốt tác dụng khi dùng kèm với bot Creation 1, anh trai của nó.", inline=False)
        embed.add_field(name=f"", value=f"{EmojiCreation2.SHINY_POINT.value} Dự án bot Creations sẽ luôn được phát triển theo thời gian, và sẽ luôn có feature mới, và đảm bảo fix bug phát sinh!", inline=False)
        embed.add_field(name=f"", value="▬▬▬▬ι═════════>", inline=False)
        list_embed.append(embed)
        
        return list_embed
        
        