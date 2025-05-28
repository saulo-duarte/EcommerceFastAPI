
from sqlalchemy.ext.asyncio import AsyncSession

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
