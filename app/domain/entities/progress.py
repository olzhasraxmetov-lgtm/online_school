from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exceptions import InvalidProgressError


@dataclass(slots=True)
class Progress:
    id: UUID
    student_id: UUID
    course_id: UUID
    complete_question_ids: list[UUID] = field(default_factory=list)
    completed_section_ids: list[UUID] = field(default_factory=list)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if len(self.complete_question_ids) != len(set(self.complete_question_ids)):
            raise InvalidProgressError("Progress cannot contain duplicate completed questions.")
        if len(self.completed_section_ids) != len(set(self.completed_section_ids)):
            raise InvalidProgressError("Progress cannot contain duplicate completed sections.")

    def has_completed_question(self, question_id: UUID) -> bool:
        return question_id in self.complete_question_ids

    def has_completed_section(self, section_id: UUID) -> bool:
        return section_id in self.completed_section_ids

    def mark_question_complete(self, question_id: UUID):
        if question_id not in self.complete_question_ids:
            self.complete_question_ids.append(question_id)

    def mark_section_complete(self, section_id: UUID):
        if section_id not in self.completed_section_ids:
            self.completed_section_ids.append(section_id)