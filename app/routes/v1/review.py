from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schema.review import ReviewCreate, ReviewRead, ReviewUpdate
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

@router.get("/", response_model=List[ReviewRead])
async def list_reviews(
    db: AsyncSession = Depends(get_async_db),
):
    review_service = ReviewService(db)
    reviews = await review_service.list_reviews()
    return reviews

@router.get("/{product_id}", response_model=List[ReviewRead])
async def get_review( product_id: UUID, db: AsyncSession = Depends(get_async_db)):
    review_service = ReviewService(db)
    review = await review_service.list_reviews(product_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewUpdate)
async def update_review(
    review_id: UUID,
    review_data: ReviewUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    review_service = ReviewService(db)
    updated_review = await review_service.update_review(review_id, review_data)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review

@router.delete("/{review_id}")
async def delete_review(
    review_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    review_service = ReviewService(db)
    await review_service.delete_review(review_id)
    return {"detail": "Review deleted successfully"}