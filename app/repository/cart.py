from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Cart
from app.schema.cart import CartCreate, CartRead

class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart(self, cart_data: CartCreate) -> Cart:
        db_cart = Cart(
            user_id=cart_data.user_id,
            is_active=True,
            is_checked_out=False,
        )
        self.db.add(db_cart)
        await self.db.commit()
        await self.db.refresh(db_cart)
        return db_cart
    
    async def get_cart_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        stmt = (
            select(Cart)
            .options(selectinload(Cart.items))
            .filter(
                Cart.user_id == user_id, 
                Cart.is_active.is_(True), 
                Cart.is_checked_out.is_(False)
            ))
        
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def list_carts(self) -> List[Cart]:
        stmt = select(Cart).options(selectinload(Cart.items))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def delete_cart(self, cart: Cart) -> None:
        await self.db.delete(cart)
        await self.db.commit()