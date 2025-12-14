from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class SkillResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[SkillResponse])
def get_all_skills(skip: int = 0, limit: int = 100):
    """Get all skills"""
    with get_db() as db:
        query = f"SELECT * FROM skills LIMIT {limit} OFFSET {skip}"
        result = db.execute(query).fetchall()
        columns = [desc[0] for desc in db.description]
        skills = [dict(zip(columns, row)) for row in result]
        
        return skills


@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int):
    """Get a specific skill by ID"""
    with get_db() as db:
        result = db.execute("SELECT * FROM skills WHERE id = ?", [skill_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        columns = [desc[0] for desc in db.description]
        skill = dict(zip(columns, result))
        
        return skill


@router.get("/name/{skill_name}", response_model=SkillResponse)
def get_skill_by_name(skill_name: str):
    """Get a specific skill by name"""
    with get_db() as db:
        result = db.execute("SELECT * FROM skills WHERE name = ?", [skill_name]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        columns = [desc[0] for desc in db.description]
        skill = dict(zip(columns, result))
        
        return skill
