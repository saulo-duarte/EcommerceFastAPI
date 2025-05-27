from fastapi import FastAPI

from app.routes.v1 import auth, user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)
app.include_router(auth.router)
