from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schema.product import ProductRead
from app.schema.user import UserRead

MIN_RATING = 1.0
MAX_RATING = 5.0
MAX_COMMENT_LENGTH = 1000


class ReviewBase(BaseModel):
    rating: float = Field(..., ge=MIN_RATING, le=MAX_RATING)
    comment: Optional[str] = Field(None, max_length=MAX_COMMENT_LENGTH)

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: float) -> float:
        if not (MIN_RATING <= value <= MAX_RATING):
            raise ValueError(f"Rating must be between {MIN_RATING} and {MAX_RATING}")
        return value

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > MAX_COMMENT_LENGTH:
            raise ValueError(f"Comment must be at most {MAX_COMMENT_LENGTH} characters")
        return value

class ReviewCreate(ReviewBase):
    product_id: UUID
    user_id: UUID

class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=MIN_RATING, le=MAX_RATING)
    comment: Optional[str] = Field(None, max_length=MAX_COMMENT_LENGTH)

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (MIN_RATING <= value <= MAX_RATING):
            raise ValueError(f"Rating must be between {MIN_RATING} and {MAX_RATING}")
        return value

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > MAX_COMMENT_LENGTH:
            raise ValueError(f"Comment must be at most {MAX_COMMENT_LENGTH} characters")
        return value

class ReviewRead(BaseModel):
    id: UUID
    product_id: UUID
    user_id: UUID
    rating: float
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime

    product: Optional[ProductRead]
    user: Optional[UserRead]

    model_config = ConfigDict(from_attributes=True, strict=True)
