from uuid import UUID

from pydantic import ConfigDict, BaseModel

from app.domain.entities.question import QuestionType


class AnswerOptionDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text: str
    position: int


class QuestionDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    section_id: UUID
    text: str
    position: int
    question_type: QuestionType
    max_attempts: int
    reward_points: int
    answer_options: list[AnswerOptionDetailsResponse]


class TaskDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    section_id: UUID
    title: str
    statement: str
    position: int
    max_attempts: int
    reward_points: int


class CodeTaskDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    section_id: UUID
    title: str
    statement: str
    position: int
    language: str
    starter_code: str
    max_attempts: int
    reward_points: int
    time_limit_seconds: int
    memory_limit_mb: int