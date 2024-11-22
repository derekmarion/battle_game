from src.core import Battle
from src.core import Character
from src.core import ActionType
import pytest


class TestBattle:
    """Test cases for the Battle class."""

    @pytest.fixture
    def setup(self):
        """Setup new battle and character instances for each test."""

        self.battle = Battle()
        self.battle.selected_character = Character("Test", 10, 5, True)
        self.battle.target_character = Character("Test2", 10, 5, False)

    def test_init(self, setup):
        """Test the __init__ method of the Battle class."""

        assert self.battle.current_turn == 0
        assert self.battle.battle_log == []
        assert self.battle.selected_character
        assert self.battle.target_character

    def test_handle_turn_attack(self, setup):
        """Test the handle_turn method of the Battle Class for an attack action."""

        starting_hp = self.battle.target_character.current_hp

        self.battle.handle_turn(ActionType.ATTACK)

        assert len(self.battle.battle_log) == 1
        assert self.battle.current_turn == 1

        # Check that the target character took damage post swap
        assert self.battle.selected_character.current_hp < starting_hp

    def test_handle_turn_defend(self, setup):
        """Test the handle_turn method of the Battle Class for a defend action."""

        self.battle.handle_turn(ActionType.DEFEND)

        assert len(self.battle.battle_log) == 1
        assert self.battle.current_turn == 1

        # Check that the target character is defending post swap
        assert self.battle.target_character.is_defending
