from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from section_model import SectionModel
    from lecture_comment_model import LectureCommentModel

class LectureModel(Base):
    __tablename__ = "lectures"
    __table_args__ = (
        Index(
            'ix_lectures_section_position',
            'section_id',
            'position',
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    section_id: Mapped[str] = mapped_column(ForeignKey("sections.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer)

    section: Mapped["SectionModel"] = relationship("SectionModel", back_populates="lectures")
    lecture_comments: Mapped[list['LectureCommentModel']] = relationship(
        'LectureCommentModel',
        back_populates='lecture',
        cascade='all, delete-orphan',
        order_by='LectureCommentModel.id',
    )