"""delete columns in User table and new column role

Revision ID: ef7531e77eed
Revises: 173f0e5ecfd9
Create Date: 2026-07-19 15:44:49.238630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef7531e77eed'
down_revision: Union[str, Sequence[str], None] = '173f0e5ecfd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Объявляем именованный Enum для PostgreSQL
    user_role_enum = sa.Enum("customer", "manager", "admin", name="userrole")

    # 2. ЯВНО создаем тип в базе данных
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # 3. Добавляем колонку, которая теперь видит созданный тип
    op.add_column(
        "users",
        sa.Column("role", user_role_enum, nullable=False, server_default="customer"),
    )

    # Удаляем старую колонку
    op.drop_column("users", "is_superuser")


def downgrade() -> None:
    # Возвращаем старую колонку обратно
    op.add_column(
        "users",
        sa.Column("is_superuser", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )

    # Удаляем колонку role
    op.drop_column("users", "role")

    # Удаляем тип 'userrole' из PostgreSQL, чтобы не оставалось мусора
    user_role_enum = sa.Enum(name="userrole")
    user_role_enum.drop(op.get_bind(), checkfirst=True)
