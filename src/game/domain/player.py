from dataclasses import dataclass
from typing import List, Optional
import random

@dataclass
class Card:
    type: str      # "monster", "weapon", "potion"
    name: str
    value: int

@dataclass
class Player:
    health: int = 20
    rooms_passed: int = 0
    weapon: int = 0
    last_killed_w_weapon: int = 20
    avoided_prev_room: bool = False
    potions_taken_this_turn: bool = False
    end_game_status: bool = False
    any_cards_picked: bool = False
    debug_mode: bool = False
    pick_counter: int = 3
    score: int = 0
    room: List[Card] = None
    deck_of_cards: List[Card] = None

    def __post_init__(self):
        if self.room is None:
            self.room = []
        if self.deck_of_cards is None:
            self.make_deck()

    def make_deck(self):
        """Создаёт колоду из монстров, оружия, зелий."""
        monsters = [
            Card("monster", "😈", i) for i in [14,14,13,13,12,12,11,11,10,10,9,9,8,8,7,7,6,6,5,5,4,4,3,3,2,2]
        ]
        weapons = [Card("weapon", "🗡️", i) for i in [10,9,8,7,6,5,4,3,2]]
        potions = [Card("potion", "💙", i) for i in [10,9,8,7,6,5,4,3,2]]
        
        self.deck_of_cards = monsters + weapons + potions
        random.shuffle(self.deck_of_cards)

    def make_room(self):
        """Создаёт комнату из 4 карт."""
        self.room = []
        while len(self.room) < 4 and self.deck_of_cards:
            self.room.append(self.deck_of_cards.pop(0))

    def can_skip(self) -> bool:
        return not self.avoided_prev_room and not self.any_cards_picked

    def apply_pick(self, index: int):
        """Применяет выбор карты."""
        if not (0 <= index < len(self.room)):
            raise ValueError("Invalid card index")
            
        picked = self.room.pop(index)
        self.any_cards_picked = True
        self.pick_counter -= 1

        if picked.type == "monster":
            self._kill_monster(picked.value)
            self.score += picked.value
        elif picked.type == "weapon":
            self._take_weapon(picked.value)
        elif picked.type == "potion":
            self._take_potion(picked.value)

    def skip_room(self) -> bool:
        if self.avoided_prev_room:
            return False
        self.avoided_prev_room = True
        self.deck_of_cards.extend(self.room)
        self.room = []
        self.pick_counter = 3
        return True

    def _take_weapon(self, value: int):
        self.weapon = value
        self.last_killed_w_weapon = 20

    def _kill_monster(self, value: int):
        if self.weapon != 0 and value <= self.last_killed_w_weapon:
            dmg = max(0, value - self.weapon)
            self.last_killed_w_weapon = value
        else:
            dmg = value
        self.health -= dmg

    def _take_potion(self, value: int):
        if not self.potions_taken_this_turn:
            new_health = self.health + value
            self.potions_taken_this_turn = True
            self.health = min(20, new_health) if not self.debug_mode else 999

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
        self.score += self.rooms_passed
        return None

    def start_turn(self):
        """Начало нового хода."""
        self.avoided_prev_room = False
        self.potions_taken_this_turn = False
        self.any_cards_picked = False
        self.pick_counter = 3
        self.make_room()