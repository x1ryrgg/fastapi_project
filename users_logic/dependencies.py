from typing import Any, Coroutine, Annotated

from fastapi import HTTPException, Path, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from core.database import get_db
from core.models import User


async def get_user_by_id(user_id: Annotated[int, Path], db: AsyncSession = Depends(get_db)) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

