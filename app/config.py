from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/demo"
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 60  # seconds

    class Config:
        env_file = ".env"


settings = Settings()
