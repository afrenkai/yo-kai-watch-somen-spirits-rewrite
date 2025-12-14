from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import socketio
from app.core.config import settings
from app.core.database import init_db
from app.api import yokai, teams, matchmaking, battles, users, attacks, attitudes, equipment, inspirits, skills, soul_gems, soultimates, techniques
from app.sockets import battle_socket


sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ORIGINS.split(',')
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Somen Spirits API",
    description="Backend API for Yo-kai Watch Somen Spirits battle simulator",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yokai.router, prefix="/api/yokai", tags=["yokai"])
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
app.include_router(matchmaking.router, prefix="/api/matchmaking", tags=["matchmaking"])
app.include_router(battles.router, prefix="/api/battles", tags=["battles"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(attacks.router, prefix="/api/attacks", tags=["attacks"])
app.include_router(attitudes.router, prefix="/api/attitudes", tags=["attitudes"])
app.include_router(equipment.router, prefix="/api/equipment", tags=["equipment"])
app.include_router(inspirits.router, prefix="/api/inspirits", tags=["inspirits"])
app.include_router(skills.router, prefix="/api/skills", tags=["skills"])
app.include_router(soul_gems.router, prefix="/api/soul-gems", tags=["soul-gems"])
app.include_router(soultimates.router, prefix="/api/soultimates", tags=["soultimates"])
app.include_router(techniques.router, prefix="/api/techniques", tags=["techniques"])

battle_socket.register_events(sio)


socket_app = socketio.ASGIApp(sio, app)


@app.get("/")
async def root():
    return {
        "message": "Yo-kai Watch Somen Spirits API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
