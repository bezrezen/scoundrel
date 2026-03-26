import random
import os
import sys
from prettytable import PrettyTable


class Player:
    def __init__(self):
        self.health = 20
        self.rooms_passed = 0
        self.weapon = 0
        self.last_killed_w_weapon = 20
        self.avoided_prev_room = False
        self.potions_taken_this_turn = False
        self.end_game_status = False
        self.any_cards_picked = False
        self.debug_mode = False
        self.pick_counter = 3
        self.deck_of_cards = []
        self.monsters = [
            ["monster", "♠ demigod", 14],["monster", "♣ demigod", 14],
            ["monster", "♠ dragon", 13], ["monster", "♣ dragon", 13],
            ["monster", "♠ wyrm", 12], ["monster", "♣ wyrm", 12],
            ["monster", "♠ giant", 11], ["monster", "♣ giant", 11],
            ["monster", "♠ troll", 10], ["monster", "♣ troll", 10],
            ["monster", "♠ shade", 9], ["monster", "♣ shade", 9],
            ["monster", "♠ bear", 8], ["monster", "♣ bear", 8],
            ["monster", "♠ orc", 7], ["monster", "♣ orc", 7],
            ["monster", "♠ hobgoblin", 6], ["monster", "♣ hobgoblin", 6],
            ["monster", "♠ goblin", 5], ["monster", "♣ goblin", 5],
            ["monster", "♠ kobold", 4], ["monster", "♣ kobold", 4],
            ["monster", "♠ snake", 3], ["monster", "♣ snake", 3],   
            ["monster", "♠ rat", 2], ["monster", "♣ rat", 2]
        ]
        self.weapons = [
            ["weapon", "♦ Divine sword", 10],
            ["weapon", "♦ Halberd", 9],
            ["weapon", "♦ Falscion", 8],
            ["weapon", "♦ Broadsword", 7],
            ["weapon", "♦ Spear", 6],
            ["weapon", "♦ Axe", 5],
            ["weapon", "♦ Dagger", 4],
            ["weapon", "♦ Club", 3],
            ["weapon", "♦ Fork", 2],
        ]
        self.potions = [
            ["potion", "♥ Health potion", 10],
            ["potion", "♥ Health potion", 9],
            ["potion", "♥ Health potion", 8],
            ["potion", "♥ Health potion", 7],
            ["potion", "♥ Health potion", 6],
            ["potion", "♥ Health potion", 5],
            ["potion", "♥ Health potion", 4],
            ["potion", "♥ Health potion", 3],
            ["potion", "♥ Health potion", 2],
        ]
        self.room = []

    def pick_card(self):
        avaible_answers = [str(i + 1) for i in range(len(self.room))]
        avaible_answers.append("s")
        avaible_answers.append("debug")
        while True:
            card = input("pick a card: ")
            if card == "s" and self.any_cards_picked == False:
                self.skip_room()
                return
            elif card == "s" and self.any_cards_picked == True:
                print("you already picked a card and cannot skip for the rest of your turn")
            elif card in avaible_answers[:-2]:
                picked = self.room[int(card) - 1]
                card_type = picked[0]
                card_value = picked[2]
                self.any_cards_picked = True
                self.pick_counter -= 1
                if card_type == "monster":
                    self.kill_monster(card_value)
                elif card_type == "weapon":
                    self.take_weapon(card_value)
                elif card_type == "potion":
                    self.take_potion(card_value)
                self.room.remove(picked)
                return
            elif card == "debug":
                self.debug_mode = True
                self.debug()
                return
            else:
                print("incorrect pick. try again")

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
            new_health = self.health + card_value
            self.potions_taken_this_turn = True
            if new_health > 20 and self.debug_mode != True:
                self.health = 20
            elif new_health <= 20 and self.debug_mode != True:
                self.health = new_health
            else:
                self.health = 999
        else:
            print("already took a potion this turn")

    def make_a_deck(self):
        for item in self.weapons:
            self.deck_of_cards.append(item)
        for item in self.monsters:
            self.deck_of_cards.append(item)
        for item in self.potions:
            self.deck_of_cards.append(item)
        random.shuffle(self.deck_of_cards)

    def make_a_room(self):
        while len(self.room) < 4:
            put_card_in_room = self.deck_of_cards[0]
            self.room.append(put_card_in_room)
            self.deck_of_cards.remove(put_card_in_room)

        return sorted(self.room)
    
    def skip_room(self):
        if self.avoided_prev_room == False:
            self.avoided_prev_room = True
            for item in self.room:
                self.deck_of_cards.append(item)
            self.room = []
            self.make_a_room()
            self.pick_counter = 3
        else:
            print("you cannot skip")

    def print_current_room(self):
        current_room = PrettyTable()
        for i, item in enumerate(self.room):
                current_room.add_column(f"{i+1}", [self.room[i]])
        print(current_room)
        if self.avoided_prev_room == False:
            print(f"s) skip")
        else:      
            print(f"\ncannot skip this turn")
        return sorted(self.room)

    def check_end(self):
        if len(self.deck_of_cards) <= 0:
            self.end_game_status = True
            print("win")
        elif self.health <= 0:
            self.end_game_status = True
            print("lost")
        else:
            return

    def clear_console(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_grafic(self):
        self.clear_console()
        current_room = PrettyTable()
        current_room.max_table_width = 80
        current_room.min_table_width = 80
        status_bar = PrettyTable()
        status_bar.max_table_width = 80
        status_bar.min_table_width = 80
        for i, item in enumerate(self.room):
                current_room.add_column(f"{i+1}", [f"{self.room[i][1]}\n{self.room[i][2]}"])
        current_room.add_column("s",["Cant\nskip"] 
                                if self.avoided_prev_room == True or self.any_cards_picked == True 
                                else ["Can\nskip"])
        
        status_bar.add_column("Health",[self.health])
        status_bar.add_column("Can pick potion", ["Yes" if self.potions_taken_this_turn == False else "No"])
        status_bar.add_column("Weapon",[self.weapon])
        status_bar.add_column("Last killed",[0 if self.last_killed_w_weapon == 20 else self.last_killed_w_weapon])
        status_bar.add_column("Rooms passed", [self.rooms_passed])
        
        print(status_bar)
        print(current_room)

    def debug(self):
        self.health = 999



def main():
    player = Player()
    player.make_a_deck()
    while player.end_game_status == False:
        player.avoided_prev_room = False
        player.potions_taken_this_turn = False
        player.any_cards_picked = False
        player.make_a_room()
        player.pick_counter = 3
        while player.pick_counter > 0:
            player.print_grafic()
            try:
                player.pick_card()
            except KeyboardInterrupt, EOFError:
                print("ended by user")
                player.end_game_status = True
                break
            player.check_end()
            if player.end_game_status == True:
                break
            if player.avoided_prev_room == True:
                continue
        player.rooms_passed += 1


if __name__ == "__main__":
    main()
