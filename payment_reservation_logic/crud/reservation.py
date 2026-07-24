from datetime import datetime, timedelta, timezone, date
import random

from fastapi import HTTPException, status
from decimal import Decimal

from sqlalchemy.orm import joinedload, selectinload

from core.logging_system import logger
from sqlalchemy import select, Result, and_
from core.models.payment import BankAccount, Payment, PaymentStatus, VerificationCode
from core.models.user import User
from core.models.hotel import Hotel, Room
from core.models.reservation import Reservation, ReservationStatus
from sqlalchemy.ext.asyncio import AsyncSession
from cashews import cache


@cache(ttl=60*10, key="reservations:user:{user.id}")
async def get_user_reservations(user: User, db: AsyncSession):
    """ Возрат Reservation по User"""
    stmt: Result = await db.execute(
        select(Reservation)
        .where(Reservation.user_id == user.id)
        .order_by(Reservation.date_to.desc())
        # .options(
        #     selectinload(Reservation.room).selectinload(Room.hotel),
        #     selectinload(Reservation.room).selectinload(Room.room_information),
        #     selectinload(Reservation.payment),
        # )
    )

    reservations = stmt.scalars().all()

    return reservations


async def room_reservation_check(room_id: int, date_from: date, date_to: date, db: AsyncSession) -> bool:
    """ Проверка есть ли активные бронирования на комнату в указанные даты """
    stmt = select(Reservation).where(
        and_(
            Reservation.room_id == room_id,
            # Игнорируем отменённые брони
            Reservation.status.in_(
                [ReservationStatus.CONFIRMED, ReservationStatus.PENDING]
            ),
            # Условие пересечения интервалов
            Reservation.date_from < date_to,
            Reservation.date_to > date_from,
        )
    )
    overlap_res: Result = await db.execute(stmt)
    existing_reservation = overlap_res.scalar_one_or_none()
    if existing_reservation:
        return True
    return False


def calculate_price_booking_range(date_from: date, date_to: date, price_per_night: Decimal) -> Decimal:
    nights = (date_to - date_from).days
    total_price = Decimal(nights) * price_per_night
    logger.info(f"[calculate_price_booking_range] nights: {nights} | price_per_night: {price_per_night} | "
                f"total_price: {total_price}")
    return total_price
