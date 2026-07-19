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
    room_information = RoomInformation(**room_information_data)

    db.add(room_information)
    await db.commit()
    await db.refresh(room_information)

    return room_information
