from pydantic import BaseModel
from typing import Optional


class Technique(BaseModel):
    id: str  # Hex ID from json
    command: str 
    lv1_power: Optional[int] = None
    lv10_power: Optional[int] = None
    n_hits: int = 1
    element: Optional[str] = None  # Fire, Water, Ice, Lightning, Earth, Wind, Drain, etc.
    extra: Optional[str] = None
    
    class Config:
        from_attributes = True

