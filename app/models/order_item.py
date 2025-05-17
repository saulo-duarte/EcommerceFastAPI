from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models import Order, Product


@mapper_registry.mapped
class OrderItem:
    __tablename__ = "order_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_snapshot: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        return (
            f"<OrderItem id={self.id} product_id={self.product_id} "
            f"quantity={self.quantity} price_snapshot={self.price_snapshot}>"
        )

    @validates("quantity")
    def validate_quantity(self, key, value: int) -> int:
        if value <= 0:
            raise ValueError("quantity must be positive")
        return value

    @validates("price_snapshot")
    def validate_price_snapshot(self, key, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("price_snapshot must be non-negative")
        return value
