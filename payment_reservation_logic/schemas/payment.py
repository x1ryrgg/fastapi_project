from decimal import Decimal
from datetime import datetime
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from core.models.hotel import RoomType
from core.models.payment import PaymentStatus


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    reservation_id: Optional[int] = None
    amount: Decimal
    status: PaymentStatus
    created_at: datetime


class PaymentForReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    amount: Decimal
    status: PaymentStatus
    created_at: datetime
