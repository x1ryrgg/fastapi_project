import traceback
from typing import List

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from core.models.hotel import Hotel, Room, RoomInformation, UserHotel
from hotel_logic.schemas import HotelCreate, HotelUpdate
from core.logging_system import logger
from fastapi import Depends, HTTPException, status
from hotel_logic.dependencies import get_hotel_by_id



async def create_hotel(hotel_in: HotelCreate, user_id: int, db: AsyncSession) -> Hotel:
    """ Создание Hotel """
    hotel_info = hotel_in.model_dump()
    hotel = Hotel(**hotel_info)

    user_hotel = UserHotel(user_id=user_id)
    hotel.users_link.append(user_hotel)

    db.add(hotel)
    await db.commit()
    await db.refresh(hotel)

    return hotel


async def get_all_hotels(db: AsyncSession) -> List[Hotel]:
    """ Получение всех Hotel"""
    result: Result = await db.execute(select(Hotel).order_by(Hotel.id))
    hotels = result.scalars().all()

    return hotels


async def update_hotel(hotel_id: int, hotel_in: HotelUpdate, db: AsyncSession):
    """ Обновление Hotel"""
    hotel = await get_hotel_by_id(hotel_id, db=db)

    hotel_data = hotel_in.model_dump(exclude_unset=True)

    for field, value in hotel_data.items():
        setattr(hotel, field, value)

    await db.commit()
    await db.refresh(hotel)
    return hotel


async def delete_hotel(hotel_id: int, db: AsyncSession) -> bool:
    """ Удаление Hotel"""
    hotel = await get_hotel_by_id(hotel_id, db=db)

    hotel_name = hotel.name # для лога

    await db.delete(hotel)
    await db.commit()
    logger.info(f"[delete_hotel] Hotel {hotel_name} successfully deleted. ")
    return True
