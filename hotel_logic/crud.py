import traceback

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from core.models.hotel import Hotel, Room, RoomInformation, UserHotel
from hotel_logic.schemas import HotelCreate
from core.logging_system import logger


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


async def get_all_hotels(db: AsyncSession):
    try:
        result: Result = await db.execute(select(Hotel).order_by(Hotel.id))
        users = result.scalars().all()

        return users
    except Exception as e:
        logger.error(f"[get_all_hotels] Exception: {e} | {traceback.format_exc()}")
        return None