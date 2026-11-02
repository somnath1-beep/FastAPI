"""Add Content Column to posts 

Revision ID: fcc4eb34e9f7
Revises: 858fad870055
Create Date: 2026-10-31 19:16:14.302329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcc4eb34e9f7'
down_revision: Union[str, Sequence[str], None] = '858fad870055'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
