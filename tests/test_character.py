class TestCharacter:
    """Test the Character class."""

    from src.core import Character

    character = Character("Test", 10, 5, True)

    def test_character_init(self):
        """Test the __init__ method of the Character class."""

        assert self.character.name == "Test"
        assert self.character.max_hp == 100
        assert self.character.current_hp == 100
        assert self.character.attack_points == 10
        assert self.character.defense_points == 5
        assert self.character.experience == 0
        assert self.character.level == 1
        assert self.character.is_defending is False
        assert self.character.special_cooldown == 0

    def test_character_take_damage(self):
        """Test the take_damage method of the Character class."""

        assert self.character.take_damage(10) == 10
        assert self.character.current_hp == 90

        self.character.is_defending = True
        assert self.character.take_damage(10) == 5
        assert self.character.current_hp == 85

    def test_character_heal(self):
        """Test the heal method of the Character class."""

        self.character.current_hp = 50
        self.character.heal(10)
        assert self.character.current_hp == 60

        self.character.heal(50)
        assert self.character.current_hp == 100

    def test_character_is_alive(self):
        """Test the is_alive method of the Character class."""

        assert self.character.is_alive() is True

        self.character.current_hp = 0
        assert self.character.is_alive() is False

    def test_character_gain_experience(self):
        """Test the gain_experience method of the Character class."""

        self.character.gain_experience(50)
        assert self.character.experience == 50

        self.character.gain_experience(50)
        assert self.character.experience == 0
        assert self.character.level == 2
        assert self.character.max_hp == 110
        assert self.character.current_hp == 110
        assert self.character.attack_points == 12
        assert self.character.defense_points == 6
