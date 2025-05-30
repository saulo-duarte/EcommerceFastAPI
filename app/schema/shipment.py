from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import ShipmentStatus
from app.schema.address import AddressRead
from app.schema.order import OrderRead


class ShipmentBase(BaseModel):
    order_id: UUID
    tracking_number: str = Field(..., max_length=50)
    status: ShipmentStatus = Field(default=ShipmentStatus.PENDING)
    shipping_address_id: UUID
    billing_address_id: Optional[UUID] = None

    @field_validator("tracking_number")
    @classmethod
    def validate_tracking_number(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Tracking number is required")
        return value


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    tracking_number: Optional[str] = Field(None, max_length=50)
    status: Optional[ShipmentStatus] = None
    shipping_address_id: Optional[UUID] = None
    billing_address_id: Optional[UUID] = None

    @field_validator("tracking_number")
    @classmethod
    def validate_tracking_number(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Tracking number cannot be empty")
        return value


class ShipmentRead(BaseModel):
    id: UUID
    order_id: UUID
    tracking_number: str
    status: ShipmentStatus
    shipping_address_id: UUID
    billing_address_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    shipping_address: Optional[AddressRead]
    billing_address: Optional[AddressRead]
    order: Optional[OrderRead] = None

    model_config = ConfigDict(from_attributes=True, strict=True)
