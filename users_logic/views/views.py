import traceback
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from sqlalchemy import select
from starlette import status

from users_logic.dependencies import get_user_by_id, get_current_user
from users_logic.schemas.schemas import UserCreate, UserResponse, UsersResponse, UserUpdate
from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from core.models.user import User
from pydantic import EmailStr
from core.logging_system import logger
from users_logic import crud


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/all/", response_model=List[UsersResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    if not users:
        logger.info(f"Нет пользователей.")
    logger.info(f"Ответ по {len(users)} пользователям")

    return users


@router.get("/profile/", response_model=UserResponse)
async def user_info_view(user: User = Depends(get_current_user)):
    return user


@router.get("/by_username/{username}/", response_model=UsersResponse)
async def view_get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.get_user_by_username(username=username, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {e}: {traceback.format_exc()}",
        )


@router.get("/{user_id}/", response_model=UserResponse)
async def view_get_user(user: User = Depends(get_user_by_id)):
    return user


@router.post("/create/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
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


@router.delete("/{user_id}/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await crud.delete_user(user_id=user_id, db=db)
        return JSONResponse(content="User successfully deleted.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {e}: {traceback.format_exc()}",
        )


@router.patch("/{user_id}/update/", response_model=UserResponse, status_code=status.HTTP_200_OK)
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
