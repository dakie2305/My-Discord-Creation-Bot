
from CustomEnum.SlashEnum import SlashCommand 
from CustomEnum.EmojiEnum import EmojiCreation2
from Handling.Economy.Profile.ProfileClass import Profile
import random
from datetime import datetime, timedelta, time
import os
import CustomFunctions as CustomFunctions

class UtilitiesFunctions():
    USER_NAME_MONGODB = CustomFunctions.USER_NAME_MONGODB
    PASSWORD_MONGODB = CustomFunctions.PASSWORD_MONGODB
    
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
        if total_wealth > 200025026000:
            text= "Đỉnh Cấp Xã Hội"
        elif total_wealth > 160250260000:
            text= "Giới Tinh Anh"
        elif total_wealth > 101025026000:
            text= "Phú Hào"
        elif total_wealth > 61025026000:
            text= "Giàu Nứt Vách"
        elif total_wealth > 41025026000:
            text= "Nhất Quan"
        elif total_wealth > 21025026000:
            text= "Quý Tộc"
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
    
    @staticmethod
    def check_if_within_time_delta(input: datetime, time_window: timedelta):
        now = datetime.now()
        if now - time_window <= input <= now + time_window:
            return True
        else:
            return False
    
    @staticmethod
    def is_within_time_range(from_time: time = time(2, 0), to_time: time = time(5, 0)):
        now = datetime.now().time()
        # Handle time range that does not cross midnight
        if from_time <= to_time:
            return from_time <= now <= to_time
        # Handle time range that crosses midnight
        return from_time <= now or now <= to_time
    
    @staticmethod
    def get_cap_do_quest(input: int):
        text = "Dễ"
        if input == 1:
            text = "Dễ"
        elif input == 2:
            text = "Vừa Phải"
        elif input == 3:
            text = "Khó"
        elif input == 4:
            text = "Huyền Thoại"
        return text
    
    @staticmethod
    def get_heart_emoji_on_rank(rank: int):
        text = "💘"
        if rank >= 20:
            text= "❤️‍🔥"
        elif rank == 19:
            text= "💝"
        elif rank == 18:
            text= "💓"
        elif rank == 17:
            text= "💗"
        elif rank == 16:
            text= "💞"
        elif rank == 15:
            text= "💕"
        elif rank == 14:
            text= "💖"
        elif rank == 13:
            text= "❣️"
        elif rank == 12:
            text= "❤️"
        elif rank == 11:
            text= "🩷"
        elif rank == 10:
            text= "🧡"
        elif rank == 9:
            text= "💛"
        elif rank == 8:
            text= "💚"
        elif rank == 7:
            text= "🩵"
        elif rank == 6:
            text= "💙"
        elif rank == 5:
            text= "💜"
        elif rank == 4:
            text= "🤍"
        elif rank == 3:
            text= "🩶"
        elif rank == 2:
            text= "🖤"
        elif rank == 1:
            text= "💘"
        return text
    
    @staticmethod
    def get_text_on_love_rank(rank: int):
        text = "Mới Quen"
        if rank >= 20:
            text= "Bạn Đời Vĩnh Cữu"
        elif rank >= 19:
            text= "Đôi Tri Kỉ"
        elif rank >= 16:
            text= "Đôi Uyên Ương"
        elif rank >= 12:
            text= "Tri Kỷ Tâm Giao"
        elif rank >= 10:
            text= "Nửa Kia Hoàn Hảo"
        elif rank >= 10:
            text= "Tâm Đầu Ý Hợp"
        elif rank >= 8:
            text= "Nhạc Sĩ Mộng Mơ Và Nàng Thơ"
        elif rank >= 6:
            text= "Người Yêu"
        elif rank >= 4:
            text= "Người Tình"
        elif rank >= 2:
            text= "Tình Chớm Nở"
        return text
    
    @staticmethod
    def progress_bar_plant(start_time: datetime, end_time: datetime, bar_length: int = 15) -> str:
        now = datetime.now()
        
        if start_time > end_time:
            bar = "█" * bar_length
            return f"{bar} 100%"
        
        if datetime.now() > end_time:
            bar = "█" * bar_length
            return f"{bar} 100%"
        
        total_duration = (end_time - start_time).total_seconds()
        elapsed_time = (now - start_time).total_seconds()
        
        # Ensure progress is within bounds (0 to 100%)
        progress_percentage = max(0, min(100, (elapsed_time / total_duration) * 100))
        
        # Calculate the number of "filled" blocks in the bar
        filled_length = int(bar_length * (progress_percentage / 100))
        empty_length = bar_length - filled_length
        
        # Create the bar
        bar = "█" * filled_length + "░" * empty_length
        return f"{bar} {progress_percentage:.0f}%"
    
    @staticmethod
    def get_text_on_guardian_level(level: int):
        text = "Tân Binh"
        if level >= 120:
            text= "Thượng Cổ Đại Thần"
        elif level >= 100:
            text= "Vệ Chiến Thần"
        elif level >= 95:
            text= "Thiên Tử"
        elif level >= 90:
            text= "Tử Thần"
        elif level >= 80:
            text= "Bất Diệt Chiến Đế"
        elif level >= 80:
            text= "Đại Chiến Tôn"
        elif level >= 70:
            text= "Chúa Tể"
        elif level >= 60:
            text= "Đại Hộ Vệ"
        elif level >= 50:
            text= "Lãnh Quản Chiến Khí"
        elif level >= 40:
            text= "Thống Lãnh"
        elif level >= 30:
            text= "Tư Lệnh"
        elif level >= 25:
            text= "Tướng Quân"
        elif level >= 20:
            text= "Chỉ Huy"
        elif level >= 15:
            text= "Tinh Anh"
        elif level >= 10:
            text= "Dị Nhân"
        elif level >= 5:
            text= "Đấu Sĩ"
        return text
    
    @staticmethod
    def progress_bar(input_value: int, total_progress: int = 1000, bar_length=15):
        # Calculate the percentage of progress
        percentage = (input_value / total_progress) * 100
        # Determine the number of filled (█) characters
        filled_length = int(bar_length * input_value // total_progress)
        # Create the progress bar string
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        # Format the output with percentage
        return f'{bar} **{int(percentage)}%**'

    @staticmethod
    def progress_bar_stat(input_value: int, max_value: int, emoji: str, bar_length=15):
        # Calculate the percentage of progress
        percentage = (input_value / max_value) * 100
        # Determine the number of filled (█) characters
        filled_length = int(bar_length * input_value // max_value)
        # Create the progress bar string
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        # Format the output with percentage
        return f'{emoji}: {bar} ({input_value}/{max_value})'

    @staticmethod
    def get_chance_guardian_actual_death(level: int):
        chance = 0
        if level <= 25: chance = 1
        if level > 25 and level < 50: chance = 9
        if level >= 50 and level < 75: chance = 8
        if level >= 75 and level < 99: chance = 6
        else: chance = 5
        return chance