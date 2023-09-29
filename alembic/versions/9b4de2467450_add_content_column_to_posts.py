"""add content column to posts

Revision ID: 9b4de2467450
Revises: c7f6b0bc2d46
Create Date: 2023-09-28 22:44:38.743774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b4de2467450'
down_revision: Union[str, None] = 'c7f6b0bc2d46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
