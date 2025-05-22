from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models import User
from app.schema.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        db_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=user_data.password.hash(),
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
        )
        self.db.add(db_user)
        try:
            await self.db.commit()
            await self.db.refresh(db_user)
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Email already exists") from e
        return db_user

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.get(User, user_id)
        return result

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).filter(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update(self, user: User, updates: UserUpdate) -> User:
        for field, value in updates.model_dump(exclude_unset=True).items():
            if field == "password":
                setattr(user, "hashed_password", value.hash())
            else:
                setattr(user, field, value)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
