"""add cols published, created-at to posts

Revision ID: 971d23c3b340
Revises: de78cf35760d
Create Date: 2026-11-01 09:49:09.665513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '971d23c3b340'
down_revision: Union[str, Sequence[str], None] = 'de78cf35760d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
