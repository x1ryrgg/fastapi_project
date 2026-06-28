from contextlib import asynccontextmanager
from core.database import engine, Base
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.views import router as user_router
from core.logging_system import logger


# ╨б╨╛╨╖╨┤╨░╨╡╨╝ ╤В╨░╨▒╨╗╨╕╤Ж╤Л ╨┐╤А╨╕ ╨╖╨░╨┐╤Г╤Б╨║╨╡ ╨┐╤А╨╕╨╗╨╛╨╢╨╡╨╜╨╕╤П
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ╨Ч╨░╨┐╤Г╤Б╨║
    logger.info("ЁЯЪА Starting application...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("тЬЕ Database tables created/verified")
    yield
    # ╨Ю╤Б╤В╨░╨╜╨╛╨▓╨║╨░
    logger.info("ЁЯЫС Shutting down application...")
    await engine.dispose()
    logger.info("тЬЕ Database connections closed")

app = FastAPI(lifespan=lifespan, title='TEST FASTAPI')

app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/json/ping/")
async def json_ping():
    return JSONResponse(content={"response": "PONG"})


@app.get("/car/")
async def get_car_from_query(mark: str = None):
    if mark:
        mark = mark.strip("_").upper()
        return {"Car mark": mark}
    else:
        return {"No mark provided"}
