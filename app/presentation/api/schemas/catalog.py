from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entities.course import CourseStatus


class CourseCatalogCountersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    module_count: int
    section_count: int
    lecture_count: int
    question_count: int
    task_count: int
    code_task_count: int

class CourseCatalogItemsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    status: CourseStatus
    counters: CourseCatalogCountersResponse

class CourseCatalogSectionPreviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int

class CourseCatalogModulePreviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int
    sections: list[CourseCatalogSectionPreviewResponse]

class CourseCatalogCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    status: CourseStatus
    counters: CourseCatalogCountersResponse
    modules: list[CourseCatalogModulePreviewResponse]