import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schema.category import CategoryRead


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    stock: int = Field(..., ge=0)
    price: float = Field(..., ge=0)
    is_active: bool = Field(default=True)

    @field_validator("name", "description")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value.strip()) < 2:
            raise ValueError("Description must be at least 2 characters")
        return value.strip() if value else value


class ProductCreate(ProductBase):
    category_id: uuid.UUID


class ProductUpdate(BaseModel):
    category_id: Optional[uuid.UUID] = None
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, min_length=2, max_length=255)
    stock: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None

    @field_validator("name", "description")
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value.strip()) < 2:
            raise ValueError("Description must be at least 2 characters")
        return value.strip() if value else value

class ProductRead(ProductBase):
    id: uuid.UUID
    category: CategoryRead
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(strict=True, from_attributes=True)
