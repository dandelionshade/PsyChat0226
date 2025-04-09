# 核心配置模块
from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[str]
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()