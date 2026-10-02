"""Create LectureCommntModel

Revision ID: acdb4bf3a2da
Revises: b73d6ce2cb30
Create Date: 2026-09-30 19:36:49.645743

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'acdb4bf3a2da'
down_revision: Union[str, Sequence[str], None] = 'b73d6ce2cb30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('lecture_comments',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('lecture_id', sa.String(length=36), nullable=False),
    sa.Column('text', sa.String(length=2000), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lectures.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('lecture_comments')
