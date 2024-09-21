from typing import List, Optional
from datetime import datetime, timedelta

#region WordMatchingInfo
class WordMatchingInfo:
    def __init__(self, channel_id: int, channel_name: str, current_player_id: int = None, current_player_name: str = None, current_word: str = None, first_character: str = None, last_character: str = None, special_point: int = None, special_item: Optional['SpecialItem'] = None, remaining_word: int = None, used_words: List[str] = None, player_profiles: Optional[List['PlayerProfile']] = None, player_effects : Optional[List['PlayerEffect']] = None, player_bans : Optional[List['PlayerBan']] = None):
        self.channel_id = channel_id 
        self.channel_name = channel_name
        self.current_player_id = current_player_id
        self.current_player_name = current_player_name
        self.current_word = current_word
        self.first_character = first_character
        self.last_character = last_character
        self.remaining_word = remaining_word
        self.special_point = special_point
        self.used_words: List[str] = used_words if used_words else []
        self.special_item: SpecialItem = special_item if special_item else None
        self.player_profiles: List[PlayerProfile] = player_profiles if player_profiles else []
        self.player_effects: List[PlayerEffect] = player_effects if player_effects else []
        self.player_bans: List[PlayerBan] = player_bans if player_bans else []
    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "current_player_id": self.current_player_id,
            "current_player_name": self.current_player_name,
            "current_word": self.current_word,
            "first_character": self.first_character,
            "last_character": self.last_character,
            "remaining_word": self.remaining_word,
            "special_point": self.special_point,
            "used_words": [data for data in self.used_words],
            "special_item": self.special_item.to_dict() if self.special_item else None,
            "player_profiles": [data.to_dict() for data in self.player_profiles],
            "player_effects": [data.to_dict() for data in self.player_effects],
            "player_bans": [data.to_dict() for data in self.player_bans],
        }

    @staticmethod
    def from_dict(data:dict):
        return WordMatchingInfo(
            channel_id=data["channel_id"],
            channel_name=data["channel_name"],
            current_player_id = data["current_player_id"],
            current_player_name = data["current_player_name"],
            current_word = data["current_word"],
            first_character = data["first_character"],
            last_character = data["last_character"],
            remaining_word = data["remaining_word"],
            special_point= data["special_point"],
            used_words = data["used_words"],
            special_item = SpecialItem.from_dict(data.get("special_item", None)) if data.get("special_item") else None,
            player_profiles = [PlayerProfile.from_dict(item) for item in data.get("player_profiles", [])],
            player_effects = [PlayerEffect.from_dict(item) for item in data.get("player_effects", [])],
            player_bans = [PlayerBan.from_dict(item) for item in data.get("player_bans", [])]
        )


#region PlayerProfile
class PlayerProfile:
    def __init__(self, user_id: int, username: str, user_display_name: str, points: int = 0, special_items: Optional[List['SpecialItem']] = None):
        self.user_id = user_id 
        self.username = username
        self.user_display_name = user_display_name
        self.points = points
        self.special_items: List[SpecialItem] = special_items if special_items else []
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "user_display_name": self.user_display_name,
            "points": self.points,
            "special_items": [data.to_dict() for data in self.special_items],
        }

    @staticmethod
    def from_dict(data:dict):
        return PlayerProfile(
            user_id=data["user_id"],
            username=data["username"],
            user_display_name = data["user_display_name"],
            points = data["points"],
            special_items = [SpecialItem.from_dict(item) for item in data.get("special_items", [])]
        )
        
#region SpecialItem
class SpecialItem:
    def __init__(self, item_id: str, item_name: str, item_description: str, level: str, quantity: int, point:int, required_target: bool):
        self.item_id = item_id 
        self.item_name = item_name
        self.item_description = item_description
        self.required_target = required_target
        self.quantity = quantity
        self.point = point
        self.level = level
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "item_description": self.item_description,
            "quantity": self.quantity,
            "point": self.point,
            "level": self.level,
            "required_target": self.required_target
        }

    @staticmethod
    def from_dict(data:dict):
        return SpecialItem(
            item_id=data["item_id"],
            item_name=data["item_name"],
            item_description = data["item_description"],
            quantity = data["quantity"],
            point = data["point"],
            level = data["level"],
            required_target = data["required_target"]
        )

#region Player Effect
class PlayerEffect:
    def __init__(self, user_id: int, username: str, effect_id: str, effect_name: str):
        self.user_id = user_id 
        self.username = username
        self.effect_id = effect_id
        self.effect_name = effect_name
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "effect_id": self.effect_id,
            "effect_name": self.effect_name,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return PlayerEffect(
            user_id=data.get("user_id", None),
            username=data.get("username", None),
            effect_id = data.get("effect_id", None),
            effect_name = data.get("effect_name", None),
        )

#region Player Ban
class PlayerBan:
    def __init__(self, user_id: int, username: str, ban_remaining: int):
        self.user_id = user_id 
        self.username = username
        self.ban_remaining = ban_remaining
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "ban_remaining": self.ban_remaining,
        }
        
    @staticmethod
    def from_dict(data:dict):
        return PlayerBan(
            user_id=data.get("user_id", None),
            username=data.get("username", None),
            ban_remaining = data.get("ban_remaining", None),
        )

list_special_items_cap_thap = [
    SpecialItem(
        item_id="ct_minus",
        item_name="Trừ Điểm Của Đối Phương",
        item_description="Kỹ năng này sẽ trừ đi 2 điểm của đối thủ trong trò chơi nối chữ, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_minus <@315835396305059840>**",
        quantity = 1,
        point =2,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_add",
        item_name="Cộng Điểm Bản Thân",
        item_description="Kỹ năng này sẽ cộng cho bản thân 2 điểm trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_add**",
        quantity = 1,
        point =2,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_hint",
        item_name="Gợi Ý Nửa Từ",
        item_description="Kỹ năng này sẽ gợi ý một nửa từ cần thiết để hoàn thành lượt chơi nối chữ hiện tại. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_hint**",
        quantity = 1,
        point =0,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_minus_first",
        item_name="Trừ Điểm Top 1",
        item_description="Kỹ năng này sẽ trừ 10 điểm của player top 1 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_minus_first**",
        quantity = 1,
        point=10,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_minus_second",
        item_name="Trừ Điểm Top 2",
        item_description="Kỹ năng này sẽ trừ 8 điểm của player top 2 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_minus_second**",
        quantity = 1,
        point=8,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_add_user",
        item_name="Cộng Điểm Đối Phương",
        item_description="Kỹ năng này sẽ cộng 2 điểm cho đối phương bất kỳ ngoại trừ bản thân, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_add_user <@315835396305059840>**",
        quantity = 1,
        point=2,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_allow",
        item_name="Cho Phép Tiếp Tục Chơi",
        item_description="Kỹ năng này sẽ cho phép tiếp tục nối từ dù vừa mới nối từ xong. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_allow**",
        quantity = 1,
        point=0,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_curr_player",
        item_name="Vui Lòng Né Qua Chỗ Khác",
        item_description="Kỹ năng này sẽ biến đối phương thành người đã nối từ hiện tại (dù cho người nối từ hiện tại có là ai khác). Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_curr_player <@315835396305059840>**",
        quantity = 1,
        point=0,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_random_skill_cc",
        item_name="Đổi Điểm",
        item_description="Kỹ năng này sẽ đổi 1 điểm của bạn để đổi lấy một kỹ năng rank Cấp Cao ngẫu nhiên. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_random_skill_cc**",
        quantity = 1,
        point=1,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_steal_point",
        item_name="Ăn Cắp Điểm",
        item_description="Kỹ năng này sẽ có 50/50 phần trăm ăn cắp 3 điểm của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_steal_point <@315835396305059840>**",
        quantity = 1,
        point=3,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_protect",
        item_name="Bảo Hộ",
        item_description="Kỹ năng này sẽ bảo vệ người chơi và vô hiệu hoá kỹ năng của player khác. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_protect**",
        quantity = 1,
        point=1,
        level="Cấp Thấp",
        required_target=False
    ),
    SpecialItem(
        item_id="ct_protect_user",
        item_name="Bảo Hộ Đối Phương",
        item_description="Kỹ năng này sẽ bảo vệ đối phương và vô hiệu hoá kỹ năng của player khác. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_protect_user <@315835396305059840>**",
        quantity = 1,
        point=1,
        level="Cấp Thấp",
        required_target=True
    ),
    SpecialItem(
        item_id="ct_ban",
        item_name="Câm Lặng",
        item_description="Kỹ năng này sẽ khoá miệng đối phương, ban đối phương khỏi trò chơi nối từ trong 2 vòng nhất định. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill ct_ban <@315835396305059840>**",
        quantity = 1,
        point=2,
        level="Cấp Thấp",
        required_target=True
    ),
]

list_special_items_cap_cao = [
    SpecialItem(
        item_id="cc_minus",
        item_name="Trừ Điểm Đối Phương",
        item_description="Kỹ năng này sẽ trừ đi 5 điểm của đối thủ trong trò chơi nối chữ, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_minus <@315835396305059840>**",
        quantity = 1,
        point=5,
        level="Cấp Cao",
        required_target=True
    ),
    SpecialItem(
        item_id="cc_minus_all",
        item_name="Trừ Điểm Tất Cả Player",
        item_description="Kỹ năng này sẽ trừ 3 điểm cho tất cả player. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_minus_all**",
        quantity = 1,
        point=3,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_add",
        item_name="Cộng Điểm Bản Thân",
        item_description="Kỹ năng này sẽ cộng cho bản thân 5 điểm trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_add**",
        quantity = 1,
        point=5,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_hint",
        item_name="Gợi Ý",
        item_description="Kỹ năng này sẽ gợi ý từ cần thiết để hoàn thành lượt chơi nối chữ hiện tại. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_hint**",
        quantity = 1,
        point=0,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_minus_first",
        item_name="Trừ Điểm Top 1",
        item_description="Kỹ năng này sẽ trừ 20 điểm của player top 1 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_minus_first**",
        quantity = 1,
        point=20,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_minus_second",
        item_name="Trừ Điểm Top 2",
        item_description="Kỹ năng này sẽ trừ 16 điểm của player top 2 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_minus_second**",
        quantity = 1,
        point=16,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_add_user",
        item_name="Cộng Điểm Đối Phương",
        item_description="Kỹ năng này sẽ cộng 5 điểm cho đối phương bất kỳ ngoại trừ bản thân, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_add_user <@315835396305059840>**",
        quantity = 1,
        point=5,
        level="Cấp Cao",
        required_target=True
    ),
    SpecialItem(
        item_id="cc_random_skill_dc",
        item_name="Đổi Điểm",
        item_description="Kỹ năng này sẽ đổi 2 điểm của bạn để đổi lấy một kỹ năng rank Đẳng Cấp ngẫu nhiên. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_random_skill_dc**",
        quantity = 1,
        point=2,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_steal_point",
        item_name="Ăn Cắp Điểm",
        item_description="Kỹ năng này sẽ ăn cắp 6 điểm của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_steal_point <@315835396305059840>**",
        quantity = 1,
        point=6,
        level="Cấp Cao",
        required_target=True
    ),
    SpecialItem(
        item_id="cc_protect",
        item_name="Bảo Hộ Giáp Gai",
        item_description="Kỹ năng này sẽ bảo hộ người chơi và phản lại kỹ năng của player khác. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_protect**",
        quantity = 1,
        point=1,
        level="Cấp Cao",
        required_target=False
    ),
    SpecialItem(
        item_id="cc_ban",
        item_name="Câm Lặng",
        item_description="Kỹ năng này sẽ khoá miệng đối phương, ban đối phương khỏi trò chơi nối từ trong 4 vòng nhất định. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill cc_ban <@315835396305059840>**",
        quantity = 1,
        point=4,
        level="Cấp Cao",
        required_target=True
    ),
]
list_special_items_dang_cap = [
    SpecialItem(
        item_id="dc_minus",
        item_name="Trừ Điểm Đối Phương",
        item_description="Kỹ năng này sẽ trừ đi 10 điểm của đối thủ trong trò chơi nối chữ, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_minus <@315835396305059840>**",
        quantity = 1,
        point=10,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_minus_all",
        item_name="Trừ Điểm Tất Cả Player",
        item_description="Kỹ năng này sẽ trừ 8 điểm cho tất cả player. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_minus_all**",
        quantity = 1,
        point=8,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_add",
        item_name="Cộng Điểm Bản Thân",
        item_description="Kỹ năng này sẽ cộng cho bản thân 10 điểm trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_add**",
        quantity = 1,
        point=10,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_minus_first",
        item_name="Trừ Điểm Top 1",
        item_description="Kỹ năng này sẽ trừ 25 điểm của player top 1 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_minus_first**",
        quantity = 1,
        point=25,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_minus_second",
        item_name="Trừ Điểm Top 2",
        item_description="Kỹ năng này sẽ trừ 20 điểm của player top 2 trong bảng xếp hạng. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_minus_second**",
        quantity = 1,
        point=16,
        level="Đẳng Cấp",
        required_target=False
    ),
    SpecialItem(
        item_id="dc_add_user",
        item_name="Cộng Điểm Cho Đối Phương",
        item_description="Kỹ năng này sẽ cộng 10 điểm cho đối phương bất kỳ ngoại trừ bản thân, lưu ý là đối phương đã từng chơi trò này. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_add_user <@315835396305059840>**",
        quantity = 1,
        point=10,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_del_skill",
        item_name="Huỷ Kỹ Năng Đối Thủ",
        item_description="Kỹ năng này sẽ xoá đi một kỹ năng ngẫu nhiên của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_del_skill <@315835396305059840>**",
        quantity = 1,
        point=0,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_steal_skill",
        item_name="Ăn Cắp Kỹ Năng Đối Thủ",
        item_description="Kỹ năng này sẽ ăn cắp một kỹ năng ngẫu nhiên của đối phương cho bản thân. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_steal_skill <@315835396305059840>**",
        quantity = 1,
        point=0,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_steal_point",
        item_name="Ăn Cắp Điểm",
        item_description="Kỹ năng này sẽ ăn cắp 9 điểm của đối phương. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_steal_point <@315835396305059840>**",
        quantity = 1,
        point=9,
        level="Đẳng Cấp",
        required_target=True
    ),
    SpecialItem(
        item_id="dc_protect",
        item_name="Bảo Hộ Hoàn Giáp",
        item_description="Kỹ năng này sẽ bảo hộ người chơi, phản lại kỹ năng của player khác và cướp luôn kỹ năng của đối thủ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill dc_protect**",
        quantity = 1,
        point=1,
        level="Đẳng Cấp",
        required_target=False
    ),
]
list_special_items_toi_thuong = [
    SpecialItem(
        item_id="tt_minus_all",
        item_name="Trừ Điểm Tối Thượng",
        item_description="Kỹ năng này sẽ trừ đi 25 điểm của toàn bộ đối thủ trong trò chơi nối chữ. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill tt_minus_all**",
        quantity = 1,
        point=25,
        level="Tối Thượng",
        required_target=False
    ),
    SpecialItem(
        item_id="tt_swap_3",
        item_name="Thay Thế Top 3",
        item_description="Kỹ năng này sẽ lập tức cộng đủ điểm để đẩy người chơi lên top 3. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill tt_swap_3**",
        quantity = 1,
        point=5,
        level="Tối Thượng",
        required_target=False
    ),
    SpecialItem(
        item_id="tt_swap_2",
        item_name="Thay Thế Top 2",
        item_description="Kỹ năng này sẽ lập tức cộng đủ điểm để đẩy người chơi lên top 2. Cách sử dụng rất đơn giản, chỉ việc nhập đúng lệnh như thế này:\n **!use_skill tt_swap_2**",
        quantity = 1,
        point=5,
        level="Tối Thượng",
        required_target=False
    ),
]