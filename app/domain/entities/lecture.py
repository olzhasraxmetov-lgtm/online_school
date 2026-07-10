from dataclasses import dataclass
from uuid import UUID

from app.domain.exceptions import InvalidLectureError


@dataclass(slots=True)
class Lecture:
    id: UUID
    section_id: UUID
    title: str
    position: int
    content: str


    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.title or not self.title.strip():
            raise InvalidLectureError("Lecture title cannot be empty.")

        if not self.content or not self.content.strip():
            raise InvalidLectureError("Lecture content cannot be empty.")

        if self.position < 1:
            raise InvalidLectureError("Lecture position must be positive.")

    def update(self, title: str, content: str, position: int):
        self.title = title
        self.content = content
        self.position = position
        self._validate()