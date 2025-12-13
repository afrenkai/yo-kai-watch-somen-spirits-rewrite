from pydantic import BaseModel
from typing import Optional


class Soultimate(BaseModel):
    id: int
    code: str
    name: str
    bp: int  # Base power
    hits: int
    targets: str
    attribute: str
    effect: Optional[str] = None  # Additional effects
    
    class Config:
        from_attributes = True
