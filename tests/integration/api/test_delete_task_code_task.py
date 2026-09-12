from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_ensure_task_not_in_course_structure_after_deleting(
        client,
        admin_auth_headers,
        seeded_tasks_tree
):
    response = await client.post(
        f'/api/admin/sections/{seeded_tasks_tree.section_id}/tasks',
        headers=admin_auth_headers,
        json={
              "title": "HTTP-метод для чтения",
              "statement": "Введите HTTP-метод, который обычно используют для чтения ресурса.",
              "position": 3,
              "check_type": "exact_match",
              "expected_answer": "GET",
              "accepted_answers": [],
              "answer_pattern": "",
              "max_attempts": 2,
              "reward_points": 3
        }
    )
    assert response.status_code == 201

    delete_response = await client.delete(
        f'/api/admin/tasks/{seeded_tasks_tree.task_id}',
        headers=admin_auth_headers,
    )

    assert delete_response.status_code == 204

    response_structure = await client.get(
        f'/api/courses/{seeded_tasks_tree.course_id}/structure',
    )

    section = response_structure.json()['modules'][0]['sections']

    assert seeded_tasks_tree.task_id not in section[0]['task_ids']
    assert all(item['id'] != seeded_tasks_tree.task_id for item in section[0]['tasks'])

@pytest.mark.asyncio
async def test_author_cannot_delete_task_with_code_submission(
        client,
        admin_auth_headers,
        seeded_code_submission,
        seeded_tasks_tree,
        student_auth_headers
):
    response = await client.delete(
        f'/api/admin/code-tasks/{seeded_tasks_tree.code_task_id}',
        headers=admin_auth_headers,
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'application_error'

    submission_response = await client.get(
        f'/api/learning/code-submissions/{seeded_code_submission.code_submission_id}',
        headers=student_auth_headers
    )

    submission_payload = submission_response.json()

    assert submission_response.status_code == 200
    assert submission_payload['id'] == seeded_code_submission.code_submission_id

@pytest.mark.asyncio
async def test_author_cannot_delete_test_case_when_its_single(
        client,
        seeded_tasks_tree,
        author_auth_headers,
):
    non_hidden_test_case = await client.post(
        f'/api/admin/code-tasks/{seeded_tasks_tree.code_task_id}/test-cases',
        headers=author_auth_headers,
        json={
            "position": 1,
            "input_data": "2 3",
            "expected_output": "5",
            "is_hidden": 'false',
            "explanation": "Базовый сценарий сложения двух положительных чисел."
        }
    )
    assert non_hidden_test_case.status_code == 201

    hidden_test_case = await client.post(
        f'/api/admin/code-tasks/{seeded_tasks_tree.code_task_id}/test-cases',
        headers=author_auth_headers,
        json={
            "position": 2,
            "input_data": "-4 7",
            "expected_output": "3",
            "is_hidden": "true",
            "explanation": "Проверяем, что решение корректно работает с отрицательными числами."
        }
    )
    non_hidden_test_case_id = non_hidden_test_case.json()['id']
    hidden_test_case_id = hidden_test_case.json()['id']

    assert hidden_test_case.status_code == 201

    delete_test_case = await client.delete(
        f'/api/admin/test-cases/{non_hidden_test_case_id}',
        headers=author_auth_headers,
    )
    assert delete_test_case.status_code == 204

    delete_second_test_case = await client.delete(
        f'/api/admin/test-cases/{hidden_test_case_id}',
        headers=author_auth_headers,
    )

    assert delete_second_test_case.status_code == 400
    assert delete_second_test_case.json()['error'] == 'domain_error'

@pytest.mark.asyncio
async def test_author_cannot_delete_test_case_when_it_has_submission(
        client,
        seeded_tasks_tree,
        author_auth_headers,
        seeded_code_submission,
):
    test_case = await client.post(
        f'/api/admin/code-tasks/{seeded_tasks_tree.code_task_id}/test-cases',
        headers=author_auth_headers,
        json={
            "position": 1,
            "input_data": "2 3",
            "expected_output": "5",
            "is_hidden": 'false',
            "explanation": "Базовый сценарий сложения двух положительных чисел."
        }
    )
    assert test_case.status_code == 201
    test_case_id = test_case.json()['id']

    delete_test_case = await client.delete(
        f'/api/admin/test-cases/{test_case_id}',
        headers=author_auth_headers,
    )

    assert delete_test_case.status_code == 400
    assert delete_test_case.json()['error'] == 'application_error'

@pytest.mark.asyncio
async def test_returns_404_when_code_task_is_missing(
        client,
        author_auth_headers,
):
    response = await client.delete(
        f'/api/admin/code-tasks/{uuid4()}',
        headers=author_auth_headers,
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_returns_404_when_test_case_is_missing(
        client,
        author_auth_headers,
):
    response = await client.delete(
        f'/api/admin/test-cases/{uuid4()}',
        headers=author_auth_headers,
    )

    assert response.status_code == 404