"""extend UserModel for its profiles

Revision ID: 9e35c19ebac5
Revises: 15863520156c
Create Date: 2026-09-24 20:07:33.728180

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '9e35c19ebac5'
down_revision: Union[str, Sequence[str], None] = '15863520156c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('full_name', sa.String(length=120), server_default='', nullable=False))
    op.add_column('users', sa.Column('bio', sa.String(length=500), server_default='', nullable=False))
    op.add_column('users', sa.Column('avatar_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'avatar_url')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'full_name')
