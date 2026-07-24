from uuid import uuid4

import pytest

from app.domain.entities.course import Course
from app.domain.exceptions import InvalidCourseError

def test_course_is_created_with_valid_data() -> None:
    course = Course(
        id=uuid4(),
        title="SQLAlchemy",
        description="SQLAlchemy practicing",
    )
    assert course.title == "SQLAlchemy"
    assert course.description == "SQLAlchemy practicing"
    assert course.module_ids == []

def test_course_raises_error_when_title_is_blank() -> None:
    with pytest.raises(InvalidCourseError):
        Course(
            id=uuid4(),
            title="",
            description="SQLAlchemy practicing",
        )

def test_course_raises_error_when_description_is_blank() -> None:
    with pytest.raises(InvalidCourseError):
        Course(
            id=uuid4(),
            title="Valid title",
            description="",
        )

def test_course_update_changes_title() -> None:
    course = Course(
        id=uuid4(),
        title="SQLAlchemy",
        description="SQLAlchemy practicing",
    )

    course.update(title="New title", description="New description")

    assert course.title == "New title"
    assert course.description == "New description"