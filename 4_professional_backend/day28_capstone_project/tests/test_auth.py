import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_register_and_login(client: AsyncClient):
    # register
    payload = {
        'email': 'test@example.com',
        'password': '123456',
        'full_name': 'Test user'
    }
    response = await client.post('/user/register', json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == 'test@example.com'


    # login
    response2 = await client.post('/token', data={'username': 'test@example.com', 'password': '123456'})
    assert response2.status_code == 200
    token_data = response2.json()
    assert 'access_token' in token_data
