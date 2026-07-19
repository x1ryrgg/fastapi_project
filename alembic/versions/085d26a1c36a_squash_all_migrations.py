"""Squash all migrations

Revision ID: 085d26a1c36a
Revises: b4465e6c1da2
Create Date: 2026-07-19 22:59:45.818930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '085d26a1c36a'
down_revision: Union[str, Sequence[str], None] = 'b4465e6c1da2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
