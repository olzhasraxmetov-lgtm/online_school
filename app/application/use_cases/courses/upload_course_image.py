from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.services.image_storage import ImageStorage
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.domain.entities.course import Course
from app.domain.entities.image_files import ImageCover
from app.domain.entities.user import User


@dataclass(slots=True)
class UploadCourseImageCommand:
    course_id: UUID
    actor: User
    content_type: str
    content: bytes

class CourseImageUploadUseCase:
    def __init__(
            self,
            uow: UnitOfWork,
            image_storage: ImageStorage,
    ):
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)
        self.image_storage_service = image_storage

    async def execute(self, command: UploadCourseImageCommand) -> Course:
        async with self.uow:
            course = await self.uow.courses.get_by_id(command.course_id)
            if course is None:
                raise CourseNotFoundError('Course not found.')

            await self.course_access_service.ensure_can_manage_course(
                actor=command.actor,
                course_id=course.id,
            )

            cover_image = ImageCover(content=command.content, content_type=command.content_type)

            file_name = f"{uuid4()}{cover_image.extension}"

            image_url = await self.image_storage_service.save(file_name=file_name, content=cover_image.content)

            course.update_cover_image(url=image_url)

            await self.uow.courses.update(course)
            await self.uow.commit()
            return course