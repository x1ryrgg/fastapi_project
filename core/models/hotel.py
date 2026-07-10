from datetime import datetime
from enum import Enum
import uuid
from random import choices

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Float, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional, TYPE_CHECKING

from core.mixins import UserRelationMixin
from core.models.base import Base

if TYPE_CHECKING:
    from .reservation import Reservation


class Hotel(UserRelationMixin, Base):
    __tablename__ = "hotels"

    _user_nullable = True
    _user_back_populates = "hotels"

    name: Mapped[str] = mapped_column(
        String(300), comment="Название отеля", nullable=False, index=True
    )
    city: Mapped[str] = mapped_column(
        String(300), comment="Город местоположения", nullable=False, index=True
    )
    address: Mapped[str] = mapped_column(String(300), comment="Адрес", nullable=False)
    region: Mapped[str] = mapped_column(String(300), comment="Регион", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        Text, comment="Описание", nullable=True, default="Нет описания."
    )
    stars: Mapped[int] = mapped_column(
        Integer, comment="Количество звезд", nullable=False, default=0
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), comment="Номер телефона", nullable=True
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(300), comment="Почта", nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # Связи
    rooms: Mapped[List["Room"]] = relationship(
        "Room", back_populates="hotel", cascade="all, delete-orphan"
    )

    __table_args__ = (CheckConstraint("stars <= 5", name="stars_max_count"),)


class RoomType(Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TWIN = "twin"
    SUITE = "suite"
    FAMILY = "family"
    APARTMENT = "apartment"


class Room(Base):
    __tablename__ = "rooms"

    hotel_id: Mapped[int] = mapped_column(
        ForeignKey("hotels.id", ondelete="CASCADE"),
        comment="Внешний ключ к отелю",
        nullable=False,
    )
    info_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("room_information.id", ondelete="SET NULL"), nullable=True
    )
    type: Mapped[RoomType] = mapped_column(
        SQLEnum(RoomType), nullable=False, default=RoomType.SINGLE
    )
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # Связи
    hotel: Mapped["Hotel"] = relationship(
        "Hotel", back_populates="rooms", uselist=False
    )
    room_information: Mapped[Optional["RoomInformation"]] = relationship(
        "RoomInformation", back_populates="room", uselist=False
    )
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", uselist=True, back_populates="room", cascade="all, delete-orphan"
    )


class RoomInformation(Base):
    __tablename__ = "room_information"

    price_per_night: Mapped[float] = mapped_column(Float, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    size: Mapped[float] = mapped_column(Float, nullable=False, default=15)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # Связи
    room: Mapped[List["Room"]] = relationship("Room", uselist=True, back_populates="room_information")

    __table_args__ = (
        CheckConstraint("size >= 12", name="size_min_length"),
        CheckConstraint("capacity > 0", name="capacity_positive"),
    )
