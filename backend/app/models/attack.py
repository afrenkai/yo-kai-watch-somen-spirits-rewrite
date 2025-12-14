from pydantic import BaseModel
from typing import Optional


class Attack(BaseModel):
    id: str  # Hex ID from json e.g., "0x1B8F94AB"
    command: str  # The attack name
    lv1_power: Optional[int] = None  # Power at level 1
    lv10_power: Optional[int] = None  # Power at level 10
    n_hits: int = 1  # Number of hits
    element: Optional[str] = None  # Element type (Fire, Water, etc.) or None for physical
    extra: Optional[str] = None
    
    class Config:
        from_attributes = True

