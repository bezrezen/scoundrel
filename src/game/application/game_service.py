from src.game.domain.player import Player

class GameService:
    """Оркестратор бизнес-логики."""
    
    def __init__(self):
        self.player = Player()

    def start_turn(self):
        """Начать новый ход."""
        if self.player.end_game_status:
            return {"error": "Game already ended"}
        self.player.start_turn()
        return self.get_game_state()

    def pick_card(self, index: int):
        """Выбрать карту."""
        if self.player.end_game_status:
            return {"error": "Game already ended"}
        if self.player.pick_counter <= 0:
            return {"error": "No picks left"}
            
        try:
            self.player.apply_pick(index)
            result = self.player.check_end()
            if result:
                return {"game_ended": result, "state": self.get_game_state()}
            if self.player.pick_counter <= 0:
                self.player.rooms_passed += 1
                return {"turn_ended": True, "state": self.get_game_state()}
            return {"state": self.get_game_state()}
        except ValueError as e:
            return {"error": str(e)}

    def skip_room(self):
        """Пропустить комнату."""
        if self.player.end_game_status:
            return {"error": "Game already ended"}
        if not self.player.can_skip():
            return {"error": "Cannot skip"}
        
        if self.player.skip_room():
            self.player.rooms_passed += 1
            return {"skipped": True, "state": self.get_game_state()}
        return {"error": "Skip failed"}

    def toggle_debug(self):
        self.player.switch_debug()
        return self.get_game_state()

    def get_game_state(self):
        """Текущее состояние игры."""
        return {
            "health": self.player.health,
            "rooms_passed": self.player.rooms_passed,
            "weapon": self.player.weapon,
            "pick_counter": self.player.pick_counter,
            "score": self.player.score,
            "debug_mode": self.player.debug_mode,
            "can_skip": self.player.can_skip(),
            "room": [
                {"type": c.type, "name": c.name, "value": c.value} 
                for c in self.player.room
            ],
            "game_ended": self.player.end_game_status
        }