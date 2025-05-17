import uuid

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models import User, Product


MIN_RATING = 1.0
MAX_RATING = 5.0
MAX_COMMENT_LENGTH = 1000

@mapper_registry.mapped
class Review:
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    product: Mapped["Product"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship(back_populates="reviews")


    @validates("rating")
    def validate_rating(self, key, rating: float) -> float:
        if not (MIN_RATING <= rating <= MAX_RATING):
            raise ValueError(f"Rating must be between {MIN_RATING} and {MAX_RATING}")
        return rating

    @validates("comment")
    def validate_comment(self, key, comment: str | None) -> str | None:
        if comment and len(comment) > MAX_COMMENT_LENGTH:
            raise ValueError(f"Comment must be at most {MAX_COMMENT_LENGTH} characters")
        return comment