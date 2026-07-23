from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Numeric, ForeignKey, Boolean, func, DateTime, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base

if TYPE_CHECKING:
    from .user import User
    from .reservation import Reservation


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    account_number: Mapped[str] = mapped_column(
        String(34), unique=True, index=True, nullable=False, comment="Номер счета"
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00"), comment="Баланс"
    )

    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="RUB", comment="Валюта")
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, comment="Статус аккаунта")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship("User", uselist=False, back_populates="bank_account")
    payments: Mapped[list["Payment"]] = relationship("Payment", uselist=True, back_populates="account")

    def __str__(self):
        return f"[BankAccount] User ID: {self.user_id} | Balance: {self.balance} {self.currency}"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    account_id: Mapped[int] = mapped_column(
        ForeignKey("bank_accounts.id", ondelete="RESTRICT"), nullable=False
    )
    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id", ondelete="CASCADE"),
        nullable=True, unique=True,
        comment="ID бронирования (NULL если это пополнение счета)"
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment="Сумма")
    status: Mapped[PaymentStatus] = mapped_column(
        String(20), nullable=False, default=PaymentStatus.PENDING, comment="Статус операции"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    account: Mapped["BankAccount"] = relationship("BankAccount", uselist=False, back_populates="payments")
    reservation: Mapped["Reservation"] = relationship("Reservation", uselist=False, back_populates="payment")


class VerificationCode(Base):
    __tablename__ = "code_verifications"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="Внешний ключ к пользователю",
    )
    code: Mapped[str] = mapped_column(
        String(6), nullable=False, comment="Код"
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False, default=True, comment="Статус кода"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="Время окончания действия кода"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now()
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="code_verifications"
    )

    __table_args__ = (Index("ix_user_code_active", "user_id", "code", "is_active"),)
