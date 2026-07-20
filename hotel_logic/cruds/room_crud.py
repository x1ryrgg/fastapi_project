import traceback
from typing import List

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.models.hotel import Hotel, Room, RoomInformation, UserHotel
from hotel_logic.cruds.hotel_crud import get_hotel_by_id
from hotel_logic.dependencies import get_room_information_by_id
from hotel_logic.schemas import RoomInformationCreate, RoomInformationUpdate, RoomCreate, RoomUpdate
from core.logging_system import logger
from fastapi import Depends, HTTPException, status


# =========================== RoomInformation CRUD ==========================
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

async def update_room_information(room_info_id: int, room_info_in: RoomInformationUpdate, db: AsyncSession):
    """ Частичное обновление RoomInformation """
    room_info = await get_room_information_by_id(room_info_id, db=db)

    room_info_data = room_info_in.model_dump(exclude_unset=True)

    for field, value in room_info_data.items():
        setattr(room_info, field, value)

    await db.commit()
    await db.refresh(room_info)
    return room_info

async def delete_room_information(room_info_id: int, db: AsyncSession) -> bool:
    """ Удаление RoomInformation """
    room_info = await get_room_information_by_id(room_info_id, db=db)

    room_info_id = room_info.id # для лога

    await db.delete(room_info)
    await db.commit()
    logger.info(f"[delete_room_information] Hotel #{room_info_id} successfully deleted. ")
    return True


# =========================== Room CRUD ==========================
async def create_room(room_in: RoomCreate, db: AsyncSession) -> Room:
    """ """
    room_data = room_in.model_dump(exclude_unset=True)

    await get_hotel_by_id(hotel_id=room_data.get('hotel_id'), db=db)

    info_id = room_data.get('info_id')
    if info_id:
        await get_room_information_by_id(room_info_id=info_id, db=db)

    result: Result = await db.execute(select(Room)
        .where((Room.hotel_id == room_data.get('hotel_id')) & (Room.number == room_data.get('number')))
        )
    existing_room = result.scalars().one_or_none()
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room with that number already has in this hotel."
        )

    room = Room(**room_data)

    db.add(room)
    await db.commit()
    await db.refresh(room)

    return room

async def get_all_rooms(hotel_id: int, db: AsyncSession) -> List[Room]:
    """ """
    result: Result = await db.execute(select(Room).options(
        joinedload(Room.hotel),
        joinedload(Room.room_information)
            ).where(Room.hotel_id == hotel_id)
        )
    rooms = result.scalars().all()

    return rooms