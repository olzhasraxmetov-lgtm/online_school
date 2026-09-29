"""Create Course Review

Revision ID: b73d6ce2cb30
Revises: 9e35c19ebac5
Create Date: 2026-09-26 17:04:15.337432

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'b73d6ce2cb30'
down_revision: Union[str, Sequence[str], None] = '9e35c19ebac5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('course_reviews',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('course_id', sa.String(length=36), nullable=False),
    sa.Column('student_id', sa.String(length=36), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=2000), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id', 'course_id', name='uq_course_review_student_course')
    )
    op.create_index(op.f('ix_course_reviews_course_id'), 'course_reviews', ['course_id'], unique=False)
    op.create_index(op.f('ix_course_reviews_student_id'), 'course_reviews', ['student_id'], unique=False)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_course_reviews_student_id'), table_name='course_reviews')
    op.drop_index(op.f('ix_course_reviews_course_id'), table_name='course_reviews')
    op.drop_table('course_reviews')
