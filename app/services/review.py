from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models import Product, Review, User
from app.repository.review import ReviewRepository
from app.schema.review import ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.review_repository = ReviewRepository(db)

    async def create_review(self, review_data: ReviewCreate) -> Review:
        product = await self.db.execute(select(Product).where(Product.id == review_data.product_id))
        product_result = product.scalar_one_or_none()

        if product_result is None:
            raise ValueError(f"Product with id {review_data.product_id} does not exist")

        user = await self.db.execute(select(User).where(User.id == review_data.user_id))
        user_result = user.scalar_one_or_none()

        if user_result is None:
            raise ValueError(f"User with id {review_data.user_id} does not exist")

        db_review = Review(
            product_id=review_data.product_id,
            user_id=review_data.user_id,
            rating=review_data.rating,
            comment=review_data.comment
        )
        self.db.add(db_review)
        await self.db.commit()
        await self.db.refresh(db_review)

        stmt = (
            select(Review)
            .options(
                selectinload(Review.product).selectinload(Product.category),
                selectinload(Review.user).selectinload(User.addresses)
            )
            .where(Review.id == db_review.id)
        )

        result = await self.db.execute(stmt)
        db_review = result.scalar_one()

        return db_review

    async def list_reviews(self, product_id: Optional[UUID] = None) -> List[Review]:
        stmt = select(Review).options(
            selectinload(Review.product).selectinload(Product.category),
            selectinload(Review.user).selectinload(User.addresses)
        )

        if product_id:
            stmt = stmt.where(Review.product_id == product_id)

        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def update_review(self, review_id: UUID, review_data: ReviewUpdate) -> Review:
        db_review = await self.review_repository.get_review_by_id(review_id)
        if not db_review:
            raise ValueError("Review not found")

        if review_data.rating is not None:
            db_review.rating = review_data.rating
        if review_data.comment is not None:
            db_review.comment = review_data.comment

        await self.db.commit()
        await self.db.refresh(db_review)

        return db_review

    async def delete_review(self, review_id: UUID) -> None:
        db_review = await self.review_repository.get_review_by_id(review_id)

        if not db_review:
            raise HTTPException(status_code=404, detail="Review not found")

        await self.db.delete(db_review)
        await self.db.commit()
