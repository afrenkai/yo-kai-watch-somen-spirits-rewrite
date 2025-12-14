from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class InspiritEffect(BaseModel):
    EffectDesc: str
    GenericEffectID: str
    Target: str
    Tier: Optional[int] = None


class Inspirit(BaseModel):
    id: str  # Hex ID from JS
    command: str  # The inspirit name
    effects: List[InspiritEffect]  # Array of effects
    image: Optional[str] = None
    
    class Config:
        from_attributes = True

