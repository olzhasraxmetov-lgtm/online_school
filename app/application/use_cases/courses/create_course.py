from dataclasses import dataclass
from uuid import uuid4

from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities import User
from app.domain.entities.course import Course, CourseDifficulty


@dataclass(slots=True)
class CreateCourseCommand:
    actor: User
    title: str
    description: str
    short_description: str = ''
    difficulty: CourseDifficulty = CourseDifficulty.BEGINNER
    tag_names: list[str] | None = None


class CreateCourseUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: CreateCourseCommand) -> Course:
        if not command.actor.can_manage_learning_content():
            raise PermissionError("User cannot create courses.")
        async with self.uow:
            course = Course(
                id=uuid4(),
                title=command.title,
                description=command.description,
                author_id=command.actor.id,
                short_description=command.short_description,
                tag_names=list(command.tag_names or []),
                difficulty=command.difficulty,
            )
            await self.uow.courses.add(course)
            await self.uow.commit()
            return course