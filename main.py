# main.py
from src.game.interfaces.api.fastapi_app import app
import uvicorn
# import sys
# from pathlib import Path
# sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    