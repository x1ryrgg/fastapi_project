import traceback
from typing import List, Annotated
from urllib.request import Request

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from sqlalchemy import select
from starlette import status

from core.models import Hotel
from hotel_logic.dependencies import get_hotel_by_id
from users_logic.dependencies import get_user_by_id
from hotel_logic.schemas import HotelCreate, HotelResponse, HotelUpdate
from fastapi import Depends, Path, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from core.models.user import User
from pydantic import EmailStr
from core.logging_system import logger
from hotel_logic import crud


router = APIRouter(
    prefix="/hotels",
    tags=["hotels"]
)


@router.post("/create/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel_in: HotelCreate, db: AsyncSession = Depends(get_db)):
    """ View создания отеля. """
    return await crud.create_hotel(hotel_in=hotel_in, db=db)


@router.get("/all/", response_model=List[HotelResponse], status_code=status.HTTP_200_OK)
async def get_all_hotels(db: AsyncSession = Depends(get_db)):
    """ View выдача всех отелей. """
    return await crud.get_all_hotels(db=db)


@router.get("/{hotel_id}/", response_model=HotelResponse, status_code=status.HTTP_200_OK)
async def get_hotel(hotel: Hotel = Depends(get_hotel_by_id)):
    """ View для получения Hotel по его id. """
    return hotel


@router.delete("/{hotel_id}/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id: int, db: AsyncSession = Depends(get_db)):
    """ """
    return await crud.delete_hotel(hotel_id=hotel_id, db=db)


@router.patch("/{hotel_id}/patch/", response_class=HotelResponse, status_code=status.HTTP_200_OK)
async def patch_hotel(hotel_id: int, hotel_in: HotelUpdate, db: AsyncSession = Depends(get_db)):
    """ """
    return await crud.update_hotel(hotel_id=hotel_id, hotel_in=hotel_in, db=db)