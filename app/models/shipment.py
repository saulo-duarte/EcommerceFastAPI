import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models import Address, Order


class ShipmentStatus(str, PyEnum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    RETURNED = "returned"


@mapper_registry.mapped
class Shipment:
    __tablename__ = "shipments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    tracking_number: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[ShipmentStatus] = mapped_column(
        Enum(ShipmentStatus, native_enum=False),
        name="shipment_status",
        default=ShipmentStatus.PENDING,
        nullable=False,
    )
    shipping_address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False
    )
    billing_address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("addresses.id")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    order: Mapped["Order"] = relationship(back_populates="shipments")
    shipping_address: Mapped["Address"] = relationship(
        back_populates="shipping_shipments", foreign_keys=[shipping_address_id]
    )

    billing_address: Mapped["Address"] = relationship(
        back_populates="billing_shipments", foreign_keys=[billing_address_id]
    )

    @validates("status")
    def validate_status(self, key, value):
        if value not in ShipmentStatus:
            raise ValueError(f"Invalid shipment status: {value}")
        return value

    @validates("tracking_number")
    def validate_tracking_number(self, key, value):
        if not value:
            raise ValueError("Tracking number is required")
        return value
