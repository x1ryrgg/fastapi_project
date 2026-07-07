import traceback
from typing import List, Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from sqlalchemy import select
from starlette import status

from users.schemas import UserCreate, UserResponse, UsersResponse, UserUpdate
from fastapi import Depends, Path, APIRouter, HTTPException
from core.models.user import User
from pydantic import EmailStr
from core.logging_system import logger
from users import crud


router = APIRouter(
    prefix="/users",  # ╨Ю╨▒╤Й╨╕╨╣ ╨┐╤А╨╡╤Д╨╕╨║╤Б ╨┤╨╗╤П ╨▓╤Б╨╡╤Е ╤Н╨╜╨┤╨┐╨╛╨╕╨╜╤В╨╛╨▓ ╨▓ ╤Н╤В╨╛╨╝ ╤А╨╛╤Г╤В╨╡╤А╨╡
    tags=["users"]    # ╨в╨╡╨│ ╨┤╨╗╤П ╨┤╨╛╨║╤Г╨╝╨╡╨╜╤В╨░╤Ж╨╕╨╕
)

@router.get("/all/", response_model=List[UsersResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    if not users:
        logger.info(f"Нет пользователей.")
    logger.info(f"Ответ по {len(users)} пользователям")

    return users

@router.get("/{id}/", response_model=UserResponse)
async def get_user(id: Annotated[int, Path(ge=1, le=1_000_000)], db: AsyncSession = Depends(get_db)):
    try:
        return await crud.get_user(user_id=id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found: {e}"
        )

# Пример post запроса с передачей данных через url
@router.post("/{username}/{email}/{password}/", response_model=UserResponse)
async def create_user(username: str, email: EmailStr, password: str, db: AsyncSession = Depends(get_db)):
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


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


@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.delete_user(user_id=user_id, db=db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {e}: {traceback.format_exc()}",
        )


@router.patch("/update/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
        Частичное обновление пользователя.
        Обновляются только переданные поля.
    """
    try:
        return await crud.update_user(user_id=user_id, user_in=user_update, db=db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to patch user: {e}: {traceback.format_exc()}",
        )
