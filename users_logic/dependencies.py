from typing import Any, Coroutine, Annotated

from fastapi import HTTPException, Path, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from core.database import get_db
from core.models import User
from users_logic.crud import get_user_by_username
from users_logic.schemas.schemas import UserLogin
from users_logic.schemas.token_schemas import RefreshTokenRequest

from users_logic.security import decode_token, verify_password

async def get_user_by_id(user_id: Annotated[int, Path], db: AsyncSession = Depends(get_db)) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Получение текущего пользователя из Bearer токена."""
    token = credentials.credentials

    # Декодируем токен
    payload = decode_token(token)

    # Проверяем тип токена
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    # Извлекаем user_id
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # Ищем пользователя в БД
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Проверяем, активен ли пользователь
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Проверяет, является ли текущий пользователь суперпользователем, и возвращает его."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user


async def authenticate_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Аутентифицирует пользователя и возвращает объект User."""
    user = await get_user_by_username(username=login_data.username, db=db)

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def refresh_token_verification(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """ Проверка refresh токена для выдачи user из него, """
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

    return user
