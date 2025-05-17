from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models.product import Product

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 255


@mapper_registry.mapped
class Category:
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )

    @validates("name")
    def validate_name(self, key: str, name: str) -> str:
        if len(name) < MIN_NAME_LENGTH or len(name) > MAX_NAME_LENGTH:
            raise ValueError(
                f"Name must be between {MIN_NAME_LENGTH} and "
                f"{MAX_NAME_LENGTH} characters"
            )
        return name

    @validates("description")
    def validate_description(self, key: str, desc: str | None) -> str | None:
        if desc is not None and len(desc) > MAX_NAME_LENGTH:
            raise ValueError("Description must be at most 255 characters")
        return desc
