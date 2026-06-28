import re

from datetime import datetime
from typing import Annotated
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
            raise ValueError('╨Я╨░╤А╨╛╨╗╤М ╨┤╨╛╨╗╨╢╨╡╨╜ ╤Б╨╛╨┤╨╡╤А╨╢╨░╤В╤М ╨╝╨╕╨╜╨╕╨╝╤Г╨╝ 8 ╤Б╨╕╨╝╨▓╨╛╨╗╨╛╨▓')
        # Проверка на буквенные знаки
        # if not re.search(r'[A-Z]', v):
        #     raise ValueError('╨Я╨░╤А╨╛╨╗╤М ╨┤╨╛╨╗╨╢╨╡╨╜ ╤Б╨╛╨┤╨╡╤А╨╢╨░╤В╤М ╤Е╨╛╤В╤П ╨▒╤Л ╨╛╨┤╨╜╤Г ╨╖╨░╨│╨╗╨░╨▓╨╜╤Г╤О ╨▒╤Г╨║╨▓╤Г')
        # # Проверка на цифры
        # if not re.search(r'[0-9]', v):
        #     raise ValueError('╨Я╨░╤А╨╛╨╗╤М ╨┤╨╛╨╗╨╢╨╡╨╜ ╤Б╨╛╨┤╨╡╤А╨╢╨░╤В╤М ╤Е╨╛╤В╤П ╨▒╤Л ╨╛╨┤╨╜╤Г ╤Ж╨╕╤Д╤А╤Г')
        # # Проверка на специальные знаки
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        #     raise ValueError('╨Я╨░╤А╨╛╨╗╤М ╨┤╨╛╨╗╨╢╨╡╨╜ ╤Б╨╛╨┤╨╡╤А╨╢╨░╤В╤М ╤Е╨╛╤В╤П ╨▒╤Л ╨╛╨┤╨╕╨╜ ╤Б╨┐╨╡╤Ж╨╕╨░╨╗╤М╨╜╤Л╨╣ ╤Б╨╕╨╝╨▓╨╛╨╗')
        return v


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        from_attributes = True


class UsersResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
