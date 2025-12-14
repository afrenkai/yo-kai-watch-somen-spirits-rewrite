from fastapi import APIRouter, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel


router = APIRouter()


class AttackResponse(BaseModel):
    id: str
    command: str
    lv1_power: int | None = None
    lv10_power: int | None = None
    n_hits: int
    element: str | None = None
    extra: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AttackResponse])
def get_all_attacks(
    skip: int = 0,
    limit: int = 100,
    element: str | None = None
):
    with get_db() as db:
        query = "SELECT * FROM attacks WHERE 1=1"
        params = []
        
        if element:
            query += " AND element = ?"
            params.append(element)
        
        query += f" LIMIT {limit} OFFSET {skip}"
        
        result = db.execute(query, params).fetchall()
        columns = [desc[0] for desc in db.description]
        attacks = [dict(zip(columns, row)) for row in result]
        
        return attacks


@router.get("/{attack_id}", response_model=AttackResponse)
def get_attack(attack_id: str):
     with get_db() as db:
        result = db.execute("SELECT * FROM attacks WHERE id = ?", [attack_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Attack not found")
        
        columns = [desc[0] for desc in db.description]
        attack = dict(zip(columns, result))
        
        return attack
