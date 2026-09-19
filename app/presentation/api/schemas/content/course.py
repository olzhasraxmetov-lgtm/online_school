from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.course import CourseStatus, CourseDifficulty
from app.presentation.api.schemas.content.module import ModuleStructureResponse


class CourseBaseResponse(BaseModel):
   model_config = ConfigDict(from_attributes=True)

   id: UUID
   title: str
   description: str
   status: CourseStatus
   short_description: str
   cover_image_url: str | None
   difficulty: CourseDifficulty
   tag_names: list[str]

class CourseListItemResponse(CourseBaseResponse):
   pass

class CourseResponse(CourseBaseResponse):
   pass

class CourseStructureResponse(CourseBaseResponse):
    modules: list[ModuleStructureResponse]


class CourseWriteRequest(BaseModel):
   title: str = Field(min_length=1, max_length=255)
   description: str = Field(min_length=1)
   short_description: str = Field(default='', max_length=280)
   difficulty: CourseDifficulty = CourseDifficulty.BEGINNER
   tag_names: list[str] = Field(default_factory=list, max_length=10)


class CreateCourseRequest(CourseWriteRequest):
   pass


class UpdateCourseRequest(CourseWriteRequest):
   pass

