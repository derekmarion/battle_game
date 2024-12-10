from core import Battle, Menu


def main():
    menu = Menu()
    menu.run()
    battle = Battle(False, menu.player_character, menu.non_player_character)
    battle.run(gui=False)


if __name__ == "__main__":
    main()
