from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
from typing import Optional, List


class User(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    hashed_password: str
    created_at: datetime = datetime.now(timezone.utc)
    total_battles: int = 0
    wins: int = 0
    losses: int = 0
    
    class Config:
        from_attributes = True


class Team(BaseModel):
    id: int
    name: str
    owner_id: int
    yokai_ids: List[int]
    tier: str = "OU"
    is_public: int = 1
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True


class Battle(BaseModel):
    id: int
    player1_id: int
    player2_id: int
    team1_id: int
    team2_id: int
    winner_id: Optional[int] = None
    battle_log: Optional[List] = None
    duration: Optional[int] = None
    turns: int = 0
    status: str = "pending"  # pending, active, completed, abandoned
    created_at: datetime = datetime.now(timezone.utc)
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

