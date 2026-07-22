import asyncio
from sqlalchemy import select
from core.database import async_session_maker
from core.models.user import User, UserRole
from core.models.hotel import Hotel, RoomInformation

from seeds.seed_users import seed_users
from seeds.seed_room_infos import seed_room_infos
from seeds.seed_hotels import seed_hotels
from seeds.seed_rooms import seed_rooms


async def seed_database():
    async with async_session_maker() as session:
        print("🚀 Начинаем процесс сидирования базы данных...\n")

        # 1. Пользователи
        users_data = await seed_users(session)

        # Получаем менеджера (если сид пользователей пропущен, ищем из БД)
        if users_data and users_data.get("managers"):
            manager = users_data["managers"][0]
        else:
            manager = await session.scalar(
                select(User).where(User.role == UserRole.HOTEL_MANAGER)
            )

        # 2. Типы комнат
        room_infos = await seed_room_infos(session)

        # 3. Отели
        hotels = await seed_hotels(session, manager=manager)

        # 4. Физические комнаты
        await seed_rooms(session, hotels=hotels, room_infos=room_infos)

        # Коммитим ВСЮ транзакцию в самом конце
        await session.commit()
        print("\n🎉 Сидирование успешно завершено!")


if __name__ == "__main__":
    asyncio.run(seed_database())
