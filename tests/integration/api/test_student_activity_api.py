from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.infrastructure.database.models import StudentActivityModel

MY_ACTIVITIES_URL = '/api/profile/me/activities'
ADMIN_ACTIVITIES_URL = '/api/admin/activities'


async def seed_activity(
        session_factory,
        student_id: str,
        course_id: str,
        activity_type: str = 'question_completed',
        title: str = 'Seeded activity',
        occurred_at: datetime | None = None,
) -> str:
    activity_id = str(uuid4())
    async with session_factory() as session:
        session.add(
            StudentActivityModel(
                id=activity_id,
                student_id=student_id,
                course_id=course_id,
                activity_type=activity_type,
                entity_id=str(uuid4()),
                title=title,
                details={},
                occurred_at=occurred_at or datetime.now(UTC),
            )
        )
        await session.commit()
    return activity_id


@pytest.mark.asyncio
async def test_correct_question_answer_appears_in_my_activities(
        client,
        student_auth_headers,
        seeded_interactive_tree,
):
    answer_response = await client.post(
        f'/api/learning/questions/{seeded_interactive_tree.question_id}/attempts',
        headers=student_auth_headers,
        json={'selected_option_ids': [seeded_interactive_tree.correct_option_id]},
    )
    assert answer_response.status_code == 201

    response = await client.get(MY_ACTIVITIES_URL, headers=student_auth_headers)

    assert response.status_code == 200
    question_activities = [
        item for item in response.json()['items']
        if item['activity_type'] == 'question_completed'
    ]
    assert len(question_activities) == 1
    assert question_activities[0]['entity_id'] == seeded_interactive_tree.question_id
    assert question_activities[0]['course_id'] == seeded_interactive_tree.course_id
    assert question_activities[0]['details']['awarded_points'] == 5


@pytest.mark.asyncio
async def test_wrong_question_answer_does_not_create_activity(
        client,
        student_auth_headers,
        seeded_interactive_tree,
):
    answer_response = await client.post(
        f'/api/learning/questions/{seeded_interactive_tree.question_id}/attempts',
        headers=student_auth_headers,
        json={'selected_option_ids': [seeded_interactive_tree.wrong_option_id]},
    )
    assert answer_response.status_code == 201

    response = await client.get(MY_ACTIVITIES_URL, headers=student_auth_headers)

    assert response.status_code == 200
    assert response.json()['items'] == []
    assert response.json()['total'] == 0


@pytest.mark.asyncio
async def test_my_activities_contain_only_current_user_activities(
        client,
        session_factory,
        student_auth_headers,
        seeded_student_user,
        seeded_other_student_user,
        seeded_course_tree,
):
    own_id = await seed_activity(session_factory, seeded_student_user.id, seeded_course_tree.course_id)
    await seed_activity(session_factory, seeded_other_student_user.id, seeded_course_tree.course_id)

    response = await client.get(MY_ACTIVITIES_URL, headers=student_auth_headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload['total'] == 1
    assert [item['id'] for item in payload['items']] == [own_id]
    assert payload['items'][0]['student_id'] == seeded_student_user.id


@pytest.mark.asyncio
async def test_my_activities_ignore_student_id_query_parameter(
        client,
        session_factory,
        student_auth_headers,
        seeded_student_user,
        seeded_other_student_user,
        seeded_course_tree,
):
    await seed_activity(session_factory, seeded_other_student_user.id, seeded_course_tree.course_id)

    response = await client.get(
        MY_ACTIVITIES_URL,
        headers=student_auth_headers,
        params={'student_id': seeded_other_student_user.id},
    )

    assert response.status_code == 200
    assert response.json()['total'] == 0
    assert response.json()['items'] == []


@pytest.mark.asyncio
async def test_my_activities_are_paginated_newest_first(
        client,
        session_factory,
        student_auth_headers,
        seeded_student_user,
        seeded_course_tree,
):
    now = datetime.now(UTC)
    oldest = await seed_activity(
        session_factory, seeded_student_user.id, seeded_course_tree.course_id,
        title='oldest', occurred_at=now - timedelta(minutes=2),
    )
    middle = await seed_activity(
        session_factory, seeded_student_user.id, seeded_course_tree.course_id,
        title='middle', occurred_at=now - timedelta(minutes=1),
    )
    newest = await seed_activity(
        session_factory, seeded_student_user.id, seeded_course_tree.course_id,
        title='newest', occurred_at=now,
    )

    first_page = await client.get(
        MY_ACTIVITIES_URL,
        headers=student_auth_headers,
        params={'limit': 2, 'offset': 0},
    )
    second_page = await client.get(
        MY_ACTIVITIES_URL,
        headers=student_auth_headers,
        params={'limit': 2, 'offset': 2},
    )

    assert first_page.status_code == 200
    assert second_page.status_code == 200
    first_payload = first_page.json()
    second_payload = second_page.json()
    assert first_payload['total'] == 3
    assert first_payload['limit'] == 2
    assert first_payload['offset'] == 0
    assert [item['id'] for item in first_payload['items']] == [newest, middle]
    assert second_payload['total'] == 3
    assert [item['id'] for item in second_payload['items']] == [oldest]


@pytest.mark.asyncio
async def test_my_activities_require_authentication(client):
    response = await client.get(MY_ACTIVITIES_URL)

    assert response.status_code == 401
    assert response.json()['error'] == 'authentication_error'


@pytest.mark.asyncio
@pytest.mark.parametrize('params', [{'limit': 0}, {'limit': 101}, {'offset': -1}])
async def test_my_activities_reject_invalid_pagination(client, student_auth_headers, params):
    response = await client.get(MY_ACTIVITIES_URL, headers=student_auth_headers, params=params)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_admin_sees_activities_of_all_students(
        client,
        session_factory,
        admin_auth_headers,
        seeded_student_user,
        seeded_other_student_user,
        seeded_course_tree,
):
    first = await seed_activity(session_factory, seeded_student_user.id, seeded_course_tree.course_id)
    second = await seed_activity(session_factory, seeded_other_student_user.id, seeded_course_tree.course_id)

    response = await client.get(ADMIN_ACTIVITIES_URL, headers=admin_auth_headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload['total'] == 2
    assert {item['id'] for item in payload['items']} == {first, second}


@pytest.mark.asyncio
async def test_admin_can_filter_activities_by_student(
        client,
        session_factory,
        admin_auth_headers,
        seeded_student_user,
        seeded_other_student_user,
        seeded_course_tree,
):
    own_id = await seed_activity(session_factory, seeded_student_user.id, seeded_course_tree.course_id)
    await seed_activity(session_factory, seeded_other_student_user.id, seeded_course_tree.course_id)

    response = await client.get(
        ADMIN_ACTIVITIES_URL,
        headers=admin_auth_headers,
        params={'student_id': seeded_student_user.id},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['total'] == 1
    assert [item['id'] for item in payload['items']] == [own_id]


@pytest.mark.asyncio
async def test_admin_can_filter_activities_by_course(
        client,
        session_factory,
        admin_auth_headers,
        seeded_student_user,
        seeded_course_tree,
        seeded_author_course_tree,
):
    target_id = await seed_activity(session_factory, seeded_student_user.id, seeded_course_tree.course_id)
    await seed_activity(session_factory, seeded_student_user.id, seeded_author_course_tree.course_id)

    response = await client.get(
        ADMIN_ACTIVITIES_URL,
        headers=admin_auth_headers,
        params={'course_id': seeded_course_tree.course_id},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['total'] == 1
    assert [item['id'] for item in payload['items']] == [target_id]


@pytest.mark.asyncio
async def test_admin_can_filter_activities_by_type(
        client,
        session_factory,
        admin_auth_headers,
        seeded_student_user,
        seeded_course_tree,
):
    await seed_activity(
        session_factory, seeded_student_user.id, seeded_course_tree.course_id,
        activity_type='question_completed',
    )
    section_id = await seed_activity(
        session_factory, seeded_student_user.id, seeded_course_tree.course_id,
        activity_type='section_completed',
    )

    response = await client.get(
        ADMIN_ACTIVITIES_URL,
        headers=admin_auth_headers,
        params={'activity_type': 'section_completed'},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['total'] == 1
    assert [item['id'] for item in payload['items']] == [section_id]


@pytest.mark.asyncio
async def test_admin_activities_reject_unknown_activity_type(client, admin_auth_headers):
    response = await client.get(
        ADMIN_ACTIVITIES_URL,
        headers=admin_auth_headers,
        params={'activity_type': 'unknown_type'},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_student_cannot_view_admin_activities(client, student_auth_headers):
    response = await client.get(ADMIN_ACTIVITIES_URL, headers=student_auth_headers)

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_author_cannot_view_admin_activities(client, author_auth_headers):
    response = await client.get(ADMIN_ACTIVITIES_URL, headers=author_auth_headers)

    assert response.status_code == 403
    assert response.json()['error'] == 'permission_denied'


@pytest.mark.asyncio
async def test_admin_activities_require_authentication(client):
    response = await client.get(ADMIN_ACTIVITIES_URL)

    assert response.status_code == 401
    assert response.json()['error'] == 'authentication_error'
