import re

from datetime import datetime
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from core.models.hotel import RoomType


class HotelCreate(BaseModel):
    name: str = Annotated[str, MaxLen(300)]
    city: str = Annotated[str, MaxLen(300)]
    address: str = Annotated[str, MaxLen(300)]
    region: str = Annotated[str, MaxLen(300)]
    description: Optional[str]
    stars: int = Annotated[int, MaxLen(5)]
    phone: Optional[str]
    email: Optional[str]
    created_at: datetime
    updated_at: datetime


class HotelUpdate(BaseModel):
    name: Optional[Annotated[str, Field(max_length=300)]] = None
    city: Optional[Annotated[str, Field(max_length=300)]] = None
    address: Optional[Annotated[str, Field(max_length=300)]] = None
    region: Optional[Annotated[str, Field(max_length=300)]] = None
    description: Optional[str] = None
    stars: Optional[Annotated[int, Field(ge=1, le=5)]] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class HotelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    city: str
    address: str
    region: str
    description: str
    stars: int
    phone: str
    email: str


class RoomInformationCreate(BaseModel):
    price_per_night: float
    capacity: Optional[Annotated[int, Field(ge=1)]] = None
    size: Optional[Annotated[float, Field(ge=15)]] = None
    type: Optional[RoomType] = None


class RoomInformationUpdate(BaseModel):
    price_per_night: Optional[float] = None
    capacity: Optional[Annotated[int, Field(ge=1)]] = None
    size: Optional[Annotated[float, Field(ge=15)]] = None
    type: Optional[RoomType] = None


class RoomInformationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    price_per_night: float
    capacity: int
    size: float
    type: RoomType
    created_at: datetime
    updated_at: datetime
