from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DUCKDB_PATH: str = "./data/somen_spirits.duckdb"
    REDIS_URL: str = "redis://localhost:6379/0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    SECRET_KEY: str = "some super secure key not sure how to do this yet."
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: str = "http://localhost:3000"
    SOCKETIO_PATH: str = "/socket.io"
    
    class Config:
        env_file = ".env"


settings = Settings()
