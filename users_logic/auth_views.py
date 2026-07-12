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
from users_logic.authentication_system import hash_password, verify_password
from users_logic.schemas import UserResponse, UserCreate
from users_logic import crud

router = APIRouter(
    prefix="/authentication",
    tags=["authentication"]
)

http_basic = HTTPBasic()


@router.get("/basic_auth/")
async def basic_credentials_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(http_basic)],
    db: AsyncSession = Depends(get_db),
):
    username, password = credentials.username, credentials.password

    result: Result = await db.execute(
        select(User).where((User.username == username))
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Basic"},
        )

    return {"in_system": True, "message": f"Hello {username}!"}


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
