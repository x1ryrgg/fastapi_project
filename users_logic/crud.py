import pytz

from sqlalchemy.sql import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core.logging_system import logger
from users_logic.security import hash_password
from core.models.user import User
from users_logic.schemas.schemas import UserCreate, UserUpdate


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

    password = hash_password(user_data.pop('password'))

    user = User(**user_data, password=password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info(f"[create_user] User created: id={user.id}, username={user.username}")

    return user


async def get_user_by_id(user_id: int, db: AsyncSession) -> type[User]:
    """
    Выдача пользователя по его id

    :param user_id: int
    :param db: AsyncSession
    :return: User or None
    """
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    msk_time = pytz.timezone("Europe/Moscow")
    user.created_at = user.created_at.astimezone(msk_time)

    logger.info(f"[get_user_by_id] Return User #{user.id} with name: {user.username}")
    return user


async def get_user_by_username(username: str, db: AsyncSession) -> type[User]:
    """
    Выдача пользователя по username

    :param username: str
    :param db: AsyncSession
    :return: User or None
    """
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"[get_user_by_username] Return User #{user.id} with name: {user.username}")
    return user


async def delete_user(user_id: int, db: AsyncSession) -> bool:
    """
    Удаление пользователя

    :param user_id: int
    :param db: AsyncSession
    :return: True
    """
    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()
    logger.info(f"[delete_user] User #{user.id} deleted")
    return True


async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_data = user_in.model_dump(exclude_unset=True, exclude_defaults=True, exclude_none=True)

    for field in User.UNIQUE_FIELDS:
        if field in user_data:
            existing = await db.execute(
                select(User).where(
                    getattr(User, field) == user_data[field],
                    User.id != user_id
                )
            )
            if existing.scalar_one_or_none():
                raise HTTPException(400, f"{field.capitalize()} already taken")

    for field, value in user_data.items():
        if field == "password":
            value = hash_password(value)
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user
