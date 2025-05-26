from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models import Address, Cart, Coupon, Order, Review

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
)

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 50


@mapper_registry.mapped
class User:
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    addresses: Mapped[list[Address]] = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    carts: Mapped["Cart"] = relationship("Cart", back_populates="user")
    orders: Mapped[list[Order]] = relationship(
        "Order", back_populates="user", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )
    coupons: Mapped[list["Coupon"]] = relationship(
        "Coupon", back_populates="user", cascade="all, delete-orphan"
    )

    @validates("email")
    def validate_email(self, key: str, email: str) -> str:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email

    @validates("full_name")
    def validate_full_name(self, key: str, full_name: str) -> str:
        full_name = full_name.strip()

        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿÇç\s]+", full_name):
            raise ValueError("Full name must contain only letters and spaces")

        if len(full_name) < MIN_NAME_LENGTH or len(full_name) > MAX_NAME_LENGTH:
            raise ValueError("Full name must be between 2 and 50 characters")

        return full_name

    @validates("hashed_password")
    def validate_hashed_password(self, key: str, hashed_password: str) -> str:
        if not PASSWORD_REGEX.match(hashed_password):
            raise ValueError(
                "Password must be at least 8 characters long and "
                "include at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character."
            )
        return hashed_password
