from .action import ActionType
import random


class Character:
    """Main class for all characters in the game."""

    def __init__(
        self,
        name: str,
        attack_points: int,
        defense_points: int,
        hp: int = 100,
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
        self.confused = False
        self.special_ability_name = ""
        self.skip_turn = False

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
        """Level up the character. Not used in the current version of the game."""

        self.level += 1
        self.experience -= 100
        self.max_hp += 10
        self.current_hp = self.max_hp
        self.attack_points += 2
        self.defense_points += 1

    def get_enemy_action(self) -> ActionType:
        """Get the enemy action based on the current hp of the character."""

        # If enemy has great than 50 hp, select randomly between attack and special
        if self.current_hp >= 50:
            return random.choice([ActionType.ATTACK, ActionType.SPECIAL])
        else:  # If enemy has less than 50 hp, select randomly between attack and defend
            return random.choice([ActionType.ATTACK, ActionType.DEFEND])


class cPlusPlus(Character):
    def __init__(self, player_character: bool = False):
        super().__init__("C++", 20, 10)
        self.special_cooldown = 0
        self.special_ability_name = "Memory Leak"
        self.player_character = player_character

    def special_ability(self, target: Character) -> str:
        """C++ special ability: Memory Leak.

        Causes the other character to randomly choose their next action.
        """
        target.confused = True
        return f"{self.name} causes {target.name} to be confused!"


class Python(Character):
    def __init__(self, player_character: bool = False):
        super().__init__("Python", 20, 10)
        self.special_cooldown = 0
        self.special_ability_name = "Dynamic Typing"
        self.player_character = player_character

    def special_ability(self, target: Character) -> str:
        """Python special ability: Dynamic Typing.

        Causes the other character to skip their next turn."""
        target.skip_turn = True
        return f"{target.name} skips their next turn!"


class Rust(Character):
    def __init__(self, player_character: bool = False):
        super().__init__("Rust", 20, 10)
        self.special_cooldown = 0
        self.special_ability_name = "Borrow Checker"
        self.player_character = player_character

    def special_ability(self, target: Character) -> str:
        """Rust special ability: Borrow Checker.

        Heals 30 HP."""
        self.heal(30)
        return f"{self.name} heals 30 HP!"
