"""create payment account tables

Revision ID: 12df4141614a
Revises: 5bc37a7bba15
Create Date: 2025-02-02 16:25:34.548852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12df4141614a'
down_revision: Union[str, None] = '5bc37a7bba15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создаём таблицу accounts
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("balance", sa.Numeric(10, 2), nullable=False),
    )

    # Создаём таблицу payments
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.id"), nullable=False),
        sa.Column("transaction_id", sa.String, unique=True, nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
    )


def downgrade():
    # Удаляем таблицу payments сначала (из-за ForeignKey)
    op.drop_table("payments")

    # Удаляем таблицу accounts
    op.drop_table("accounts")