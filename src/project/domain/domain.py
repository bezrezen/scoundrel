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
            ["monster", "o(｀ω´ )o", 14], ["monster", "o(｀ω´ )o", 14],
            ["monster", "o(｀ω´ )o", 13],  ["monster", "o(｀ω´ )o", 13],
            ["monster", "o(｀ω´ )o", 12],    ["monster", "o(｀ω´ )o", 12],
            ["monster", "o(｀ω´ )o", 11],   ["monster", "o(｀ω´ )o", 11],
            ["monster", "o(｀ω´ )o", 10],   ["monster", "o(｀ω´ )o", 10],
            ["monster", "o(｀ω´ )o", 9],    ["monster", "o(｀ω´ )o", 9],
            ["monster", "o(｀ω´ )o", 8],     ["monster", "o(｀ω´ )o", 8],
            ["monster", "o(｀ω´ )o", 7],      ["monster", "o(｀ω´ )o", 7],
            ["monster", "o(｀ω´ )o", 6],["monster", "o(｀ω´ )o", 6],
            ["monster", "o(｀ω´ )o", 5],   ["monster", "o(｀ω´ )o", 5],
            ["monster", "o(｀ω´ )o", 4],   ["monster", "o(｀ω´ )o", 4],
            ["monster", "o(｀ω´ )o", 3],    ["monster", "o(｀ω´ )o", 3],
            ["monster", "o(｀ω´ )o", 2],      ["monster", "o(｀ω´ )o", 2],
        ]
        self.weapons = [
            ["weapon", "+=={::::::::::::>", 10],
            ["weapon", "+=={::::::::::::>", 9],
            ["weapon", "+=={::::::::::::>", 8],
            ["weapon", "+=={::::::::::::>", 7],
            ["weapon", "+=={::::::::::::>", 6],
            ["weapon", "+=={::::::::::::>", 5],
            ["weapon", "+=={::::::::::::>", 4],
            ["weapon", "+=={::::::::::::>", 3],
            ["weapon", "+=={::::::::::::>", 2],
        ]
        self.potions = [
            ["potion", "🧪", 10],
            ["potion", "🧪", 9],
            ["potion", "🧪", 8],
            ["potion", "🧪", 7],
            ["potion", "🧪", 6],
            ["potion", "♥ Health potion 🧪", 5],
            ["potion", "♥ Health potion 🧪", 4],
            ["potion", "♥ Health potion 🧪", 3],
            ["potion", "♥ Health potion 🧪", 2],
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

    def switch_debug(self):
        if not self.debug_mode:
            self.health = 999
        self.debug_mode = not self.debug_mode

    def check_end(self):
        if len(self.deck_of_cards) <= 0:
            self.end_game_status = True
            return "win"
        if self.health <= 0:
            self.end_game_status = True
            return "lost"
        return None