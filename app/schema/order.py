from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models import OrderStatus
from app.schema.address import AddressRead
from app.schema.order_item import OrderItemRead
from app.schema.payment import PaymentRead
from app.schema.user import UserRead

if TYPE_CHECKING:
    from app.schema.shipment import ShipmentRead

class OrderBase(BaseModel):
    user_id: UUID
    shipping_address_id: UUID
    billing_address_id: Optional[UUID]
    status: OrderStatus = OrderStatus.PENDING
    total_price: Decimal = Field(..., ge=0)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address_id: Optional[UUID] = None
    billing_address_id: Optional[UUID] = None
    total_price: Optional[Decimal] = Field(None, ge=0)

class OrderRead(BaseModel):
    id: UUID
    user: UserRead
    status: OrderStatus
    total_price: Decimal

    shipping_address: AddressRead
    billing_address: Optional[AddressRead]

    items: List[OrderItemRead] = []
    payments: List[PaymentRead] = []
    shipments: list["ShipmentRead"] = []

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, strict=True)
