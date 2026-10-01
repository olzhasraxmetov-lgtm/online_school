from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import LectureCommentNotFoundError, PermissionDeniedError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_content_access_service import CourseContentAccessService
from app.domain.entities import User


@dataclass(slots=True)
class DeleteLectureCommentCommand:
    actor: User
    lecture_comment_id: UUID

class DeleteLectureCommentUseCase:
    def __init__(
            self,
            uow: UnitOfWork,
            access_service: CourseContentAccessService
    ) -> None:
        self.uow = uow
        self.access_service = access_service

    async def execute(self, command: DeleteLectureCommentCommand) -> None:
        async with self.uow:
            lecture_comment = await self.uow.lecture_comments.get_by_id(
                lecture_comment_id=command.lecture_comment_id,
            )

            if lecture_comment is None:
                raise LectureCommentNotFoundError('Lecture comment not found.')

            lecture = await self.uow.lectures.get_by_id(lecture_comment.lecture_id)

            if lecture is None:
                raise LectureCommentNotFoundError('Lecture comment not found.')

            course = await self.access_service.get_course_by_section_id(
                section_id=lecture.section_id,
            )
            if course is None:
                raise LectureCommentNotFoundError('Lecture comment not found.')

            if not self.access_service.is_course_visible_to(
                course=course,
                actor=command.actor,
            ):
                raise LectureCommentNotFoundError('Lecture comment not found.')

            if not (
                lecture_comment.is_written_by(user_id=command.actor.id) or
                course.is_owned_by(command.actor.id) or
                command.actor.can_manage_platform()
            ):
                raise PermissionDeniedError(
                    'Only the comment author, the course author or an administrator can delete this comment.'
                )

            await self.uow.lecture_comments.remove(lecture_comment.id)
            await self.uow.commit()