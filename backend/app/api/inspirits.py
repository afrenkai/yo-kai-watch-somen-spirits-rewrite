from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Union
from app.core.database import get_db
from pydantic import BaseModel
import json


router = APIRouter()


class InspiritResponse(BaseModel):
    id: str
    command: str
    effects: Union[Dict[str, Any], List[Any], None] = None
    image: str | None = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[InspiritResponse])
def get_all_inspirits(skip: int = 0, limit: int = 100):
    with get_db() as db:
        query = f"SELECT * FROM inspirit LIMIT {limit} OFFSET {skip}"
        result = db.execute(query).fetchall()
        columns = [desc[0] for desc in db.description]
        inspirits = []
        for row in result:
            inspirit = dict(zip(columns, row))
            # Parse JSON effects if it's a string
            if inspirit.get('effects'):
                if isinstance(inspirit['effects'], str):
                    try:
                        inspirit['effects'] = json.loads(inspirit['effects'])
                    except (json.JSONDecodeError, TypeError):
                        # If parsing fails, keep as None or leave as is
                        inspirit['effects'] = None
            inspirits.append(inspirit)
        
        return inspirits


@router.get("/{inspirit_id}", response_model=InspiritResponse)
def get_inspirit(inspirit_id: str):
    with get_db() as db:
        result = db.execute("SELECT * FROM inspirit WHERE id = ?", [inspirit_id]).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Inspirit not found")
        
        columns = [desc[0] for desc in db.description]
        inspirit = dict(zip(columns, result))
        
        # Parse JSON effects if it's a string
        if inspirit.get('effects'):
            if isinstance(inspirit['effects'], str):
                try:
                    inspirit['effects'] = json.loads(inspirit['effects'])
                except (json.JSONDecodeError, TypeError):
                    # If parsing fails, keep as None
                    inspirit['effects'] = None
        
        return inspirit
        
        return inspirit
