from fastapi import FastAPI

from app.routes.v1 import auth, category, product, user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(product.router)
