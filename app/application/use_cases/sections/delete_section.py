from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import ModuleNotFoundError
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities import User
from app.infrastructure.database.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteSectionCommand:
    section_id: UUID
    actor: User


class DeleteSectionUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteSectionCommand) -> None:
        async with self.uow:
            section = await self.course_access_service.ensure_can_manage_section(
                actor=command.actor,
                section_id=command.section_id,
            )

            module = await self.uow.modules.get_by_id(section.module_id)
            if module is None:
                raise ModuleNotFoundError("Module not found")

            module.remove_section(section.id)
            await self.uow.modules.update(module)
            await self.uow.sections.remove(section.id)
            await self.uow.commit()
