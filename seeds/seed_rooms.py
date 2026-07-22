import random
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.hotel import Room, Hotel, RoomInformation, ReservationStatus


async def seed_rooms(
    session: AsyncSession,
    hotels: list[Hotel],
    room_infos: list[RoomInformation]
) -> list[Room]:
    """Сидирует физические комнаты (Rooms)."""
    existing_room = await session.scalar(select(Room).limit(1))
    if existing_room:
        print("⚠️ Комнаты уже существуют. Пропускаем.")
        return []

    print("🚪 Заполнение физических комнат (Rooms)...")
    created_rooms = []

    for hotel in hotels:
        for floor in range(1, 4):
            for num in range(1, 5):
                room_number = floor * 100 + num
                selected_info = random.choice(room_infos)

                room_status = ReservationStatus.VACANT if num % 2 == 0 else ReservationStatus.OCCUPIED

                room = Room(
                    hotel_id=hotel.id,
                    info_id=selected_info.id,
                    floor=floor,
                    number=room_number,
                    status=room_status
                )
                session.add(room)
                created_rooms.append(room)

    await session.flush()
    print(f"✅ Добавлено комнат: {len(created_rooms)}")
    return created_rooms


if __name__ == "__main__":
    import asyncio
    from core.database import async_session_maker  # Импорт вашей фабрики сессий

    async def run():
        async with async_session_maker() as session:
            stmt_hotels: Result = await session.execute(select(Hotel))
            hotels = stmt_hotels.scalars().all()

            stmt_infos: Result = await session.execute(select(RoomInformation))
            room_infos = stmt_infos.scalars().all()

            # 1. Заполняем комнаты
            await seed_rooms(session=session, hotels=hotels, room_infos=room_infos)

            # 2. 💡 ОБЯЗАТЕЛЬНО фиксируем изменения в БД!
            await session.commit()
            print("💾 Изменения успешно сохранены в БД!")

    asyncio.run(run())

#  python -m seeds.seed_rooms