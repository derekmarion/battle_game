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

    def take_damage(self, damage: int) -> int:
        """Calculate the damage taken by the character."""

        actual_damage = damage
        if self.is_defending:
            actual_damage = damage // 2
            self.is_defending = False

        self.current_hp -= actual_damage
        return actual_damage

    def heal(self, amount: int):
        """Heal the character by a certain amount."""

        self.current_hp = min(self.current_hp + amount, self.max_hp)

    def is_alive(self) -> bool:
        """Check if the character is alive."""

        return self.current_hp > 0

    def gain_experience(self, amount: int):
        """Gain experience points and level up if necessary."""

        self.experience += amount
        while self.experience >= 100:
            self.level_up()

    def level_up(self):
        """Level up the character."""

        self.level += 1
        self.experience -= 100
        self.max_hp += 10
        self.current_hp = self.max_hp
        self.attack_points += 2
        self.defense_points += 1
