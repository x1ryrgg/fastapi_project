from enum import Enum
import uuid
from random import choices

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Float, Text

from core.models.base import Base


class Hotel(Base):
    __tablename__ = 'hotels'

    name = Column(String(300), nullable=False, index=True)
    city = Column(String(300), nullable=False, index=True)
    address = Column(String(300), nullable=False)
    region = Column(String(300), nullable=False)
    description = Column(Text, nullable=True, default="Нет описания.")
    phone = Column(String(20), nullable=True)
    email = Column(String(300), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    rooms = relationship('Room',
                         uselist=True,
                         back_populates='hotel',
                         cascade='all, delete-orphan')

class RoomType(Enum):
    SINGLE = "single"        # одноместный
    DOUBLE = "double"        # двухместный
    TWIN = "twin"            # с двумя отдельными кроватями
    SUITE = "suite"          # люкс
    FAMILY = "family"        # семейный
    APARTMENT = "apartment"  # апартаменты


class Room(Base):
    __tablename__ = 'rooms'

    hotel_id = Column(Integer, ForeignKey('hotels.id', ondelete='CASCADE'), nullable=False)
    info_id = Column(Integer, ForeignKey('room_information.id', ondelete='SET NULL'), nullable=True)
    type = Column(Enum(RoomType), nullable=False, default=RoomType.SINGLE)
    floor = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    hotel = relationship("Hotel",
                         uselist=False,
                         back_populates="rooms")

    room_information = relationship("RoomInformation",
                                    uselist=False,
                                    back_populates="room")


class RoomInformation(Base):
    __tablename__ = 'room_information'

    price_per_night = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False, default=1)
    size = Column(Float, nullable=False, default=15)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("size >= 12", name="size_min_length"),
        CheckConstraint("capacity > 0", name="capacity_more_than_one")
    )

    room = relationship("Room",
                        uselist=True,
                        back_populates="room_information")