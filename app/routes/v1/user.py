from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schema.user import UserCreate, UserRead
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        user_service = UserService(db)
        user = await user_service.create_user_with_addresses(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
