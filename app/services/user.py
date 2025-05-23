from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repository.address import AddressRepository
from app.repository.user import UserRepository
from app.schema.user import UserCreate


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.address_repository = AddressRepository(db)

    async def create_user_with_addresses(self, user_data: UserCreate) -> User:
        try:
            new_user = await self.user_repository.create_user(user_data)

            for address_data in user_data.addresses:
                await self.address_repository.create_address(address_data, new_user.id)

            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user

        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("User creation failed due to integrity error") from e
