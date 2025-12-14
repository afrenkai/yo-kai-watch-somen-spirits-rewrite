from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class SoultimateResponse(BaseModel):
    id: str
    command: str
    lv1_power: int | None = None
    lv10_power: int | None = None
    lv1_soul_charge: int
    lv10_soul_charge: int
    n_hits: int
    element: str | None = None
    extra: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[SoultimateResponse])
def get_all_soultimates(
    skip: int = 0,
    limit: int = 100,
    element: str | None = None
):
    with get_db() as db:
        query = "SELECT * FROM soultimate WHERE 1=1"
        params = []
        
        if element:
            query += " AND element = ?"
            params.append(element)
        
        query += f" LIMIT {limit} OFFSET {skip}"
        
        result = db.execute(query, params).fetchall()
        columns = [desc[0] for desc in db.description]
        soultimates = [dict(zip(columns, row)) for row in result]
        
        return soultimates


@router.get("/{soultimate_id}", response_model=SoultimateResponse)
def get_soultimate(soultimate_id: str):
    """Get a specific soultimate by ID"""
    with get_db() as db:
        result = db.execute("SELECT * FROM soultimate WHERE id = ?", [soultimate_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Soultimate not found")
        
        columns = [desc[0] for desc in db.description]
        soultimate = dict(zip(columns, result))
        
        return soultimate
