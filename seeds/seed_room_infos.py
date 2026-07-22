from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.hotel import RoomType, RoomInformation

ROOM_INFO_DATA = [
    {"type": RoomType.SINGLE, "price_per_night": 2500.0, "capacity": 1, "size": 18.0},
    {"type": RoomType.DOUBLE, "price_per_night": 4500.0, "capacity": 2, "size": 25.0},
    {"type": RoomType.TWIN, "price_per_night": 4200.0, "capacity": 2, "size": 24.0},
    {"type": RoomType.SUITE, "price_per_night": 9000.0, "capacity": 3, "size": 45.0},
    {"type": RoomType.FAMILY, "price_per_night": 7000.0, "capacity": 4, "size": 38.0},
]

async def seed_room_infos(session: AsyncSession) -> list[RoomInformation]:
    """Сидирует типы комнат (RoomInformation)."""
    existing_info = await session.scalar(select(RoomInformation).limit(1))
    if existing_info:
        print("⚠️ Типы комнат уже существуют. Пропускаем.")
        # Если данные есть, получаем их для дальнейшего использования в rooms
        result = await session.execute(select(RoomInformation))
        return list(result.scalars().all())

    print("🛏 Заполнение типов комнат (RoomInformation)...")
    room_infos = [RoomInformation(**info) for info in ROOM_INFO_DATA]
    session.add_all(room_infos)
    await session.flush()

    print(f"✅ Добавлено типов комнат: {len(room_infos)}")
    return room_infos
