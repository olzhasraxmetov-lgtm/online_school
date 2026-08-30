from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.interfaces.unit_of_work import UnitOfWork
from app.infrastructure.database.repositories import (
    SqlAlchemyCourseRepository,
    SqlAlchemyLectureRepository,
    SqlAlchemyModuleRepository,
    SqlAlchemySectionRepository,
    SqlAlchemyUserRepository,
    SqlAlchemyAnswerOptionRepository,
    SqlAlchemyQuestionRepository,
    SqlAlchemyQuestionAttemptRepository,
    SqlAlchemyProgressRepository,
    SqlAlchemyTaskRepository,
    SqlAlchemyTaskAttemptRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(
            self,
            session_factory: async_sessionmaker[AsyncSession] | None = None,
            session: AsyncSession | None = None,
    ) -> None:
        self.session_factory = session_factory
        self._external_session = session
        self.session: AsyncSession | None = session

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        if self.session is None:
            if  self.session_factory is None:
                raise RuntimeError("Session factory is required when session is not provided")
            self.session = self.session_factory()

        self.courses = SqlAlchemyCourseRepository(session=self.session)
        self.modules = SqlAlchemyModuleRepository(session=self.session)
        self.sections = SqlAlchemySectionRepository(session=self.session)
        self.lectures = SqlAlchemyLectureRepository(session=self.session)
        self.users = SqlAlchemyUserRepository(session=self.session)
        self.questions = SqlAlchemyQuestionRepository(session=self.session)
        self.answer_options = SqlAlchemyAnswerOptionRepository(session=self.session)
        self.question_attempts = SqlAlchemyQuestionAttemptRepository(session=self.session)
        self.tasks = SqlAlchemyTaskRepository(self.session)
        self.task_attempts = SqlAlchemyTaskAttemptRepository(self.session)
        self.progress = SqlAlchemyProgressRepository(session=self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session is None:
            return

        if exc_type is not None:
            await self.rollback()

        if self._external_session is None:
            await self.session.close()
            self.session = None

    async def commit(self) -> None:
        if self.session is not None:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session is not None:
            await self.session.rollback()
