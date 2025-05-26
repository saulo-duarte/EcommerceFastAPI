from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import User
from app.repository.address import AddressRepository
from app.repository.user import UserRepository
from app.schema.user import UserCreate, UserRead


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.address_repository = AddressRepository(db)

    async def create_user_with_addresses(self, user_data: UserCreate) -> UserRead:
        try:
            new_user = await self.user_repository.create_user(user_data)

            for address_data in user_data.addresses:
                await self.address_repository.create_address(address_data, new_user.id)

            await self.db.refresh(new_user)
            await self.db.commit()

            stmt = select(User).options(selectinload(User.addresses)).where(User.id == new_user.id)
            result = await self.db.execute(stmt)
            user_with_addresses = result.scalar_one()

            return UserRead.model_validate(user_with_addresses, from_attributes=True)

        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("User creation failed due to integrity error") from e

    async def list_users(self) -> list[UserRead]:
        stmt = select(User).options(selectinload(User.addresses))
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        return [UserRead.model_validate(user) for user in users]


    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def update_user(self, user_id: UUID, user_data: UserCreate) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        updated_user = await self.user_repository.update(user, user_data)
        await self.db.commit()
        await self.db.refresh(updated_user)
        return updated_user

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        await self.user_repository.delete(user)
        await self.db.commit()
