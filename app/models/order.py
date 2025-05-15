from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, Enum, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from enum import Enum as PyEnum

from app.db import mapper_registry

if TYPE_CHECKING:
   from app.models import Address, User, OrderItem

class OrderStatus(str, PyEnum):   
   PENDING = "pending"
   SHIPPED = "shipped"
   DELIVERED = "delivered"
   CANCELED = "canceled"

@mapper_registry.mapped
class Order:
   __tablename__ = "orders"

   id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
   )
   user_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
   )
   status: Mapped[OrderStatus] = mapped_column(
      Enum(OrderStatus), name="order_status", native_enum=False, 
      default=OrderStatus.PENDING, nullable=False
   )
   total_price: Mapped[Numeric] = mapped_column(
      Numeric(10, 2), nullable=False
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

   user: Mapped["User"] = relationship(
      "User", back_populates="orders"
   )
   shipping_address: Mapped["Address"] = relationship(
      "Address", foreign_keys=[shipping_address_id]
   )
   billing_address: Mapped["Address"] = relationship(
      "Address", foreign_keys=[billing_address_id]
   )
   items: Mapped[list["OrderItem"]] = relationship(
      "OrderItem", back_populates="order", cascade="all, delete-orphan"
   )

   @validates("total_price")
   def validate_total_price(self, key, value: Decimal) -> Decimal:
      if value < 0:
         raise ValueError("total_price must be non-negative")
      return value