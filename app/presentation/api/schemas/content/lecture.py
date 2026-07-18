from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LectureBaseResponse(BaseModel):
   model_config = ConfigDict(from_attributes=True)

   id: UUID
   title: str
   position: int

class LectureResponse(LectureBaseResponse):
   content: str
   section_id: UUID

class LectureStructureResponse(LectureBaseResponse):
    pass

class LectureWriteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    position: int = Field(ge=1)


class CreateLectureRequest(LectureWriteRequest):
    pass


class UpdateLectureRequest(LectureWriteRequest):
    pass