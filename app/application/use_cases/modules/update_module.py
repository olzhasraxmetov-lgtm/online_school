from dataclasses import dataclass
from uuid import UUID

from app.application.interfaces.repositories.course_repository import CourseRepository
from app.application.interfaces.repositories.module_repository import ModuleRepository
from app.domain.entities import Module


@dataclass(slots=True)
class UpdateModuleCommand:
    module_id: UUID
    title: str
    description: str
    position: int

class UpdateModuleUseCase:
    def __init__(
            self,
            course_repository: CourseRepository,
            module_repository: ModuleRepository,
    ) -> None:
        self.course_repository = course_repository
        self.module_repository = module_repository

    async def execute(self, command: UpdateModuleCommand) -> Module:
        module = await self.module_repository.get_by_id(command.module_id)
        module.update(
            title=command.title,
            description=command.description,
            position=command.position,
        )
        await self.module_repository.update(module)
        return module