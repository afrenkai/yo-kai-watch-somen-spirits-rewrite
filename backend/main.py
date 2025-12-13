from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import socketio
from app.core.config import settings
from app.core.database import init_db
from app.api import yokai, teams, matchmaking, battles, users
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
