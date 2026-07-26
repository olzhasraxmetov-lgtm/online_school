import pytest

@pytest.mark.asyncio
async def test_register_creates_student_user(client):
    response = await client.post(
        f'/api/auth/register',
        json={
            'email': 'student@example.com',
            'password': 'password123',
        }
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['email'] == 'student@example.com'
    assert payload['role'] == 'student'

@pytest.mark.asyncio
async def test_register_returns_400_when_user_already_registered(client):
    await client.post(
        f'/api/auth/register',
        json={
            'email': 'student@example.com',
            'password': 'password123',
        }
    )

    response = await client.post(
        f'/api/auth/register',
        json={
            'email': 'student@example.com',
            'password': 'newpassword123',
        }
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload['error'] == 'application_error'

@pytest.mark.asyncio
async def test_login_returns_access_token(client, seeded_student_user):
    response = await client.post(
        f'/api/auth/login',
        json={
            'email': 'student@example.com',
            'password': 'new_password1234',
        }
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['token_type'] == 'bearer'
    assert 'access_token' in payload

@pytest.mark.asyncio
async def test_login_returns_400_for_invalid_credentials(client):
    response = await client.post(
        f'/api/auth/login',
        json={
            'email': 'someoneelse@example.com',
            'password': 'wrong_123',
        }
    )
    assert response.status_code == 400
    payload = response.json()
    assert payload['error'] == 'application_error'

@pytest.mark.asyncio
async def test_auth_me_returns_current_user(client, student_auth_headers):
    response = await client.get(f'/api/auth/me', headers=student_auth_headers)
    assert response.status_code == 200
    payload = response.json()
    assert payload['email'] == 'student@example.com'
    assert payload['role'] == 'student'

@pytest.mark.asyncio
async def test_admin_route_returns_401_without_token(client):
    response = await client.post(
        f'/api/admin/courses',
        json={
            'title': 'New course title',
            'description': 'New course description',
        }
    )
    assert response.status_code == 401
    payload = response.json()
    assert payload['error'] == 'authentication_error'

@pytest.mark.asyncio
async def test_admin_route_returns_403_for_student(client, student_auth_headers):
    response = await client.post(
        '/api/admin/courses',
        headers=student_auth_headers,
        json={
            'title': 'New course title',
            'description': 'New course description',
        }
    )

    assert response.status_code == 403
    payload = response.json()
    assert payload['error'] == 'permission_denied'

@pytest.mark.asyncio
async def test_admin_route_allows_admin_user(client, admin_auth_headers):
    response = await client.post(
        '/api/admin/courses',
        headers=admin_auth_headers,
        json={
            'title': 'New course title',
            'description': 'New course description',
        }
    )

    assert response.status_code == 201
