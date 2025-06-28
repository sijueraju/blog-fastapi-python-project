from collections import UserString
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database.models import *
from ..auth import authenticate_user, get_current_user,get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..database.database import get_db, EDITOR_ROLE

router = APIRouter()


@router.post("/user/register", tags=["user"])
async def user_rgister(user: UserCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id from users WHERE username = ? OR email = ?", (user.username, user.email))
        if cursor.fetchone():
            raise HTTPException(status_code = 400, detail = "Username or email already exists")
        password = get_password_hash(user.password)
        cursor.execute("INSERT INTO users (username, email, password, name, role) VALUES(?,?,?,?,?)",(user.username, user.email, password, user.name, EDITOR_ROLE))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
        new_user = dict(cursor.fetchone())

    return UserResponse(**new_user)


@router.post("/user/login", tags=["user"])
async def user_login(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid username or password", headers={"WWW-Authenticate": "Bearer"},)
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
