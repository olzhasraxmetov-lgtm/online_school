from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.presentation.api.schemas.content.section import SectionStructureResponse


class ModuleBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class ModuleStructureResponse(ModuleBaseResponse):
    sections: list[SectionStructureResponse]