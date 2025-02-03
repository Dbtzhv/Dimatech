"""create two users

Revision ID: fd65f9b4797c
Revises: c0d9fd343121
Create Date: 2025-02-03 13:48:30.150696

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import text

from app.users.auth import get_password_hash

# revision identifiers, used by Alembic.
revision: str = 'fd65f9b4797c'
down_revision: Union[str, None] = 'c0d9fd343121'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    conn.execute(
        text("""
        INSERT INTO users (email, full_name, hashed_password, role)
        VALUES (:email, :full_name, :hashed_password, :role)
        RETURNING id
        """),
        {
            "email": "testuser@example.com",
            "full_name": "Test User",
            "hashed_password": get_password_hash("testpassword"),
            "role": "user",
        },
    )
    test_user_id = conn.execute(text("SELECT id FROM users WHERE email = 'testuser@example.com'")).scalar()

    # Создаем счет для тестового пользователя
    if test_user_id:
        conn.execute(
            text("INSERT INTO accounts (user_id, balance) VALUES (:user_id, :balance)"),
            {"user_id": test_user_id, "balance": 0.00},
        )

    conn.execute(
        text("""
        INSERT INTO users (email, full_name, hashed_password, role)
        VALUES (:email, :full_name, :hashed_password, :role)
        """),
        {
            "email": "admin@example.com",
            "full_name": "Admin User",
            "hashed_password": get_password_hash("adminpassword"),
            "role": "admin",
        },
    )


def downgrade():
    conn = op.get_bind()

    # Получаем ID тестового пользователя
    test_user_id = conn.execute(text("SELECT id FROM users WHERE email = 'testuser@example.com'")).scalar()

    # Удаляем связанные записи
    if test_user_id:
        conn.execute(text("DELETE FROM accounts WHERE user_id = :user_id"), {"user_id": test_user_id})

    conn.execute(text("DELETE FROM users WHERE email IN ('testuser@example.com', 'admin@example.com')"))
