import random


class Player:
    def __init__(self):
        self.health = 20
        self.turn_count = 11
        self.weapon = 0
        self.last_killed_w_weapon = None
        self.avoided_prev_room = False
        self.potions_taken_this_turn = False
        self.end_game_status = 0
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
        self.weapons = ["weapon 10", "weapon 9", "weapon 8", "weapon 7", "weapon 6", "weapon 5", "weapon 4", "weapon 3", "weapon 2"]
        self.potions = ["potion 10", "potion 9", "potion 8", "potion 7", "potion 6", "potion 5", "potion 4", "potion 3", "potion 2"]
        self.room = []

    def pick_card(self, card, room):
        if card == "skip":
            if self.avoided_prev_room == False:
                self.avoided_prev_room = True
            else:
                print("you cannot skip")
            return 0
        else:
            picked = room[int(card)]
            print(picked)
            if picked.split()[0] == "monster":
                self.kill_monster(picked)
            elif picked.split()[0] == "weapon":
                self.take_weapon(picked)
            elif picked.split()[0] == "potion":
                self.take_potion(picked)
            room.remove(picked)       

    def take_weapon(self, card):
        self.weapon = int(card.split()[-1])

    def kill_monster(self, card):
        dmg = int(card.split()[-1]) - self.weapon
        if dmg <= 0:
            dmg = 0
        self.health -= dmg

    def take_potion(self, card):
        self.health += int(card.split()[-1])
        if self.health > 20:
            self.health = 20

    def skip_room(self):
        self.avoided_prev_room = True
   

    def make_a_deck(self, whole_deck, weapons, monsters, potions):
        for item in weapons:
            whole_deck.append(item)
        for item in monsters:
            whole_deck.append(item)
        for item in potions:
            whole_deck.append(item)
        self.deck_of_cards = whole_deck
        return whole_deck


    def make_a_room(self, deck, room):
        for i in range(4):
            picked_card = random.choice(deck)
            room.append(picked_card)
            deck.remove(picked_card)
        self.turn_count -= 1
        return room
        
    
    def print_surrent_room(self, room):
        if self.avoided_prev_room == False:
            print(f"Room: {room} or skip?")
        else:
            print(f"Room: {room} cannot skip this turn")
        return room

    
    def clean_room(self):
        self.room = []

    def check_end(self, end_game_status):
        if self.turn_count <= 0:
            self.end_game_status = 1
            print("win")
        elif self.health <=0:
            self.end_game_status = 1
            print("lost")
        return self.end_game_status

    def print_statusbar(self):
        print(f"health: {self.health}, weapon: {self.weapon}, rooms left: {self.turn_count}")
    

def main():
    player = Player()
    deck = player.make_a_deck(player.deck_of_cards, player.weapons, player.monsters, player.potions)
    while player.end_game_status != 1:
        room = player.make_a_room(deck, player.room)
        for i in range(len(room)):
            player.check_end(player.end_game_status)
            player.print_surrent_room(room)
            players_choice = input("take turn: ")
            player.pick_card(players_choice, room)
            
            player.clean_room()
            player.print_statusbar()



if __name__ == "__main__":
    main()

