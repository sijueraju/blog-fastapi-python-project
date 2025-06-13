from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str
