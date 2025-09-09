import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/user", json={"name": "Alice", "email": "alice@example.com", "role": "admin"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Alice"

def test_get_user_not_found():
    response = client.get("/user/64b9f2e8f8a4a9e6d2a00000")
    assert response.status_code == 404
