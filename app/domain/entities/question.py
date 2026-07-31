import typing
from dataclasses import dataclass, field
from typing import Sequence
from uuid import UUID

from app.domain.exceptions import InvalidQuestionError

if typing.TYPE_CHECKING:
    from app.domain.entities.answer_option import AnswerOption

class QuestionType:
    SINGLE_CHOICE = 'single_choice'
    MULTIPLE_CHOICE = 'multiple_choice'

@dataclass(slots=True)
class Question:
    id: UUID
    section_id: UUID
    text: str
    position: int
    question_type: QuestionType = QuestionType.SINGLE_CHOICE
    answer_option_ids: list[UUID] = field(default_factory=list)
    max_attempts: int = 1
    reward_points: int = 1

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.text or not self.text.strip():
            raise InvalidQuestionError("Question text cannot be empty.")

        if self.position < 1:
            raise InvalidQuestionError("Question position must be positive.")

        if self.max_attempts < 1:
            raise InvalidQuestionError("Question max attempts must be positive.")

        if self.reward_points < 1:
            raise InvalidQuestionError("Question reward points must be positive.")

    def validate_answer_options_configuration(
            self,
            answer_options: Sequence['AnswerOption']
    ) -> None:
        if len(answer_options) < 2:
            raise InvalidQuestionError("Question must have at least two answer options.")

        correct_options_count = sum(1 for option in answer_options if option.is_correct)

        if correct_options_count == 0:
            raise InvalidQuestionError("Question must have at least one answer option.")

        if self.is_single_choice() and correct_options_count != 1:
            raise InvalidQuestionError(
                "Single chose question must have exactly one answer option."
            )

        if self.is_multiple_choice() and correct_options_count < 2:
            raise InvalidQuestionError(
                "Multiple chose question must have at least two correct answer options."
            )

    def update(
            self,
            text: str,
            position: int,
            max_attempts: int,
            reward_points: int,
    ) -> None:
        self.text = text
        self.position = position
        self.max_attempts = max_attempts
        self.reward_points = reward_points
        self._validate()

    def add_answer_option(self, answer_option_id: UUID) -> None:
        if answer_option_id not in self.answer_option_ids:
            self.answer_option_ids.append(answer_option_id)
    def remove_answer_option(self, answer_option_id: UUID) -> None:
        if answer_option_id in self.answer_option_ids:
            self.answer_option_ids.remove(answer_option_id)

    def has_answer_options(self) -> bool:
        return bool(self.answer_option_ids)

    def is_single_choice(self) -> bool:
        return self.question_type is QuestionType.SINGLE_CHOICE

    def is_multiple_choice(self) -> bool:
        return self.question_type is QuestionType.MULTIPLE_CHOICE

    def allows_multiple_answers(self) -> bool:
        return self.is_multiple_choice()