from src.core import Battle
from src.core import Character, cPlusPlus, Python
from src.core import ActionType
import pytest


class TestBattle:
    """Test cases for the Battle class."""

    @pytest.fixture
    def setup(self):
        """Setup new battle and character instances for each test."""

        self.battle = Battle(False)
        self.battle.selected_character = cPlusPlus()
        self.battle.target_character = Python()

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

        starting_hp = self.battle.target_character.current_hp

        self.battle.handle_turn(ActionType.ATTACK)

        assert len(self.battle.battle_log) == 1
        assert self.battle.current_turn == 1

        # Check that the target character took damage post swap, or that the attack missed
        assert (
            self.battle.selected_character.current_hp < starting_hp
            or self.battle.battle_log[-1].endswith("but does no damage!")
        )

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

        assert (
            len(self.battle.battle_log) == 2
        )  # 2 because the special ability message is logged
        assert self.battle.current_turn == 1

        # Check that the target character reset their special cooldown post swap
        assert self.battle.target_character.special_cooldown == 2

    def test_handle_turn_skip(self, setup):
        """Test the handle_turn method of the Battle Class for a skip action."""

        self.battle.handle_turn(ActionType.SKIP)

        assert len(self.battle.battle_log) == 1
        assert self.battle.current_turn == 1

        # Check that the selected character skipped their turn
        assert self.battle.battle_log[-1].endswith("skips their turn!")

    def test_handle_turn_confused(self, setup):
        """Test the handle_turn method of the Battle Class for a confused character."""

        self.battle.selected_character.confused = True

        self.battle.handle_turn(ActionType.ATTACK)

        # Not checking battle log length because a confused character will return a random action
        assert self.battle.current_turn == 1

        # Check that the battle log reflects the confused state
        assert self.battle.battle_log[0].endswith("is confused!")
        # Check that the selected character reset their confused state (post swap)
        assert not self.battle.target_character.confused

    def test_handle_turn_skip_turn(self, setup):
        """Test the handle-turn method of the Battle Class for a skip turn action."""

        self.battle.selected_character.skip_turn = True

        self.battle.handle_turn(ActionType.ATTACK)

        assert len(self.battle.battle_log) == 1

        # Check that the selected characters turn was skipped in battle log and skip was reset
        assert not self.battle.target_character.skip_turn
        assert self.battle.battle_log[-1].endswith("skips their turn!")

    def test_handle_game_over(self, setup):
        """Test the handle_game_over method of the Battle Class."""

        self.battle.target_character.current_hp = 0

        self.battle._handle_game_over()

        assert self.battle.battle_log[-1] == "Python has been defeated!"
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
