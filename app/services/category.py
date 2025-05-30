from typing import List
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.category import CategoryRepository
from app.schema.category import CategoryCreate, CategoryRead, CategoryUpdate


class CategoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    async def create_category(self, category_data: CategoryCreate) -> CategoryRead:
        try:
            new_category = await self.category_repository.create_category(category_data)
            await self.db.commit()
            await self.db.refresh(new_category)

            return CategoryRead.model_validate(new_category, from_attributes=True)

        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Category creation failed due to integrity error") from e

    async def get_category_by_id(self, category_id: UUID) -> CategoryRead:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        return CategoryRead.model_validate(category, from_attributes=True)

    async def list_categories(self) -> List[CategoryRead]:
        categories = await self.category_repository.list_categories()
        return [
            CategoryRead.model_validate(category, from_attributes=True)
            for category in categories
        ]

    async def update_category(
        self, category_id: UUID, category_data: CategoryUpdate
    ) -> CategoryRead:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        updated_category = await self.category_repository.update(
            category, category_data
        )
        return CategoryRead.model_validate(updated_category, from_attributes=True)

    async def delete_category(self, category_id: UUID) -> None:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        await self.category_repository.delete(category)
        await self.db.commit()
        return {"detail": "Category deleted successfully"}
