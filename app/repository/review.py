from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Review
from app.schema.review import ReviewCreate


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_review(self, review_data: ReviewCreate) -> Review:
        db_review = Review(
            product_id=review_data.product_id,
            user_id=review_data.user_id,
            rating=review_data.rating,
            comment=review_data.comment
        )
        self.db.add(db_review)
        await self.db.commit()
        await self.db.refresh(db_review)
        return db_review

    async def get_reviews_by_product_id(self, product_id: UUID) -> List[Review]:
        stmt = (
            select(Review)
            .options(selectinload(Review.user))
            .filter(Review.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_review_by_id(self, review_id: UUID) -> Optional[Review]:
        stmt = select(Review).filter(Review.id == review_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def list_reviews(self) -> List[Review]:
        stmt = select(Review).options(selectinload(Review.user))
        result = await self.db.execute(stmt)
        return result.scalars().all()
