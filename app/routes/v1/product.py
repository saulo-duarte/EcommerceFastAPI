from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schema.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/", response_model=ProductRead)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        product_service = ProductService(db)
        product = await product_service.create_product(product_data)
        return product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProductRead])
async def list_products(db: AsyncSession = Depends(get_async_db)):
    product_service = ProductService(db)
    products = await product_service.list_products()
    return products

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        product_service = ProductService(db)
        product = await product_service.get_product_by_id(product_id)
        return product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        product_service = ProductService(db)
        updated_product = await product_service.update_product(product_id, product_data)
        return updated_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        product_service = ProductService(db)
        await product_service.delete_product(product_id)
        return {"detail": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
