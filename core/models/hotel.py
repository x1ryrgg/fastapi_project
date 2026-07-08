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
from typing import List, Optional

from core.models import User
from core.mixins import UserRelationMixin
from core.models.base import Base


class Hotel(UserRelationMixin, Base):
    __tablename__ = 'hotels'

    _user_nullable = True
    _user_back_populates = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    region: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="Нет описания.")
    stars: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="hotel",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("stars <= 5", name="stars_max_count"),
    )


class RoomType(Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TWIN = "twin"
    SUITE = "suite"
    FAMILY = "family"
    APARTMENT = "apartment"


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hotel_id: Mapped[int] = mapped_column(
        ForeignKey('hotels.id', ondelete='CASCADE'),
        nullable=False
    )
    info_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('room_information.id', ondelete='SET NULL'),
        nullable=True
    )
    type: Mapped[RoomType] = mapped_column(
        SQLEnum(RoomType),
        nullable=False,
        default=RoomType.SINGLE
    )
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    hotel: Mapped["Hotel"] = relationship(
        "Hotel",
        back_populates="rooms",
        uselist=False
    )
    room_information: Mapped[Optional["RoomInformation"]] = relationship(
        "RoomInformation",
        back_populates="room",
        uselist=False
    )


class RoomInformation(Base):
    __tablename__ = 'room_information'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    price_per_night: Mapped[float] = mapped_column(Float, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    size: Mapped[float] = mapped_column(Float, nullable=False, default=15)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Связь
    room: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="room_information"
    )

    __table_args__ = (
        CheckConstraint("size >= 12", name="size_min_length"),
        CheckConstraint("capacity > 0", name="capacity_positive"),
    )