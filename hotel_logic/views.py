import traceback
from typing import List, Annotated
from urllib.request import Request

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from sqlalchemy import select
from starlette import status

from users_logic.dependencies import get_user_by_id
from hotel_logic.schemas import HotelCreate, HotelResponse
from fastapi import Depends, Path, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from core.models.user import User
from pydantic import EmailStr
from core.logging_system import logger
from users_logic import crud
from hotel_logic import crud


router = APIRouter(
    prefix="/hotels",
    tags=["hotels"]
)


@router.post("/create/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel_in: HotelCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_hotel(db=db, hotel_in=hotel_in)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create Hotel",
        )

@router.get("/all/", response_model=List[HotelResponse], status_code=status.HTTP_200_OK)
async def get_all_hotels(db: AsyncSession = Depends(get_db)):
    try:
        return await crud.get_all_hotels(db=db)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get all Hotels",
        )