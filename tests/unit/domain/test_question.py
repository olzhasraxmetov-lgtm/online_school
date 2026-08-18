from uuid import uuid4

import pytest

from app.domain.entities import AnswerOption, QuestionResultStatus
from app.domain.entities.question import Question, QuestionType
from app.domain.exceptions import InvalidQuestionError


def test_question_is_created_with_valid_data() -> None:
    question = Question(
        id=uuid4(),
        section_id=uuid4(),
        text="What does Depends mean?",
        position=1,
        question_type=QuestionType.SINGLE_CHOICE,
        max_attempts=2,
        reward_points=5
    )

    assert question.text == "What does Depends mean?"
    assert question.max_attempts == 2
    assert question.reward_points == 5


def test_question_raises_error_when_text_is_blank() -> None:
    with pytest.raises(InvalidQuestionError):
        Question(
            id=uuid4(),
            section_id=uuid4(),
            text="",
            position=1,
        )

def test_single_choice_question_requires_exactly_one_correct_option() -> None:
    question = Question(
        id=uuid4(),
        section_id=uuid4(),
        text="Single choice",
        position=1,
        question_type=QuestionType.SINGLE_CHOICE,
    )
    options = [
        AnswerOption(id=uuid4(), question_id=question.id, text="A", position=1, is_correct=True),
        AnswerOption(id=uuid4(), question_id=question.id, text="B", position=1, is_correct=True),
    ]

    with pytest.raises(InvalidQuestionError):
        question.validate_answer_options_configuration(options)

def test_question_resolves_correct_status_and_points() -> None:
    correct_option_id = uuid4()
    wrong_option_id = uuid4()
    question = Question(
        id=uuid4(),
        section_id=uuid4(),
        text="What method allows to send  data?",
        position=1,
        question_type=QuestionType.SINGLE_CHOICE,
        answer_option_ids=[correct_option_id, wrong_option_id],
        reward_points=5,
    )
    options = [
        AnswerOption(id=wrong_option_id, question_id=question.id, text='POST', position=1, is_correct=True),
        AnswerOption(id=correct_option_id, question_id=question.id, text='GET', position=2, is_correct=False),
    ]

    assert question.resolve_result_status([correct_option_id], options) is QuestionResultStatus.CORRECT
    assert question.resolve_awarded_points([correct_option_id], options) == 5
    assert question.resolve_awarded_points([wrong_option_id], options) == 0