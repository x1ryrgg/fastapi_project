from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.models.user import UserRole, User
from core.permissions import RoleChecker
from hotel_logic.dependencies import get_hotel_by_id, get_room_by_id, check_manager_permissions
from payment_reservation_logic.schemas.bank_account import *
from payment_reservation_logic.crud.bank_account import *
from payment_reservation_logic.dependencies import *
from payment_reservation_logic.service import AccountReplenishment, DefaultReplenishmentService


router = APIRouter(
    prefix='/bank_account',
    tags=['bank_account']
)

@router.post('/', response_model=BankAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_bank_account(user: User = Depends(RoleChecker()), db: AsyncSession = Depends(get_db)):
    """ View Создание личного внутреннего счета для пользователя """
    return await create_user_bank_account(user=user, db=db)


@router.get('/', response_model=BankAccountResponse, status_code=status.HTTP_200_OK)
async def get_bank_account(user: User = Depends(RoleChecker()), db: AsyncSession = Depends(get_db)):
    return await get_bank_account_by_user_id(user_id=user.id, db=db, load_relationships=True)


@router.post("/top-up", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def top_up_bank_account(
    dto: TopUpRequest,
    user: User = Depends(RoleChecker()),
    db: AsyncSession = Depends(get_db)
):
    """ Пополнение счета через генерацию и проведение платежа """
    account_replenishment_service: AccountReplenishment = DefaultReplenishmentService(
        user=user, db=db, code_sender=email_service
    )
    return await account_replenishment_service.process_top_up(amount=dto.amount)


@router.post("/confirm-top-up", response_model=BankAccountConfirmTopUpResponse, status_code=status.HTTP_200_OK)
async def confirm_top_up_bank_account(dto: ConfirmTopUpRequest,
                                      user: User = Depends(RoleChecker()),
                                      db: AsyncSession = Depends(get_db)):
    """ Подтверждение пополнения счета вводом кода из Email """
    account_replenishment_service: AccountReplenishment = DefaultReplenishmentService(
        user=user, db=db, code_sender=email_service
    )
    return await account_replenishment_service.confirm_top_up(payment_id=dto.payment_id, code=dto.code)
