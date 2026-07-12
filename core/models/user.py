import uuid
from datetime import datetime
from random import choices
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Float
from core.models.base import Base

if TYPE_CHECKING:
    from .hotel import Hotel
    from .reservation import Reservation


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Связи
    hotels: Mapped[list["Hotel"]] = relationship(
        "Hotel", secondary="users_hotels", back_populates="users", lazy="selectin"
    )
    hotels_link: Mapped[list["UserHotel"]] = relationship(
        "UserHotel", back_populates="user", cascade="all, delete-orphan"
    )

    reservations: Mapped[list["Reservation"]] = relationship("Reservation", uselist=True, back_populates="user")

    UNIQUE_FIELDS = ["username", "email"]

    def __str__(self):
        return f"[{self.__class__.__name__} table] - {self.username} | {self.email}"

    def __repr__(self):
        return self
