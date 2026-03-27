# src/scoundrel_game/adapters/dtos/pick_request.py
from pydantic import BaseModel
from typing import Literal, Optional

class PickRequest(BaseModel):
    action: Literal["card", "skip", "debug"]
    index: Optional[int] = None