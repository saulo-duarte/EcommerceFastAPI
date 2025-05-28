
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schema.review import ReviewCreate, ReviewRead
from app.services.review import ReviewService

router = APIRouter(prefix="/review", tags=["review"])

@router.post("/", response_model=ReviewRead)
async def create_review(
    review_data: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        review_service = ReviewService(db)
        review = await review_service.create_review(review_data)
        return review
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ReviewRead])
async def list_reviews(
    db: AsyncSession = Depends(get_async_db),
):
    review_service = ReviewService(db)
    reviews = await review_service.list_reviews()
    return reviews