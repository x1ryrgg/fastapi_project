from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer
from core.config import settings

# класс служит основой (регистрацией) для всех ваших ORM-моделей
class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)