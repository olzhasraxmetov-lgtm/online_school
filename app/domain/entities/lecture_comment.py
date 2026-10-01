from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID

from app.domain.exceptions import InvalidLectureCommentError


@dataclass(slots=True)
class LectureComment:
    id: UUID
    lecture_id: UUID
    user_id: UUID
    text: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    def __post_init__(self):
        self.text = self.text.strip()
        self._validate()

    def _validate(self):
        if not self.text:
            raise InvalidLectureCommentError("Lecture comment text cannot be empty.")

        if len(self.text) > 2000:
            raise InvalidLectureCommentError(
                'Lecture comment text cannot exceed 2000 characters.'
            )

    def update(self, text: str) -> None:
        self.text = text.strip()
        self.updated_at = datetime.now(UTC)
        self._validate()

    def is_written_by(self, user_id: UUID) -> bool:
        return self.user_id == user_id