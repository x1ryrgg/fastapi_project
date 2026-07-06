from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer
from core.config import settings

# класс служит основой (регистрацией) для всех ваших ORM-моделей
class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)

DATABASE_URL = settings.db_url

# ╨б╨╛╨╖╨┤╨░╨╡╨╝ ╨░╤Б╨╕╨╜╤Е╤А╨╛╨╜╨╜╤Л╨╣ ╨┤╨▓╨╕╨╢╨╛╨║
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # ╨Т╨║╨╗╤О╤З╨░╨╡╨╝ ╨╗╨╛╨│╨╕╤А╨╛╨▓╨░╨╜╨╕╨╡ SQL-╨╖╨░╨┐╤А╨╛╤Б╨╛╨▓ (╨┐╨╛╨╗╨╡╨╖╨╜╨╛ ╨┤╨╗╤П ╨╛╤В╨╗╨░╨┤╨║╨╕)
    future=True,
    pool_pre_ping=True,  # ╨Я╤А╨╛╨▓╨╡╤А╤П╨╡╨╝ ╤Б╨╛╨╡╨┤╨╕╨╜╨╡╨╜╨╕╨╡ ╨┐╨╡╤А╨╡╨┤ ╨╕╤Б╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╨╜╨╕╨╡╨╝
)

# ╨б╨╛╨╖╨┤╨░╨╡╨╝ ╤Д╨░╨▒╤А╨╕╨║╤Г ╤Б╨╡╤Б╤Б╨╕╨╣
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ╨Ч╨░╨▓╨╕╤Б╨╕╨╝╨╛╤Б╤В╤М ╨┤╨╗╤П ╨┐╨╛╨╗╤Г╤З╨╡╨╜╨╕╤П ╤Б╨╡╤Б╤Б╨╕╨╕ ╨▓ ╤Н╨╜╨┤╨┐╨╛╨╕╨╜╤В╨░╤Е FastAPI
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
