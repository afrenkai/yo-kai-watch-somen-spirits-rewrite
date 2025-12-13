from pydantic import BaseModel


class Attack(BaseModel):
    id: int
    code: str
    name: str
    bp: int  # Base power
    hits: int
    targets: str
    attribute: str
    
    class Config:
        from_attributes = True
