from uuid import uuid4

import pytest

from app.domain.entities.course import Course
from app.domain.entities.image_files import ImageCover
from app.domain.exceptions import InvalidCoverImageError


def build_course() -> Course:
    return Course(
        id=uuid4(),
        author_id=uuid4(),
        title='FastAPI course',
        description='Clean architecture in practice.',
    )

def build_image_cover(*, content_type: str = 'image/png', size: int = 1024) -> ImageCover:
    return ImageCover(content_type=content_type, content=b'x' * size)

def test_image_cover_created_with_valid_content_type() -> None:
    image_cover = build_image_cover()

    assert image_cover.content_type == 'image/png'

def test_image_cover_raises_error_when_content_is_empty() -> None:
    with pytest.raises(InvalidCoverImageError):
        ImageCover(content_type='image/png', content=b'')

def test_image_cover_raises_error_when_content_type_is_invalid() -> None:
    with pytest.raises(InvalidCoverImageError):
        ImageCover(content_type='application/pdf', content=b'x' * 1024)

def test_image_cover_returns_its_extension() -> None:
    image_cover = build_image_cover()

    assert image_cover.extension == '.png'

def test_image_cover_is_created_when_max_size_is_valid() -> None:
    image_cover = build_image_cover(size=ImageCover.MAX_COVER_IMAGE_SIZE)

    assert len(image_cover.content) == ImageCover.MAX_COVER_IMAGE_SIZE

def test_image_cover_raises_error_when_max_size_is_invalid() -> None:
    with pytest.raises(InvalidCoverImageError):
        ImageCover(content_type='image/png', content=b'x' * (ImageCover.MAX_COVER_IMAGE_SIZE + 1))