from src.core import Menu
import pytest


class TestCharacterSelection:
    """Test cases for the Menu class."""

    @pytest.fixture
    def setup(self):
        """Setup new battle and character instances for each test."""

        self.menu = Menu()

    @pytest.fixture
    def mock_user_input_text(self, monkeypatch):
        """Mock user input for testing purposes."""

        def mock_input(user_input):
            # This will result in an NPC character selection
            return "1"

        monkeypatch.setattr("builtins.input", mock_input)

    def test_init(self, setup):
        """Test the __init__ method of the Menu class."""

        assert self.menu.player_character is None
        assert self.menu.non_player_character is None

    def test_character_selection(self, setup, mock_user_input_text):
        """Test the character_selection method of the Menu class."""

        self.menu.run()

        # Check that both characters are selected
        assert self.menu.player_character
        assert self.menu.non_player_character

        # Check that the player character is a player character
        assert self.menu.player_character.player_character
        assert not self.menu.non_player_character.player_character
