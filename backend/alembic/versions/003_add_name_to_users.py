"""Add name column to users table

Revision ID: 003
Revises: 002
Create Date: 2026-01-15 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add name column to users table
    op.add_column('users', sa.Column('name', sa.String(length=255), nullable=False, server_default=''))


def downgrade() -> None:
    # Remove name column from users table
    op.drop_column('users', 'name')