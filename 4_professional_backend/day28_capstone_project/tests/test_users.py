import pytest

@pytest.mark.anyio
async def test_protected_route(client):
    payload = {
        'email': 'test2@example.com',
        'password': '123456',
        'full_name': 'Test user2',
    }

    response = await client.post('/user/register', json=payload)
    assert response.status_code == 201

    response2 = await client.post('/token', data={'username': 'test2@example.com', 'password': '123456'})
    token = response2.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response3 = await client.get('/users/me', headers=headers)
    assert response3.status_code == 200
    data = response3.json()
    assert data['email'] == 'test2@example.com'
