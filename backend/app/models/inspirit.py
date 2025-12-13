from pydantic import BaseModel
from typing import Optional


class Inspirit(BaseModel):
    id: int
    code: str
    name: str
    effect: str  # Confusion, StatDown, StatUp, Drain, etc.
    power: Optional[int] = None
    duration: int  # Number of turns
    targets: str
    
    class Config:
        from_attributes = True
