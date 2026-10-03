from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.student_activity import StudentActivity


class StudentActivityRepository(ABC):
    @abstractmethod
    async def add(self, activity: StudentActivity) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_student_id(
        self,
        student_id: UUID,
        limit: int,
        offset: int,
    ) -> list[StudentActivity]:
        raise NotImplementedError

    @abstractmethod
    async def count_by_student_id(self, student_id: UUID) -> int:
        raise NotImplementedError