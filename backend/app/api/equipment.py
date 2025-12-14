from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class EquipmentResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    str_bonus: str | None = None
    spr_bonus: str | None = None
    def_bonus: str | None = None
    spd_bonus: str | None = None
    image: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[EquipmentResponse])
def get_all_equipment(skip: int = 0, limit: int = 100):
    """Get all equipment items"""
    with get_db() as db:
        query = f"SELECT * FROM equipment LIMIT {limit} OFFSET {skip}"
        result = db.execute(query).fetchall()
        columns = [desc[0] for desc in db.description]
        equipment = [dict(zip(columns, row)) for row in result]
        
        return equipment


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(equipment_id: int):
    """Get a specific equipment item by ID"""
    with get_db() as db:
        result = db.execute("SELECT * FROM equipment WHERE id = ?", [equipment_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Equipment not found")
        
        columns = [desc[0] for desc in db.description]
        equipment = dict(zip(columns, result))
        
        return equipment


@router.get("/name/{equipment_name}", response_model=EquipmentResponse)
def get_equipment_by_name(equipment_name: str):
    """Get a specific equipment item by name"""
    with get_db() as db:
        result = db.execute("SELECT * FROM equipment WHERE name = ?", [equipment_name]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Equipment not found")
        
        columns = [desc[0] for desc in db.description]
        equipment = dict(zip(columns, result))
        
        return equipment
