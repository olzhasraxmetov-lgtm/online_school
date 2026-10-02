from dataclasses import dataclass
from uuid import UUID, uuid4

from app.application.dto.lecture_comment import LectureCommentDTO
from app.application.exceptions import LectureNotFoundError, PermissionDeniedError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_content_access_service import CourseContentAccessService
from app.domain.entities import User, LectureComment


@dataclass(slots=True)
class CreateLectureCommentCommand:
    actor: User
    text: str
    lecture_id: UUID


class CreateLectureCommentUseCase:
    def __init__(self, uow: UnitOfWork, access_service: CourseContentAccessService) -> None:
        self.uow = uow
        self.access_service = access_service

    async def execute(self, command: CreateLectureCommentCommand) -> LectureCommentDTO:
        if not command.actor.is_student():
            raise PermissionDeniedError('Only students can leave lecture comments.')

        async with self.uow:
            lecture = await self.uow.lectures.get_by_id(command.lecture_id)
            if lecture is None:
                raise LectureNotFoundError("Lecture not found.")

            can_view = await self.access_service.can_view_section_content(
                section_id=lecture.section_id,
                actor=command.actor,
            )
            if not can_view:
                raise LectureNotFoundError('Lecture not found.')

            lecture_comment = LectureComment(
                id=uuid4(),
                user_id=command.actor.id,
                lecture_id=lecture.id,
                text=command.text,
            )

            await self.uow.lecture_comments.add(lecture_comment)
            await self.uow.commit()

            return LectureCommentDTO(
                id=lecture_comment.id,
                user_id=lecture_comment.user_id,
                lecture_id=lecture_comment.lecture_id,
                text=lecture_comment.text,
                updated_at=lecture_comment.updated_at,
                created_at=lecture_comment.created_at,
            )
