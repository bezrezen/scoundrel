# src/scoundrel_game/interfaces/api/fastapi_app.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.game.application.game_service import GameService

from src.game.adapters.controllers.game_controller import GameController
from src.game.adapters.dtos.pick_request import PickRequest

app = FastAPI(title="Scoundrel Game API")

# Dependency Injection — создаём сервисы
game_service = GameService()
controller = GameController(game_service)

# Монтируем статику
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()
 
@app.get("/api/game/state")
async def get_state():
    return controller.game_service.get_game_state()

@app.post("/api/game/start-turn")
async def start_turn():
    result = controller.start_turn()
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/game/pick")
async def pick_card(request: PickRequest):
    result = controller.pick_action(request)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result