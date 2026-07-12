import traceback
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from starlette import status
from core.database import get_db
from core.models import User
from users_logic.schemas.token_schemas import TokenResponse, RefreshTokenRequest
from users_logic.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from users_logic.schemas.schemas import UserResponse, UserCreate, UserLogin
from users_logic import crud

router = APIRouter(prefix="/authentication", tags=["authentication"])


@router.post("/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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


@router.post("/login/", response_model=TokenResponse)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """Вход — возвращает access и refresh токены."""
    # Поиск пользователя
    result = await db.execute(select(User).where(User.username == login_data.username))
    user = result.scalar_one_or_none()

    # Проверка
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Создаем оба токена
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh/", response_model=TokenResponse)
async def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Обновление access токена через refresh токен."""
    # 1. Декодируем refresh токен
    payload = decode_token(refresh_data.refresh_token)

    # 2. Проверяем тип
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    # 3. Проверяем пользователя
    user_id = payload.get("user_id")
    user = await db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # 4. Создаем новые токены
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout/")
async def logout_user():
    """Выход — клиент должен удалить токены."""
    return {"message": "Logout successful"}


# Базовая аунтификация
# http_basic = HTTPBasic()
# @router.get("/basic_auth/")
# async def basic_credentials_auth(
#     credentials: Annotated[HTTPBasicCredentials, Depends(http_basic)],
#     db: AsyncSession = Depends(get_db),
# ):
#     username, password = credentials.username, credentials.password
#
#     result: Result = await db.execute(
#         select(User).where((User.username == username))
#     )
#     user = result.scalar_one_or_none()
#
#     if not user or not verify_password(password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password.",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#
#     return {"in_system": True, "message": f"Hello {username}!"}
