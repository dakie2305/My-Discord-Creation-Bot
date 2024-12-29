from typing import List, Optional
from datetime import datetime
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from CustomEnum.EmojiEnum import EmojiCreation2

class GuardianAngelAttackClass:
    def __init__(self, player_ga: GuardianAngel, player_profile: Profile = None, starting_at_round:int = 1):
        self.player_profile = player_profile
        self.player_ga = player_ga
        self.starting_at_round = starting_at_round