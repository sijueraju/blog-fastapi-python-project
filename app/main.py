from typing import Union

from fastapi import FastAPI

from .routers import user

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}



#
