import pytest

@pytest.mark.asyncio
async def test_delete_course_returns_not_found(client ,seeded_course_tree, admin_auth_headers):
    response = await client.delete(
        f'/api/admin/courses/{seeded_course_tree.course_id}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 204
    response_get = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}',
    )
    assert response_get.status_code == 404

@pytest.mark.asyncio
async def test_delete_module_returns_empty_structure_for_sections_and_lectures(
        client,
        seeded_course_tree,
        admin_auth_headers
):
    response = await client.delete(
        f'/api/admin/modules/{seeded_course_tree.module_id}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 204

    response_get_structure = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure',
    )

    assert response_get_structure.status_code == 200
    payload = response_get_structure.json()
    assert len(payload['modules']) == 0

@pytest.mark.asyncio
async def test_delete_lecture_returns_not_found_when_its_missing(client, admin_auth_headers, seeded_course_tree):
    response = await client.delete(
        f'/api/admin/lectures/{seeded_course_tree.lecture_id}',
        headers=admin_auth_headers,
    )
    assert response.status_code == 204

    response_get = await client.get(
        f'/api/lectures/{seeded_course_tree.lecture_id}',
    )
    assert response_get.status_code == 404
    assert response_get.json()['error'] == 'lecture_not_found'

@pytest.mark.asyncio
async def test_route_return_unauthenticated(client, seeded_course_tree):
    response = await client.delete(f'/api/admin/courses/{seeded_course_tree.course_id}')

    assert response.status_code == 401
    assert response.json()['error'] == 'authentication_error'

@pytest.mark.asyncio
async def test_route_return_403_for_student_user(client, student_auth_headers, seeded_course_tree):
    response = await client.delete(
        f'/api/admin/courses/{seeded_course_tree.course_id}',
        headers=student_auth_headers,
    )

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'