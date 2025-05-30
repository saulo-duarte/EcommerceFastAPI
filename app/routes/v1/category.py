from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schema.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category import CategoryService

router = APIRouter(prefix="/category", tags=["category"])


@router.post("/", response_model=CategoryRead)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        category_service = CategoryService(db)
        category = await category_service.create_category(category_data)
        return category
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_async_db)):
    category_service = CategoryService(db)
    categories = await category_service.list_categories()
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: str,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        category_service = CategoryService(db)
        category = await category_service.get_category_by_id(category_id)
        return category
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        category_service = CategoryService(db)
        updated_category = await category_service.update_category(
            category_id, category_data
        )
        return updated_category
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{category_id}")
async def delete_category(
    category_id: str,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        category_service = CategoryService(db)
        await category_service.delete_category(category_id)
        return {"detail": "Category deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
