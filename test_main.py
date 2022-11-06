from fastapi.testclient import TestClient

from src.main import app
from src.auth import AuthHandler

client = TestClient(app)

def test_unprotected():
    response = client.get("/unprotected")
    assert response.status_code == 200
    assert response.json() == { 'hello': 'world' }

def test_auth():
    temp_token = AuthHandler().encode_token("test")
    response = client.get("/protected",headers={f"Authorization": "Bearer {}".format(temp_token)})
    assert response.status_code == 200
    

def test_read_main():
    response = client.post("/login",json={"username": "test", "password": "test"})
    assert response.status_code == 200

test_auth()