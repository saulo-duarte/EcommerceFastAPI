from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schema.user import UserCreate, UserRead, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


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


@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_async_db)):
    user_service = UserService(db)
    users = await user_service.list_users()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_async_db)):
    service = UserService(db)
    user = await service.get_user_by_id(user_id)
    return UserRead.model_validate(user)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    user_service = UserService(db)
    try:
        updated_user = await user_service.update_user(user_id, user_data)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    user_service = UserService(db)
    try:
        await user_service.delete_user(user_id)
        return {"detail": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
