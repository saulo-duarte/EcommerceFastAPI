import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from app.db.registry import mapper_registry

@mapper_registry.mapped
class User:
   __tablename__ = 'users'

   id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   email: Mapped[str] = Column(String, unique=True, nullable=False, index=True)
   hashed_password: Mapped[str] = Column(String, nullable=False)
   full_name: Mapped[str | None] = Column(String, nullable=True)
   is_active: Mapped[bool] = Column(Boolean, default=True)
   is_superuser: Mapped[bool] = Column(Boolean, default=False)
   created_at: Mapped[datetime] = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))    
   updated_at: Mapped[datetime] = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
   