from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Address
from app.schema.address import AddressCreate, AddressUpdate


class AddressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_address(
        self, address_data: AddressCreate, user_id: UUID
    ) -> Address:
        db_address = Address(
            street=address_data.street,
            city=address_data.city,
            state=address_data.state,
            country=address_data.country,
            postal_code=address_data.postal_code,
            is_default_shipping=address_data.is_default_shipping,
            is_default_billing=address_data.is_default_billing,
            user_id=user_id
        )
        self.db.add(db_address)
        try:
            await self.db.commit()
            await self.db.refresh(db_address)
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError("Address already exists") from e
        return db_address

    async def get_by_id(self, address_id: UUID) -> Optional[Address]:
        result = await self.db.get(Address, address_id)
        return result

    async def update(self, address: Address, updates: AddressUpdate) -> Address:
        for field, value in updates.model_dump(exclude_unset=True).items():
            setattr(address, field, value)
        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def delete(self, address: Address) -> None:
        await self.db.delete(address)
        await self.db.commit()

    async def list(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Address]:
        result = await self.db.execute(
            select(Address)
            .filter(Address.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
