from pydantic import BaseModel
from typing import Optional


class SoulGem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    
    class Config:
        from_attributes = True
