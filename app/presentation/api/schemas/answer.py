from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AnswerOptionWriteRequest(BaseModel):
    text: str = Field(min_length=1)
    position: int = Field(default=0)
    is_correct: bool = False

class CreateAnswerOptionRequest(AnswerOptionWriteRequest):
    pass

class UpdateAnswerOptionRequest(AnswerOptionWriteRequest):
    pass

class AnswerOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    question_id: UUID
    text: str
    position: int
    is_correct: bool