from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from core.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.logging_system import logger

from core.models.user import User, UserRole
from core.models.payment import BankAccount, Payment, PaymentStatus
from core.models.hotel import Hotel, Room, RoomInformation


async def get_bank_account_by_user_id(user_id: int, db: AsyncSession,
                                      load_relationships: bool = False,
                                      block_update_column: bool = False) -> BankAccount:
    """ Получение BankAccount по user_id """
    stmt = select(BankAccount).where(BankAccount.user_id == user_id)

    if load_relationships:
        stmt = stmt.options(
            selectinload(BankAccount.payments), # на той стороне payments много объектов one-to-many
            joinedload(BankAccount.user) # на той стороне user 1 запись связь many-to-one / one-to-one
        )

    if block_update_column:
        stmt = stmt.with_for_update()

    stmt: Result = await db.execute(stmt)

    bank_account = stmt.unique().scalar_one_or_none()

    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BankAccount not found"
        )

    return bank_account


async def get_payment_by_id(payment_id: int, account_id: int,
                            db: AsyncSession,
                            load_relationships: bool = False,
                            payment_status: PaymentStatus = PaymentStatus.PAID) -> Payment:
    """ Получение BankAccount по user_id """
    stmt = select(Payment).where(
        (Payment.id == payment_id) &
        (Payment.account_id == account_id) &
        (Payment.status == payment_status)
    )

    if load_relationships:
        stmt = stmt.options(
            joinedload(Payment.account),
            joinedload(Payment.reservation)
        )

    stmt: Result = await db.execute(stmt)

    payment = stmt.scalar_one_or_none()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    return payment
