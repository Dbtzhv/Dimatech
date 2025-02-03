"""create user table

Revision ID: 5bc37a7bba15
Revises: 
Create Date: 2025-02-02 16:09:46.452457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bc37a7bba15'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создаём таблицу users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False),
    )


def downgrade():
    # Удаляем таблицу users
    op.drop_table("users")

    # Удаляем ENUM, если он больше не используется
    userrole_enum.drop(op.get_bind(), checkfirst=True)