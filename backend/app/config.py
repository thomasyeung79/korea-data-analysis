from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./korea_analysis.db"
    CORS_ORIGINS: str = "*"
    OPENAI_API_KEY: str | None = None
    AI_PROVIDER: str = "local"
    JWT_SECRET_KEY: str = "change-me"
    JWT_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
