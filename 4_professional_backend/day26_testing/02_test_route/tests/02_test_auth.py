from fastapi.testclient import TestClient
from app3.main import app

client = TestClient(app)

def test_login_and_token():
    data = {'username': 'admin@example.com', 'password': '123456'}
    response = client.post('/token', data=data)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'