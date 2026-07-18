from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.presentation.api.schemas.content.lecture import LectureStructureResponse


class SectionBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class SectionStructureResponse(SectionBaseResponse):
    lectures: list[LectureStructureResponse]