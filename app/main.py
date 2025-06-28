from typing import Union

from fastapi import FastAPI

from .routers import user, blog

app = FastAPI()

app.include_router(user.router)
app.include_router(blog.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


