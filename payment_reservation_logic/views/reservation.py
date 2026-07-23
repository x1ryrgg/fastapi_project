from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.models import Reservation
from core.models.user import UserRole, User
from core.permissions import RoleChecker
from hotel_logic.dependencies import get_hotel_by_id, get_room_by_id, check_manager_permissions
from payment_reservation_logic.crud.reservation import get_user_reservations
from payment_reservation_logic.schemas.bank_account import *
from payment_reservation_logic.crud.bank_account import *
from payment_reservation_logic.dependencies import *
from payment_reservation_logic.schemas.reservation import (
    ReservationResponse,
    SimpleReservationResponse, CreateReservationRequest,
)
from payment_reservation_logic.service import BookingService

router = APIRouter(
    prefix='/reservation',
    tags=['reservations']
)


@router.get("/", response_model=List[SimpleReservationResponse], status_code=status.HTTP_200_OK)
async def get_reservations(user: User = Depends(RoleChecker()), db: AsyncSession = Depends(get_db)):
    """ View Возвращает бранирования пользователя """
    return await get_user_reservations(user=user, db=db)


@router.get("/{reservation_id}", response_model=ReservationResponse, status_code=status.HTTP_200_OK)
async def get_user_reservation(reservation_id: int,
                               user: User = Depends(RoleChecker()),
                               db: AsyncSession = Depends(get_db)):
    """ View Получение информации по бронированию """
    return await get_user_reservation_by_id(reservation_id=reservation_id, user_id=user.id, db=db, load_relationships=True)


@router.post("/book", response_model=SimpleReservationResponse, status_code=status.HTTP_201_CREATED)
async def book_hotel_room(dto: CreateReservationRequest,
                          user: User = Depends(RoleChecker()),
                          db: AsyncSession = Depends(get_db)):
    booking_service = BookingService(user=user, db=db, code_sender=email_service)
    return await booking_service.book_room(
        room_id=dto.room_id,
        date_from=dto.date_from,
        date_to=dto.date_to,
    )