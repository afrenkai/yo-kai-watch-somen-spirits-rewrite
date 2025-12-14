from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class SoulGemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    image: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[SoulGemResponse])
def get_all_soul_gems(skip: int = 0, limit: int = 100):
    """Get all soul gems"""
    with get_db() as db:
        query = f"SELECT * FROM soul_gems LIMIT {limit} OFFSET {skip}"
        result = db.execute(query).fetchall()
        columns = [desc[0] for desc in db.description]
        soul_gems = [dict(zip(columns, row)) for row in result]
        
        return soul_gems


@router.get("/{soul_gem_id}", response_model=SoulGemResponse)
def get_soul_gem(soul_gem_id: int):
    with get_db() as db:
        result = db.execute("SELECT * FROM soul_gems WHERE id = ?", [soul_gem_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Soul gem not found")
        
        columns = [desc[0] for desc in db.description]
        soul_gem = dict(zip(columns, result))
        
        return soul_gem


@router.get("/name/{soul_gem_name}", response_model=SoulGemResponse)
def get_soul_gem_by_name(soul_gem_name: str):
    with get_db() as db:
        result = db.execute("SELECT * FROM soul_gems WHERE name = ?", [soul_gem_name]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Soul gem not found")
        
        columns = [desc[0] for desc in db.description]
        soul_gem = dict(zip(columns, result))
        
        return soul_gem
