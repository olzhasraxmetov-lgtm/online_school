from uuid import uuid4, UUID

from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.module import Module
from app.domain.entities.progress import Progress
from app.domain.entities.section import Section
from app.domain.entities.student_activity import StudentActivity, StudentActivityType


class StudentActivityService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def record_structure_completion(
        self,
        progress: Progress,
        section: Section,
        module: Module,
        student_id: UUID
    ) -> None:
        section_completed = progress.sync_section_completion(section)
        module_completed = progress.sync_module_completion(module)
        if section_completed:
            activity = StudentActivity(
                id=uuid4(),
                student_id=student_id,
                course_id=module.course_id,
                activity_type=StudentActivityType.SECTION_COMPLETED,
                entity_id=section.id,
                title=section.title,
            )

            await self.uow.student_activities.add(activity)

        if module_completed:
            activity = StudentActivity(
                id=uuid4(),
                student_id=student_id,
                course_id=module.course_id,
                activity_type=StudentActivityType.MODULE_COMPLETED,
                entity_id=module.id,
                title=module.title,
            )

            await self.uow.student_activities.add(activity)