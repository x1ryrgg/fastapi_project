from decimal import Decimal
from datetime import datetime, date
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from core.models.hotel import RoomType
from core.models.payment import PaymentStatus
from hotel_logic.schemas import RoomResponse, RoomForReservationResponse
from payment_reservation_logic.schemas.payment import PaymentForReservationResponse


class SimpleReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    date_from: datetime
    date_to: datetime


class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    room_id: int
    date_from: datetime
    date_to: datetime

    room: RoomForReservationResponse
    payment: PaymentForReservationResponse


class CreateReservationRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

    @field_validator("date_to")
    @classmethod
    def validate_dates(cls, v: date, values):
        if "date_from" in values.data and v <= values.data["date_from"]:
            raise ValueError("Дата выезда (date_to) должна быть строго позже даты заезда (date_from)")
        return v
