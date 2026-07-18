from uuid import UUID

from pydantic import BaseModel, ConfigDict


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