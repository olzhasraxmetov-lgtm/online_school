from dataclasses import dataclass

from app.application.dto.student_activity import StudentActivityPageDTO, StudentActivityDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.user import User


@dataclass(slots=True)
class GetMyActivitiesQuery:
    actor: User
    limit: int
    offset: int

class GetMyActivitiesUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
            self,
            query: GetMyActivitiesQuery,
    ) -> StudentActivityPageDTO:

        async with self.uow:
            activities = await self.uow.student_activities.list_by_student_id(
                student_id=query.actor.id,
                limit=query.limit,
                offset=query.offset,
            )

            dtos = [
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
            ]

            total = await self.uow.student_activities.count_by_student_id(student_id=query.actor.id)

            return StudentActivityPageDTO(
                items=dtos,
                limit=query.limit,
                offset=query.offset,
                total=total,
            )
