from core.database import async_session_maker
from core.models.hotel import Hotel
from core.models.user import User, UserRole
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload, selectinload
from users_logic.security import hash_password, verify_password

load_dotenv()


user_names = [
    'Александр', 'Алексей', 'Анатолий', 'Андрей', 'Антон'
    ]

async def create_users():
    async with async_session_maker() as session:
        password = hash_password("12345678")
        root_user = User(username="root",
                         password=password,
                         email='root@inbox.ru',
                         role=UserRole.ADMIN)
        manager_user = User(username="manager",
                            password=password,
                            email='manager@inbox.ru',
                            role=UserRole.HOTEL_MANAGER)
        session.add(root_user)
        session.add(manager_user)
        await session.commit()

        for username in user_names:
            email = f"{username}@example.com"
            user = User(username=username, email=email, password=password)
            session.add(user)
            await session.commit()


async def check_orm_results():
    async with async_session_maker() as session:
        result = await session.execute(select(User).options(joinedload(User.hotels)).where(User.id == 1))
        users = result.unique().scalars().all()

        for user in users:
            print(f"USER {user.username}")
            for hotel in user.hotels:
                print(f"HOTEL {hotel.name}")


async def check_selectinload():
    # selectinload работает хорошо к связи один ко многим и уникальные значения сразу берет не надо unique
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).options(
                selectinload(User.hotels)
            ).order_by(User.id)
        )

        users = result.scalars().all()

        for user in users:
            print(f"\nUSER {user.username}")
            for hotel in user.hotels:
                print(f"HOTEL {hotel.name}")


async def check_code_decode_system():
    async with async_session_maker() as session:
        stmt = await session.execute(select(User).where(User.id == 119))
        user = stmt.scalar_one_or_none()

        password = user.password

        decode_password = verify_password('12345678', password)

        print(decode_password)

        test_password = "test_password"

        print(hash_password(test_password))


if __name__ == "__main__":
    asyncio.run(check_code_decode_system())
