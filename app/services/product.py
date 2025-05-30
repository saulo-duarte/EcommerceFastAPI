from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.category import CategoryRepository
from app.repository.product import ProductRepository
from app.schema.product import ProductCreate, ProductRead, ProductUpdate


class ProductService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        category = await self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise ValueError("Category not found")

        try:
            new_product = await self.product_repository.create_product(
                product_data, category.id
            )
            await self.db.commit()
            await self.db.refresh(new_product)

            return ProductRead.model_validate(new_product, from_attributes=True)

        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Product creation failed due to integrity error") from e

    async def get_product_by_id(self, product_id: UUID) -> ProductRead:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return ProductRead.model_validate(product, from_attributes=True)

    async def list_products(self) -> list[ProductRead]:
        products = await self.product_repository.list_products()
        return [
            ProductRead.model_validate(product, from_attributes=True)
            for product in products
        ]

    async def update_product(
        self, product_id: UUID, product_data: ProductUpdate
    ) -> ProductRead:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        updated_product = await self.product_repository.update(product, product_data)
        return ProductRead.model_validate(updated_product, from_attributes=True)

    async def delete_product(self, product_id: UUID) -> None:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        await self.product_repository.delete(product)
        await self.db.commit()
        return {"detail": "Product deleted successfully"}
