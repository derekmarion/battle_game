from typing import Optional
import pygame
import random
from .character import Character
from .action import ActionType


class Battle:
    """Class to handle core battle logic."""

    def __init__(
        self,
        gui: bool = False,
        player_character: Character = None,
        enemy_character: Character = None,
    ):
        if gui:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.clock = pygame.time.Clock()
        self.current_turn = 0
        self.battle_log = []
        # Initialize the selected and target characters
        # to facilitate battle logic
        self.selected_character: Optional[Character] = (
            player_character  # Player character goes first
        )
        self.target_character: Optional[Character] = enemy_character
        # Initilize attributes for the player and enemy characters
        # to facilitate UI messages
        self.player_character = player_character
        self.enemy_character = enemy_character
        self._game_over = False

    def handle_turn(self, action: ActionType):
        """Handle a turn in the battle."""
        if not self.selected_character or not self.target_character:
            return

        # Check for special conditions
        action = self._handle_special_conditions(action)

        # Handle the selected action
        if action == ActionType.ATTACK:
            self._attack()
        elif action == ActionType.DEFEND:
            self._defend()
        elif action == ActionType.SPECIAL:
            self._handle_special()
        elif action == ActionType.SKIP:
            self._skip()

        # Decrement the special cooldown times for both characters after each turn
        self._special_cooldown_decrement()

        # Increment the turn counter
        self.current_turn += 1

        # Switch the selected character and target character for the next turn
        self.selected_character, self.target_character = (
            self.target_character,
            self.selected_character,
        )

        # Check for character death and end game if necessary
        self._check_win_condition()

    def _skip(self):
        """Handle a skip action."""
        self.battle_log.append(f"{self.selected_character.name} skips their turn!")

    def _attack(self):
        """Handle an attack action."""
        damage = (
            self.selected_character.attack_points
            - self.target_character.defense_points
            + random.randint(-5, 10)
        )
        actual_damage = self.target_character.take_damage(max(0, damage))
        if actual_damage > 0:
            self.battle_log.append(
                f"{self.selected_character.name} attacks {self.target_character.name} for {actual_damage} damage!"
            )
        elif actual_damage == 0:  # Check if the attack did no damage
            self.battle_log.append(
                f"{self.selected_character.name} attacks {self.target_character.name} but does no damage!"
            )

    def _defend(self):
        """Handle a defend action."""
        self.selected_character.is_defending = True
        self.battle_log.append(
            f"{self.selected_character.name} takes a defensive stance!"
        )

    def _handle_special(self):
        """Handle a special action."""
        if self.selected_character.special_cooldown == 0:
            #  Call the special ability of the selected character and get description
            battle_log_description = self.selected_character.special_ability(
                self.target_character
            )  # Call the special ability of the selected character and get description
            self.selected_character.special_cooldown = 3  # Reset the special cooldown
            self.battle_log.append(
                f"{self.selected_character.name} uses {self.selected_character.special_ability_name}!"
            )  # Append the use of special ability to the battle log
            self.battle_log.append(
                battle_log_description
            )  # Append the special ability description to the battle log
        else:
            self.battle_log.append(
                f"{self.selected_character.name} is still recharging their special ability!"
            )

    def _handle_special_conditions(self, action: ActionType) -> ActionType:
        """Check for special conditions before handling the action."""
        if self.selected_character.confused:
            self.battle_log.append(f"{self.selected_character.name} is confused!")
            self.selected_character.confused = False  # Reset the confused state
            return random.choice(list(ActionType))
        elif self.selected_character.skip_turn:
            self.selected_character.skip_turn = False  # Reset the skip turn state
            return ActionType.SKIP
        return action

    def _special_cooldown_decrement(self):
        """Decrement the special cooldown for all characters."""
        if self.selected_character.special_cooldown > 0:
            self.selected_character.special_cooldown -= 1
        if self.target_character.special_cooldown > 0:
            self.target_character.special_cooldown -= 1

    def _check_win_condition(self):
        """Handle the game over state."""
        # Check whether the player or enemy character has been defeated
        if not self.player_character.is_alive() or not self.enemy_character.is_alive():
            if not self.player_character.is_alive():
                self.battle_log.append("\nYou have been defeated!")
                self.battle_log.append("Game Over!")
            elif not self.enemy_character.is_alive():
                self.battle_log.append("\nThe enemy has been defeated!")
                self.battle_log.append("You win!")
            # Display the last two battle log entries and break the game loop
            print(f"{self.battle_log[-2]}")
            print(f"{self.battle_log[-1]}")
            self._game_over = True

    def run(self, gui: bool = False):
        """Run the battle loop."""
        running = True

        while running and gui:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
        while running:
            if not self._game_over:
                # Get user input for their turn and handle turn
                user_action = self._text_handle_user_input()
                self.handle_turn(user_action)

            if not self._game_over:
                # Get enemy action and handle turn
                enemy_action = self.selected_character.get_enemy_action()
                self.handle_turn(enemy_action)

            if self._game_over:
                running = False

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
            # Check battle log for emptiness and print game start message
            if not self.battle_log:
                self.battle_log.append("Battle Start!")

            # Display the game context. This is implemented here
            # because the text-based UI is awaiting user input
            self._display_game_context()

            print("Select an action:")
            print("1. Attack")
            print("2. Defend")
            print("3. Special")

            # Get user input and return the corresponding action
            while True:
                user_input = input("Enter the number of your choice: ")
                match user_input:
                    case "1":
                        return ActionType.ATTACK
                    case "2":
                        return ActionType.DEFEND
                    case "3":
                        return ActionType.SPECIAL
                    case _:
                        print("Invalid input. Please try again.")

    def _display_game_context(self):
        """Display the current game context."""
        # TODO: Display character stats
        player_character_stats_display = f"Player({self.player_character.name}): {self.player_character.current_hp} HP"
        enemy_character_stats_display = (
            f"Enemy({self.enemy_character.name}): {self.enemy_character.current_hp} HP"
        )
        # Display last 5 battle log entries in reverse order
        battle_log_display = f"""
        ##############Battle Log##############
        {self.battle_log[-5] if len(self.battle_log) > 4 else ""}
        {self.battle_log[-4] if len(self.battle_log) > 3 else ""}
        {self.battle_log[-3] if len(self.battle_log) > 2 else ""}
        {self.battle_log[-2] if len(self.battle_log) > 1 else ""}
        {self.battle_log[-1]}
        ######################################
        """
        print(battle_log_display)
        print(f"{player_character_stats_display}\t\t{enemy_character_stats_display}\n")
