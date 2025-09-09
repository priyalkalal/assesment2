from fastapi import FastAPI, HTTPException
from .models import UserCreate, UserResponse
from . import crud

app = FastAPI()

@app.post("/user", response_model=UserResponse)
def create_user(user: UserCreate):
    user_dict = user.model_dump()
    user_id = crud.create_user(user_dict)
    return {"id": user_id, **user_dict}

@app.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    user = crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
