from typing import List, Optional
from datetime import datetime
from Handling.Economy.Profile.ProfileClass import Profile
from Handling.Economy.GA.GuardianAngelClass import GuardianAngel, GuardianAngelSkill
import Handling.Economy.GA.ListGAAndSkills as ListGAAndSkills
from CustomEnum.EmojiEnum import EmojiCreation2

# class GuardianAngelAttackClass:
#     def __init__(self, list_allied_ga: Optional[List['GuardianAngel']] = None, list_enemy_ga: Optional[List['GuardianAngel']] = None, round: int =1, text: List[str] = None, max_players: int = 1):
#         self.list_allied_ga = list_allied_ga if list_allied_ga else None
#         self.list_enemy_ga = list_enemy_ga if list_enemy_ga else None
#         self.round = round
#         self.text = text if text else None
#         self.max_players = max_players
        
class GuardianAngelAttackClass:
    def __init__(self, player_ga: GuardianAngel, player_profile: Profile = None):
        self.player_profile = player_profile
        self.player_ga = player_ga