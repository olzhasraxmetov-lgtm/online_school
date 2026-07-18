from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.presentation.api.schemas.content.module import ModuleStructureResponse


class CourseBaseResponse(BaseModel):
   model_config = ConfigDict(from_attributes=True)

   id: UUID
   title: str
   description: str

class CourseListItemResponse(CourseBaseResponse):
   pass

class CourseResponse(CourseBaseResponse):
   pass

class CourseStructureResponse(CourseBaseResponse):
    modules: list[ModuleStructureResponse]