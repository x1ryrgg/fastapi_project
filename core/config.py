import os

from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    db_url: str = os.getenv("DATABASE_URL", "")