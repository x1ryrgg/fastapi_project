from abc import ABC, abstractmethod
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from core.models.payment import Payment, BankAccount


class AccountReplenishment(ABC):
    """ Интерфейс сервиса пополнения счета банковского аккаунта BankAccount """

    @abstractmethod
    async def reserve_payment(self, amount: Decimal, db: AsyncSession) -> Payment:
        """
        Стадия 1: Создание платежа со статусом PENDING/RESERVED,
        генерация одноразового кода и отправка его на почту.
        """
        pass

    @abstractmethod
    async def confirm_payment(self, payment_id: int, code: str, db: AsyncSession) -> BankAccount:
        """
        Стадия 2: Проверка введенного кода.
        При успехе: Payment.status -> PAID, BankAccount.balance += amount.
        """
        pass


class EmailReplenishmentService(AccountReplenishment):
    pass


class