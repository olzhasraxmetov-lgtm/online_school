from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import CodeTaskNotFoundError, CodeTaskAlreadyUsedError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities import User


@dataclass(slots=True)
class DeleteCodeTaskCommand:
    actor: User
    code_task_id: UUID


class DeleteCodeTaskUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteCodeTaskCommand) -> None:
        async with self.uow:
            code_task = await self.uow.code_tasks.get_by_id(command.code_task_id)
            if code_task is None:
                raise CodeTaskNotFoundError('Code Task not found.')

            section = await self.course_access_service.ensure_can_manage_section(
                actor=command.actor,
                section_id=code_task.section_id,
            )

            has_submissions = await self.uow.code_submissions.exists_by_code_task_id(code_task.id)

            if has_submissions:
                raise CodeTaskAlreadyUsedError(
                    'Code task already has student submissions and cannot be deleted safely.'
                )

            section.remove_code_task(code_task.id)
            await self.uow.code_tasks.remove(code_task.id)
            await self.uow.sections.update(section)
            await self.uow.commit()