"""create_table_products

Revision ID: 9e0d2a513204
Revises: 9a84b2b12ec2
Create Date: 2024-03-29 01:12:57.754422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9e0d2a513204'
down_revision: Union[str, None] = '9a84b2b12ec2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False, index=True),
        sa.Column('description', sa.String),
        sa.Column('price', sa.Float, nullable=False, index=True),
        sa.Column('stock_quantity', sa.Integer, nullable=False, index=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id')),
    )


def downgrade() -> None:
    op.drop_table('products')
