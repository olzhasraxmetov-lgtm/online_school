from uuid import uuid4

import pytest


async def create_lecture_comment(
        client,
        lecture_id,
        headers,
        text = 'Test lecture comment'
):
    response_create_comment = await client.post(
        f'/api/lectures/{lecture_id}/comments',
        headers=headers,
        json={"text": text},
    )
    assert response_create_comment.status_code == 201
    return response_create_comment.json()

@pytest.mark.asyncio
async def test_student_can_get_comments_for_visible_lecture(
        client,
        seeded_author_course_tree,
        student_auth_headers,
        seeded_student_user,
):

    await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    response_get_comment = await client.get(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
        headers=student_auth_headers,
    )
    assert response_get_comment.status_code == 200

    payload = response_get_comment.json()

    assert len(payload) == 1
    assert payload[0]['text'] == 'Test lecture comment'
    assert payload[0]['user_id'] == seeded_student_user.id


@pytest.mark.asyncio
async def test_student_can_create_comment_for_visible_lecture(
        client,
        seeded_author_course_tree,
        student_auth_headers,
        seeded_student_user,
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    assert comment['text'] == 'Test lecture comment'
    assert comment['id'] is not None
    assert comment['user_id'] == seeded_student_user.id
    assert comment['lecture_id'] == seeded_author_course_tree.lecture_id
    assert comment['updated_at'] is None

@pytest.mark.asyncio
async def test_anonymous_user_cannot_create_comment_for_visible_lecture(
        client,
        seeded_author_course_tree,
):
    response = await client.post(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
        json={"text": "Test lecture comment"},
    )

    assert response.status_code == 401
    assert response.json()['error'] == 'authentication_error'

@pytest.mark.asyncio
async def test_student_cannot_create_comment_for_non_visible_lecture(
        client,
        student_auth_headers,
        seeded_draft_course_tree
):
    response = await client.post(
        f'/api/lectures/{seeded_draft_course_tree.lecture_id}/comments',
        headers=student_auth_headers,
        json={"text": "Test lecture comment"},
    )

    assert response.status_code == 404
    assert response.json()['error'] == 'lecture_not_found'

@pytest.mark.asyncio
async def test_comment_author_can_update_own_comment(
        client,
        seeded_author_course_tree,
        student_auth_headers,
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    comment_id = comment['id']

    response_update_comment = await client.patch(
        f'/api/comments/{comment_id}',
        headers=student_auth_headers,
        json={"text": "Updated comment"},
    )

    assert response_update_comment.status_code == 200
    assert response_update_comment.json()['text'] == 'Updated comment'
    assert response_update_comment.json()['updated_at'] is not None


@pytest.mark.asyncio
async def test_other_student_cannot_update_comment(
        client,
        seeded_author_course_tree,
        student_auth_headers,
        other_student_auth_headers
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )
    comment_id = comment['id']

    response_update_comment = await client.patch(
        f'/api/comments/{comment_id}',
        headers=other_student_auth_headers,
        json={"text": "Updated comment"},
    )

    assert response_update_comment.status_code == 403
    assert response_update_comment.json()['error'] == 'permission_denied'

@pytest.mark.asyncio
async def test_comment_author_can_delete_own_comment(
        client,
        seeded_author_course_tree,
        student_auth_headers,
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    delete_response = await client.delete(
        f'/api/comments/{comment["id"]}',
        headers=student_auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = await client.get(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
        headers=student_auth_headers,
    )

    assert get_response.status_code == 200
    assert len(get_response.json()) == 0

@pytest.mark.asyncio
async def test_course_author_can_delete_comment_in_own_course(
        client,
        seeded_author_course_tree,
        student_auth_headers,
        author_auth_headers
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    delete_response = await client.delete(
        f'/api/comments/{comment["id"]}',
        headers=author_auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = await client.get(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
        headers=author_auth_headers,
    )

    assert get_response.status_code == 200
    assert len(get_response.json()) == 0

@pytest.mark.asyncio
async def test_other_course_author_cannot_delete_comment(
        client,
        seeded_author_course_tree,
        author_auth_headers,
        student_auth_headers,
        other_author_auth_headers
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    delete_response = await client.delete(
        f'/api/comments/{comment["id"]}',
        headers=other_author_auth_headers,
    )

    assert delete_response.status_code == 403
    assert delete_response.json()['error'] == 'permission_denied'

    get_response = await client.get(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
        headers=author_auth_headers,
    )

    assert get_response.status_code == 200
    assert len(get_response.json()) == 1

@pytest.mark.asyncio
async def test_admin_can_delete_any_comment(
        client,
        seeded_author_course_tree,
        student_auth_headers,
        admin_auth_headers
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    delete_response = await client.delete(
        f'/api/comments/{comment["id"]}',
        headers=admin_auth_headers,
    )

    assert delete_response.status_code == 204

    get_response = await client.get(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
        headers=admin_auth_headers,
    )

    assert get_response.status_code == 200
    assert len(get_response.json()) == 0

@pytest.mark.asyncio
async def test_lecture_comments_are_returned_in_creation_order(
        client,
        seeded_author_course_tree,
        student_auth_headers,
):
    await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
        text='First comment text',
    )

    await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
        text='Second comment text',
    )

    get_response = await client.get(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
        headers=student_auth_headers,
    )

    assert get_response.status_code == 200
    payload = get_response.json()

    assert len(payload) == 2
    assert payload[0]['text'] == 'First comment text'
    assert payload[1]['text'] == 'Second comment text'

@pytest.mark.asyncio
async def test_student_cannot_see_comments_of_invisible_lecture(
        client,
        student_auth_headers,
        seeded_draft_course_tree
):
    get_response = await client.get(
        f'/api/lectures/{seeded_draft_course_tree.lecture_id}/comments',
        headers=student_auth_headers,
    )

    assert get_response.status_code == 404
    assert get_response.json()['error'] == 'lecture_not_found'

@pytest.mark.asyncio
async def test_anonymous_user_cannot_see_comments(
        client,
        seeded_author_course_tree
):
    get_response = await client.get(
        f'/api/lectures/{seeded_author_course_tree.lecture_id}/comments',
    )

    assert get_response.status_code == 401
    assert get_response.json()['error'] == 'authentication_error'

@pytest.mark.asyncio
async def test_delete_missing_comment_returns_404(
        client,
        student_auth_headers,
):
    delete_response = await client.delete(
        f'/api/comments/{uuid4()}',
        headers=student_auth_headers,
    )

    assert delete_response.status_code == 404
    assert delete_response.json()['error'] == 'lecture_comment_not_found'

@pytest.mark.asyncio
async def test_course_author_cannot_update_student_comment(
        client,
        student_auth_headers,
        seeded_author_course_tree,
        author_auth_headers
):
    comment = await create_lecture_comment(
        client,
        seeded_author_course_tree.lecture_id,
        student_auth_headers,
    )

    comment_id = comment['id']

    response_update = await client.patch(
        f'/api/comments/{comment_id}',
        headers=author_auth_headers,
        json={"text": "Updated comment"},
    )

    assert response_update.status_code == 403
    assert response_update.json()['error'] == 'permission_denied'