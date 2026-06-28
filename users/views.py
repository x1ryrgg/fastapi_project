import traceback
from typing import List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import select
from starlette import status

from users.schemas import UserCreate, UserResponse
from fastapi import Depends, Path, APIRouter, HTTPException
from users.models import User
from pydantic import EmailStr
from logging_system import logger
from users import crud
import pytz

# uvicorn main:app --reload

router = APIRouter(
    prefix="/users",  # ╨Ю╨▒╤Й╨╕╨╣ ╨┐╤А╨╡╤Д╨╕╨║╤Б ╨┤╨╗╤П ╨▓╤Б╨╡╤Е ╤Н╨╜╨┤╨┐╨╛╨╕╨╜╤В╨╛╨▓ ╨▓ ╤Н╤В╨╛╨╝ ╤А╨╛╤Г╤В╨╡╤А╨╡
    tags=["users"]    # ╨в╨╡╨│ ╨┤╨╗╤П ╨┤╨╛╨║╤Г╨╝╨╡╨╜╤В╨░╤Ж╨╕╨╕
)

@router.get("/all/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    if not users:
        logger.info(f"╨Э╨╡╤В ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╨╡╨╣.")
    logger.info(f"╨Я╨╛╨╗╤Г╤З╨╕╨╗╨╕ {len(users)} ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╨╡╨╣")

    return users

@router.get("/{id}/", response_model=UserResponse)
async def get_user(id: Annotated[int, Path(ge=1, le=1_000_000)], db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    msk_time = pytz.timezone("Europe/Moscow")
    user.created_at = user.created_at.astimezone(msk_time)

    return user


# ╨Я╤А╨╕╨╝╨╡╤А ╤Н╨╜╨┤╨┐╨╛╨╕╨╜╤В╨░ ╨┤╨╗╤П ╤Б╨╛╨╖╨┤╨░╨╜╨╕╤П ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╤З╨╡╤А╨╡╨╖ url
@router.post("/{username}/{email}/{password}/", response_model=UserResponse)
async def create_user(username: str, email: EmailStr, password: str, db: AsyncSession = Depends(get_db)):
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# ╨Я╤А╨╕╨╝╨╡╤А Post ╨╖╨░╨┐╤А╨╛╤Б╨░ ╤Б Pydantic ╨╕ ╤З╨╡╤А╨╡╨╖ ╤В╨╡╨╗╨╛ ╨╖╨░╨┐╤А╨╛╤Б╨░
# @router.post("/create/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(
#         select(User).where(
#             (User.email == user.email) |
#             (User.username == user.username)
#         )
#     )
#     existing_user = result.scalar_one_or_none()
#
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username or email already registered"
#         )
#
#     new_user = User(username=user.username, email=user.email, password=user.password)
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)
#     return new_user

@router.post("/create/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_user(user_in=user, db=db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {e}: {traceback.format_exc()}",
        )
