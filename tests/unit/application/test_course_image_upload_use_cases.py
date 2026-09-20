from uuid import uuid4

import pytest

from app.application.exceptions import CourseNotFoundError, PermissionDeniedError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.courses.upload_course_image import CourseImageUploadUseCase, UploadCourseImageCommand
from app.domain.entities import Course, User, UserRole
from app.domain.entities.image_files import ImageCover
from app.domain.exceptions import InvalidCoverImageError

def make_admin() -> User:
    return User(
        id=uuid4(),
        email="admin@example.com",
        hashed_password="admin-password",
        role=UserRole.ADMIN,
    )


def make_author() -> User:
    return User(
        id=uuid4(),
        email="author@example.com",
        hashed_password="some-password",
        role=UserRole.AUTHOR,
    )

def make_other_author() -> User:
    return User(
        id=uuid4(),
        email="other@example.com",
        hashed_password="hashed-password",
        role=UserRole.AUTHOR,
    )

def make_image_cover(
        content_type: str = 'image/jpeg',
        content=b'x' * ImageCover.MAX_COVER_IMAGE_SIZE
) -> ImageCover:
    return ImageCover(
       content_type=content_type,
       content=content,
    )

def make_owned_course(author: User) -> Course:
    return Course(
        id=uuid4(),
        author_id=author.id,
        title='Course',
        description='Description',
    )

class FakeImageStorage:
    def __init__(self) -> None:
        self.saved_file_name = None
        self.saved_content = None

    async def save(self, file_name: str, content: bytes) -> str:
        self.saved_file_name = file_name
        self.saved_content = content
        return f'/static/{file_name}'

class FakeCourseRepository:
    def __init__(self) -> None:
        self.items = {}

    async def get_by_id(self, course_id):
        return self.items.get(course_id)

    async def list(self):
        return list(self.items.values())

    async def add(self, course: Course) -> None:
        self.items[course.id] = course

    async def update(self, course) -> None:
        self.items[course.id] = course

    async def remove(self, course_id) -> None:
        self.items.pop(course_id, None)

class FakeUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.courses = FakeCourseRepository()
        self.users = None
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True

@pytest.mark.asyncio
async def test_upload_course_image_sets_cover_url_and_commits() -> None:
    author = make_author()
    course = make_owned_course(author)
    uow = FakeUnitOfWork()
    await uow.courses.add(course)
    image_cover = make_image_cover()
    image_storage = FakeImageStorage()
    use_case = CourseImageUploadUseCase(uow=uow, image_storage=image_storage)

    await use_case.execute(
        UploadCourseImageCommand(
            course_id=course.id,
            actor=author,
            content_type=image_cover.content_type,
            content=image_cover.content,
        )
    )

    assert course.cover_image_url != ''
    assert course.cover_image_url.endswith(image_cover.extension)
    assert course.cover_image_url.startswith('/static/')
    assert image_storage.saved_content == image_cover.content
    assert uow.committed is True


@pytest.mark.asyncio
async def test_course_image_upload_raises_error_when_its_missing() -> None:
    author = make_author()
    course = make_owned_course(author)
    uow = FakeUnitOfWork()
    await uow.courses.add(course)
    image_cover = make_image_cover()
    image_storage = FakeImageStorage()
    use_case = CourseImageUploadUseCase(uow=uow, image_storage=image_storage)

    with pytest.raises(CourseNotFoundError):
        await use_case.execute(
            UploadCourseImageCommand(
                course_id=uuid4(),
                actor=author,
                content_type=image_cover.content_type,
                content=image_cover.content,
            )
        )

    assert image_storage.saved_file_name is None
    assert uow.committed is False

@pytest.mark.asyncio
async def test_course_image_upload_raises_error_when_it_belongs_to_foreign_author() -> None:
    author = make_author()
    course = make_owned_course(author)
    other_author = make_other_author()
    uow = FakeUnitOfWork()
    await uow.courses.add(course)
    image_cover = make_image_cover()
    image_storage = FakeImageStorage()
    use_case = CourseImageUploadUseCase(uow=uow, image_storage=image_storage)

    with pytest.raises(PermissionDeniedError):
        await use_case.execute(
            UploadCourseImageCommand(
                course_id=course.id,
                actor=other_author,
                content_type=image_cover.content_type,
                content=image_cover.content,
            )
        )

    assert image_storage.saved_file_name is None
    assert uow.committed is False

@pytest.mark.asyncio
async def test_upload_course_image_succeeds_for_admin_who_is_not_owner() -> None:
    admin = make_admin()
    author = make_author()
    course = make_owned_course(author)
    uow = FakeUnitOfWork()
    await uow.courses.add(course)
    image_cover = make_image_cover()
    image_storage = FakeImageStorage()
    use_case = CourseImageUploadUseCase(uow=uow, image_storage=image_storage)

    result = await use_case.execute(
        UploadCourseImageCommand(
            course_id=course.id,
            actor=admin,
            content_type=image_cover.content_type,
            content=image_cover.content,
        )
    )
    assert result.cover_image_url is not None
    assert result.cover_image_url.endswith(image_cover.extension)
    assert image_storage.saved_file_name is not None
    assert uow.committed is True

@pytest.mark.asyncio
async def test_upload_course_image_raises_error_when_file_size_is_invalid() -> None:
    author = make_author()
    course = make_owned_course(author)
    uow = FakeUnitOfWork()
    await uow.courses.add(course)
    image_cover = make_image_cover()
    image_storage = FakeImageStorage()
    use_case = CourseImageUploadUseCase(uow=uow, image_storage=image_storage)

    with pytest.raises(InvalidCoverImageError):
        await use_case.execute(
            UploadCourseImageCommand(
                course_id=course.id,
                actor=author,
                content_type=image_cover.content_type,
                content = b'x' * (ImageCover.MAX_COVER_IMAGE_SIZE + 1)
            )
        )
    assert image_storage.saved_file_name is None
    assert uow.committed is False