"""create full name field

Revision ID: c0d9fd343121
Revises: 12df4141614a
Create Date: 2025-02-02 16:31:35.205534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0d9fd343121'
down_revision: Union[str, None] = '12df4141614a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users", sa.Column("full_name", sa.String, nullable=False, server_default=""))


def downgrade():
    op.drop_column("users", "full_name")