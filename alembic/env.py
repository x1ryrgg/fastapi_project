import os
from logging.config import fileConfig

from sqlalchemy import pool, create_engine

from alembic import context
import sys
from pathlib import Path
from core.database import Base
from dotenv import load_dotenv

load_dotenv()

# ╨Ф╨╛╨▒╨░╨▓╨╗╤П╨╡╨╝ ╨║╨╛╤А╨╜╨╡╨▓╤Г╤О ╨┐╨░╨┐╨║╤Г ╨┐╤А╨╛╨╡╨║╤В╨░ ╨▓ Python path
sys.path.append(str(Path(__file__).parent.parent))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ╨Ф╨╛╨▒╨░╨▓╨╗╤П╨╡╨╝ ╨║╨╛╤А╨╜╨╡╨▓╤Г╤О ╨┐╨░╨┐╨║╤Г ╨┐╤А╨╛╨╡╨║╤В╨░ ╨▓ ╨┐╤Г╤В╤М Python
# ╨н╤В╨╛ ╨╜╤Г╨╢╨╜╨╛, ╨╡╤Б╨╗╨╕ ╨▓╤Л ╨╖╨░╨┐╤Г╤Б╨║╨░╨╡╤В╨╡ alembic ╨╕╨╖ ╨║╨╛╤А╨╜╤П ╨┐╤А╨╛╨╡╨║╤В╨░
sys.path.append(str(Path(__file__).parent.parent))

target_metadata = Base.metadata


def get_sync_database_url():
    """╨Я╤А╨╡╨╛╨▒╤А╨░╨╖╤Г╨╡╤В ╨░╤Б╨╕╨╜╤Е╤А╨╛╨╜╨╜╤Л╨╣ URL ╨▓ ╤Б╨╕╨╜╤Е╤А╨╛╨╜╨╜╤Л╨╣ ╨┤╨╗╤П Alembic"""
    async_url = os.getenv("DATABASE_URL")
    if not async_url:
        raise ValueError("DATABASE_URL not set in environment variables")

    # ╨Ч╨░╨╝╨╡╨╜╤П╨╡╨╝ asyncpg ╨╜╨░ psycopg2
    sync_url = async_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    return sync_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_sync_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # ╨Ш╤Б╨┐╨╛╨╗╤М╨╖╤Г╨╡╨╝ ╤Б╨╕╨╜╤Е╤А╨╛╨╜╨╜╤Л╨╣ ╨┤╨▓╨╕╨╢╨╛╨║ ╤Б psycopg2
    sync_url = get_sync_database_url()

    # ╨б╨╛╨╖╨┤╨░╨╡╨╝ ╤Б╨╕╨╜╤Е╤А╨╛╨╜╨╜╤Л╨╣ ╨┤╨▓╨╕╨╢╨╛╨║
    connectable = create_engine(
        sync_url,
        poolclass=pool.NullPool,
        pool_pre_ping=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # ╨б╤А╨░╨▓╨╜╨╕╨▓╨░╨╡╤В ╤В╨╕╨┐╤Л ╨║╨╛╨╗╨╛╨╜╨╛╨║
            compare_server_default=True,  # ╨б╤А╨░╨▓╨╜╨╕╨▓╨░╨╡╤В ╨╖╨╜╨░╤З╨╡╨╜╨╕╤П ╨┐╨╛ ╤Г╨╝╨╛╨╗╤З╨░╨╜╨╕╤О
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
