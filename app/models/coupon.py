from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import mapper_registry
from app.models.order_coupons import order_coupons

if TYPE_CHECKING:
    from app.models import Order, User


class CouponType(str, PyEnum):
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"

MAX_DISCOUNT_PERCENTAGE = 100

@mapper_registry.mapped
class Coupon:
    __tablename__ = "coupons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    type: Mapped[CouponType] = mapped_column(
        Enum(CouponType, native_enum=False), name="coupon_type", nullable=False
    )

    discount_percent: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2), nullable=True
    )

    discount_fixed: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )

    min_order_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    usage_limit: Mapped[int] = mapped_column(Integer, nullable=True)
    used_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="coupons")
    orders: Mapped[list["Order"]] = relationship(
        back_populates="coupons", secondary=order_coupons
    )

    @validates("discount_percent")
    def validate_discount_percent(self, key, value: Decimal | None) -> Decimal | None:
        if value is not None and not (0 < value <= MAX_DISCOUNT_PERCENTAGE):
            raise ValueError(
                f"discount_percent must be between 0 and {MAX_DISCOUNT_PERCENTAGE}"
            )
        return value

    @validates("discount_fixed")
    def validate_discount_fixed(self, key, value: Decimal | None) -> Decimal | None:
        if value is not None and value < 0:
            raise ValueError("discount_fixed must be non-negative")
        return value

    @validates("min_order_value")
    def validate_min_order_value(self, key, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("min_order_value must be non-negative")
        return value

    @validates("usage_limit", "used_count")
    def validate_usage_limits(self, key, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError(f"{key} must be non-negative")
        return value
