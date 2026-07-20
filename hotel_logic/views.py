from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from starlette import status

from core.models import Hotel, RoomInformation, Room
from core.models.user import UserRole, User
from core.permissions import RoleChecker
from hotel_logic.dependencies import get_hotel_by_id, get_room_information_by_id, get_room_by_id
from hotel_logic.schemas import (HotelCreate, HotelResponse, HotelUpdate,
                                 RoomInformationResponse, RoomInformationCreate, RoomInformationUpdate, RoomCreate,
                                 RoomResponse, RoomUpdate)
from fastapi import Depends, APIRouter, HTTPException, status
from hotel_logic.cruds import hotel_crud, room_crud
from users_logic.getters import get_hotel_owners_ids

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"]
)


# ======================== HOTEL VIEWS ==============================
@router.post("/create/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel_in: HotelCreate,
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(RoleChecker(UserRole.HOTEL_MANAGER))):
    """ View создания отеля. """
    return await hotel_crud.create_hotel(hotel_in=hotel_in, user_id=user.id, db=db)


@router.get("/all/", response_model=List[HotelResponse], status_code=status.HTTP_200_OK)
async def get_all_hotels(db: AsyncSession = Depends(get_db), ):
    """ View выдача всех отелей. """
    return await hotel_crud.get_all_hotels(db=db)


@router.get("/{hotel_id}/", response_model=HotelResponse, status_code=status.HTTP_200_OK)
async def get_hotel(hotel: Hotel = Depends(get_hotel_by_id)):
    """ View для получения Hotel по его id. """
    return hotel


@router.delete("/{hotel_id}/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id: int,
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(RoleChecker(UserRole.HOTEL_MANAGER))):
    """ """
    return await hotel_crud.delete_hotel(hotel_id=hotel_id, db=db)


@router.patch("/{hotel_id}/patch/", response_model=HotelResponse, status_code=status.HTTP_200_OK)
async def patch_hotel(hotel_id: int, hotel_in: HotelUpdate,
                      db: AsyncSession = Depends(get_db),
                      user: User = Depends(RoleChecker(UserRole.HOTEL_MANAGER))):
    """ """
    return await hotel_crud.update_hotel(hotel_id=hotel_id, hotel_in=hotel_in, db=db)


# =========================== ROOM INFORMATION VIEWS ==========================
@router.post("/rooms/information/create/", response_model=RoomInformationResponse, status_code=status.HTTP_201_CREATED)
async def create_room_information(room_information_in: RoomInformationCreate,
                                  db: AsyncSession = Depends(get_db),
                                  user: User = Depends(RoleChecker(UserRole.HOTEL_MANAGER))):
    """ """
    return await room_crud.create_room_information(room_information_in=room_information_in, db=db)


@router.get("/rooms/information/all/", response_model=List[RoomInformationResponse], status_code=status.HTTP_200_OK)
async def get_all_room_information(db: AsyncSession = Depends(get_db), user: User = Depends(RoleChecker())):
    """ """
    return await room_crud.get_all_hotel_information(db=db)


@router.get("/rooms/information/{room_info_id}/", response_model=RoomInformationResponse, status_code=status.HTTP_200_OK)
async def get_room_information(db: AsyncSession = Depends(get_db),
                                   user: User = Depends(RoleChecker()),
                                   room_information: RoomInformation = Depends(get_room_information_by_id)):
    """ """
    return room_information


@router.patch("/rooms/information/{room_info_id}/patch/", response_model=RoomInformationResponse, status_code=status.HTTP_200_OK)
async def patch_room_information(room_info_id: int, room_info_in: RoomInformationUpdate,
                                 db: AsyncSession = Depends(get_db),
                                 user: User = Depends(RoleChecker(UserRole.HOTEL_MANAGER))):
    """ """
    return await room_crud.update_room_information(room_info_id=room_info_id, room_info_in=room_info_in, db=db)


@router.delete("/rooms/information/{room_info_id}/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(room_info_id: int,
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(RoleChecker(UserRole.HOTEL_MANAGER))):
    """ """
    return await room_crud.delete_room_information(room_info_id=room_info_id, db=db)


# =========================== ROOM VIEWS ==========================
@router.post("/rooms/create/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(room_in: RoomCreate,
                      db: AsyncSession = Depends(get_db),
                      user: User =Depends(RoleChecker(UserRole.HOTEL_MANAGER))):
    """ """
    hotel = await get_hotel_by_id(hotel_id=room_in.hotel_id, db=db)

    owner_ids = get_hotel_owners_ids(hotel=hotel)
    if user.role != UserRole.ADMIN and user.id not in owner_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )

    return await room_crud.create_room(room_in=room_in, db=db)


@router.get("/{hotel_id}/rooms/all/", response_model=List[RoomResponse], status_code=status.HTTP_200_OK)
async def get_all_rooms(hotel_id:int, db: AsyncSession = Depends(get_db)):
    """ """
    return await room_crud.get_all_rooms(hotel_id=hotel_id, db=db)


@router.get("/rooms/{room_id}/", response_model=RoomResponse, status_code=status.HTTP_200_OK)
async def get_room(room: Room = Depends(get_room_by_id)):
    return room


@router.patch("/rooms/{room_id}/patch/", response_model=RoomResponse, status_code=status.HTTP_200_OK)
async def patch_room(room_id: int, room_in: RoomUpdate,
                     user: User = Depends(RoleChecker(UserRole.HOTEL_MANAGER)), db: AsyncSession = Depends(get_db)):
    """ """
    pass

@router.delete("/rooms/{room_id}/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    """ """
    pass