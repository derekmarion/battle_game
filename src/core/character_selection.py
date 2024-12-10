from .character import Character, cPlusPlus, Python, Rust
from typing import Tuple
import random


class Menu:
    """Class to handle character selection."""

    def __init__(self):
        self.player_character = None
        self.non_player_character = None

    def run(self):
        """Run the menu character selection menu."""
        self.character_selection()
        print(f"You have selected {self.player_character.name} as your character.")
        print(f"Your opponent will be {self.non_player_character.name}.")

    def character_selection(self) -> Tuple[Character, Character]:
        """Select two characters to battle."""

        # Initialized list of character to select from
        characters = [cPlusPlus, Python, Rust]

        # Randomly assign npc
        self.non_player_character = random.choice(characters)(player_character=False)

        # Present user with choice of player character
        self.player_character = self.choose_character()

    def choose_character(self) -> Character:
        """Prompt user to select a character."""

        running = True
        while running:
            print("Select a character:")
            print("1. C++")
            print("2. Python")
            print("3. Rust")
            choice = input("Enter the number of your choice: ")

            if choice == "1":
                return cPlusPlus(player_character=True)
            elif choice == "2":
                return Python(player_character=True)
            elif choice == "3":
                return Rust(player_character=True)
            else:
                print("Invalid choice. Please try again.")
