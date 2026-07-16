from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from module_model import ModuleModel

class CourseModel(Base):
    __tablename__ = 'courses'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)

    modules: Mapped[list["ModuleModel"]] = relationship(
        'ModuleModel',
        back_populates='course',
        cascade='all, delete, delete-orphan',
        order_by='ModuleModel.position',
    )