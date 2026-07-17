import re

from datetime import datetime
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class HotelCreate(BaseModel):
    name: str = Annotated[str, MaxLen(300)]
    city: str = Annotated[str, MaxLen(300)]
    address: str = Annotated[str, MaxLen(300)]
    region: str = Annotated[str, MaxLen(300)]
    description: Optional[str]
    stars: int = Annotated[int, MaxLen(5)]
    phone: Optional[str]
    email: Optional[str]


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
    description: Optional[str]
    stars: int
    phone: Optional[str]
    email: Optional[str]
