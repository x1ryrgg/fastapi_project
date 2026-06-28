import os

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