from typing import List

from core.models import Hotel
from core.logging_system import logger


def get_hotel_owners_ids(hotel: Hotel) -> List[int]:
    """ Возвращает список ID владельцев отеля """
    owner_ids = [link.user_id for link in hotel.users_link]

    if not owner_ids:
        logger.info(f"[get_hotel_owners_ids] У Отеля {hotel.name} (ID: {hotel.id}) нет владельцев.")

    return owner_ids

