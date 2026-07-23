from datetime import datetime, timedelta, timezone
import secrets
from abc import ABC, abstractmethod
from decimal import Decimal

import fastapi
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from fastapi import HTTPException, status

from core.email_service import EmailService
from core.models.user import User
from core.models.payment import Payment, BankAccount, PaymentStatus, VerificationCode
from payment_reservation_logic.dependencies import (
    get_bank_account_by_user_id,
    get_payment_by_id,
)

class AccountReplenishment(ABC):
    """ Интерфейс сервиса пополнения счета банковского аккаунта BankAccount """

    @abstractmethod
    async def process_top_up(self, amount: Decimal) -> Payment:
        """
        Стадия 1: Создание платежа со статусом PENDING,
        генерация одноразового кода и отправка его на почту.
        """
        pass

    @abstractmethod
    async def confirm_top_up(self, payment_id: int, code: str) -> BankAccount:
        """
        Стадия 2: Проверка введенного кода.
        При успехе: Payment.status -> PAID, BankAccount.balance += amount.
        """
        pass


class EmailReplenishmentService(AccountReplenishment):
    """ """
    def __init__(self, user: User, db: AsyncSession, email_service: EmailService):
        self.user = user
        self.db = db
        self.email_service = email_service

    @staticmethod
    def generate_verification_code() -> str:
        """Генерация 6-значного кода"""
        code = "".join(secrets.choice("0123456789") for _ in range(6))
        return code

    async def process_top_up(self, amount: Decimal) -> Payment:
        """ """
        bank_account = await get_bank_account_by_user_id(user_id=self.user.id, db=self.db)
        if bank_account.is_blocked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Аккаунт платежного сервиса заблокирован.",
            )

        new_payment = Payment(
            account_id=bank_account.id, amount=amount, status=PaymentStatus.PENDING
        )

        VERIFICATION_TIME_LIMIT = datetime.now(timezone.utc) + timedelta(
            minutes=10
        )  # 10 минут
        code = self.generate_verification_code()
        verification_code = VerificationCode(
            user_id=self.user.id,
            code=code,
            is_active=True,
            expires_at=VERIFICATION_TIME_LIMIT,
        )

        self.db.add_all([new_payment, verification_code])
        await self.db.commit()
        await self.db.refresh(new_payment)

        await self.email_service.send_confirmation_code(to_email=self.user.email, code=code)

        return new_payment

    async def confirm_top_up(self, payment_id: int, code: str) -> BankAccount:
        """Проверка кода подтверждения и проведение начисления сумму на аккаунт"""
        bank_account = await get_bank_account_by_user_id(
            user_id=self.user.id, db=self.db, block_update_column=True
        )
        if bank_account.is_blocked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Аккаунт платежного сервиса заблокирован.",
            )

        payment = await get_payment_by_id(
            payment_id=payment_id,
            account_id=bank_account.id,
            db=self.db,
            payment_status=PaymentStatus.PENDING,
        )

        stmt_code = (
            select(VerificationCode)
            .where(
                VerificationCode.user_id == self.user.id,
                VerificationCode.code == code,
                VerificationCode.is_active == True,
                VerificationCode.expires_at > datetime.now(timezone.utc),
            )
            .with_for_update() # от race conditions
        )
        res_code: Result = await self.db.execute(stmt_code)
        code_obj = res_code.scalar_one_or_none()

        if not code_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный или просроченный код подтверждения.",
            )

        # Проведение операцию
        code_obj.is_active = False
        payment.status = PaymentStatus.PAID
        bank_account.balance += payment.amount

        await self.db.commit()
        await self.db.refresh(bank_account)
        return bank_account
