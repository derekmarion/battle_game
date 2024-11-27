from src.core import Battle
from src.core import Character
from src.core import ActionType
import pytest


class TestBattle:
    """Test cases for the Battle class."""

    @pytest.fixture
    def setup(self):
        """Setup new battle and character instances for each test."""

        self.battle = Battle(False)
        self.battle.selected_character = Character("Test", 10, 5, True)
        self.battle.target_character = Character("Test2", 10, 5, False)

    @pytest.fixture
    def mock_user_input_text(self, monkeypatch):
        """Mock user input for testing purposes."""

        def mock_input(user_input):
            # This will result in an attack action
            return "1"

        monkeypatch.setattr("builtins.input", mock_input)

    def test_init(self, setup):
        """Test the __init__ method of the Battle class."""

        assert self.battle.current_turn == 0
        assert self.battle.battle_log == []
        assert self.battle.selected_character
        assert self.battle.target_character

    def test_handle_turn_attack(self, setup):
        """Test the handle_turn method of the Battle Class for an attack action."""

        # TODO: this test will sometimes fail because damage is random
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

    def test_handle_turn_special(self, setup):
        """Test the handle_turn method of the Battle Class for a special action."""

        self.battle.handle_turn(ActionType.SPECIAL)

        assert len(self.battle.battle_log) == 1
        assert self.battle.current_turn == 1

        # Check that the target character reset their special cooldown post swap
        assert self.battle.target_character.special_cooldown == 2

    def test_check_win_condition(self, setup):
        """Test the _check_win_condition method of the Battle Class."""

        self.battle.target_character.current_hp = 0

        self.battle._check_win_condition()

        assert self.battle.battle_log[-1] == "Test2 has been defeated!"
        assert (
            self.battle.current_turn == 0
        )  # 0 because the turn counter is not incremented here

    def test_text_menu(self, setup, mock_user_input_text):
        """Test the _text_menu method of the Battle Class for text input."""

        assert self.battle._text_menu() == ActionType.ATTACK  # Mocked input enters "1"

    def test_text_menu_invalid_input(self, setup, monkeypatch, capsys):
        """Test the _text_menu method of the Battle Class for invalid text input."""

        # Mock user input for invalid input
        user_responses = iter(["4", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(user_responses))

        # Call the method and capture the output
        self.battle._text_menu()
        output = capsys.readouterr()

        assert "Invalid input." in output.out
