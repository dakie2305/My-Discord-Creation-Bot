from typing import List, Optional
from datetime import datetime

class GuardianAngel:
    def __init__(self, ga_id: str, ga_name: str, ga_emoji: str, stamina: int, max_stamina: int, health: int, max_health: int, mana: int, max_mana:int, attack_power: int = 10, buff_attack_percent: int = 0, level: int = 1, level_progressing: int = 0, stats_point: int = 0, list_skills : Optional[List['GuardianAngelSkill']] = None, max_skills: int = 1, is_injured: bool = False, time_to_recover: datetime = None, worth_amount: int = 50, worth_type: str = "D", last_feed: datetime = None, last_meditation: datetime = None):
        self.ga_id = ga_id
        self.ga_name = ga_name
        self.ga_emoji = ga_emoji
        self.stamina = stamina
        self.max_stamina = max_stamina
        self.health = health
        self.max_health = max_health
        self.mana = mana
        self.max_mana = max_mana
        self.level = level
        self.level_progressing = level_progressing
        self.attack_power = attack_power
        self.buff_attack_percent = buff_attack_percent
        self.stats_point = stats_point
        self.max_skills = max_skills
        self.worth_amount = worth_amount
        self.worth_type = worth_type
        
        self.last_feed = last_feed if last_feed else None
        self.last_meditation = last_meditation if last_meditation else None
        
        self.is_injured = is_injured
        self.time_to_recover = time_to_recover if time_to_recover else None
        
        self.list_skills: List[GuardianAngelSkill] = list_skills if list_skills else []
    def to_dict(self):
        return {
            "ga_id": self.ga_id,
            "ga_name": self.ga_name,
            "ga_emoji": self.ga_emoji,
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
            "health": self.health,
            "max_health": self.max_health,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "level": self.level,
            "level_progressing": self.level_progressing,
            "attack_power": self.attack_power,
            "buff_attack_percent": self.buff_attack_percent,
            "stats_point": self.stats_point,
            "max_skills": self.max_skills,
            "worth_amount": self.worth_amount,
            "worth_type": self.worth_type,
            
            "is_injured": self.is_injured,
            "time_to_recover": self.time_to_recover if self.time_to_recover else None,
            "last_feed": self.last_feed if self.last_feed else None,
            "last_meditation": self.last_meditation if self.last_meditation else None,
            
            "list_skills": [data.to_dict() for data in self.list_skills],
        }
    
    @staticmethod
    def from_dict(data:dict):
        return GuardianAngel(
                ga_id=data.get("ga_id", None),
                ga_name=data.get("ga_name", None),
                ga_emoji=data.get("ga_emoji", None),
                stamina=data.get("stamina", 0),
                max_stamina=data.get("max_stamina", 0),
                health=data.get("health", 0),
                max_health=data.get("max_health", 0),
                mana=data.get("mana", 0),
                max_mana=data.get("max_mana", 0),
                level=data.get("level", 1),
                level_progressing=data.get("level_progressing", 0),
                attack_power=data.get("attack_power", 10),
                buff_attack_percent=data.get("buff_attack_percent", 0),
                stats_point=data.get("stats_point", 0),
                max_skills=data.get("max_skills", 0),
                worth_type=data.get("worth_type", "D"),
                worth_amount=data.get("worth_amount", 10),
                
                is_injured=data.get("is_injured", False),
                time_to_recover=data.get("time_to_recover", None),
                last_meditation=data.get("last_meditation", None),
                last_feed=data.get("last_feed", None),
                
                list_skills = [GuardianAngelSkill.from_dict(data) for data in data.get("list_skills", [])],
            )

class GuardianAngelSkill:
    def __init__(self, skill_id: str, skill_name: str, skill_desc: str, skill_type: str, emoji: str, attack_power: int = 10, defense_power: int = 10, buff_attack_percent = 1, buff_defense_percent = 1, min_level_required: int = 1, item_worth_amount: int = 100, item_worth_type: str = "G", percent_min_stamina_req: int = 1, percent_min_health_req: int = 1, percent_min_mana_req: int = 1, stamina_loss: int = 0, health_loss: int = 0, mana_loss: int = 0):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        self.skill_type = skill_type
        self.emoji = emoji
        self.attack_power = attack_power
        self.defense_power = defense_power
        self.buff_attack_percent = buff_attack_percent
        self.buff_defense_percent = buff_defense_percent
        self.min_level_required = min_level_required
        self.item_worth_amount = item_worth_amount
        self.item_worth_type = item_worth_type
        self.percent_min_stamina_req = percent_min_stamina_req
        self.percent_min_health_req = percent_min_health_req
        self.percent_min_mana_req = percent_min_mana_req
        self.stamina_loss = stamina_loss
        self.health_loss = health_loss
        self.mana_loss = mana_loss

    def to_dict(self):
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "skill_desc": self.skill_desc,
            "skill_type": self.skill_type,
            "emoji": self.emoji,
            "attack_power": self.attack_power,
            "defense_power": self.defense_power,
            "buff_attack_percent": self.buff_attack_percent,
            "buff_defense_percent": self.buff_defense_percent,
            "min_level_required": self.min_level_required,
            "item_worth_amount": self.item_worth_amount,
            "item_worth_type": self.item_worth_type,
            "percent_min_stamina_req": self.percent_min_stamina_req,
            "percent_min_health_req": self.percent_min_health_req,
            "percent_min_mana_req": self.percent_min_mana_req,
            "stamina_loss": self.stamina_loss,
            "health_loss": self.health_loss,
            "mana_loss": self.mana_loss,
        }

    @staticmethod
    def from_dict(data: dict):
        return GuardianAngelSkill(
            skill_id=data.get("skill_id", None),
            skill_name=data.get("skill_name", None),
            skill_desc=data.get("skill_desc", None),
            skill_type=data.get("skill_type", None),
            emoji=data.get("emoji", None),
            attack_power=data.get("attack_power", 10),
            defense_power=data.get("defense_power", 10),
            buff_attack_percent=data.get("buff_attack_percent", 1),
            buff_defense_percent=data.get("buff_defense_percent", 1),
            min_level_required=data.get("min_level_required", 1),
            item_worth_amount=data.get("item_worth_amount", 100),
            item_worth_type=data.get("item_worth_type", "G"),
            percent_min_stamina_req=data.get("percent_min_stamina_req", 1),
            percent_min_health_req=data.get("percent_min_health_req", 1),
            percent_min_mana_req=data.get("percent_min_mana_req", 1),
        )

