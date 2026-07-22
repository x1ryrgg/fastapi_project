from datetime import datetime
from typing import TYPE_CHECKING, Optional
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime, String
from core.mixins import UserRelationMixin
from core.models.base import Base

if TYPE_CHECKING:
    from .hotel import Room
    from .payment import Payment
    from .user import User


class Reservation(Base):
    __tablename__ = "reservations"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rooms.id"), comment="Внешний ключ к номеру", nullable=False
    )
    date_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), comment="Дата от", nullable=False
    )
    date_to: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), comment="Дата до", nullable=True
    )

    # Связи
    room: Mapped["Room"] = relationship("Room",
                                        uselist=False,
                                        back_populates="reservations",
                                        )
    payment: Mapped[Optional["Payment"]] = relationship(
        "Payment", back_populates="reservation", uselist=False
    )
    user: Mapped["User"] = relationship(
        "User",
        uselist=False,
        back_populates="reservations",
    )
