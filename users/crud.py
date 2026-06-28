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
    ╨б╨╛╨╖╨┤╨░╨╜╨╕╨╡ ╨╜╨╛╨▓╨╛╨│╨╛ ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П.

    Args:
        user_in: ╨Ф╨░╨╜╨╜╤Л╨╡ ╨┤╨╗╤П ╤Б╨╛╨╖╨┤╨░╨╜╨╕╤П ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П
        db: ╨б╨╡╤Б╤Б╨╕╤П ╨▒╨░╨╖╤Л ╨┤╨░╨╜╨╜╤Л╤Е

    Returns:
        UserResponse: ╨б╨╛╨╖╨┤╨░╨╜╨╜╤Л╨╣ ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М
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
