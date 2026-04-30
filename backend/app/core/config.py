from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite+aiosqlite:///./pathforge.db"
    FAISS_INDEX_PATH: str = "faiss_index"
    ENVIRONMENT: str = "development"
    MAX_COURSES_PER_GAP: int = 2
    MAX_WEEKS: int = 24
    ALLOWED_ORIGINS: str = "http://localhost:5173,https://pathforge.vercel.app"

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    model_config = {"env_file": ".env"}


settings = Settings()