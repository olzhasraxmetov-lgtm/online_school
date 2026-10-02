from dataclasses import dataclass
from uuid import UUID

from app.application.dto.lecture_comment import LectureCommentDTO
from app.application.exceptions import PermissionDeniedError, LectureCommentNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_content_access_service import CourseContentAccessService
from app.domain.entities import User


@dataclass(slots=True)
class UpdateLectureCommentCommand:
    actor: User
    text: str
    lecture_comment_id: UUID

class UpdateLectureCommentUseCase:
    def __init__(
            self,
            uow: UnitOfWork,
            access_service: CourseContentAccessService
    ) -> None:
        self.uow = uow
        self.access_service = access_service

    async def execute(self, command: UpdateLectureCommentCommand) -> LectureCommentDTO:
        async with self.uow:
            lecture_comment = await self.uow.lecture_comments.get_by_id(
                lecture_comment_id=command.lecture_comment_id,
            )

            if lecture_comment is None:
                raise LectureCommentNotFoundError('Lecture comment not found.')

            lecture = await self.uow.lectures.get_by_id(lecture_comment.lecture_id)

            if lecture is None:
                raise LectureCommentNotFoundError('Lecture comment not found.')

            can_view = await self.access_service.can_view_section_content(
                section_id=lecture.section_id,
                actor=command.actor,
            )

            if not can_view:
                raise LectureCommentNotFoundError('Lecture comment not found.')

            if not lecture_comment.is_written_by(command.actor.id):
                raise PermissionDeniedError(
                    'Only an author of this comment can change the comment.'
                )

            lecture_comment.update(text=command.text)
            await self.uow.lecture_comments.update(lecture_comment)
            await self.uow.commit()
            return LectureCommentDTO(
                id=lecture_comment.id,
                user_id=lecture_comment.user_id,
                lecture_id=lecture_comment.lecture_id,
                text=lecture_comment.text,
                updated_at=lecture_comment.updated_at,
                created_at=lecture_comment.created_at,
            )