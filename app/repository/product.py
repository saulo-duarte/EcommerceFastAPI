from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Product
from app.schema.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(
        self, product_data: ProductCreate, category_id: UUID
    ) -> Product:
        db_product = Product(
            name=product_data.name,
            description=product_data.description,
            stock=product_data.stock,
            price=product_data.price,
            category_id=category_id,
        )
        self.db.add(db_product)
        await self.db.flush()

        return db_product

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        stmt = (
            select(Product)
            .options(selectinload(Product.category))
            .filter(Product.id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Product]:
        stmt = select(Product).filter(Product.name == name)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update(self, product: Product, updates: ProductUpdate) -> Product:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.db.delete(product)
        await self.db.commit()

    async def list_products(self) -> list[Product]:
        stmt = select(Product).options(selectinload(Product.category))
        result = await self.db.execute(stmt)
        return result.scalars().all()
