from abc import ABC, abstractmethod

from app.application.interfaces.repositories import (
    CourseRepository,
    LectureRepository,
    ModuleRepository,
    SectionRepository,
    UserRepository,
    QuestionRepository,
    AnswerOptionRepository,
)


class UnitOfWork(ABC):
    courses: CourseRepository
    modules: ModuleRepository
    lectures: LectureRepository
    sections: SectionRepository
    users: UserRepository
    questions: QuestionRepository
    answer_options: AnswerOptionRepository

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError