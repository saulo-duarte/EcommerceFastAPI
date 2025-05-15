from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from app.db import mapper_registry

if TYPE_CHECKING:
    from app.models.address import Address


@mapper_registry.mapped
class User:
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = Column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = Column(String, nullable=False)
    full_name: Mapped[str | None] = Column(String, nullable=True)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    is_superuser: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    addresses: Mapped["Address"] = relationship("Address", back_populates="user")
