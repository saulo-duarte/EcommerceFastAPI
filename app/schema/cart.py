import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schema.cart_item import CartItemRead


class CartBase(BaseModel):
    user_id: uuid.UUID
    is_active: bool = Field(default=True)
    is_checked_out: bool = Field(default=False)


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_checked_out: Optional[bool] = None


class CartRead(CartBase):
    id: uuid.UUID
    items: list[CartItemRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, strict=True)
