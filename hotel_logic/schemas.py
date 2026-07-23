import re
from decimal import Decimal
from datetime import datetime
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from core.models.hotel import RoomType


class HotelCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=300)]
    city: Annotated[str, Field(min_length=1, max_length=300)]
    address: Annotated[str, Field(min_length=1, max_length=300)]
    region: Annotated[str, Field(min_length=1, max_length=300)]
    description: Optional[str] = "Нет описания."
    stars: Annotated[int, Field(ge=1, le=5)]
    phone: Optional[Annotated[str, Field(max_length=20)]] = None
    email: Optional[EmailStr] = None


class HotelUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=300)]] = None
    city: Optional[Annotated[str, Field(min_length=1, max_length=300)]] = None
    address: Optional[Annotated[str, Field(min_length=1, max_length=300)]] = None
    region: Optional[Annotated[str, Field(min_length=1, max_length=300)]] = None
    description: Optional[str] = None
    stars: Optional[Annotated[int, Field(ge=1, le=5)]] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class HotelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    address: str
    region: str
    description: Optional[str] = None
    stars: int
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class RoomInformationCreate(BaseModel):
    price_per_night: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2, description="Цена за сутки")]
    capacity: Optional[Annotated[int, Field(ge=1)]] = 1
    size: Optional[Annotated[float, Field(ge=15)]] = 15
    type: Optional[RoomType] = RoomType.SINGLE


class RoomInformationUpdate(BaseModel):
    price_per_night: Optional[Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2, description="Цена за сутки")]] = None
    capacity: Optional[Annotated[int, Field(ge=1)]] = None
    size: Optional[Annotated[float, Field(ge=15)]] = None
    type: Optional[RoomType] = None


class RoomInformationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    price_per_night: Decimal
    capacity: int
    size: float
    type: RoomType
    created_at: datetime
    updated_at: datetime


class RoomCreate(BaseModel):
    hotel_id: Annotated[int, Field(ge=1)]
    info_id: Optional[Annotated[int, Field(ge=1)]] = None
    floor: Annotated[int, Field(ge=1)]
    number: Annotated[int, Field(ge=1)]


class RoomUpdate(BaseModel):
    hotel_id: Optional[Annotated[int, Field(ge=1)]] = None
    info_id: Optional[Annotated[int, Field(ge=1)]] = None
    floor: Optional[Annotated[int, Field(ge=1)]] = None
    number: Optional[Annotated[int, Field(ge=1)]] = None


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    floor: int
    number: int
    created_at: datetime
    updated_at: datetime

    hotel: HotelResponse
    room_information: RoomInformationResponse


class HotelForReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    address: str
    region: str
    phone: Optional[str] = None
    email: Optional[str] = None


class RoomForReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    floor: int
    number: int

    hotel: HotelForReservationResponse
    room_information: RoomInformationResponse

