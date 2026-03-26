from src.domain.domain import Player
import os
from prettytable import PrettyTable

class ConsoleUI:
    def __init__(self, player: Player):
        self.player = player

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def render(self):
        self.clear()
        p = self.player

        status_bar = PrettyTable()
        
        status_bar.max_width = 80
        status_bar.min_width = 20

        current_room = PrettyTable()
        current_room.max_width = 80
        current_room.min_width = 20

        # комната
        for i, card in enumerate(p.room):
            current_room.add_column(
                f"{i+1}",
                [f"{card[1]}\n{card[2]}"],
            )

        skip_col = (
            ["Cant\nskip"]
            if p.avoided_prev_room or p.any_cards_picked
            else ["Can\nskip"]
        )
        current_room.add_column("s", skip_col)

        # статус
        status_bar.add_column("Health", [p.health])
        status_bar.add_column("Can pick potion", ["Yes" if not p.potions_taken_this_turn else "No"])
        status_bar.add_column("Weapon", [p.weapon])
        status_bar.add_column("Last killed", [0 if p.last_killed_w_weapon == 20 else p.last_killed_w_weapon])
        status_bar.add_column("Rooms passed", [p.rooms_passed])
        if self.player.debug_mode:
            status_bar.add_column("Debug", ["ON"])

        print(status_bar)
        print(current_room)

    def ask_action(self) -> str:
        """
        Возвращает:
          - "s"  — если игрок ввёл skip
          - "debug" — включить debug
          - индекс (int) 0..len(room)-1 — если выбрана карта
        """
        p = self.player
        available_answers = [str(i + 1) for i in range(len(p.room))]
        available_answers.append("s")
        available_answers.append("debug")

        while True:
            card = input("pick a card: ").strip()
            if card == "debug":
                return "debug"
            if card == "s":
                return "s"
            if card in available_answers[:-2]:
                return int(card) - 1
            print("incorrect pick. try again")