from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.database import get_db
from pydantic import BaseModel
from datetime import datetime
import json


router = APIRouter()


class TeamCreate(BaseModel):
    name: str
    yokai_ids: List[int]
    tier: str = "OU"


class TeamResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    yokai_ids: List[int]
    tier: str
    is_public: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[TeamResponse])
def get_teams(
    skip: int = 0,
    limit: int = 50,
    tier: str | None = None,
    owner_id: int | None = None
):
    with get_db() as db:
        query = "SELECT * FROM teams WHERE is_public = 1"
        params = []
        
        if tier:
            query += " AND tier = ?"
            params.append(tier)
        if owner_id:
            query += " AND owner_id = ?"
            params.append(owner_id)
        
        query += f" LIMIT {limit} OFFSET {skip}"
        
        result = db.execute(query, params).fetchall()
        
        columns = [desc[0] for desc in db.description]
        teams = []
        for row in result:
            team = dict(zip(columns, row))
            team['yokai_ids'] = json.loads(team['yokai_ids'])
            teams.append(team)
        
        return teams


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int):
    with get_db() as db:
        result = db.execute(
            "SELECT * FROM teams WHERE id = ?",
            [team_id]
        ).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Team not found")
        
        columns = [desc[0] for desc in db.description]
        team = dict(zip(columns, result))
        team['yokai_ids'] = json.loads(team['yokai_ids'])
        
        return team


@router.post("/", response_model=TeamResponse)
def create_team(
    team: TeamCreate,
    user_id: int = 1
):
    if len(team.yokai_ids) != 3:
        raise HTTPException(status_code=400, detail="Team must have exactly 3 Yo-kai")
    
    with get_db() as db:
        max_id = db.execute("SELECT MAX(id) FROM teams").fetchone()[0]
        new_id = (max_id or 0) + 1
        
        db.execute("""
            INSERT INTO teams (id, name, owner_id, yokai_ids, tier)
            VALUES (?, ?, ?, ?, ?)
        """, [new_id, team.name, user_id, json.dumps(team.yokai_ids), team.tier])
        
        result = db.execute("SELECT * FROM teams WHERE id = ?", [new_id]).fetchone()
        columns = [desc[0] for desc in db.description]
        new_team = dict(zip(columns, result))
        new_team['yokai_ids'] = json.loads(new_team['yokai_ids'])
        
        return new_team


@router.delete("/{team_id}")
def delete_team(
    team_id: int,
    user_id: int = 1
):
    with get_db() as db:
        result = db.execute(
            "SELECT * FROM teams WHERE id = ?",
            [team_id]
        ).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Team not found")
        
        columns = [desc[0] for desc in db.description]
        team = dict(zip(columns, result))
        
        if team['owner_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this team")
        
        db.execute("DELETE FROM teams WHERE id = ?", [team_id])
        
        return {"message": "Team deleted successfully"}
