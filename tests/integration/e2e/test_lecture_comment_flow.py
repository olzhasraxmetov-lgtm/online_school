import pytest


@pytest.mark.asyncio
async def test_lecture_comment_flow_from_author_creating_course_and_student_creating_comment(
    client,
    author_auth_headers,
    student_auth_headers,
    other_student_auth_headers,
):
    course_response = await client.post(
        '/api/admin/courses',
        headers=author_auth_headers,
        json={
            'title': 'Interactive FastAPI',
            'description': 'Course with lecture discussions.',
        },
    )
    assert course_response.status_code == 201
    course_payload = course_response.json()
    assert course_payload['status'] == 'draft'
    course_id = course_payload['id']

    module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=author_auth_headers,
        json={'title': 'HTTP', 'description': 'Methods', 'position': 1},
    )
    assert module_response.status_code == 201
    module_id = module_response.json()['id']

    section_response = await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=author_auth_headers,
        json={'title': 'Basics', 'description': 'Intro', 'position': 1},
    )
    assert section_response.status_code == 201
    section_id = section_response.json()['id']

    lecture_response = await client.post(
        f'/api/admin/sections/{section_id}/lectures',
        headers=author_auth_headers,
        json={
            'title': 'Bearer token in practice',
            'content': 'Lecture content',
            'position': 1,
        },
    )
    assert lecture_response.status_code == 201
    lecture_id = lecture_response.json()['id']

    draft_get_response = await client.get(
        f'/api/lectures/{lecture_id}/comments',
        headers=student_auth_headers,
    )
    assert draft_get_response.status_code == 404
    assert draft_get_response.json()['error'] == 'lecture_not_found'

    publish_response = await client.post(
        f'/api/admin/courses/{course_id}/publish',
        headers=author_auth_headers,
    )
    assert publish_response.status_code == 200

    create_response = await client.post(
        f'/api/lectures/{lecture_id}/comments',
        headers=student_auth_headers,
        json={'text': 'Test comment'},
    )
    assert create_response.status_code == 201
    create_payload = create_response.json()
    comment_id = create_payload['id']
    assert create_payload['lecture_id'] == lecture_id
    assert create_payload['text'] == 'Test comment'
    assert create_payload['updated_at'] is None

    list_response = await client.get(
        f'/api/lectures/{lecture_id}/comments',
        headers=student_auth_headers,
    )
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert len(list_payload) == 1
    assert list_payload[0]['id'] == comment_id
    assert list_payload[0]['text'] == 'Test comment'

    update_response = await client.patch(
        f'/api/comments/{comment_id}',
        headers=student_auth_headers,
        json={'text': 'Updated comment text'},
    )
    assert update_response.status_code == 200
    update_payload = update_response.json()
    assert update_payload['text'] == 'Updated comment text'
    assert update_payload['updated_at'] is not None

    list_response = await client.get(
        f'/api/lectures/{lecture_id}/comments',
        headers=student_auth_headers,
    )
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert len(list_payload) == 1
    assert list_payload[0]['text'] == 'Updated comment text'
    assert list_payload[0]['updated_at'] is not None

    other_student_update_response = await client.patch(
        f'/api/comments/{comment_id}',
        headers=other_student_auth_headers,
        json={'text': 'Hacked'},
    )
    assert other_student_update_response.status_code == 403
    assert other_student_update_response.json()['error'] == 'permission_denied'

    list_response = await client.get(
        f'/api/lectures/{lecture_id}/comments',
        headers=student_auth_headers,
    )
    assert list_response.status_code == 200
    assert list_response.json()[0]['text'] == 'Updated comment text'

    delete_response = await client.delete(
        f'/api/comments/{comment_id}',
        headers=author_auth_headers,
    )
    assert delete_response.status_code == 204

    list_response = await client.get(
        f'/api/lectures/{lecture_id}/comments',
        headers=student_auth_headers,
    )
    assert list_response.status_code == 200
    assert list_response.json() == []
