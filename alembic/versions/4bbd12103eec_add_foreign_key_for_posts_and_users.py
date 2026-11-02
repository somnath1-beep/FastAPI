"""Add Foreign Key For posts and users

Revision ID: 4bbd12103eec
Revises: 8f1284aa6467
Create Date: 2026-11-01 08:52:28.813771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bbd12103eec'
down_revision: Union[str, Sequence[str], None] = '8f1284aa6467'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Changed "Owner_id" to lowercase "owner_id"
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False)) 
    
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )

def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    # 2. Fixed order: table_name first, then column_name
    op.drop_column("posts", "owner_id") 
