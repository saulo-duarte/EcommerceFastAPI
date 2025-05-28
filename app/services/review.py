
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Product, Review, User
from app.repository.review import ReviewRepository
from app.schema.review import ReviewCreate


class ReviewService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.review_repository = ReviewRepository(db)

    async def create_review(self, review_data: ReviewCreate) -> Review:
        # 1. Cria o review
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
