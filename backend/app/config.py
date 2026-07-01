from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./korea_analysis.db"
    CORS_ORIGINS: str = "*"
    OPENAI_API_KEY: str | None = None
    AI_PROVIDER: str = "local"

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
