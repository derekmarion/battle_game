class Character:
    """Main class for all characters in the game."""

    def __init__(
        self, name: str, attack_points: int, defense_points: int, hp: int = 100
    ):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack_points = attack_points
        self.defense_points = defense_points
        self.experience = 0
        self.level = 1
        self.is_defending = False
        self.special_cooldown = 0
