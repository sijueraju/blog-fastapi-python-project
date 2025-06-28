
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database.models import *
from ..auth import authenticate_user, get_current_user,get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..database.database import get_db, EDITOR_ROLE

router = APIRouter()


@router.post("/post/create", tags=["blog"], response_model = PostResponse)
async def create_post(post: PostCreate, current_user: dict=Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts(title, content, author_id) VALUES(?,?,?)",
                       (post.title, post.content, current_user['id']))
        conn.commit()
        post_id = cursor.lastrowid
        cursor.execute("""
        SELECT p.*, u.username as author_username FROM posts p
        JOIN users u ON u.id = p.author_id
        ORDER BY p.created_at DESC """)
        new_post = dict(cursor.fetchone())
    return PostResponse(**new_post)

@router.get("/post/list", tags=["blog"], response_model = List[PostResponse])
async def get_posts():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT p.*, u.username as author_username FROM posts p
        JOIN users u ON p.author_id = u.id
        ORDER BY p.created_at DESC 
        """)
        posts = [dict(row) for row in cursor.fetchall()]
    return [PostResponse(**post) for post in posts]

@router.get("/post/my", tags=["blog"], response_model = List[PostResponse])
async def get_my_posts(current_user: dict=Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT p.*, u.username as author_username FROM posts p
                JOIN users u ON p.author_id = u.id
                WHERE p.author_id = ?
                ORDER BY p.created_at DESC 
                """,(current_user['id'],))
        posts = [dict(row) for row in cursor.fetchall()]
    return [PostResponse(**post) for post in posts]

@router.delete("/post/{post_id}", tags=["blog"])
async def delete_post(post_id:int, current_user: dict=Depends(get_current_user)):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT author_id FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code = 404, detail = "Post not found")
        if post['author_id'] != current_user['id']:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")

        cursor.execute("DELETE FROM posts where id = ?", (post_id,))
        conn.commit()
    return {"message": "Post deleted successfully"}







