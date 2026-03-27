# src/scoundrel_game/adapters/dtos/game_state.py
from pydantic import BaseModel
from typing import List, Dict, Any

class GameStateDTO(BaseModel):
    health: int
    rooms_passed: int
    weapon: int
    pick_counter: int
    score: int
    debug_mode: bool
    can_skip: bool
    room: List[Dict[str, Any]]
    game_ended: bool