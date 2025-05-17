from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import mapper_registry
from app.models import Category

if TYPE_CHECKING:
    from app.models import Review

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 255


@mapper_registry.mapped
class Product:
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Double, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="product", cascade="all, delete-orphan"
    )

    @validates("name")
    def validate_name(self, key: str, name: str) -> str:
        if len(name) < MIN_NAME_LENGTH or len(name) > MAX_NAME_LENGTH:
            raise ValueError(
                f"Name must be between {MIN_NAME_LENGTH} and "
                f"{MAX_NAME_LENGTH} characters"
            )
        return name

    @validates("price")
    def validate_price(self, key: str, price: float) -> float:
        if price <= 0:
            raise ValueError("Price must be positive")
        return price

    @validates("stock")
    def validate_stock(self, key: str, stock: int) -> int:
        if stock < 0:
            raise ValueError("Stock must be non-negative")
        return stock
