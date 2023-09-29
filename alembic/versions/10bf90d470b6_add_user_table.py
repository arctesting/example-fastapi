"""add user table

Revision ID: 10bf90d470b6
Revises: 9b4de2467450
Create Date: 2023-09-28 22:51:48.559776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10bf90d470b6'
down_revision: Union[str, None] = '9b4de2467450'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table("users",
                     sa.Column('id', sa.Integer(),nullable=False),
                     sa.Column('email', sa.String(),nullable=False),
                     sa.Column('password', sa.String(),nullable=False),
                     sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                               sever_default=sa.text('now()'), nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email'))



def downgrade() -> None:
    op.drop_table("users")
    pass
