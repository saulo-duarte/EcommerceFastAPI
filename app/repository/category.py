from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.category import Category
from app.schema.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_category(self, category_data: CategoryCreate) -> Category:
        db_category = Category(
            name=category_data.name,
            description=category_data.description,
        )
        self.db.add(db_category)
        try:
            await self.db.commit()
            await self.db.refresh(db_category)
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Category name must be unique") from e

        return db_category


    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        stmt = (
            select(Category)
            .options(selectinload(Category.products))
            .filter(Category.id == category_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Category]:
        stmt = select(Category).filter(Category.name == name)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update(self, category: Category, updates: CategoryUpdate) -> Category:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        await self.db.delete(category)
        await self.db.commit()
