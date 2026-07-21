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
from users_logic.crud import get_user_by_username
from users_logic.dependencies import authenticate_user, refresh_token_verification
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
    return await crud.create_user(user_in=user, db=db)


@router.post("/login/", response_model=TokenResponse)
async def login_user_view(user: User = Depends(authenticate_user)):
    """Вход — возвращает access и refresh токены."""
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
async def refresh_access_token(user: User = Depends(refresh_token_verification)):
    """Обновление access токена через refresh токен."""

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
