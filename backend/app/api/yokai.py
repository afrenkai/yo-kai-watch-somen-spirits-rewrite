from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class YokaiResponse(BaseModel):
    id: str
    name: str
    image: str | None = None
    bs_a_hp: int
    bs_a_str: int
    bs_a_spr: int
    bs_a_def: int
    bs_a_spd: int
    bs_b_hp: int
    bs_b_str: int
    bs_b_spr: int
    bs_b_def: int
    bs_b_spd: int
    fire_res: float
    water_res: float
    electric_res: float
    earth_res: float
    wind_res: float
    ice_res: float
    equipment_slots: int
    attack_prob: float
    attack_id: str
    technique_prob: float
    technique_id: str | None = None
    inspirit_prob: float
    inspirit_id: str | None = None
    guard_prob: float
    soultimate_id: str
    skill_id: int | None = None
    rank: str
    tribe: str
    artwork_image: str | None = None
    tier: str | None = None
    extra: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[YokaiResponse])
def get_all_yokai(
    skip: int = 0,
    limit: int = 1000,  # Increased from 100 to fetch all yokai at once
    tribe: str | None = None,
    rank: str | None = None,
    tier: str | None = None
):
    """Get all Yo-kai with optional filtering"""
    with get_db() as db:
        query = "SELECT * FROM yokai WHERE 1=1"
        params = []
        
        if tribe:
            query += " AND tribe = ?"
            params.append(tribe)
        if rank:
            query += " AND rank = ?"
            params.append(rank)
        if tier:
            query += " AND tier = ?"
            params.append(tier)
        
        # Add ORDER BY for consistent results
        query += " ORDER BY id"
        query += f" LIMIT {limit} OFFSET {skip}"
        
        result = db.execute(query, params).fetchall()
        columns = [desc[0] for desc in db.description]
        yokai_list = [dict(zip(columns, row)) for row in result]
        
        return yokai_list


@router.get("/{yokai_id}", response_model=YokaiResponse)
def get_yokai(yokai_id: str):
    with get_db() as db:
        result = db.execute("SELECT * FROM yokai WHERE id = ?", [yokai_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Yokai not found")
        
        columns = [desc[0] for desc in db.description]
        yokai = dict(zip(columns, result))
        
        return yokai


@router.get("/name/{yokai_name}", response_model=YokaiResponse)
def get_yokai_by_name(yokai_name: str):
    with get_db() as db:
        result = db.execute("SELECT * FROM yokai WHERE name = ?", [yokai_name]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Yokai not found")
        
        columns = [desc[0] for desc in db.description]
        yokai = dict(zip(columns, result))
        
        return yokai
