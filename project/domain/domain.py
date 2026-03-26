import random

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
            ["monster", "♠ demigod", 14], ["monster", "♣ demigod", 14],
            ["monster", "♠ dragon", 13],  ["monster", "♣ dragon", 13],
            ["monster", "♠ wyrm", 12],    ["monster", "♣ wyrm", 12],
            ["monster", "♠ giant", 11],   ["monster", "♣ giant", 11],
            ["monster", "♠ troll", 10],   ["monster", "♣ troll", 10],
            ["monster", "♠ shade", 9],    ["monster", "♣ shade", 9],
            ["monster", "♠ bear", 8],     ["monster", "♣ bear", 8],
            ["monster", "♠ orc", 7],      ["monster", "♣ orc", 7],
            ["monster", "♠ hobgoblin", 6],["monster", "♣ hobgoblin", 6],
            ["monster", "♠ goblin", 5],   ["monster", "♣ goblin", 5],
            ["monster", "♠ kobold", 4],   ["monster", "♣ kobold", 4],
            ["monster", "♠ snake", 3],    ["monster", "♣ snake", 3],
            ["monster", "♠ rat", 2],      ["monster", "♣ rat", 2],
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

    # --- чистая игровая логика, без input/print ---

    def make_deck(self):
        self.deck_of_cards = self.weapons + self.monsters + self.potions
        random.shuffle(self.deck_of_cards)

    def make_room(self):
        while len(self.room) < 4 and self.deck_of_cards:
            card = self.deck_of_cards.pop(0)
            self.room.append(card)

    def can_skip(self) -> bool:
        return not self.avoided_prev_room and not self.any_cards_picked

    def apply_pick(self, index: int):
        """Применить выбор карты по индексу в self.room (0-based)."""
        picked = self.room[index]
        card_type, _, card_value = picked
        card_value = int(card_value)

        self.any_cards_picked = True
        self.pick_counter -= 1

        if card_type == "monster":
            self._kill_monster(card_value)
        elif card_type == "weapon":
            self._take_weapon(card_value)
        elif card_type == "potion":
            self._take_potion(card_value)

        self.room.pop(index)

    def skip_room(self):
        """Бизнес-логика скипа: запрет двух подряд и перенос карт назад в колоду."""
        if self.avoided_prev_room:
            return False  # нельзя скипнуть

        self.avoided_prev_room = True
        self.deck_of_cards.extend(self.room)
        self.room.clear()
        self.pick_counter = 3
        return True

    def _take_weapon(self, value: int):
        self.weapon = value
        self.last_killed_w_weapon = 20

    def _kill_monster(self, value: int):
        if self.weapon != 0 and value <= self.last_killed_w_weapon:
            dmg = value - self.weapon
            self.last_killed_w_weapon = value
            if dmg < 0:
                dmg = 0
            self.health -= dmg
        else:
            self.health -= value

    def _take_potion(self, value: int):
        if not self.potions_taken_this_turn:
            new_health = self.health + value
            self.potions_taken_this_turn = True
            if not self.debug_mode:
                self.health = min(20, new_health)
            else:
                self.health = new_health

    def debug(self):
        if self.debug_mode == False:
            self.health = 999
            self.debug_mode = True
        elif self.debug_mode == True:
            self.debug_mode = False

    def check_end(self):
        if len(self.deck_of_cards) <= 0:
            self.end_game_status = True
            return "win"
        if self.health <= 0:
            self.end_game_status = True
            return "lost"
        return None