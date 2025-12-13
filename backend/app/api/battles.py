from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel
from datetime import datetime
import json


router = APIRouter()


class BattleResponse(BaseModel):
    id: int
    player1_id: int
    player2_id: int
    team1_id: int
    team2_id: int
    winner_id: int | None
    duration: int | None
    turns: int
    status: str
    created_at: str
    started_at: str | None
    ended_at: str | None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[BattleResponse])
def get_battles(
    skip: int = 0,
    limit: int = 50,
    user_id: int | None = None,
    status: str | None = None
):
    with get_db() as db:
        query = "SELECT * FROM battles WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND (player1_id = ? OR player2_id = ?)"
            params.extend([user_id, user_id])
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += f" ORDER BY created_at DESC LIMIT {limit} OFFSET {skip}"
        
        result = db.execute(query, params).fetchall()
        
        columns = [desc[0] for desc in db.description]
        battles = [dict(zip(columns, row)) for row in result]
        
        return battles


@router.get("/{battle_id}", response_model=BattleResponse)
def get_battle(battle_id: int):
    with get_db() as db:
        result = db.execute(
            "SELECT * FROM battles WHERE id = ?",
            [battle_id]
        ).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Battle not found")
        
        columns = [desc[0] for desc in db.description]
        battle = dict(zip(columns, result))
        
        return battle


@router.get("/{battle_id}/log")
def get_battle_log(battle_id: int):
    with get_db() as db:
        result = db.execute(
            "SELECT id, battle_log, duration, turns FROM battles WHERE id = ?",
            [battle_id]
        ).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Battle not found")
        
        battle_log = json.loads(result[1]) if result[1] else []
        
        return {
            "battle_id": result[0],
            "log": battle_log,
            "duration": result[2],
            "turns": result[3]
        }
