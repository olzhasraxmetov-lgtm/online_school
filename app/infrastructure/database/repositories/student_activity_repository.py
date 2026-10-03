from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.repositories.student_activity_repository import (
    StudentActivityRepository,
)
from app.domain.entities import StudentActivityType
from app.domain.entities.student_activity import StudentActivity
from app.infrastructure.database.mappers.student_activity_mapper import (
    StudentActivityMapper,
)
from app.infrastructure.database.models.student_activity_model import (
    StudentActivityModel,
)


class SqlAlchemyStudentActivityRepository(StudentActivityRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, activity: StudentActivity) -> None:
        self.session.add(StudentActivityMapper.to_model(activity))
        await self.session.flush()

    async def list_by_student_id(
        self,
        student_id: UUID,
        limit: int,
        offset: int,
    ) -> list[StudentActivity]:
        stmt = (
            select(StudentActivityModel)
            .where(StudentActivityModel.student_id == str(student_id))
            .order_by(
                StudentActivityModel.occurred_at.desc(),
                StudentActivityModel.id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return [
            StudentActivityMapper.to_domain(model)
            for model in result.scalars().all()
        ]

    async def count_by_student_id(self, student_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(StudentActivityModel)
            .where(StudentActivityModel.student_id == str(student_id))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def count_all(
            self,
            student_id: UUID | None = None,
            course_id: UUID | None = None,
            activity_type: StudentActivityType | None = None,
    ) -> int:
        filters = self._build_filters(student_id, course_id, activity_type)
        stmt = (
            select(func.count())
            .select_from(StudentActivityModel)
            .where(*filters)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def list_all(
            self,
            limit: int,
            offset: int,
            student_id: UUID | None = None,
            course_id: UUID | None = None,
            activity_type: StudentActivityType | None = None,
    ) -> list[StudentActivity]:
        filters = self._build_filters(student_id, course_id, activity_type)
        stmt = (
            select(StudentActivityModel)
            .where(*filters)
            .order_by(
                StudentActivityModel.occurred_at.desc(),
                StudentActivityModel.id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(stmt)
        return [
            StudentActivityMapper.to_domain(model)
            for model in result.scalars().all()
        ]

    def _build_filters(
            self,
            student_id: UUID | None = None,
            course_id: UUID | None = None,
            activity_type: StudentActivityType | None = None,
    ) -> list:
        filters = []
        if student_id is not None:
            filters.append(StudentActivityModel.student_id == str(student_id))

        if course_id is not None:
            filters.append(StudentActivityModel.course_id == str(course_id))

        if activity_type is not None:
            filters.append(StudentActivityModel.activity_type == str(activity_type))

        return filters