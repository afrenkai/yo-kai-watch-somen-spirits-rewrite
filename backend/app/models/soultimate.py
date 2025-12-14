from pydantic import BaseModel
from typing import Optional


class Soultimate(BaseModel):
    id: str  # Hex ID from json
    command: str
    lv1_power: Optional[int] = None
    lv10_power: Optional[int] = None
    lv1_soul_charge: Optional[int] = None
    lv10_soul_charge: Optional[int] = None
    n_hits: int = 1
    element: Optional[str] = None
    extra: Optional[str] = None
    
    class Config:
        from_attributes = True

