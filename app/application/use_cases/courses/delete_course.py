from dataclasses import dataclass
from uuid import UUID

from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities import User


@dataclass(slots=True)
class DeleteCourseCommand:
    course_id: UUID
    actor: User

class DeleteCourseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteCourseCommand) -> None:
        async with self.uow:
            course = await self.course_access_service.ensure_can_manage_course(
                course_id=command.course_id,
                actor=command.actor,
            )
            await self.uow.courses.remove(course.id)
            await self.uow.commit()