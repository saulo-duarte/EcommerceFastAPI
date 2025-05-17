from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, validates

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models import Shipment, User


@mapper_registry.mapped
class Address:
    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    street: Mapped[str] = Column(String(255), nullable=False)
    city: Mapped[str] = Column(String(255), nullable=False)
    state: Mapped[str] = Column(String(255), nullable=False)
    country: Mapped[str] = Column(String(255), nullable=False)
    postal_code: Mapped[str] = Column(String(20), nullable=False)
    is_default_shipping: Mapped[bool] = Column(Boolean, default=False)
    is_default_billing: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    user: Mapped["User"] = relationship("User", back_populates="addresses")
    shipping_shipments: Mapped[list["Shipment"]] = relationship(
        "Shipment",
        back_populates="shipping_address",
        foreign_keys="[Shipment.shipping_address_id]",
    )
    billing_shipments: Mapped[list["Shipment"]] = relationship(
        "Shipment",
        back_populates="billing_address",
        foreign_keys="[Shipment.billing_address_id]",
    )

    @validates("street", "city", "state", "country", "postal_code")
    def validate_not_empty(self, key, value):
        if not value or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"{key} is required and cannot be empty")
        if key == "postal_code":
            pattern = r"^\d{5}-?\d{3}$"
            if not re.match(pattern, value):
                raise ValueError(
                    "Invalid postal code format. Expected '12345-678' or '12345678'"
                )
        return value
