import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# ╨з╨╕╤В╨░╨╡╨╝ URL ╨▒╨░╨╖╤Л ╨┤╨░╨╜╨╜╤Л╤Е ╨╕╨╖ ╨┐╨╡╤А╨╡╨╝╨╡╨╜╨╜╤Л╤Е ╨╛╨║╤А╤Г╨╢╨╡╨╜╨╕╤П
DATABASE_URL = os.getenv("DATABASE_URL", "")

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

# ╨С╨░╨╖╨╛╨▓╤Л╨╣ ╨║╨╗╨░╤Б╤Б ╨┤╨╗╤П ╨╝╨╛╨┤╨╡╨╗╨╡╨╣
Base = declarative_base()

# ╨Ч╨░╨▓╨╕╤Б╨╕╨╝╨╛╤Б╤В╤М ╨┤╨╗╤П ╨┐╨╛╨╗╤Г╤З╨╡╨╜╨╕╤П ╤Б╨╡╤Б╤Б╨╕╨╕ ╨▓ ╤Н╨╜╨┤╨┐╨╛╨╕╨╜╤В╨░╤Е FastAPI
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
