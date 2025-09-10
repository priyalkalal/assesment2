# tests/test_main.py
import sys
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

# Mock data
test_user = {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
}

@pytest.fixture
def mock_mongo():
    with patch('crud.users_collection') as mock_collection:
        yield mock_collection

def test_create_user(mock_mongo):
    # Mock the insert_one method
    mock_result = MagicMock()
    mock_result.inserted_id = "507f1f77bcf86cd799439011"
    mock_mongo.insert_one.return_value = mock_result
    
    response = client.post("/user", json=test_user)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user["name"]
    assert data["email"] == test_user["email"]
    assert data["role"] == test_user["role"]
    assert "id" in data

def test_get_user_found(mock_mongo):
    # Mock the find_one method
    user_id = "507f1f77bcf86cd799439011"
    mock_user = {
        "_id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "role": "admin"
    }
    mock_mongo.find_one.return_value = mock_user
    
    response = client.get(f"/user/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "John Doe"

def test_get_user_not_found(mock_mongo):
    # Mock the find_one method to return None
    mock_mongo.find_one.return_value = None
    
    response = client.get("/user/nonexistent")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user_invalid_email():
    invalid_user = {
        "name": "John Doe",
        "email": "invalid-email",
        "role": "admin"
    }
    
    response = client.post("/user", json=invalid_user)
    assert response.status_code == 422

def test_create_user_short_name():
    invalid_user = {
        "name": "J",  # Too short
        "email": "john@example.com",
        "role": "admin"
    }
    
    response = client.post("/user", json=invalid_user)
    assert response.status_code == 422