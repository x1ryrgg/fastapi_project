import asyncio
from sqlalchemy import text
from core.database import engine  # Ваш путь к engine


async def reset_alembic():
    """Удаляет таблицу alembic_version из базы данных."""
    try:
        async with engine.connect() as conn:
            # Удаляем таблицу alembic_version
            await conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))
            await conn.commit()
            print("✅ Таблица alembic_version успешно удалена")

            # Проверяем, что таблица удалена
            result = await conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_name = 'alembic_version';")
            )
            if result.fetchone():
                print("❌ Таблица все еще существует")
            else:
                print("✅ Таблица успешно удалена")

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(reset_alembic())