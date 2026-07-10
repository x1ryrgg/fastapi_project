from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, DateTime
from core.mixins import UserRelationMixin
from core.models.base import Base

if TYPE_CHECKING:
    from .hotel import Room


class Reservation(UserRelationMixin, Base):
    __tablename__ = "reservations"

    _user_back_populates = "reservations"
    _use_list = True

    room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rooms.id"), comment="Внешний ключ к номеру", nullable=False
    )
    date_from: Mapped[datetime] = mapped_column(
        DateTime, comment="Дата от", nullable=False
    )
    date_to: Mapped[datetime] = mapped_column(
        DateTime, comment="Дата до", nullable=True
    )

    # Связи
    room: Mapped["Room"] = relationship("Room",
                                        uselist=False,
                                        back_populates="reservations",
                                        )
