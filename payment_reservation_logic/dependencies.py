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


async def get_bank_account_by_user_id(user_id: int, db: AsyncSession, load_relationships: bool = False) -> BankAccount:
    """ Получение BankAccount по user_id """
    stmt = select(BankAccount).where(BankAccount.user_id == user_id)

    if load_relationships:
        stmt = stmt.options(
            selectinload(BankAccount.payments), # на той стороне payments много объектов one-to-many
            joinedload(BankAccount.user) # на той стороне user 1 запись связь many-to-one / one-to-one
        )

    stmt: Result = await db.execute(stmt)

    bank_account = stmt.scalar_one_or_none()

    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BankAccount not found"
        )

    return bank_account
