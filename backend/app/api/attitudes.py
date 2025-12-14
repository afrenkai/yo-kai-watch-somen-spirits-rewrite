from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class AttitudeResponse(BaseModel):
    id: int
    name: str
    boost_hp: int
    boost_str: int
    boost_spr: int
    boost_def: int
    boost_spd: int
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AttitudeResponse])
def get_all_attitudes(skip: int = 0, limit: int = 100):
    """Get all attitudes"""
    with get_db() as db:
        query = f"SELECT * FROM attitudes LIMIT {limit} OFFSET {skip}"
        result = db.execute(query).fetchall()
        columns = [desc[0] for desc in db.description]
        attitudes = [dict(zip(columns, row)) for row in result]
        
        return attitudes


@router.get("/{attitude_id}", response_model=AttitudeResponse)
def get_attitude(attitude_id: int):
    """Get a specific attitude by ID"""
    with get_db() as db:
        result = db.execute("SELECT * FROM attitudes WHERE id = ?", [attitude_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Attitude not found")
        
        columns = [desc[0] for desc in db.description]
        attitude = dict(zip(columns, result))
        
        return attitude


@router.get("/name/{attitude_name}", response_model=AttitudeResponse)
def get_attitude_by_name(attitude_name: str):
    """Get a specific attitude by name"""
    with get_db() as db:
        result = db.execute("SELECT * FROM attitudes WHERE name = ?", [attitude_name]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Attitude not found")
        
        columns = [desc[0] for desc in db.description]
        attitude = dict(zip(columns, result))
        
        return attitude
