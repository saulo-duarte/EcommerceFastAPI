import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schema.product import ProductRead


class CartItemBase(BaseModel):
    cart_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int = Field(..., ge=1)
    price_snapshot: Decimal = Field(..., ge=0)

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)

class CartItemRead(BaseModel):
    id: uuid.UUID
    cart_id: uuid.UUID
    product: ProductRead
    quantity: int
    price_snapshot: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, strict=True)
