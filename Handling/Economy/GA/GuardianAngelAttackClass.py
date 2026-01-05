from typing import List, Optional
from datetime import datetime
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from CustomEnum.EmojiEnum import EmojiCreation2
import uuid


class GuardianAngelAttackClass:
    def __init__(self, player_ga: GuardianAngel, player_profile: Profile = None, starting_at_round:int = 1, recovery_time:int = 0, max_recovery:int = 2, max_mass_restored_mana_skill: int = 2, is_used_skill_critical_strike = False, brain_washed_round: int = 0, stunned_round: int = 0, is_dead_ga = False, has_used_summoning = False, is_summoned = False, summoner_owner_id: int = None, is_used_skill_resurrection = False, max_shield = 3, max_summon_sacrifice = 1, is_upper_side = True):
        self.ga_attack_uid = str(uuid.uuid4())
        self.player_profile = player_profile
        self.player_ga = player_ga
        self.starting_at_round = starting_at_round
        
        self.recovery_time = recovery_time
        self.max_recovery = max_recovery
        self.max_mass_restored_mana_skill = max_mass_restored_mana_skill
        
        self.is_used_skill_critical_strike = is_used_skill_critical_strike
        self.brain_washed_round = brain_washed_round
        self.stunned_round = stunned_round
        self.is_dead_ga = is_dead_ga

        self.has_used_summoning = has_used_summoning
        self.is_summoned = is_summoned
        self.summoner_owner_id = summoner_owner_id
        self.is_used_skill_resurrection = is_used_skill_resurrection
        
        self.max_shield = max_shield
        self.max_summon_sacrifice = max_summon_sacrifice
        
        self.is_upper_side = is_upper_side