# src/scoundrel_game/adapters/controllers/game_controller.py
from src.game.application.game_service import GameService
from src.game.adapters.dtos.pick_request import PickRequest
from typing import Dict, Any

class GameController:
    def __init__(self, game_service: GameService):
        self.game_service = game_service  # ← DI!

    def start_turn(self) -> Dict[str, Any]:
        return self.game_service.start_turn()

    def pick_action(self, request: PickRequest) -> Dict[str, Any]:
        if request.action == "debug":
            return self.game_service.toggle_debug()
        elif request.action == "skip":
            return self.game_service.skip_room()
        elif request.action == "card" and request.index is not None:
            return self.game_service.pick_card(request.index)
        raise ValueError("Invalid action")