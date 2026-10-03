from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.interfaces.content_cache import ContentCache
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities import User
from app.domain.entities.lecture import Lecture


@dataclass(slots=True)
class CreateLectureCommand:
    actor: User
    section_id: UUID
    title: str
    content: str
    position: int


class CreateLectureUseCase:
    def __init__(self, uow: UnitOfWork, content_cache: ContentCache | None = None):
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)
        self.content_cache = content_cache

    async def execute(self, command: CreateLectureCommand) -> Lecture:
        async with self.uow:
            section = await self.course_access_service.ensure_can_manage_section(
                actor=command.actor,
                section_id=command.section_id,
            )
            module = await self.uow.modules.get_by_id(section.module_id)

            lecture = Lecture(
                id=uuid4(),
                section_id=command.section_id,
                title=command.title,
                content=command.content,
                position=command.position,
            )
            section.add_lecture(lecture.id)

            await self.uow.lectures.add(lecture)
            await self.uow.sections.update(section)
            await self.uow.commit()

            if self.content_cache is not None:
                await self.content_cache.invalidate_course(
                    module.course_id
                )

            return lecture