from pydantic import BaseModel
from typing import Optional


class Equipment(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    str_bonus: Optional[str] = None  # String like "+10" or "-5"
    spr_bonus: Optional[str] = None
    def_bonus: Optional[str] = None
    spd_bonus: Optional[str] = None
    image: Optional[str] = None
    
    class Config:
        from_attributes = True
