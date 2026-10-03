from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.entities import StudentActivityType


@dataclass(slots=True)
class StudentActivityDTO:
    id: UUID
    student_id: UUID
    course_id: UUID
    activity_type: StudentActivityType
    entity_id: UUID
    title: str
    details: dict[str, str | int | float | bool]
    occurred_at: datetime

@dataclass(slots=True)
class StudentActivityPageDTO:
    items: list[StudentActivityDTO]
    total: int
    limit: int
    offset: int