from dataclasses import dataclass
from uuid import UUID

from app.application.dto.student_activity import StudentActivityDTO, StudentActivityPageDTO
from app.application.exceptions import PermissionDeniedError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities import StudentActivityType
from app.domain.entities.user import User


@dataclass(slots=True)
class GetAdminActivitiesQuery:
    actor: User
    limit: int
    offset: int
    student_id: UUID | None = None
    course_id: UUID | None = None
    activity_type: StudentActivityType | None = None


class GetAdminActivitiesUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, query: GetAdminActivitiesQuery) -> StudentActivityPageDTO:
        if not query.actor.can_manage_platform():
            raise PermissionDeniedError('Only administrators can view platform activities.')

        async with self.uow:
            activities = await self.uow.student_activities.list_all(
                limit=query.limit,
                offset=query.offset,
                student_id=query.student_id,
                course_id=query.course_id,
                activity_type=query.activity_type,
            )
            total = await self.uow.student_activities.count_all(
                student_id=query.student_id,
                course_id=query.course_id,
                activity_type=query.activity_type,
            )

            return StudentActivityPageDTO(
                items=[
                    StudentActivityDTO(
                        id=activity.id,
                        student_id=activity.student_id,
                        course_id=activity.course_id,
                        activity_type=activity.activity_type,
                        entity_id=activity.entity_id,
                        title=activity.title,
                        details=activity.details,
                        occurred_at=activity.occurred_at,
                    )
                    for activity in activities
                ],
                total=total,
                limit=query.limit,
                offset=query.offset,
            )
