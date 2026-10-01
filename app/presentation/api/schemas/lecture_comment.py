from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LectureCommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    lecture_id: UUID
    text: str
    updated_at: datetime | None = None
    created_at: datetime

class CreateLectureCommentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

class UpdateLectureCommentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)