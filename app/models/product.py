import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from app.db import mapper_registry
from app.models import Category


@mapper_registry.mapped
class Product:
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(Text, nullable=True)
    stock: Mapped[int] = Column(Integer, nullable=False)
    price: Mapped[float] = Column(Double, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    category_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    category: Mapped["Category"] = relationship("Category", back_populates="products")
