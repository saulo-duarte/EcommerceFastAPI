from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.session import get_async_db
from app.schema.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product import ProductService

router =  APIRouter(prefix="/product", tags=["product"])

@router.post("/", response_model=ProductRead)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_async_db),
):
    product_service = ProductService(db)
    try:
        product = await product_service.create_product(product_data)
        return product
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error on product creation")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[ProductRead])
async def list_products(db: AsyncSession = Depends(get_async_db)):
    product_service = ProductService(db)
    products = await product_service.list_products()
    return products

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_async_db)):
    product_service = ProductService(db)
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductRead.model_validate(product)