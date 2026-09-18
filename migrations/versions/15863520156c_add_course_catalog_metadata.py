"""add course catalog metadata

Revision ID: 15863520156c
Revises: 7ecfeaf94314
Create Date: 2026-09-18 18:47:29.210538

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '15863520156c'
down_revision: Union[str, Sequence[str], None] = '7ecfeaf94314'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('courses', sa.Column('cover_image_url', sa.String(length=500), nullable=True))
    op.add_column('courses', sa.Column('short_description', sa.String(length=280), nullable=False, server_default=''))
    op.add_column('courses', sa.Column('difficulty', sa.String(length=32), nullable=False, server_default='beginner'))
    op.add_column('courses', sa.Column('tag_names', sa.JSON(), nullable=False, server_default='[]'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('courses', 'tag_names')
    op.drop_column('courses', 'difficulty')
    op.drop_column('courses', 'short_description')
    op.drop_column('courses', 'cover_image_url')
