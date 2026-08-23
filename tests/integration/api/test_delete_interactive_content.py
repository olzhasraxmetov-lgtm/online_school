from uuid import uuid4

import pytest

from tests.conftest import student_auth_headers


@pytest.mark.asyncio
async def tests_returns_404_when_question_is_missing(client, author_auth_headers):
    delete_question_response = await client.delete(
        f'/api/admin/questions/{uuid4()}',
        headers=author_auth_headers,
    )

    assert delete_question_response.status_code == 404
    assert delete_question_response.json()['message'] == 'Question not found.'

@pytest.mark.asyncio
async def tests_returns_404_when_answer_option_is_missing(client, author_auth_headers):
    delete_question_response = await client.delete(
        f'/api/admin/answer-options/{uuid4()}',
        headers=author_auth_headers,
    )

    assert delete_question_response.status_code == 404
    assert delete_question_response.json()['message'] == 'Answer option not found.'

@pytest.mark.asyncio
async def test_delete_answer_option_returns_400_when_question_has_ony_one_option(
    client,
    author_auth_headers,
    seeded_interactive_tree,
):
    response = await client.delete(
        f"/api/admin/answer-options/{seeded_interactive_tree.wrong_option_id}",
        headers=author_auth_headers,
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload['error'] == 'domain_error'

@pytest.mark.asyncio
async def test_delete_answer_option_returns_400_when_question_has_only_wrong_options(
    client,
    author_auth_headers,
    seeded_interactive_tree,
):
    await client.post(
        f'/api/admin/questions/{seeded_interactive_tree.question_id}/answers-options',
        headers=author_auth_headers,
        json={'text': 'POST', 'position': 1, 'is_correct': False},
    )
    delete_correct_option_response = await client.delete(
        f"/api/admin/answer-options/{seeded_interactive_tree.correct_option_id}",
        headers=author_auth_headers,
    )
    assert delete_correct_option_response.status_code == 400
    assert delete_correct_option_response.json()['error'] == 'domain_error'


@pytest.mark.asyncio
async def test_delete_answer_option_and_question_from_structure(
        client,
        seeded_author_user,
        author_auth_headers,
        student_auth_headers,
        seeded_interactive_tree
):
    await client.post(
        f'/api/admin/questions/{seeded_interactive_tree.question_id}/answers-options',
        headers=author_auth_headers,
        json={'text': 'POST', 'position': 1, 'is_correct': False},
    )

    delete_option_response = await client.delete(
        f'/api/admin/answer-options/{seeded_interactive_tree.wrong_option_id}',
        headers=author_auth_headers,
    )

    assert delete_option_response.status_code == 204

    get_question_response = await client.get(
        f'/api/learning/questions/{seeded_interactive_tree.question_id}/attempt',
        headers=student_auth_headers,
    )
    question_response_data = get_question_response.json()
    assert len(question_response_data['answer_options']) == 2
    assert question_response_data['question_id'] is not None

    delete_question_response = await client.delete(
        f'/api/admin/questions/{seeded_interactive_tree.question_id}',
        headers=author_auth_headers,
    )

    assert delete_question_response.status_code == 204
    section_response = await client.get(
        f'/api/courses/{seeded_interactive_tree.course_id}/structure',
    )
    section_response_data = section_response.json()
    question_ids = section_response_data['modules'][0]['sections'][0]['question_ids']
    assert len(question_ids) == 0

@pytest.mark.asyncio
async def test_author_cannot_delete_answer_option_and_question_when_it_has_student_attempts(
        client,
        seeded_author_user,
        author_auth_headers,
        student_auth_headers,
        seeded_interactive_tree
):
    start_response = await client.get(
        f'/api/learning/questions/{seeded_interactive_tree.question_id}/attempt',
        headers=student_auth_headers,
    )

    assert start_response.status_code == 200

    submit_response = await client.post(
        f'/api/learning/questions/{seeded_interactive_tree.question_id}/attempts',
        headers=student_auth_headers,
        json={'selected_option_ids': [seeded_interactive_tree.correct_option_id]},
    )

    assert submit_response.status_code == 201

    delete_option_response = await client.delete(
        f'/api/admin/questions/{seeded_interactive_tree.question_id}',
        headers=author_auth_headers
    )
    assert delete_option_response.status_code == 400
    assert delete_option_response.json()['error'] == 'application_error'