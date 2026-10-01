from dataclasses import dataclass
from uuid import UUID

from app.application.dto.lecture_comment import LectureCommentDTO
from app.application.exceptions import LectureNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_content_access_service import CourseContentAccessService
from app.domain.entities import User


@dataclass(slots=True)
class GetLectureCommentsQuery:
    actor: User
    lecture_id: UUID


class GetLectureCommentsUseCase:
    def __init__(self, uow: UnitOfWork, access_service: CourseContentAccessService) -> None:
        self.uow = uow
        self.access_service = access_service

    async def execute(self, query: GetLectureCommentsQuery) -> list[LectureCommentDTO]:
        async with self.uow:
            lecture = await self.uow.lectures.get_by_id(query.lecture_id)

            if lecture is None:
                raise LectureNotFoundError('Lecture not found.')

            can_view = await self.access_service.can_view_section_content(
                section_id=lecture.section_id,
                actor=query.actor,
            )

            if not can_view:
                raise LectureNotFoundError('Lecture not found.')

            lecture_comments = await self.uow.lecture_comments.list_by_lecture_id(
                lecture_id=lecture.id,
            )

            result = [
                LectureCommentDTO(
                    id=lecture_comment.id,
                    user_id=lecture_comment.user_id,
                    text=lecture_comment.text,
                    updated_at=lecture_comment.updated_at,
                    created_at=lecture_comment.created_at,
                    lecture_id=lecture_comment.lecture_id,
                )
                for lecture_comment in lecture_comments
            ]

            return result