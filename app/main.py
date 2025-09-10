from fastapi import FastAPI, HTTPException
from models import UserCreate, UserResponse
import crud

app = FastAPI(title="FastAPI MongoDB App", version="1.0.0")

@app.get("/")
def root():
    """Root endpoint for health check"""
    return {"message": "FastAPI MongoDB App is running!"}

@app.post("/user", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user"""
    user_dict = user.model_dump()
    user_id = crud.create_user(user_dict)
    return {"id": user_id, **user_dict}

@app.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Get a user by ID"""
    user = crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user