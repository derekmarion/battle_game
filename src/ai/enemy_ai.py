from src.core.action import ActionType


def get_enemy_action() -> ActionType:
    """Get the enemy action based on the current state of the battle."""

    # For now, the enemy will always attack
    return ActionType.ATTACK
