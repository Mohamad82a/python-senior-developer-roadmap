from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get('/ping')
def ping():
    return {'message': 'pong'}

client = TestClient(app)

def test_pint():
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'message': 'pong'}



