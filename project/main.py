import random
import os


class Player:
    def __init__(self):
        self.health = 20
        self.turn_count = 11
        self.weapon = 0
        self.last_killed_w_weapon = 20
        self.avoided_prev_room = False
        self.potions_taken_this_turn = False
        self.end_game_status = False
        self.deck_of_cards = []
        self.monsters = [
            "monster 14",
            "monster 14",
            "monster 13",
            "monster 13",
            "monster 12",
            "monster 12",
            "monster 11",
            "monster 11",
            "monster 10",
            "monster 10",
            "monster 9",
            "monster 9",
            "monster 8",
            "monster 8",
            "monster 7",
            "monster 7",
            "monster 6",
            "monster 6",
            "monster 5",
            "monster 5",
            "monster 4",
            "monster 4",
            "monster 3",
            "monster 3",
            "monster 2",
            "monster 2",
        ]
        self.weapons = [
            "weapon 10",
            "weapon 9",
            "weapon 8",
            "weapon 7",
            "weapon 6",
            "weapon 5",
            "weapon 4",
            "weapon 3",
            "weapon 2",
        ]
        self.potions = [
            "potion 10",
            "potion 9",
            "potion 8",
            "potion 7",
            "potion 6",
            "potion 5",
            "potion 4",
            "potion 3",
            "potion 2",
        ]
        self.room = []

    def pick_card(self):

        card = input("pick a card: ")

        avaible_answers = ["1", "2", "3", "4", "skip"]
        if card in avaible_answers:
            if card == "skip":
                if self.avoided_prev_room == False:
                    self.avoided_prev_room = True
                    self.room = []
                    self.make_a_room()
                else:
                    print("you cannot skip")
            else:
                picked = self.room[int(card) - 1]
                card_type = picked.split()[0]
                card_value = int(picked.split()[-1])
                print(f"_" * 25)
                print(f"you picked: {picked}")
                if card_type == "monster":
                    self.kill_monster(card_value)
                elif card_type == "weapon":
                    self.take_weapon(card_value)
                elif card_type == "potion":
                    self.take_potion(card_value)
                self.room.remove(picked)
            return self.room
        else:
            self.pick_card()

    def take_weapon(self, card_value):
        self.weapon = card_value
        self.last_killed_w_weapon = 20

    def kill_monster(self, card_value):
        if self.weapon != 0 and card_value <= self.last_killed_w_weapon:
            dmg = card_value - self.weapon
            self.last_killed_w_weapon = card_value
            if dmg <= 0:
                dmg = 0
            self.health -= dmg
        else:
            dmg = card_value
            self.health -= dmg

    def take_potion(self, card_value):
        if self.potions_taken_this_turn == False:
            self.health += card_value
            self.potions_taken_this_turn = True
            if self.health > 20:
                self.health = 20
        else:
            print("already took a potion this turn")

    def make_a_deck(self):
        for item in self.weapons:
            self.deck_of_cards.append(item)
        for item in self.monsters:
            self.deck_of_cards.append(item)
        for item in self.potions:
            self.deck_of_cards.append(item)

    def make_a_room(self):
        while len(self.room) < 4:
            picked_card = random.choice(self.deck_of_cards)
            self.room.append(picked_card)
            self.deck_of_cards.remove(picked_card)

        return sorted(self.room)

    def print_current_room(self):
        print(f"_" * 15)
        if self.avoided_prev_room == False:
            for i, item in enumerate(self.room):
                print(f"{i+1}) {self.room[i]}")
            print(f"\n{len(self.room) + 1}) skip")
        else:
            for i, item in enumerate(self.room):
                print(f"{i+1}) {self.room[i]}")
            print(f"\ncannot skip this turn")
        print(f"_" * 15)
        return sorted(self.room)

    def check_end(self):
        if self.turn_count <= 0:
            self.end_game_status = True
            print("win")
        elif self.health <= 0:
            self.end_game_status = True
            print("lost")
        else:
            self.print_statusbar()

    def print_statusbar(self):
        print(f"_" * 41)
        print(
            f"| health: {self.health}, weapon: {self.weapon}, rooms left: {self.turn_count} |"
        )
        print(f"-" * 41)

    def clear_console(self):
        os.system("cls" if os.name == "nt" else "clear")


def main():
    player = Player()
    player.make_a_deck()
    while player.end_game_status == False:
        player.avoided_prev_room = False
        player.potions_taken_this_turn = False
        player.make_a_room()
        for i in range(len(player.room) - 1):
            player.print_current_room()
            player.pick_card()
            player.check_end()
            # player.clear_console()
            if player.end_game_status == True:
                break
            if player.avoided_prev_room == True:
                continue

        player.turn_count -= 1


if __name__ == "__main__":
    main()


# TODO:
# fix weapon
# fix turn count decreasing with multiple skips
