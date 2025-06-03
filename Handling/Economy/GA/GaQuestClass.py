from Handling.Economy.GA.GuardianAngelClass import GuardianAngel
class GuardianAngelQuest:
    def __init__(self, guardian: GuardianAngel, user_name: str, user_display_name: str, channel_name: str, quest_lines: list['GuardianQuestLines']):
        self.guardian = guardian
        self.user_name = user_name
        self.user_display_name = user_display_name
        self.channel_name = channel_name
        self.quest_lines = quest_lines
        

class NextSteps:
    def __init__(self, choice_a: str, choice_b: str, choice_c: str, timeout: str):
        self.choice_a = choice_a
        self.choice_b = choice_b
        self.choice_c = choice_c
        self.timeout = timeout

    def get_next_id(self, choice: str) -> str:
        if choice == "A":
            return self.choice_a
        elif choice == "B":
            return self.choice_b
        elif choice == "C":
            return self.choice_c
        elif choice == "timeout":
            return self.timeout
        else:
            return None

class GuardianQuestLines:
    def __init__(self, title: str, description: str, choice_a: str, choice_b: str, choice_c: str, choice_timeout: str, next_steps: NextSteps, id = "start", ga_health: int = 0, ga_stamina: int = 0, ga_mana: int = 0, ga_exp: int = 0, gold: int = 0, silver: int = 0, dignity_point: int = 0, force_injury = False, force_dead = False):
        self.id = id
        self.title = title
        self.description = description
        self.choice_a = choice_a
        self.choice_b = choice_b
        self.choice_c = choice_c
        self.choice_timeout = choice_timeout
        self.ga_health = ga_health
        self.ga_stamina = ga_stamina
        self.ga_mana = ga_mana
        self.ga_exp = ga_exp
        self.gold = gold
        self.silver = silver
        self.dignity_point = dignity_point
        self.force_injury = force_injury
        self.force_dead = force_dead
        self.next_steps = next_steps
    
    def replace_guardian_name(self, guardian_name: str):
        # Replace in all string attributes
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                setattr(self, attr, value.replace("{guardian.ga_name}", guardian_name))

        # If you have a nested NextSteps class (adjust if different)
        if hasattr(self, 'next_steps'):
            for attr, value in self.next_steps.__dict__.items():
                if isinstance(value, str):
                    setattr(self.next_steps, attr, value.replace("{guardian.ga_name}", guardian_name))