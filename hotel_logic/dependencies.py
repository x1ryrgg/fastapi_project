from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from core.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.hotel import Hotel, Room, RoomInformation


async def get_hotel_by_id(hotel_id: int, db: AsyncSession = Depends(get_db)):
    """ Нахождение записи Hotel по id. """
    stmt = (
        select(Hotel)
        .options(selectinload(Hotel.users_link))  # <-- Жадно подгружаем связь
        .where(Hotel.id == hotel_id)
    )
    result = await db.execute(stmt)
    hotel = result.scalar_one_or_none()

    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found"
        )

    return hotel

async def get_room_information_by_id(room_info_id: int, db: AsyncSession = Depends(get_db)) -> RoomInformation:
    """ Возврат RoomInformation по id """
    room_info = await db.get(RoomInformation, room_info_id)
    if not room_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RoomInformation not found"
        )

    return room_info

async def get_room_by_id(room_id: int, db: AsyncSession = Depends(get_db)) -> Room:
    """ Возврат Room по id """
    result: Result = await db.execute(select(Room).options(
        joinedload(Room.hotel),
        joinedload(Room.room_information)
    ).where(Room.id == room_id)
    )
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )

    return room
