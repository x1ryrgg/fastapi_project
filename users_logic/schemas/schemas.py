import re

from datetime import datetime
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class UserCreate(BaseModel):
    username: str = Annotated[str, MaxLen(50)]
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        # Проверка на длину
        if len(v) < 8:
            raise ValueError('[validate_password] пароль должен быть минимум в 8 символов.')
        # Проверка на буквенные знаки
        # if not re.search(r'[A-Z]', v):
        #     raise ValueError('[validate_password] пароль должен иметь хотя бы одну английскую буку')
        # # Проверка на цифры
        # if not re.search(r'[0-9]', v):
        #     raise ValueError('[validate_password] пароль должен иметь хотя бы одну цифру')
        # # Проверка на специальные знаки
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        #     raise ValueError('[validate_password] пароль должен иметь хотя бы один специальный знак')
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[Annotated[str, Field(max_length=50)]] = None
    email: Optional[EmailStr] = None
    password: Optional[Annotated[str, Field(min_length=8)]] = None


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserResponse(UserBase):
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime


class UsersResponse(UserBase):
    username: str
    email: EmailStr
    created_at: datetime
