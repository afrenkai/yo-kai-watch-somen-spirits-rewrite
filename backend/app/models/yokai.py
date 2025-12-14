from pydantic import BaseModel, Field
from typing import Optional

#TODO: remove nullility where it obviously doesnt apply (attr)

class Yokai(BaseModel):
    id: str  # The non hex ID from the json (e.g., "001" for pandle)
    name: str
    image: Optional[str] = None
    
    # Base stats (A = at level 1, B = at level 99)
    bs_a_hp: Optional[int] = None
    bs_a_str: Optional[int] = None
    bs_a_spr: Optional[int] = None
    bs_a_def: Optional[int] = None
    bs_a_spd: Optional[int] = None
    bs_b_hp: Optional[int] = None
    bs_b_str: Optional[int] = None
    bs_b_spr: Optional[int] = None
    bs_b_def: Optional[int] = None
    bs_b_spd: Optional[int] = None

    fire_res: float = 1.0
    water_res: float = 1.0
    electric_res: float = 1.0
    earth_res: float = 1.0
    wind_res: float = 1.0
    ice_res: float = 1.0
    
    equipment_slots: int = 1
    
    attack_prob: float = 0.5
    attack_id: Optional[str] = None  # Hex ID
    technique_prob: float = 0.2
    technique_id: Optional[str] = None  # Hex ID
    inspirit_prob: float = 0.1
    inspirit_id: Optional[str] = None  # Hex ID
    guard_prob: float = 0.05
    soultimate_id: Optional[str] = None  # Hex ID
    skill_id: Optional[int] = None
    
    rank: Optional[str] = None  # E, D, C, B, A, S
    tribe: Optional[str] = None  # Brave, Mysterious, Tough, Charming, Heartful, Shady, Eerie, Slippery
    artwork_image: Optional[str] = None
    tier: Optional[str] = None  # PU, NU, RU, UU, OU, Uber, etc.
    extra: Optional[str] = None
    
    class Config:
        from_attributes = True

