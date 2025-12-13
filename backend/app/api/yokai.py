from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class YokaiResponse(BaseModel):
    id: int
    name: str
    rank: str
    tribe: str
    hp: int
    str_stat: int
    spr_stat: int
    def_stat: int
    spd_stat: int
    attack_id: int
    technique_id: int | None
    inspirit_id: int | None
    soultimate_id: int
    skill_id: int | None
    favorite_food: str | None
    image_url: str | None
    description: str | None
    tier: str | None
    is_legendary: int
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[YokaiResponse])
def get_all_yokai(
    skip: int = 0,
    limit: int = 100,
    tribe: str | None = None,
    rank: str | None = None,
    tier: str | None = None
):
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
        
        query += f" LIMIT {limit} OFFSET {skip}"
        
        result = db.execute(query, params).fetchall()
        columns = [desc[0] for desc in db.description]
        yokai_list = [dict(zip(columns, row)) for row in result]
        
        return yokai_list


@router.get("/{yokai_id}", response_model=YokaiResponse)
def get_yokai(yokai_id: int):
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
