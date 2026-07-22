from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User, UserRole
from users_logic.security import hash_password


USER_NAMES = ["alex", "john", "maria", "elena", "dmitry"]

async def seed_users(session: AsyncSession) -> dict[str, list[User]]:
    """Сидирует пользователей. Возвращает словарь с созданными пользователями."""
    existing_user = await session.scalar(select(User).limit(1))
    if existing_user:
        print("⚠️ Пользователи уже существуют. Пропускаем.")
        return {}

    print("👤 Заполнение пользователей...")
    password_hash = hash_password("12345678")

    root_user = User(
        username="root",
        password=password_hash,
        email="root@inbox.ru",
        role=UserRole.ADMIN,
    )
    manager_user = User(
        username="manager",
        password=password_hash,
        email="manager@inbox.ru",
        role=UserRole.HOTEL_MANAGER,
    )

    customers = [
        User(
            username=username,
            email=f"{username}@example.com",
            password=password_hash,
            role=UserRole.CUSTOMER,
        )
        for username in USER_NAMES
    ]

    session.add_all([root_user, manager_user, *customers])
    await session.flush()  # Получаем ID

    print(f"✅ Добавлено пользователей: {len(customers) + 2}")
    return {"admins": [root_user], "managers": [manager_user], "customers": customers}
