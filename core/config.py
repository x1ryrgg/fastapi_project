import os

from pathlib import Path
from fastapi import HTTPException
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv
from starlette import status

load_dotenv()


class Settings(BaseSettings):
    db_url: str = os.getenv("DATABASE_URL", "")

    @field_validator('db_url')
    @classmethod
    def validate_db_url(cls, v: str):
        if not v:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return v

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()


class SecuritySettings(BaseSettings):
    # JWT
    SECRET_KEY: str  # python -c "import secrets; print(secrets.token_hex(32))"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60      # Короткий срок
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7         # Долгий срок для обновления

    # База данных
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

security_settings = SecuritySettings()
