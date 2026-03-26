from src.project.domain.domain import Player
from src.project.ui.ui import ConsoleUI



def main():
    player = Player()
    ui = ConsoleUI(player)

    player.make_deck()

    while not player.end_game_status:
        # начало комнаты / хода
        # player.avoided_prev_room = False
        player.potions_taken_this_turn = False
        player.any_cards_picked = False
        player.pick_counter = 3

        player.make_room()
        if not player.room:
            player.end_game_status = True
            break  # колода кончилась

        while player.pick_counter > 0 and not player.end_game_status:
            ui.render()
            try:
                action = ui.ask_action()
            except (KeyboardInterrupt, EOFError):
                print("ended by user")
                player.end_game_status = True
                break

            if action == "debug":
                player.switch_debug()
                continue

            if action == "s":
                if not player.can_skip():
                    print("you already picked a card and cannot skip for the rest of your turn")
                    continue
                if not player.skip_room():
                    print("you cannot skip this turn")
                else:
                    break
            else:
                # выбор карты по индексу
                player.apply_pick(action)

            result = player.check_end()
            if result is not None:
                print(result)
                break

        player.rooms_passed += 1

    print("Game over")


if __name__ == "__main__":
    main()