from datetime import datetime, timedelta, timezone
import random

from fastapi import HTTPException, status
from decimal import Decimal

from core.email_service import email_service
from core.logging_system import logger
from sqlalchemy import select
from core.models.payment import BankAccount, Payment, PaymentStatus, VerificationCode
from core.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from payment_reservation_logic.dependencies import get_bank_account_by_user_id, get_payment_by_id

async def generate_account_number(db: AsyncSession) -> str:
    """ Генерация номера счета """
    prefix = "40817810"  # Стандартный префикс физических лиц
    while True:
        random_digits = "".join([str(random.randint(0, 9)) for _ in range(12)])
        acc_number = f"{prefix}{random_digits}"

        # Проверяем, существует ли уже такой номер в БД
        result = await db.execute(
            select(BankAccount).where(BankAccount.account_number == acc_number)
        )
        if not result.scalar_one_or_none():
            return acc_number

async def create_user_bank_account(user: User, db: AsyncSession) -> BankAccount:
    """ Создание личного внутреннего счета для пользователя"""

    result = await db.execute(select(BankAccount).where(BankAccount.user_id == user.id))
    existing_account = result.scalar_one_or_none()

    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть открытый банковский счёт",
        )

    account_number = await generate_account_number(db=db)

    bank_account = BankAccount(user_id=user.id, account_number=account_number)

    db.add(bank_account)
    await db.commit()
    await db.refresh(bank_account, attribute_names=["payments"])
    logger.info(f"[create_user_bank_account] Пользователь #{user.id} (username: {user.username}) "
                f"created BankAccount with number {account_number}")
    return bank_account


def generate_verification_code() -> str:
    """Генерация 6-значного кода"""
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    return code


async def process_top_up(user: User, amount: Decimal, db: AsyncSession) -> Payment:
    """ """
    bank_account = await get_bank_account_by_user_id(user_id=user.id, db=db)
    if bank_account.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Аккаунт платежного сервиса заблокирован.",
        )

    new_payment = Payment(
        account_id=bank_account.id, amount=amount, status=PaymentStatus.PENDING
    )

    VERIFICATION_TIME_LIMIT = datetime.now(timezone.utc) + timedelta(minutes=10)  # 10 минут
    code = generate_verification_code()
    verification_code = VerificationCode(
        user_id=user.id, code=code, is_active=True, expires_at=VERIFICATION_TIME_LIMIT
    )

    db.add_all([new_payment, verification_code])
    await db.commit()
    await db.refresh(new_payment)

    await email_service.send_confirmation_code(to_email=user.email, code=code)

    return new_payment


async def confirm_top_up(user: User, payment_id: int, code: str, db: AsyncSession) -> BankAccount:
    """ Проверка кода подтверждения и проведение начисления сумму на аккаунт """
    payment = await get_payment_by_id(payment_id=payment_id, db=db, payment_status=PaymentStatus.PENDING)

    stmt_code = select(VerificationCode).where(
        VerificationCode.user_id == user.id,
        VerificationCode.code == code,
        VerificationCode.is_active == True,
        VerificationCode.expires_at > datetime.now(timezone.utc),
    )
    res_code = await db.execute(stmt_code)
    code_obj = res_code.scalar_one_or_none()

    if not code_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный или просроченный код подтверждения.",
        )

    bank_account = await get_bank_account_by_user_id(user_id=user.id, db=db, block_update_column=True)
    if bank_account.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Аккаунт платежного сервиса заблокирован.",
        )

    # Пометка на использованный код
    code_obj.is_active = False
    # Обновление статуса платежа
    payment.status = PaymentStatus.PAID

    bank_account.balance += payment.amount

    await db.commit()
    await db.refresh(bank_account)
    return bank_account
