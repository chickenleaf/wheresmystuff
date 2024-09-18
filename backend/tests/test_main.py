# backend/tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Lost and Found Matcher API"}

def test_create_user():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"

# Add more tests for other endpoints