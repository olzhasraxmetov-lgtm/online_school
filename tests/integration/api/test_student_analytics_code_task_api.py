import pytest

@pytest.mark.asyncio
async def test_student_analytics_returns_empty_weak_code_task_for_not_started_course(
        client,
        student_auth_headers,
        seeded_tasks_tree,
):
    response = await client.get(
        f'/api/profile/me/courses/{seeded_tasks_tree.course_id}/analytics',
        headers=student_auth_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['weak_code_tasks'] == []

@pytest.mark.asyncio
async def test_student_analytics_excludes_code_task_passed_on_first_attempt(
        client,
        student_auth_headers,
        seeded_tasks_tree,
        seeded_student_user,
        create_code_submission
):
    await create_code_submission(
        student_id=seeded_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='passed',
    )

    response = await client.get(
        f'/api/profile/me/courses/{seeded_tasks_tree.course_id}/analytics',
        headers=student_auth_headers,
    )
    assert response.status_code == 200
    assert response.json()['weak_code_tasks'] == []

@pytest.mark.asyncio
async def test_student_analytics_includes_weak_code_task_on_first_failed_attempt(
        client,
        student_auth_headers,
        seeded_tasks_tree,
        seeded_student_user,
        create_code_submission
):
    await create_code_submission(
        student_id=seeded_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='failed',
    )

    response = await client.get(
        f'/api/profile/me/courses/{seeded_tasks_tree.course_id}/analytics',
        headers=student_auth_headers,
    )
    assert response.status_code == 200
    payload = response.json()

    weak_code_tasks = payload['weak_code_tasks']
    assert len(weak_code_tasks) == 1
    assert weak_code_tasks[0]['section_id'] == seeded_tasks_tree.section_id
    assert weak_code_tasks[0]['code_task_id'] == seeded_tasks_tree.code_task_id
    assert weak_code_tasks[0]['attempts_count'] == 1
    assert weak_code_tasks[0]['failed_attempts_count'] == 1
    assert weak_code_tasks[0]['timed_out_attempts_count'] == 0

@pytest.mark.asyncio
async def test_student_analytics_includes_weak_code_task_on_first_error_attempt(
        client,
        student_auth_headers,
        seeded_tasks_tree,
        seeded_student_user,
        create_code_submission
):
    await create_code_submission(
        student_id=seeded_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='error',
    )

    response = await client.get(
        f'/api/profile/me/courses/{seeded_tasks_tree.course_id}/analytics',
        headers=student_auth_headers,
    )
    assert response.status_code == 200
    payload = response.json()
    weak_code_tasks = payload['weak_code_tasks']
    assert len(weak_code_tasks) == 1
    assert weak_code_tasks[0]['section_id'] == seeded_tasks_tree.section_id
    assert weak_code_tasks[0]['code_task_id'] == seeded_tasks_tree.code_task_id
    assert weak_code_tasks[0]['attempts_count'] == 1
    assert weak_code_tasks[0]['failed_attempts_count'] == 0
    assert weak_code_tasks[0]['timed_out_attempts_count'] == 1

@pytest.mark.asyncio
async def test_student_analytics_includes_weak_code_task_after_retry(
        client,
        student_auth_headers,
        seeded_tasks_tree,
        seeded_student_user,
        create_code_submission
):
    await create_code_submission(
        student_id=seeded_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='failed',
        attempt_number=1
    )

    await create_code_submission(
        student_id=seeded_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='passed',
        attempt_number=2
    )

    response = await client.get(
        f'/api/profile/me/courses/{seeded_tasks_tree.course_id}/analytics',
        headers=student_auth_headers,
    )
    assert response.status_code == 200
    payload = response.json()
    weak_code_tasks = payload['weak_code_tasks']
    assert len(weak_code_tasks) == 1
    assert weak_code_tasks[0]['section_id'] == seeded_tasks_tree.section_id
    assert weak_code_tasks[0]['code_task_id'] == seeded_tasks_tree.code_task_id
    assert weak_code_tasks[0]['attempts_count'] == 2
    assert weak_code_tasks[0]['failed_attempts_count'] == 1
    assert weak_code_tasks[0]['timed_out_attempts_count'] == 0


@pytest.mark.asyncio
async def test_student_analytics_excludes_other_student_code_submission(
        client,
        student_auth_headers,
        seeded_tasks_tree,
        seeded_student_user,
        seeded_other_student_user,
        create_code_submission
):
    await create_code_submission(
        student_id=seeded_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='passed',
        attempt_number=1
    )

    await create_code_submission(
        student_id=seeded_other_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='failed',
        attempt_number=1
    )

    await create_code_submission(
        student_id=seeded_other_student_user.id,
        code_task_id=seeded_tasks_tree.code_task_id,
        status='failed',
        attempt_number=2
    )

    response = await client.get(
        f'/api/profile/me/courses/{seeded_tasks_tree.course_id}/analytics',
        headers=student_auth_headers,
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['weak_code_tasks'] == []