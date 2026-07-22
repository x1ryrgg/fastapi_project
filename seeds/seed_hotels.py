from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.hotel import Hotel
from core.models.user import UserHotel, User


HOTELS_DATA = [
    {
        "name": "Grand Palace Hotel",
        "city": "Москва",
        "address": "ул. Тверская, д. 12",
        "region": "Московская область",
        "stars": 5,
        "phone": "+74951234567",
        "email": "info@grandpalace.ru",
        "description": "Роскошный отель в самом центре столицы."
    },
    {
        "name": "Seaside Resort & Spa",
        "city": "Сочи",
        "address": "Курортный проспект, д. 85",
        "region": "Краснодарский край",
        "stars": 4,
        "phone": "+78622998877",
        "email": "booking@seaside.ru",
        "description": "Отель на первой линии с собственным пляжем."
    },
    {
        "name": "Comfort Inn",
        "city": "Санкт-Петербург",
        "address": "Невский проспект, д. 45",
        "region": "Ленинградская область",
        "stars": 3,
        "phone": "+78125553322",
        "email": "stay@comfortinn.spb.ru",
        "description": "Уютный отель для бизнес-поездок и туристов."
    }
]

async def seed_hotels(session: AsyncSession, manager: User) -> list[Hotel]:
    """Сидирует отели и привязывает их к менеджеру."""
    existing_hotel = await session.scalar(select(Hotel).limit(1))
    if existing_hotel:
        print("⚠️ Отели уже существуют. Пропускаем.")
        result = await session.execute(select(Hotel))
        return list(result.scalars().all())

    print("🏨 Заполнение отелей...")
    created_hotels = []

    for h_data in HOTELS_DATA:
        hotel = Hotel(**h_data)
        session.add(hotel)
        await session.flush()  # Получаем hotel.id

        # Привязка M2M
        user_hotel_link = UserHotel(user_id=manager.id, hotel_id=hotel.id)
        session.add(user_hotel_link)
        created_hotels.append(hotel)

    print(f"✅ Добавлено отелей: {len(created_hotels)}")
    return created_hotels