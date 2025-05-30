from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schema.product import ProductRead


class OrderItemBase(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int = Field(..., ge=1)
    price_snapshot: Decimal = Field(..., ge=0)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Quantity must be greater than zero")
        return value

    @field_validator("price_snapshot")
    @classmethod
    def validate_price_snapshot(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("Price snapshot must be non-negative")
        return value


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    price_snapshot: Optional[Decimal] = Field(None, ge=0)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value <= 0:
            raise ValueError("Quantity must be greater than zero")
        return value

    @field_validator("price_snapshot")
    @classmethod
    def validate_price_snapshot(cls, value: Optional[Decimal]) -> Optional[Decimal]:
        if value is not None and value < 0:
            raise ValueError("Price snapshot must be non-negative")
        return value


class OrderItemRead(BaseModel):
    id: UUID
    order_id: UUID
    product: ProductRead
    quantity: int
    price_snapshot: Decimal

    model_config = ConfigDict(from_attributes=True, strict=True)
