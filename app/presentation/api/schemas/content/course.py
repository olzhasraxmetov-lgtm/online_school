from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

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


class CourseWriteRequest(BaseModel):
   title: str = Field(min_length=1, max_length=255)
   description: str = Field(min_length=1)


class CreateCourseRequest(CourseWriteRequest):
   pass


class UpdateCourseRequest(CourseWriteRequest):
   pass