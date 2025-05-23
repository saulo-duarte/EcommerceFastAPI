from fastapi import FastAPI

from app.routes.v1 import user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)
