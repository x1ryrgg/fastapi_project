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


router = APIRouter(
    prefix='/payment',
    tags=['payments']
)