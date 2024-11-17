
import Handling.Economy.Quest.QuestMongoManager as QuestMongoManager
import Handling.Economy.Profile.ProfileMongoManager as ProfileMongoManager
from CustomEnum.SlashEnum import SlashCommand 
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Economy.Profile.ProfileClass import Profile
import random

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
        elif total_wealth > -60000 and total_wealth < 0:
            text= "Đáy Xã Hội"
        elif total_wealth > -80000 and total_wealth <= -60000:
            text= "Rác Rưởi Tột Cùng"
        else:
            text = "Hạ Đẳng"
        return text
    
    @staticmethod
    def get_emoji_from_card_type(card_type: str):
        card_mapping = {
            "2C": EmojiCreation2.CARD_2_C.value,
            "2D": EmojiCreation2.CARD_2_D.value,
            "2H": EmojiCreation2.CARD_2_H.value,
            "2S": EmojiCreation2.CARD_2_S.value,
            "3C": EmojiCreation2.CARD_3_C.value,
            "3D": EmojiCreation2.CARD_3_D.value,
            "3H": EmojiCreation2.CARD_3_H.value,
            "3S": EmojiCreation2.CARD_3_S.value,
            "4C": EmojiCreation2.CARD_4_C.value,
            "4D": EmojiCreation2.CARD_4_D.value,
            "4H": EmojiCreation2.CARD_4_H.value,
            "4S": EmojiCreation2.CARD_4_S.value,
            "5C": EmojiCreation2.CARD_5_C.value,
            "5D": EmojiCreation2.CARD_5_D.value,
            "5H": EmojiCreation2.CARD_5_H.value,
            "5S": EmojiCreation2.CARD_5_S.value,
            "6C": EmojiCreation2.CARD_6_C.value,
            "6D": EmojiCreation2.CARD_6_D.value,
            "6H": EmojiCreation2.CARD_6_H.value,
            "6S": EmojiCreation2.CARD_6_S.value,
            "7C": EmojiCreation2.CARD_7_C.value,
            "7D": EmojiCreation2.CARD_7_D.value,
            "7H": EmojiCreation2.CARD_7_H.value,
            "7S": EmojiCreation2.CARD_7_S.value,
            "8C": EmojiCreation2.CARD_8_C.value,
            "8D": EmojiCreation2.CARD_8_D.value,
            "8H": EmojiCreation2.CARD_8_H.value,
            "8S": EmojiCreation2.CARD_8_S.value,
            "9C": EmojiCreation2.CARD_9_C.value,
            "9D": EmojiCreation2.CARD_9_D.value,
            "9H": EmojiCreation2.CARD_9_H.value,
            "9S": EmojiCreation2.CARD_9_S.value,
            "10C": EmojiCreation2.CARD_10_C.value,
            "10D": EmojiCreation2.CARD_10_D.value,
            "10H": EmojiCreation2.CARD_10_H.value,
            "10S": EmojiCreation2.CARD_10_S.value,
            "AC": EmojiCreation2.CARD_A_C.value,
            "AD": EmojiCreation2.CARD_A_D.value,
            "AH": EmojiCreation2.CARD_A_H.value,
            "AS": EmojiCreation2.CARD_A_S.value,
            "JC": EmojiCreation2.CARD_J_C.value,
            "JD": EmojiCreation2.CARD_J_D.value,
            "JH": EmojiCreation2.CARD_J_H.value,
            "JS": EmojiCreation2.CARD_J_S.value,
            "KC": EmojiCreation2.CARD_K_C.value,
            "KD": EmojiCreation2.CARD_K_D.value,
            "KH": EmojiCreation2.CARD_K_H.value,
            "KS": EmojiCreation2.CARD_K_S.value,
            "QC": EmojiCreation2.CARD_Q_C.value,
            "QD": EmojiCreation2.CARD_Q_D.value,
            "QH": EmojiCreation2.CARD_Q_H.value,
            "QS": EmojiCreation2.CARD_Q_S.value,
        }
        # Return the mapped value or a default value
        return card_mapping.get(card_type, EmojiCreation2.CARD_2_C.value)
    
    @staticmethod
    def get_chance(chance: int):
        rand_num = random.randint(0, 100)
        if rand_num < chance:
            return True
        else:
            return False
    
    @staticmethod
    def get_emoji_from_loai_tien(loai_tien:str):
        if loai_tien == "D": return EmojiCreation2.DARKIUM.value
        if loai_tien == "G": return EmojiCreation2.GOLD.value
        if loai_tien == "S": return EmojiCreation2.SILVER.value
        return EmojiCreation2.COPPER.value