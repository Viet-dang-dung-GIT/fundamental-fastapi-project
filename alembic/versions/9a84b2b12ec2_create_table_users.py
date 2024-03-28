"""create_table_users

Revision ID: 9a84b2b12ec2
Revises: 
Create Date: 2024-03-29 01:06:28.641437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9a84b2b12ec2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column("id", sa.Integer, primary_key=True, index=True, nullable=False),
        sa.Column('username', sa.String, index=True, nullable=False),
        sa.Column('email', sa.String, index=True, nullable=False),
        sa.Column('password', sa.String, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("users")
