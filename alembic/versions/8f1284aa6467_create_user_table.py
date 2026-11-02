"""Create User Table

Revision ID: 8f1284aa6467
Revises: fcc4eb34e9f7
Create Date: 2026-10-31 19:29:39.843946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f1284aa6467'
down_revision: Union[str, Sequence[str], None] = 'fcc4eb34e9f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",sa.Column("id",sa.Integer,nullable=False,),
                    sa.Column("email",sa.String,nullable=False),
                    sa.Column("password",sa.String, nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
