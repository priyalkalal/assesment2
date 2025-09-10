import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import your app
from main import app

client = TestClient(app)

# Test data
test_user = {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@patch('crud.users_collection')
def test_create_user_success(mock_collection):
    """Test successful user creation"""
    # Mock MongoDB insert result
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

@patch('crud.users_collection')
def test_get_user_found(mock_collection):
    """Test successful user retrieval"""
    user_id = "507f1f77bcf86cd799439011"
    mock_user = {
        "_id": user_id,
        "name": "Jane Smith",
        "email": "jane@example.com",
        "role": "user"
    }
    mock_collection.find_one.return_value = mock_user
    
    response = client.get(f"/user/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Jane Smith"

@patch('crud.users_collection')
def test_get_user_not_found(mock_collection):
    """Test user not found scenario"""
    mock_collection.find_one.return_value = None
    
    response = client.get("/user/nonexistent")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user_invalid_email():
    """Test user creation with invalid email"""
    invalid_user = {
        "name": "John Doe",
        "email": "not-an-email",
        "role": "admin"
    }
    
    response = client.post("/user", json=invalid_user)
    assert response.status_code == 422

def test_create_user_missing_fields():
    """Test user creation with missing fields"""
    incomplete_user = {
        "name": "John Doe"
        # Missing email and role
    }
    
    response = client.post("/user", json=incomplete_user)
    assert response.status_code == 422