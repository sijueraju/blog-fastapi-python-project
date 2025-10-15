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

class PostCreate(BaseModel):
    title:str
    content:str

class PostUpdate(BaseModel):
    title:Optional[str] = None
    content:Optional[str] = None

class PostResponse(BaseModel):
    id :int
    title : str
    content: str
    author_id: int
    author_username : str
    created_at : str
    updated_at: str

class CommentCreate(BaseModel):
    content: str
    post_id: int

class CommentResponse(BaseModel):
    id : int
    content : str
    post_id : int
    author_id : int
    author_username: str
    created_at: str

class ContentGenerationRequest(BaseModel):
    topic: str
    tone: Optional[str] = "professional"
    max_words: Optional[int] = 20
    keywords: Optional[List[str]] = None

class ContentGenerationResponse(BaseModel):
    content: str
    tokens_used: int
    model: str