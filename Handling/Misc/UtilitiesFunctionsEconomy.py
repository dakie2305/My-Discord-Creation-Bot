
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Economy.Profile.ProfileClass import Profile

class UtilitiesFunctions():
    @staticmethod
    def shortened_currency(number: int):
        if number >= 1000000000:
            suffix = int(number % 1000000000 // 1000000)
            if suffix == 0: suffix = "" 
            return f"{int(number // 1000000000)}B{suffix}"
        elif number >= 1000000:
            suffix = int(number % 1000000 // 1000)
            if suffix == 0: suffix = "" 
            return f"{int(number // 1000000)}M{suffix}"
        elif number >= 10000:
            suffix = int(number % 1000 // 100)
            if suffix == 0: suffix = ""
            return f"{int(number // 1000)}K{suffix}"  
        else:
            return str(int(number))
    
    @staticmethod
    def get_nhan_pham(number: int):
        text = "Người Thường"
        if number >= 100:
            text = "Thánh Nhân"
        elif number >= 75:
            text = "Người Tốt"
        elif number >= 60:
            text = "Lành tính"
        elif number >= 50:
            text = "Người Thường"
        elif number >= 40:
            text = "Tiểu Nhân"
        elif number >= 30:
            text = "Quỷ Quyệt"
        elif number >= 20:
            text = "Tội Phạm"
        else:
            text = "Gian Thương Tà Đạo"
        return text
    
    @staticmethod
    def get_dia_vi(data: Profile):
        text = "Hạ Đẳng"
        total_wealth = data.copper + data.silver *5000 + data.gold * 5000 * 5000 + data.darkium * 5000 * 5000 * 10000
        if total_wealth > 20025026000:
            text= "Đỉnh Cấp Xã Hội"
        elif total_wealth > 16025026000:
            text= "Giới Tinh Anh"
        elif total_wealth > 11025026000:
            text= "Thượng Đẳng"
        elif total_wealth > 8525026000:
            text= "Thượng Lưu"
        elif total_wealth > 2205026000:
            text= "Thượng Lưu"
        elif total_wealth > 75026000:
            text= "Trung Lưu"
        elif total_wealth > 20000000:
            text= "Hạ Lưu"
        else:
            text = "Hạ Đẳng"
        return text
        