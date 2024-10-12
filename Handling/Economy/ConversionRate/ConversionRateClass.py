from typing import List, Optional
from datetime import datetime

class ConversionRate:
    def __init__(self, rate:int = 1, last_reset: datetime = None):
        self.id = "conversion_rate"
        self.rate = rate
        self.last_reset = last_reset
    
    def to_dict(self):
        return {
            "id": self.id,
            "rate": self.rate,
            "last_reset": self.last_reset,
        }
    @staticmethod
    def from_dict(data:dict):
        return ConversionRate(
            rate= data.get("rate", None),
            last_reset= data.get("last_reset", None),
        )