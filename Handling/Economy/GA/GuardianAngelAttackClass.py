from typing import List, Optional
from datetime import datetime
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from CustomEnum.EmojiEnum import EmojiCreation2

class GuardianAngelAttackClass:
    def __init__(self, player_ga: GuardianAngel, player_profile: Profile = None, starting_at_round:int = 1, recovery_time:int = 0, max_recovery:int = 2, is_used_skill_critical_strike = False, brain_washed_round: int = None, stunned_round: int = None, is_dead_ga = False):
        self.player_profile = player_profile
        self.player_ga = player_ga
        self.starting_at_round = starting_at_round
        
        self.recovery_time = recovery_time
        self.max_recovery = max_recovery
        
        self.is_used_skill_critical_strike = is_used_skill_critical_strike
        self.brain_washed_round = brain_washed_round
        self.stunned_round = stunned_round
        self.is_dead_ga = is_dead_ga