from uuid import uuid4

import pytest

from app.application.exceptions import (
    CourseNotFoundError,
    SectionNotFoundError,
    LectureNotFoundError,
    ModuleNotFoundError
)
from app.application.use_cases.courses.delete_course import (
    DeleteCourseUseCase,
    DeleteCourseCommand
)
from app.application.use_cases.lectures.delete_lecture import (
    DeleteLectureUseCase,
    DeleteLectureCommand
)
from app.application.use_cases.modules.delete_module import (
    DeleteModuleUseCase,
    DeleteModuleCommand
)
from app.application.use_cases.sections.delete_section import (
    DeleteSectionUseCase,
    DeleteSectionCommand
)
from app.domain.entities.course import Course
from app.domain.entities.lecture import Lecture
from app.domain.entities.module import Module
from app.domain.entities.section import Section
from tests.unit.application.test_content_write_use_cases import FakeUnitOfWork


@pytest.mark.asyncio
async def test_delete_existing_course() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteCourseUseCase(uow=uow)

    course = Course(
        id=uuid4(),
        title="Course title",
        description="Course Description",
    )
    await uow.courses.add(course)
    await use_case.execute(
        DeleteCourseCommand(course_id=course.id)
    )
    assert course.id not in uow.courses.items
    assert uow.committed is True

@pytest.mark.asyncio
async def test_delete_course_raises_not_found_when_its_missing() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteCourseUseCase(uow=uow)

    with pytest.raises(CourseNotFoundError):
        await use_case.execute(
            DeleteCourseCommand(course_id=uuid4())
        )

@pytest.mark.asyncio
async def test_delete_existing_module() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteModuleUseCase(uow=uow)

    course = Course(id=uuid4(), title="Course title", description="Course Description")
    module = Module(
        id=uuid4(),
        course_id=course.id,
        title="Module title",
        description="Module Description",
        position=1,
    )

    course.add_module(module_id=module.id)
    await uow.courses.add(course)
    await uow.modules.add(module)

    await use_case.execute(
        DeleteModuleCommand(module_id=module.id)
    )
    assert module.id not in uow.modules.items
    assert module.id not in course.module_ids
    assert uow.committed is True

@pytest.mark.asyncio
async def test_delete_module_raises_not_found_when_its_missing() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteModuleUseCase(uow=uow)

    with pytest.raises(ModuleNotFoundError):
        await use_case.execute(
            DeleteModuleCommand(module_id=uuid4())
        )

@pytest.mark.asyncio
async def test_delete_existing_section() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteSectionUseCase(uow=uow)

    course = Course(id=uuid4(), title="Course title", description="Course Description")

    module = Module(
        id=uuid4(),
        title="Module title",
        course_id=course.id,
        description="Module Description",
        position=1
    )
    section = Section(
        id=uuid4(),
        module_id=module.id,
        title="Section title",
        description="Section Description",
        position=1,
    )
    module.add_section(section_id=section.id)
    await uow.courses.add(course)
    await uow.modules.add(module)
    await uow.sections.add(section)

    await use_case.execute(
        DeleteSectionCommand(section_id=section.id)
    )
    assert section.id not in uow.sections.items
    assert section.id not in module.sections_ids
    assert uow.committed is True

@pytest.mark.asyncio
async def test_delete_section_raises_not_found_when_its_missing() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteSectionUseCase(uow=uow)

    with pytest.raises(SectionNotFoundError):
        await use_case.execute(
            DeleteSectionCommand(section_id=uuid4())
        )

@pytest.mark.asyncio
async def test_delete_existing_lecture() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteLectureUseCase(uow=uow)

    course = Course(id=uuid4(), title="New title", description="New Description")
    module = Module(
        id=uuid4(),
        title="Module title",
        course_id=course.id,
        description="Module Description",
        position=1
    )
    section = Section(
        id=uuid4(),
        module_id=module.id,
        title="Section title",
        description="Section Description",
        position=1,
    )
    lecture = Lecture(
        id=uuid4(),
        section_id=section.id,
        title="New lecture",
        content="New content",
        position=1,
    )
    section.add_lecture(lecture.id)
    await uow.courses.add(course)
    await uow.modules.add(module)
    await uow.sections.add(section)
    await uow.lectures.add(lecture)

    await use_case.execute(
        DeleteLectureCommand(lecture_id=lecture.id)
    )
    assert lecture.id not in uow.lectures.items
    assert lecture.id not in section.lecture_ids
    assert uow.committed is True

@pytest.mark.asyncio
async def test_delete_lecture_raises_not_found_when_its_missing() -> None:
    uow = FakeUnitOfWork()
    use_case = DeleteLectureUseCase(uow=uow)

    with pytest.raises(LectureNotFoundError):
        await use_case.execute(
            DeleteLectureCommand(lecture_id=uuid4())
        )