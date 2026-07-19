import traceback
from typing import List

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from core.models.hotel import Hotel, Room, RoomInformation, UserHotel
from hotel_logic.schemas import HotelCreate, HotelUpdate
from core.logging_system import logger
from fastapi import Depends, HTTPException, status


async def create_hotel(hotel_in: HotelCreate, db: AsyncSession) -> Hotel:
    try:
        hotel_info = hotel_in.model_dump()

        hotel = Hotel(**hotel_info)
        db.add(hotel)
        await db.commit()
    except Exception as e:
        logger.error(f"[create_hotel] Exception: {e} | {traceback.format_exc()}")
        return None

    return hotel


async def get_all_hotels(db: AsyncSession) -> List[Hotel]:
    try:
        result: Result = await db.execute(select(Hotel).order_by(Hotel.id))
        hotels = result.scalars().all()

        return hotels
    except Exception as e:
        logger.error(f"[get_all_hotels] Exception: {e} | {traceback.format_exc()}")
        return None


async def get_hotel_by_id(hotel_id: int, db: AsyncSession) -> Hotel:
    hotel = await db.get(Hotel, hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found"
        )

    return hotel


async def delete_hotel(hotel_id: int, db: AsyncSession) -> bool:
    hotel = await get_hotel_by_id(hotel_id, db=db)

    hotel_name = hotel.name # для лога

    await db.delete(hotel)
    await db.commit()
    logger.info(f"[delete_hotel] Hotel {hotel_name} successfully deleted. ")
    return True


async def update_hotel(hotel_id: int, hotel_in: HotelUpdate, db: AsyncSession):
    hotel = await get_hotel_by_id(hotel_id, db=db)

    hotel_data = hotel_in.model_dump(exclude_unset=True)

    for field, value in hotel_data.items():
        setattr(hotel, field, value)

    await db.commit()
    await db.refresh(hotel)
    return hotel
