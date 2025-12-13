from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None
    total_battles: int
    wins: int
    losses: int
    
    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    with get_db() as db:
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?",
            [user.username]
        ).fetchone()
        
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = pwd_context.hash(user.password)
        
        max_id = db.execute("SELECT MAX(id) FROM users").fetchone()[0]
        new_id = (max_id or 0) + 1
        
        db.execute("""
            INSERT INTO users (id, username, email, hashed_password)
            VALUES (?, ?, ?, ?)
        """, [new_id, user.username, user.email, hashed_password])
        
        result = db.execute("SELECT * FROM users WHERE id = ?", [new_id]).fetchone()
        columns = [desc[0] for desc in db.description]
        new_user = dict(zip(columns, result))
        
        return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    with get_db() as db:
        result = db.execute(
            "SELECT * FROM users WHERE id = ?",
            [user_id]
        ).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
        columns = [desc[0] for desc in db.description]
        user = dict(zip(columns, result))
        
        return user


@router.get("/username/{username}", response_model=UserResponse)
def get_user_by_username(username: str):
    with get_db() as db:
        result = db.execute(
            "SELECT * FROM users WHERE username = ?",
            [username]
        ).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
        columns = [desc[0] for desc in db.description]
        user = dict(zip(columns, result))
        
        return user
