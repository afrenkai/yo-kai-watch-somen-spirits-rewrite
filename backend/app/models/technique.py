from pydantic import BaseModel


class Technique(BaseModel):
    id: int
    code: str
    name: str
    bp: int  # Base power
    hits: int
    targets: str
    attribute: str
    move_type: str
    
    class Config:
        from_attributes = True
