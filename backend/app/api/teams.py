from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from pydantic import BaseModel
from datetime import datetime
import json


router = APIRouter()


class TeamYokaiData(BaseModel):
    yokai_id: str
    position: int
    nickname: Optional[str] = None
    level: int = 50
    attitude_id: str = "rough"
    loafing_attitude_id: str = "serious"
    ivs: Dict[str, int] = {"hp": 0, "str": 0, "spr": 0, "def": 0, "spd": 0}
    evs: Dict[str, int] = {"hp": 0, "str": 0, "spr": 0, "def": 0, "spd": 0}
    gym_points: Dict[str, int] = {"str": 0, "spr": 0, "def": 0, "spd": 0}
    equipment: List[str] = []


class TeamCreate(BaseModel):
    name: str
    team_type: str = "bony"  # "bony" or "fleshy"
    tier: str = "OU"
    yokai: List[TeamYokaiData] = []
    is_public: bool = True


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    team_type: Optional[str] = None
    tier: Optional[str] = None
    yokai: Optional[List[TeamYokaiData]] = None
    is_public: Optional[bool] = None


class TeamResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    team_type: str
    yokai: List[TeamYokaiData]
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
            # Parse team_data if it exists, otherwise use yokai_ids
            if team.get('team_data'):
                team['yokai'] = json.loads(team['team_data'])
            else:
                # Fallback to old format
                yokai_ids = json.loads(team['yokai_ids']) if team.get('yokai_ids') else []
                team['yokai'] = [{'yokai_id': str(yid), 'position': i, 'level': 50} 
                                for i, yid in enumerate(yokai_ids)]
            team['team_type'] = team.get('team_type') or 'bony'
            del team['yokai_ids']  # Remove old field
            if 'team_data' in team:
                del team['team_data']  # Remove raw field
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
        
        # Parse team_data if it exists, otherwise use yokai_ids
        if team.get('team_data'):
            team['yokai'] = json.loads(team['team_data'])
        else:
            yokai_ids = json.loads(team['yokai_ids']) if team.get('yokai_ids') else []
            team['yokai'] = [{'yokai_id': str(yid), 'position': i, 'level': 50} 
                            for i, yid in enumerate(yokai_ids)]
        team['team_type'] = team.get('team_type') or 'bony'
        del team['yokai_ids']
        if 'team_data' in team:
            del team['team_data']
        
        return team


@router.post("/", response_model=TeamResponse)
def create_team(
    team: TeamCreate,
    user_id: int = 1
):
    if len(team.yokai) > 6:
        raise HTTPException(status_code=400, detail="Team cannot have more than 6 Yo-kai")
    
    with get_db() as db:
        max_id = db.execute("SELECT MAX(id) FROM teams").fetchone()[0]
        new_id = (max_id or 0) + 1
        
        # Store both formats for backwards compatibility
        yokai_ids = [y.yokai_id for y in team.yokai]
        team_data = json.dumps([y.dict() for y in team.yokai])
        
        db.execute("""
            INSERT INTO teams (id, name, owner_id, yokai_ids, team_type, team_data, tier, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            new_id, 
            team.name, 
            user_id, 
            json.dumps(yokai_ids),
            team.team_type,
            team_data,
            team.tier,
            1 if team.is_public else 0
        ])
        
        result = db.execute("SELECT * FROM teams WHERE id = ?", [new_id]).fetchone()
        columns = [desc[0] for desc in db.description]
        new_team = dict(zip(columns, result))
        new_team['yokai'] = team.yokai
        new_team['team_type'] = team.team_type
        del new_team['yokai_ids']
        if 'team_data' in new_team:
            del new_team['team_data']
        
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


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_update: TeamUpdate,
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
            raise HTTPException(status_code=403, detail="Not authorized to update this team")
        
        # Build update query
        updates = []
        params = []
        
        if team_update.name is not None:
            updates.append("name = ?")
            params.append(team_update.name)
        
        if team_update.team_type is not None:
            updates.append("team_type = ?")
            params.append(team_update.team_type)
        
        if team_update.tier is not None:
            updates.append("tier = ?")
            params.append(team_update.tier)
        
        if team_update.is_public is not None:
            updates.append("is_public = ?")
            params.append(1 if team_update.is_public else 0)
        
        if team_update.yokai is not None:
            if len(team_update.yokai) > 6:
                raise HTTPException(status_code=400, detail="Team cannot have more than 6 Yo-kai")
            
            yokai_ids = [y.yokai_id for y in team_update.yokai]
            team_data = json.dumps([y.dict() for y in team_update.yokai])
            
            updates.append("yokai_ids = ?")
            params.append(json.dumps(yokai_ids))
            updates.append("team_data = ?")
            params.append(team_data)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        
        params.append(team_id)
        
        query = f"UPDATE teams SET {', '.join(updates)} WHERE id = ?"
        db.execute(query, params)
        
        # Fetch updated team
        result = db.execute("SELECT * FROM teams WHERE id = ?", [team_id]).fetchone()
        columns = [desc[0] for desc in db.description]
        updated_team = dict(zip(columns, result))
        
        if updated_team.get('team_data'):
            updated_team['yokai'] = json.loads(updated_team['team_data'])
        else:
            yokai_ids = json.loads(updated_team['yokai_ids']) if updated_team.get('yokai_ids') else []
            updated_team['yokai'] = [{'yokai_id': str(yid), 'position': i, 'level': 50} 
                                    for i, yid in enumerate(yokai_ids)]
        updated_team['team_type'] = updated_team.get('team_type') or 'bony'
        del updated_team['yokai_ids']
        if 'team_data' in updated_team:
            del updated_team['team_data']
        
        return updated_team
