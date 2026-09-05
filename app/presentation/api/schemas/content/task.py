from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskStructureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int


class CodeTaskStructureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int
    language: str