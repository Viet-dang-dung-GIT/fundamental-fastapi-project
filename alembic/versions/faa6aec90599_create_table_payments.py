"""create_table_payments

Revision ID: faa6aec90599
Revises: 9e0d2a513204
Create Date: 2024-03-29 01:19:00.846981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'faa6aec90599'
down_revision: Union[str, None] = '9e0d2a513204'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True, index=True),
        sa.Column('amount', sa.Float, index=True),
        sa.Column('status', sa.String),
        sa.Column('payment_method', sa.String),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
    )


def downgrade() -> None:
    op.drop_table('payments')
