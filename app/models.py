from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    role: str = Field(..., min_length=2, max_length=20)

class UserResponse(UserCreate):
    id: str
