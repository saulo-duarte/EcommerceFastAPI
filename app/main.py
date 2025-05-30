from fastapi import FastAPI

from app.configs.logging_middleware import LoggingMiddleware
from app.routes.v1 import auth, category, product, review, user

app = FastAPI()

app.add_middleware(LoggingMiddleware)

routers = [user.router, auth.router, category.router, product.router, review.router]

for r in routers:
    app.include_router(r)


@app.get("/")
async def root():
    return {"message": "Hello World"}
