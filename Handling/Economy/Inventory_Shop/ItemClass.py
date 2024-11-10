
from typing import List, Optional
from datetime import datetime
from CustomEnum.EmojiEnum import EmojiCreation2

class Item:
    def __init__(self, item_id: str, item_name: str, item_description: str, item_type: str, quantity: int, emoji: str, item_worth_amount: int = 5000, item_worth_type: str = "C", item_require_target: bool = False, is_self_usable = False, bonus_exp: int = 0, bonus_dignity: int = 0, rank_required: int = 1):
        self.item_id = item_id
        self.item_name = item_name
        self.item_description = item_description
        self.item_type = item_type
        self.quantity = quantity
        self.emoji = emoji
        self.item_worth_amount = item_worth_amount
        self.item_worth_type = item_worth_type
        self.item_require_target = item_require_target
        self.is_self_usable = is_self_usable
        self.bonus_exp = bonus_exp
        self.bonus_dignity = bonus_dignity
        self.rank_required = rank_required

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "item_description": self.item_description,
            "item_type": self.item_type,
            "quantity": self.quantity,
            "emoji": self.emoji,
            "item_worth_amount": self.item_worth_amount,
            "item_worth_type": self.item_worth_type,
            "item_require_target": self.item_require_target,
            "is_self_usable": self.is_self_usable,
            "bonus_exp": self.bonus_exp,
            "bonus_dignity": self.bonus_dignity,
            "rank_required": self.rank_required,
        }

    @staticmethod
    def from_dict(data:dict):
        return Item(
                item_id=data.get("item_id", None),
                item_name=data.get("item_name", None),
                item_description=data.get("item_description", None),
                item_type=data.get("item_type", None),
                quantity=data.get("quantity", None),
                emoji=data.get("emoji", None),
                item_worth_amount=data.get("item_worth_amount", None),
                item_worth_type=data.get("item_worth_type", None),
                
                item_require_target=data.get("item_require_target", False),
                is_self_usable=data.get("is_self_usable", False),
                
                bonus_exp=data.get("bonus_exp", 0),
                bonus_dignity=data.get("bonus_dignity", 0),
                rank_required=data.get("rank_required", 1),
            )

#region list gift
list_gift_items = [
    Item(
        item_id = "g_pocky",
        item_name = "Bánh Pocky",
        item_description = "Hộp bánh pocky sẽ giúp bạn tăng kinh nghiệm khi tặng cho người khác!",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_POCKY.value,
        item_worth_amount = 30,
        item_worth_type= "S",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 10,
        bonus_dignity = 0,
        rank_required = 1,
    ),
    Item(
        item_id = "g_flower",
        item_name = "Hoa Xinh",
        item_description = "Bông hoa quý báu có thể giúp tăng nhân phẩm và kinh nghiệm khi tặng cho người khác! Hoặc biết đâu sẽ khiến họ vui hơn thì sao?",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_FLOWER.value,
        item_worth_amount = 50,
        item_worth_type= "S",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 10,
        bonus_dignity = 5,
        rank_required = 5,
    ),
    Item(
        item_id = "g_chocolate",
        item_name = "Sô cô la",
        item_description = "Một thanh sô cô la ngon lành sẽ làm tăng nhân phẩm và kinh nghiệm khi tặng cho người khác!",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_CHOCOLATE.value,
        item_worth_amount = 50,
        item_worth_type= "S",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 5,
        bonus_dignity = 10,
        rank_required = 8,
    ),
    Item(
        item_id = "g_stcake",
        item_name = "Bánh kem dâu",
        item_description = "Một miếng bánh kem dâu ngon miệng sẽ làm tăng nhân phẩm và kinh nghiệm khi tặng cho người khác!",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_STRAW_CAKE.value,
        item_worth_amount = 75,
        item_worth_type= "S",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 10,
        bonus_dignity = 10,
        rank_required = 10,
    ),
    Item(
        item_id = "g_earring",
        item_name = "Khuyên Tai Bạc",
        item_description = "Một đôi khuyên tai xinh xinh cho bạn gái, có thể giúp tăng nhân phẩm và kinh nghiệm khi tặng!",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_EARRING.value,
        item_worth_amount = 100,
        item_worth_type= "S",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 15,
        bonus_dignity = 5,
        rank_required = 20,
    ),
    Item(
        item_id = "g_sring",
        item_name = "Nhẫn Bạc",
        item_description = "Nhẫn bạc quý phái và đầy thanh lịch, một món quà hoàn hảo có thể giúp tăng nhân phẩm và kinh nghiệm khi tặng cho người khác!",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_SILVER_RING.value,
        item_worth_amount = 500,
        item_worth_type= "S",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 15,
        bonus_dignity = 10, 
        rank_required = 25,
    ),
    Item(
        item_id = "g_gring",
        item_name = "Nhẫn Vàng",
        item_description = "Nhẫn vàng quý tộc và giàu sang, một món quà hoàn hảo có thể giúp tăng nhân phẩm và kinh nghiệm khi tặng cho người khác!",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_GOLD_RING.value,
        item_worth_amount = 20,
        item_worth_type= "G",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 30,
        bonus_dignity = 15,
        rank_required = 25,
    ),
    Item(
        item_id = "g_dring",
        item_name = "Nhẫn Kim Cương",
        item_description = "Nhẫn kim cương hào nhoáng và phú quý, một món quà hoàn hảo có thể giúp tăng nhân phẩm và kinh nghiệm khi tặng cho người khác!",
        item_type = "gift",
        quantity = 1,
        emoji = EmojiCreation2.GIFT_DIAMOND_RING.value,
        item_worth_amount = 120,
        item_worth_type= "G",
        item_require_target = True,
        is_self_usable = False,
        bonus_exp = 30,
        bonus_dignity = 20,
        rank_required = 35,
    ),
]