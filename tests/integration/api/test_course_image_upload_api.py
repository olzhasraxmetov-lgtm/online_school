from uuid import uuid4

import pytest

from app.domain.entities.image_files import ImageCover
from app.infrastructure.config.settings import get_settings


@pytest.fixture(autouse=True)
def isolate_image_storage(tmp_path, monkeypatch):
    monkeypatch.setenv('IMAGE_COVER_DIR', str(tmp_path) + '/')
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()

@pytest.mark.asyncio
async def test_course_image_upload_updated_successfully_for_existing_course(
    client,
    author_auth_headers,
    seeded_tasks_tree,
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=author_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 200
    assert response.json()['cover_image_url'] != ''
    assert response.json()['cover_image_url'].startswith('/static')
    assert response.json()['cover_image_url'].endswith('.jpg')

@pytest.mark.asyncio
async def test_course_image_upload_returns_not_found_when_its_missing(
    client,
    author_auth_headers,
    seeded_tasks_tree,
):
    response = await client.post(
        f'/api/admin/courses/{uuid4()}/image_cover',
        headers=author_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_course_image_upload_returns_error_when_file_size_is_invalid(
    client,
    author_auth_headers,
    seeded_tasks_tree,
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=author_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * (ImageCover.MAX_COVER_IMAGE_SIZE + 1),
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'domain_error'

@pytest.mark.asyncio
async def test_course_image_upload_returns_error_when_it_belongs_to_foreign_author(
    client,
    author_auth_headers,
    seeded_tasks_tree,
    other_author_auth_headers
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=other_author_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'

@pytest.mark.asyncio
async def test_course_image_upload_returns_error_when_actor_is_regular_user(
    client,
    seeded_tasks_tree,
    student_auth_headers
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=student_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'

@pytest.mark.asyncio
async def test_course_image_upload_returns_error_without_authorization(
    client,
    seeded_tasks_tree,
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 401
    assert response.json()['error'] == 'authentication_error'

@pytest.mark.asyncio
async def test_course_image_upload_can_be_changed_by_admin(
    client,
    seeded_tasks_tree,
    admin_auth_headers
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=admin_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 200
    assert response.json()['cover_image_url'] != ''
    assert response.json()['cover_image_url'].startswith('/static')
    assert response.json()['cover_image_url'].endswith('.jpg')

@pytest.mark.asyncio
async def test_course_image_upload_returns_error_when_content_type_is_invalid(
    client,
    seeded_tasks_tree,
    author_auth_headers,
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=author_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'application/pdf',
            )
        },
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'domain_error'

@pytest.mark.asyncio
async def test_course_image_upload_returns_error_when_file_is_missing(
    client,
    seeded_tasks_tree,
    author_auth_headers,
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=author_auth_headers,
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_course_image_upload_mounted_and_returns_file(
    client,
    seeded_tasks_tree,
    author_auth_headers,
):
    response = await client.post(
        f'/api/admin/courses/{seeded_tasks_tree.course_id}/image_cover',
        headers=author_auth_headers,
        files={
            'file': (
                f'{uuid4()}.jpg',
                b'x' * ImageCover.MAX_COVER_IMAGE_SIZE,
                'image/jpeg',
            )
        },
    )

    assert response.status_code == 200

    image_response = await client.get(response.json()['cover_image_url'])
    assert image_response.status_code == 200
    assert image_response.headers['content-type'] == 'image/jpeg'