from dataclasses import dataclass
from uuid import UUID

from app.domain.exceptions import InvalidAnswerOptionError


@dataclass(slots=True)
class AnswerOption:
    id: UUID
    question_id: UUID
    text: str
    position: int
    is_correct: bool = False

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.text or not self.text.strip():
            raise InvalidAnswerOptionError("Answer option text cannot be empty.")
        if self.position < 1:
            raise InvalidAnswerOptionError("Answer option position must be positive.")