from typing import Optional
import pygame
import random
from .character import Character
from .action import ActionType


class Battle:
    """Class to handle core battle logic."""

    def __init__(self):
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
        pass

    def run(self):
        """Run the battle loop."""
        running = True
        while running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)

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
