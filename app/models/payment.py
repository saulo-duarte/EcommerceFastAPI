import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Numeric, Enum, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from enum import Enum as PyEnum

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models import Order


class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentMethod(str, PyEnum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"


@mapper_registry.mapped
class Payment:
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    currency: Mapped[str] = mapped_column(
        String(length=3), default="brl", nullable=False
    )
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, unique=True
    )
    stripe_status: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), name="payment_status", native_enum=False,
        default=PaymentStatus.PENDING, nullable=False
    )

    method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod), name="payment_method", native_enum=False,
        default=PaymentMethod.CREDIT_CARD, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    order: Mapped["Order"] = relationship("Order", back_populates="payments")

    @validates("amount")
    def validate_amount(self, key, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("amount must be positive")
        return value

    @validates("status")
    def validate_status(self, key, value: PaymentStatus) -> PaymentStatus:
        if value not in PaymentStatus:
            raise ValueError(f"Invalid payment status: {value}")
        return value

    @validates("method")
    def validate_method(self, key, value: PaymentMethod) -> PaymentMethod:
        if value not in PaymentMethod:
            raise ValueError(f"Invalid payment method: {value}")
        return value

    @property
    def amount_in_cents(self) -> int:
        return int(self.amount * 100)

