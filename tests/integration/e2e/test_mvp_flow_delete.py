import pytest

@pytest.mark.asyncio
async def test_mvp_flow_from_deleting_to_public_read(client, seeded_admin_user):
    login_response = await client.post(
        '/api/auth/login',
        json={
            'email': 'admin@example.com',
            'password': 'strongpassword123',
        }
    )

    assert login_response.status_code == 200
    access_token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    course_response = await client.post(
        '/api/admin/courses',
        headers=headers,
        json={
            'title': 'New course title',
            'description': 'New course description',
        }
    )

    assert course_response.status_code == 201
    course_id = course_response.json()['id']

    module_response = await client.post(
        f'/api/admin/courses/{course_id}/modules',
        headers=headers,
        json={
            'title': 'New module',
            'description': 'New description',
            'position': 1
        }
    )

    assert module_response.status_code == 201
    module_id = module_response.json()['id']

    section_response = await client.post(
        f'/api/admin/modules/{module_id}/sections',
        headers=headers,
        json={
            'title': 'Auth section',
            'description': 'JWT and route protection.',
            'position': 1,
        },
    )
    assert section_response.status_code == 201
    section_id = section_response.json()['id']

    lecture_response = await client.post(
        f'/api/admin/sections/{section_id}/lectures',
        headers=headers,
        json={
            'title': 'Bearer token in practice',
            'content': 'Lecture content',
            'position': 1,
        },
    )
    assert lecture_response.status_code == 201
    lecture_id = lecture_response.json()['id']

    delete_module_response = await client.delete(
        f'/api/admin/modules/{module_id}',
        headers=headers,
    )

    assert delete_module_response.status_code == 204

    course_structure_response = await client.get(
        f'/api/courses/{course_id}/structure',
    )

    assert course_structure_response.status_code == 200
    payload = course_structure_response.json()

    assert payload['title'] == 'New course title'
    assert payload['description'] == 'New course description'
    assert len(payload['modules']) == 0
    assert 'sections' not in payload
    assert 'lectures' not in payload

    deleted_lecture_response = await client.get(
        f'/api/lectures/{lecture_id}',
    )
    assert deleted_lecture_response.status_code == 404