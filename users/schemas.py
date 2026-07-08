import re

from datetime import datetime
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str = Annotated[str, MaxLen(50)]
    email: EmailStr
    password: str
    created_at: datetime

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        # Проверка на длину
        if len(v) < 8:
            raise ValueError('[validate_password] пароль должен быть длинее 8 символов')
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


class UserUpdate(BaseModel):
    username: Optional[str] = Annotated[str, MaxLen(50)]
    email: Optional[EmailStr] = None
    password: Optional[str] = Annotated[str, MinLen(8)]


class UserBase(BaseModel):
    id: int


class UserResponse(UserBase):
    username: str
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        from_attributes = True


class UsersResponse(UserBase):
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
