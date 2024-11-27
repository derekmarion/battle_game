from typing import Optional
import pygame
import random
from .character import Character
from .action import ActionType
from src.ai.enemy_ai import get_enemy_action


class Battle:
    """Class to handle core battle logic."""

    def __init__(self, gui: bool = False):
        if gui:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.clock = pygame.time.Clock()
        self.current_turn = 0
        self.battle_log = []
        self.selected_character: Optional[Character] = None
        self.target_character: Optional[Character] = None

    def handle_turn(self, action: ActionType):
        """Handle a turn in the battle."""
        if not self.selected_character or not self.target_character:
            return

        # Handle the selected action
        if action == ActionType.ATTACK:
            self._attack()
        elif action == ActionType.DEFEND:
            self._defend()
        elif action == ActionType.SPECIAL:
            self._handle_special()

        # Decrement the special cooldown times for both characters after each turn
        self._special_cooldown_decrement()

        # Increment the turn counter
        self.current_turn += 1

        # Switch the selected character and target character for the next turn
        self.selected_character, self.target_character = (
            self.target_character,
            self.selected_character,
        )

    def _attack(self):
        """Handle an attack action."""
        damage = (
            self.selected_character.attack_points
            - self.target_character.defense_points
            + random.randint(-5, 10)
        )
        actual_damage = self.target_character.take_damage(max(0, damage))
        self.battle_log.append(
            f"{self.selected_character.name} attacks {self.target_character.name} for {actual_damage} damage!"
        )

        if not self.target_character.is_alive():
            self._check_win_condition()

    def _defend(self):
        """Handle a defend action."""
        self.selected_character.is_defending = True
        self.battle_log.append(
            f"{self.selected_character.name} takes a defensive stance!"
        )

    def _handle_special(self):
        """Handle a special action."""
        if self.selected_character.special_cooldown == 0:
            # Implement special ability logic here
            self.selected_character.special_cooldown = 3
        # TODO: Add a named special ability to the character class
        self.battle_log.append(
            {f"{self.selected_character.name} uses a special ability!"}
        )

    def _special_cooldown_decrement(self):
        """Decrement the special cooldown for all characters."""
        if self.selected_character.special_cooldown > 0:
            self.selected_character.special_cooldown -= 1
        if self.target_character.special_cooldown > 0:
            self.target_character.special_cooldown -= 1

    def _check_win_condition(self):
        """Check if the battle has been won."""
        if not self.target_character.is_alive():
            self.battle_log.append(f"{self.target_character.name} has been defeated!")

        self._game_over()

    def _game_over(self):
        """Handle the game over state."""
        # Implement game over logic here.
        return True

    def run(self, gui: bool = False):
        """Run the battle loop."""
        running = True
        while running and gui:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
        while running:
            if not self._game_over():
                # Get user input for their turn and handle turn
                user_action = self._handle_user_input_text()
                self.handle_turn(user_action)

            if not self._game_over():
                # Get enemy action and handle turn
                enemy_action = get_enemy_action()
                self.handle_turn(enemy_action)
            running = not self._game_over()

    def _handle_events(self):
        """Handle pygame events occuring in the UI."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Add event handling logic here

    def _update(self):
        """Update the game state."""
        # Add game state update logic here
        pass

    def _render(self):
        """Render the game state to the screen."""
        # Clear screen
        self.screen.fill((255, 255, 255))
        # Render game elements
        pygame.display.flip()

    def _text_handle_user_input(self) -> ActionType:
        """Handle user input for text-based UI."""

        user_action = self._text_menu()
        return user_action

    def _text_menu(self) -> ActionType:
        """Display the text-based menu and return the selected action."""
        while True:
            # Display game stats and most recent action
            print(self.battle_log[-1] if self.battle_log else "Battle Start!")
            print(
                f"{self.selected_character.name} HP: {self.selected_character.current_hp}"
            )
            print(f"{self.target_character.name} HP: {self.target_character.current_hp}")
            print("Select an action:")
            print("1. Attack")
            print("2. Defend")
            print("3. Special")

            # Get user input and return the corresponding action
            user_input = input("Enter the number of your choice: ")
            if type(int(user_input)) == int and 1 <= int(user_input) <= 3:
                match user_input:
                    case "1":
                        return ActionType.ATTACK
                    case "2":
                        return ActionType.DEFEND
                    case "3":
                        return ActionType.SPECIAL
            else:
                print("Invalid input. Please try again.")