import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Import after path modification
import main

client = TestClient(main.app)

# Mock data
test_user = {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
}

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@patch('main.crud.users_collection')
def test_create_user(mock_collection):
    """Test user creation"""
    # Mock the MongoDB insert
    mock_result = MagicMock()
    mock_result.inserted_id = "507f1f77bcf86cd799439011"
    mock_collection.insert_one.return_value = mock_result
    
    response = client.post("/user", json=test_user)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user["name"]
    assert data["email"] == test_user["email"]
    assert data["role"] == test_user["role"]
    assert "id" in data

@patch('main.crud.users_collection')
def test_get_user_found(mock_collection):
    """Test user retrieval"""
    user_id = "507f1f77bcf86cd799439011"
    mock_user = {
        "_id": user_id,
        "name": "John Doe",
        "email": "john@example.com", 
        "role": "admin"
    }
    mock_collection.find_one.return_value = mock_user
    
    response = client.get(f"/user/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"

@patch('main.crud.users_collection')
def test_get_user_not_found(mock_collection):
    """Test user not found"""
    mock_collection.find_one.return_value = None
    
    response = client.get("/user/nonexistent")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user_invalid_email():
    """Test invalid email validation"""
    invalid_user = {
        "name": "John Doe",
        "email": "invalid-email",
        "role": "admin"
    }
    
    response = client.post("/user", json=invalid_user)
    assert response.status_code == 422