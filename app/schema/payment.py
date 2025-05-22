from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

if TYPE_CHECKING:
    from app.models import PaymentMethod, PaymentStatus
    from app.schema.order import OrderRead


class PaymentBase(BaseModel):
    order_id: UUID
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(default="brl", min_length=3, max_length=3)
    stripe_payment_intent_id: Optional[str] = None
    stripe_status: Optional[str] = None
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    method: PaymentMethod = Field(default=PaymentMethod.CREDIT_CARD)

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("Amount must be positive")
        return value

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        if len(value) != 3:
            raise ValueError("Currency must be a 3-letter code")
        return value.lower()


class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    stripe_payment_intent_id: Optional[str] = None
    stripe_status: Optional[str] = None
    status: Optional[PaymentStatus] = None
    method: Optional[PaymentMethod] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Optional[Decimal]) -> Optional[Decimal]:
        if value is not None and value <= 0:
            raise ValueError("Amount must be positive")
        return value

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) != 3:
            raise ValueError("Currency must be a 3-letter code")
        return value.lower() if value else value

class PaymentRead(BaseModel):
    id: UUID
    order_id: UUID
    amount: Decimal
    currency: str
    stripe_payment_intent_id: Optional[str]
    stripe_status: Optional[str]
    status: PaymentStatus
    method: PaymentMethod
    created_at: datetime
    updated_at: datetime

    order: Optional[OrderRead] = None

    model_config = ConfigDict(from_attributes=True, strict=True)
