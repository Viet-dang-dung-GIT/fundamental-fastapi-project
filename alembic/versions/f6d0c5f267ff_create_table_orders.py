"""create_table_orders

Revision ID: f6d0c5f267ff
Revises: faa6aec90599
Create Date: 2024-03-29 01:19:27.687042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f6d0c5f267ff'
down_revision: Union[str, None] = 'faa6aec90599'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True, index=True),
        sa.Column('quantity', sa.Integer),
        sa.Column('total_price', sa.Float),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id')),
    )


def downgrade() -> None:
    op.drop_table('orders')
