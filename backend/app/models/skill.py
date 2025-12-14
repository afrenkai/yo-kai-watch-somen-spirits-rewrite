from pydantic import BaseModel


class Skill(BaseModel):
    id: int
    name: str
    description: str
    
    class Config:
        from_attributes = True

