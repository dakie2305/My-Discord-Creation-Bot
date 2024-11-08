from typing import List, Optional
from datetime import datetime

class ConversionRate:
    def __init__(self, rate:float = 1.0, shop_rate:float = 1.0, last_reset: datetime = None, last_authority: int =None):
        self.id = "conversion_rate"
        self.rate = rate
        self.shop_rate = shop_rate
        self.last_reset = last_reset
        self.last_authority = last_authority
    
    def to_dict(self):
        return {
            "id": self.id,
            "rate": self.rate,
            "shop_rate": self.shop_rate,
            "last_reset": self.last_reset,
            "last_authority": self.last_authority,
        }
    @staticmethod
    def from_dict(data:dict):
        return ConversionRate(
            rate= data.get("rate", 1.0),
            shop_rate= data.get("shop_rate", 1.0),
            last_reset= data.get("last_reset", None),
            last_authority= data.get("last_authority", None),
        )