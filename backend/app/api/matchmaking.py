from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import redis
import json
from app.core.config import settings


router = APIRouter()

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class MatchmakingRequest(BaseModel):
    user_id: int
    username: str
    team_id: int
    tier: str = "OU"


class MatchmakingStatus(BaseModel):
    in_queue: bool
    position: int | None = None
    total_in_queue: int = 0
    active_battles: int = 0


@router.post("/join")
async def join_matchmaking(request: MatchmakingRequest):
    queue_key = f"matchmaking:{request.tier}"
    
    queue_data = redis_client.lrange(queue_key, 0, -1)
    for item in queue_data:
        data = json.loads(item)
        if data['user_id'] == request.user_id:
            raise HTTPException(status_code=400, detail="Already in matchmaking queue")
    
    player_data = request.model_dump_json()
    redis_client.rpush(queue_key, player_data)
    
    redis_client.expire(queue_key, 1800)
    
    return {"message": "Joined matchmaking queue", "tier": request.tier}


@router.post("/leave")
async def leave_matchmaking(user_id: int, tier: str = "OU"):
    queue_key = f"matchmaking:{tier}"
    
    queue_data = redis_client.lrange(queue_key, 0, -1)
    for item in queue_data:
        data = json.loads(item)
        if data['user_id'] == user_id:
            redis_client.lrem(queue_key, 1, item)
            return {"message": "Left matchmaking queue"}
    
    raise HTTPException(status_code=404, detail="Not in matchmaking queue")


@router.get("/status", response_model=MatchmakingStatus)
async def get_matchmaking_status(user_id: int, tier: str = "OU"):
    queue_key = f"matchmaking:{tier}"
    
    queue_data = redis_client.lrange(queue_key, 0, -1)
    total_in_queue = len(queue_data)
    
    position = None
    in_queue = False
    
    for idx, item in enumerate(queue_data):
        data = json.loads(item)
        if data['user_id'] == user_id:
            in_queue = True
            position = idx + 1
            break
    
    active_battles = redis_client.get("active_battles") or 0
    
    return MatchmakingStatus(
        in_queue=in_queue,
        position=position,
        total_in_queue=total_in_queue,
        active_battles=int(active_battles)
    )


@router.get("/stats")
async def get_matchmaking_stats():
    stats = {}
    
    for tier in ["OU", "UU", "RU", "NU"]:
        queue_key = f"matchmaking:{tier}"
        count = redis_client.llen(queue_key)
        stats[tier] = count
    
    active_battles = redis_client.get("active_battles") or 0
    
    return {
        "queues": stats,
        "active_battles": int(active_battles),
        "total_online": sum(stats.values())
    }
