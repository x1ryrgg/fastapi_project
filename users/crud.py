import pytz

from sqlalchemy.sql import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core.logging_system import logger
from users.authentication_system import hash_password
from users.models import User
from users.schemas import UserCreate, UserResponse


async def create_user(user_in: UserCreate, db: AsyncSession) -> User:
    """
    Создаёт нового пользователя в базе данных.

    Выполняет проверку на уникальность username и email, хеширует пароль,
    сохраняет пользователя и возвращает созданный объект.

    Args:
        user_in (UserCreate): Pydantic-схема с данными для создания пользователя
                              (username, email, password).
        db (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        User: Созданный объект модели User (с заполненными полями id и created_at).

    Raises:
        HTTPException: Если пользователь с таким username или email уже существует,
                       возвращает статус 400 (Bad Request).
    """
    result = await db.execute(
        select(User).where(
            (User.email == user_in.email) | (User.username == user_in.username)
        )
    )

    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username or email already registered"
                )

    user_data = user_in.model_dump()
    logger.info(f"[create_user] Creating user: username={user_data['username']}, email={user_data['email']}")

    password = hash_password(user_data['password'])

    user = User(username=user_data['username'],
                email=user_data['email'],
                password=password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info(f"[create_user] User created: id={user.id}, username={user.username}")

    return user


async def get_user(user_id: int, db: AsyncSession) -> User | None:
    """
    Выдача пользователя по его id

    :param user_id: int
    :param db: AsyncSession
    :return: User or None
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    msk_time = pytz.timezone("Europe/Moscow")
    user.created_at = user.created_at.astimezone(msk_time)

    logger.info(f"[get_user] Return User #{user.id} with name: {user.username}")
    return user