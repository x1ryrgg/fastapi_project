import traceback
from typing import List

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from core.models.hotel import Hotel, Room, RoomInformation, UserHotel
from hotel_logic.schemas import RoomInformationCreate, RoomInformationUpdate
from core.logging_system import logger
from fastapi import Depends, HTTPException, status


async def create_room_information(room_information_in: RoomInformationCreate, db: AsyncSession) -> RoomInformation:
    """ Создание RoomInformation """
    room_information_data = room_information_in.model_dump(exclude_unset=True)
    room_info = RoomInformation(**room_information_data)

    db.add(room_info)
    await db.commit()
    await db.refresh(room_info)

    return room_info

async def get_all_hotel_information(db: AsyncSession) -> List[RoomInformation]:
    """ Возврат всех записей RoomInformation """
    result: Result = await db.execute(select(RoomInformation).order_by(RoomInformation.type))
    room_info = result.scalars().all()

    return room_info

async def get_hotel_information(room_info_id: int, db: AsyncSession) -> RoomInformation:
    """ Возврат записи RoomInformation по id """
    room_info = await db.get(RoomInformation, room_info_id)
    if not room_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HotelInformation not found"
        )

    return room_info
