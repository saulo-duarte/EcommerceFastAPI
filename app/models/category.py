from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models.product import Product


@mapper_registry.mapped
class Category:
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = Column(String(255), nullable=False, unique=True)
    description: Mapped[str] = Column(String(255), nullable=True)

    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    products: Mapped["Product"] = relationship("Product", back_populates="category")
