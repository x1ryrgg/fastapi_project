from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from core.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging_system import logger
from core.models import User
from core.models.hotel import Hotel, Room, RoomInformation
from core.models.user import UserRole


async def get_hotel_by_id(hotel_id: int, db: AsyncSession = Depends(get_db), load_relationships: bool = False) -> Hotel:
    """ Получение Hotel по id """
    stmt = (select(Hotel).where(Hotel.id == hotel_id)
    )

    if load_relationships:
        stmt = stmt.options(
            selectinload(Hotel.users_link)
        )

    result: Result = await db.execute(stmt)
    hotel = result.scalar_one_or_none()

    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found"
        )

    return hotel

async def get_room_information_by_id(room_info_id: int, db: AsyncSession = Depends(get_db)) -> RoomInformation:
    """ Получение RoomInformation по id """
    room_info = await db.get(RoomInformation, room_info_id)
    if not room_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RoomInformation not found"
        )

    return room_info


async def get_room_by_id(room_id: int, db: AsyncSession = Depends(get_db), load_relationships: bool = False) -> Room:
    """ Получение Room по id """
    stmt = select(Room).where(Room.id == room_id)

    if load_relationships:
        stmt = stmt.options(
            joinedload(Room.hotel).selectinload(Hotel.users_link),
            joinedload(Room.room_information)
        )

    result: Result = await db.execute(stmt)
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    return room


def get_hotel_owners_ids(hotel: Hotel) -> List[int]:
    """ Возвращает список ID владельцев отеля """
    owner_ids = [link.user_id for link in hotel.users_link]

    if not owner_ids:
        logger.info(f"[get_hotel_owners_ids] У Отеля {hotel.name} (ID: {hotel.id}) нет владельцев.")

    return owner_ids


def check_manager_permissions(hotel: Hotel, user: User) -> bool:
    owner_ids = get_hotel_owners_ids(hotel=hotel)

    if user.role != UserRole.ADMIN and user.id not in owner_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )
    return True

