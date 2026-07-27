from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteCourseCommand:
    course_id: UUID

class DeleteCourseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteCourseCommand) -> None:
        async with self.uow:
            course = await self.uow.courses.get_by_id(command.course_id)
            if not course:
                raise CourseNotFoundError("Course not found")
            await self.uow.courses.remove(course.id)
            await self.uow.commit()