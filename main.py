from contextlib import asynccontextmanager
from core.database import engine
from core.models.base import Base
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users_logic.views import router as user_router
from users_logic.auth_views import router as auth_router
from hotel_logic.views import router as hotel_router
from core.logging_system import logger


# uvicorn main:app --reload - запуск приложение на uvicron
# netstat -ano | findstr :8000 - нахождение активных процессов
# taskkill /PID 7348 /F - завершение активных процессов



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan, title='TEST FASTAPI')

app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping/")
async def ping():
    return JSONResponse(content={"response": "PONG"})


