from core.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.hotel import Hotel, Room, RoomInformation


async def get_hotel_by_id(hotel_id: int, db: AsyncSession = Depends(get_db)):
    """ Нахождение записи Hotel по id. """
    hotel = await db.get(Hotel, hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel not found"
        )

    return hotel