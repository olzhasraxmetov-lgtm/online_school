from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from code_task_model import CodeTaskModel

class TestCaseModel(Base):
    __tablename__ = 'test_cases'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code_task_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey('code_tasks.id', ondelete='CASCADE'),
        nullable=False,
    )
    code_task: Mapped['CodeTaskModel'] = relationship(
        'CodeTaskModel',
        back_populates='test_cases',
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    input_data: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=False, default='')