from uuid import UUID

from app.domain.entities.lecture_comment import LectureComment
from app.infrastructure.database.models.lecture_comment_model import LectureCommentModel


class LectureCommentMapper:
    @staticmethod
    def to_domain(model: LectureCommentModel) -> LectureComment:
        return LectureComment(
            id=UUID(model.id),
            lecture_id=UUID(model.lecture_id),
            user_id=UUID(model.user_id),
            updated_at=model.updated_at,
            created_at=model.created_at,
            text=model.text,
        )

    @staticmethod
    def to_model(entity: LectureComment) -> LectureCommentModel:
        return LectureCommentModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            lecture_id=str(entity.lecture_id),
            text=entity.text,
            updated_at=entity.updated_at,
            created_at=entity.created_at,
        )