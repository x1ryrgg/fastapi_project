from core.database import async_session_maker
from core.models.hotel import Hotel
from core.models.user import User
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload, selectinload

load_dotenv()


user_names = [
    'Александр', 'Алексей', 'Анатолий', 'Андрей', 'Антон', 'Аркадий', 'Арсений', 'Артём', 'Борис', 'Вадим',
    'Валентин', 'Валерий', 'Василий', 'Виктор', 'Виталий', 'Владимир', 'Владислав', 'Вячеслав', 'Геннадий', 'Георгий',
    'Григорий', 'Даниил', 'Денис', 'Дмитрий', 'Евгений', 'Егор', 'Иван', 'Игорь', 'Илья', 'Кирилл',
    'Константин', 'Леонид', 'Максим', 'Марат', 'Михаил', 'Никита', 'Николай', 'Олег', 'Павел', 'Пётр',
    'Роман', 'Руслан', 'Сергей', 'Станислав', 'Степан', 'Тимофей', 'Фёдор', 'Филипп', 'Юрий', 'Ярослав',
    'Анастасия', 'Анна', 'Валентина', 'Валерия', 'Вера', 'Виктория', 'Галина', 'Дарья', 'Евгения', 'Екатерина',
    'Елена', 'Елизавета', 'Жанна', 'Зинаида', 'Зоя', 'Ирина', 'Карина', 'Кира', 'Ксения', 'Лариса',
    'Лидия', 'Любовь', 'Людмила', 'Маргарита', 'Марина', 'Мария', 'Надежда', 'Наталья', 'Нина', 'Оксана',
    'Ольга', 'Полина', 'Раиса', 'Регина', 'Римма', 'Светлана', 'София', 'Таисия', 'Тамара', 'Татьяна',
    'Ульяна', 'Юлия', 'Яна', 'Алина', 'Диана', 'Ева', 'Милана', 'Алиса', 'Варвара', 'Василиса'
]

async def create_100_users():
    async with async_session_maker() as session:
        for username in user_names:
            email = f"{username}@example.com"
            user = User(username=username, email=email, password=os.getenv("USER_PASSWORD"))
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

if __name__ == "__main__":
    asyncio.run(check_selectinload())
