from enum import Enum


class ActionType(Enum):
    """Action type enumeration"""

    ATTACK = "attack"
    DEFEND = "defend"
    SPECIAL = "special"
    SKIP = "skip"
