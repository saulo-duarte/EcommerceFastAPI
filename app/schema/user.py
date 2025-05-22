import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.value_objects import Password
from app.schema.address import AddressRead, AddressCreate


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=50)
    is_active: bool = True
    is_superuser: bool = False

    @field_validator("full_name")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, name: str) -> str:
        name = name.strip()
        if not name.replace(" ", "").isalpha():
            raise ValueError("Full name must contain only letters and spaces")
        return name


class UserCreate(UserBase):
    password: Password
    addresses: List[AddressCreate] = []

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, name: str) -> str:
        name = name.strip()
        if not name.replace(" ", "").isalpha():
            raise ValueError("Full name must contain only letters and spaces")
        return name


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[Password] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, name: Optional[str]) -> Optional[str]:
        if name:
            name = name.strip()
            if not name.replace(" ", "").isalpha():
                raise ValueError("Full name must contain only letters and spaces")
        return name


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    addresses: list[AddressRead] = []

    model_config = ConfigDict(strict=True, from_attributes=True)
