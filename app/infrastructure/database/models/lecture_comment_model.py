from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from user_model import UserModel
    from lecture_model import LectureModel

class LectureCommentModel(Base):
    __tablename__ = 'lecture_comments'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    lecture_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('lectures.id', ondelete='CASCADE'),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(String(2000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped['UserModel'] = relationship(
        'UserModel',
        back_populates='lecture_comments'
    )

    lecture: Mapped['LectureModel'] = relationship(
        'LectureModel',
        back_populates='lecture_comments'
    )