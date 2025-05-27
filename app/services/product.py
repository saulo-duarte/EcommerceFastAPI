from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.repository.product import ProductRepository
from app.repository.category import CategoryRepository
from app.schema.product import ProductCreate, ProductRead
from app.schema.category import CategoryCreate


class ProductService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        async with self.db.begin():
            category = await self._get_or_create_category(product_data.category_name)
            product = await self.product_repository.create_product(product_data, category.id)
            return ProductRead.model_validate(product)

    async def _get_or_create_category(self, category_name: str) -> Category:
        if not category_name or not category_name.strip():
            raise ValueError("Category name must not be empty")

        category = await self.category_repository.get_by_name(category_name)
        if category:
            return category

        category_create = CategoryCreate(name=category_name)
        try:
            category = await self.category_repository.create_category(category_create)
        except IntegrityError:
            category = await self.category_repository.get_by_name(category_name)
            if category is None:
                raise
        return category

