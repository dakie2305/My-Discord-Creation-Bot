from enum import Enum


class GuardianMemoryTag(Enum):
    BATTLE = "battle"
    FEEDING = "feeding"
    MEDITATION = "meditation"
    DUNGEON = "dungeon"
    LEVEL_UP = "level_up"
    INJURY = "injury"
    DEATH = "death"
    RESURRECTION = "resurrection"
    CUSTOM = "general"