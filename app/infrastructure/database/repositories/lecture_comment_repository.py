from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.repositories.lecture_comment_repository import LectureCommentRepository
from app.domain.entities.lecture_comment import LectureComment
from app.infrastructure.database.mappers.lecture_comment_mapper import LectureCommentMapper
from app.infrastructure.database.models.lecture_comment_model import LectureCommentModel


class SqlAlchemyLectureCommentRepository(LectureCommentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, lecture_comment_id: UUID) -> LectureComment | None:
        model = await self.session.get(LectureCommentModel, str(lecture_comment_id))
        return None if model is None else LectureCommentMapper.to_domain(model)

    async def list_by_lecture_id(self, lecture_id: UUID) -> list[LectureComment]:
        stmt = (
            select(LectureCommentModel)
            .where(LectureCommentModel.lecture_id == str(lecture_id))
            .order_by(LectureCommentModel.created_at, LectureCommentModel.id)
        )
        result = await self.session.execute(stmt)
        return [LectureCommentMapper.to_domain(model) for model in result.scalars().all()]

    async def add(self, lecture_comment: LectureComment) -> None:
        self.session.add(LectureCommentMapper.to_model(lecture_comment))
        await self.session.flush()

    async def update(self, lecture_comment: LectureComment) -> None:
        model = await self.session.get(LectureCommentModel, str(lecture_comment.id))
        if model is None:
            return
        model.text = lecture_comment.text
        model.updated_at = lecture_comment.updated_at
        await self.session.flush()

    async def remove(self, lecture_comment_id: UUID) -> None:
        model = await self.session.get(LectureCommentModel, str(lecture_comment_id))
        if model is None:
            return
        await self.session.delete(model)
        await self.session.flush()