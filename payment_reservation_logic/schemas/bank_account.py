from decimal import Decimal
from datetime import datetime
from typing import Annotated, Optional, List
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from core.models.hotel import RoomType
from payment_reservation_logic.schemas.payment import PaymentResponse


class BankAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    account_number: str
    balance: Decimal
    currency: str
    is_blocked: bool
    created_at: datetime

    payments: List[PaymentResponse] = Field(default_factory=list)


class TopUpRequest(BaseModel):
    amount: Decimal = Field(gt=0, description="Сумма пополнения должна быть больше 0")
