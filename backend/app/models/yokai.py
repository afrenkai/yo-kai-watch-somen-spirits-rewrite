from pydantic import BaseModel, Field
from typing import Optional


class Yokai(BaseModel):
    id: int
    code: str
    name: str
    rank: str  # E, D, C, B, A, S
    tribe: str  # Brave, Mysterious, Tough, Charming, Heartful, Shady, Eerie, Slippery
    attribute: str
    
    # Stats
    hp: int
    str_stat: int  # Strength
    spr_stat: int  # Spirit
    def_stat: int  # Defense
    spd_stat: int  # Speed
    
    # Skills
    attack_id: int
    technique_id: Optional[int] = None
    inspirit_id: Optional[int] = None
    soultimate_id: int
    skill_id: Optional[int] = None
    
    # Resistances
    fire_res: float = 1.0
    water_res: float = 1.0
    lightning_res: float = 1.0
    earth_res: float = 1.0
    wind_res: float = 1.0
    ice_res: float = 1.0
    
    # Action probabilities
    prob_attack: float = 0.5
    prob_technique: float = 0.2
    prob_inspirit: float = 0.15
    prob_guard: float = 0.1
    prob_loaf: float = 0.05
    tier: Optional[str] = None  # OU, UU, RU, etc. keeping optional but realistically should be not null
    
    class Config:
        from_attributes = True
