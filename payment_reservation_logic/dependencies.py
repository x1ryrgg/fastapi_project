from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from core.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging_system import logger
from core.models import User, BankAccount
from core.models.hotel import Hotel, Room, RoomInformation
from core.models.user import UserRole


async def get_bank_account_by_user_id(user_id: int, db: AsyncSession):
    """ Получение BankAccount по user_id """
    stmt: Result = await db.execute(select(BankAccount)
                                    .where(BankAccount.user_id == user_id)
                                    )
    bank_account = stmt.scalar_one_or_none()

    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BankAccount not found"
        )

    return bank_account
