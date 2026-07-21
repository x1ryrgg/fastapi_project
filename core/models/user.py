import uuid
from datetime import datetime
from random import choices
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Float, Boolean
from core.models.base import Base
from enum import Enum

if TYPE_CHECKING:
    from .hotel import Hotel, UserHotel
    from .reservation import Reservation


class UserRole(str, Enum):
    CUSTOMER = "customer"  # Обычный клиент (бронирует)
    HOTEL_MANAGER = "manager"  # Сотрудник отеля (управляет комнатами)
    ADMIN = "admin" # поддержка платформы и имеет возможность ко всем функциям

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    role: Mapped[UserRole] = mapped_column(String(20), nullable=False, default=UserRole.CUSTOMER)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Связи
    hotels: Mapped[list["Hotel"]] = relationship(
        "Hotel", secondary="users_hotels", back_populates="users", lazy="selectin", viewonly=True
    )
    hotels_link: Mapped[list["UserHotel"]] = relationship( # если удалится пользователь, то удалятся все связанные данные в UserHotel
        "UserHotel", back_populates="user", cascade="all, delete-orphan"
    )

    reservations: Mapped[list["Reservation"]] = relationship(
        "Reservation", uselist=True, back_populates="user", cascade="all, delete-orphan"
    )

    bank_account: Mapped[Optional["User"]] = relationship(
        "BankAccount", uselist=False, back_populates="user"
    )

    UNIQUE_FIELDS = ["username", "email"]

    def __str__(self):
        return f"[{self.__class__.__name__} table] - {self.username} | {self.email}"

    def __repr__(self):
        return self
