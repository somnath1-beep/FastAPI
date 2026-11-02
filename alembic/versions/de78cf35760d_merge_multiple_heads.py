"""Merge multiple heads

Revision ID: de78cf35760d
Revises: 3787d08c6b03, 4bbd12103eec
Create Date: 2026-11-01 09:48:09.363675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de78cf35760d'
down_revision: Union[str, Sequence[str], None] = ('3787d08c6b03', '4bbd12103eec')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
