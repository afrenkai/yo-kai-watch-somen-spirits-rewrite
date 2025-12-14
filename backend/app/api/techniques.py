from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class TechniqueResponse(BaseModel):
    id: str
    command: str
    lv1_power: int | None = None
    lv10_power: int | None = None
    n_hits: int
    element: str | None = None
    extra: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[TechniqueResponse])
def get_all_techniques(
    skip: int = 0,
    limit: int = 100,
    element: str | None = None
):
    """Get all techniques with optional filtering by element"""
    with get_db() as db:
        query = "SELECT * FROM techniques WHERE 1=1"
        params = []
        
        if element:
            query += " AND element = ?"
            params.append(element)
        
        query += f" LIMIT {limit} OFFSET {skip}"
        
        result = db.execute(query, params).fetchall()
        columns = [desc[0] for desc in db.description]
        techniques = [dict(zip(columns, row)) for row in result]
        
        return techniques


@router.get("/{technique_id}", response_model=TechniqueResponse)
def get_technique(technique_id: str):
    """Get a specific technique by ID"""
    with get_db() as db:
        result = db.execute("SELECT * FROM techniques WHERE id = ?", [technique_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Technique not found")
        
        columns = [desc[0] for desc in db.description]
        technique = dict(zip(columns, result))
        
        return technique
