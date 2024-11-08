class TestCharacter:
    """Test the Character class."""

    def test_character_init(self):
        """Test the __init__ method of the Character class."""

        from src.core import Character

        character = Character("Test", 10, 5)

        assert character.name == "Test"
        assert character.max_hp == 100
        assert character.current_hp == 100
        assert character.attack_points == 10
        assert character.defense_points == 5
        assert character.experience == 0
        assert character.level == 1
        assert character.is_defending is False
        assert character.special_cooldown == 0
