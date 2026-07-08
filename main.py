from contextlib import asynccontextmanager
from core.database import engine
from core.models.base import Base
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.views import router as user_router
from core.logging_system import logger


# uvicorn main:app --reload - запуск приложение на uvicron
# netstat -ano | findstr :8000 - нахождение активных процессов
# taskkill /PID 7348 /F - завершение активных процессов


# ╨б╨╛╨╖╨┤╨░╨╡╨╝ ╤В╨░╨▒╨╗╨╕╤Ж╤Л ╨┐╤А╨╕ ╨╖╨░╨┐╤Г╤Б╨║╨╡ ╨┐╤А╨╕╨╗╨╛╨╢╨╡╨╜╨╕╤П
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("ЁЯЪА Starting application...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")
    yield
    logger.info("Shutting down application...")
    await engine.dispose()
    logger.info("Database connections closed")

app = FastAPI(lifespan=lifespan, title='TEST FASTAPI')

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping/")
async def ping():
    return JSONResponse(content={"response": "PONG"})


