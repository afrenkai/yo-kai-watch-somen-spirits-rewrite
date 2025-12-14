from pydantic import BaseModel


class Attitude(BaseModel):
    id: int
    name: str
    boost_hp: int = 0
    boost_str: int = 0
    boost_spr: int = 0
    boost_def: int = 0
    boost_spd: int = 0
    
    class Config:
        from_attributes = True
