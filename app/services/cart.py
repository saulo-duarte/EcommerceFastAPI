from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Cart, CartItem, Product, User
from app.repository.cart import CartRepository
from app.schema.cart import CartCreate, CartRead, CartUpdate

class CartService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.cart_repository = CartRepository(db)

    async def create_cart(self, cart_data: CartCreate) -> CartRead:
        stmt = select(Cart).where(
            Cart.user_id == cart_data.user_id,
            Cart.is_active.is_(True)
        ).options(
            selectinload(Cart.items)
            .selectinload(CartItem.product)
            .selectinload(Product.category)
        )

        result = await self.db.execute(stmt)
        existing_cart = result.scalar_one_or_none()

        if existing_cart:
            raise HTTPException(
                status_code=400,
                detail=f"Cart for user {cart_data.user_id} already exists."
            )

        new_cart = Cart(
            user_id=cart_data.user_id,
            is_active=True,
            is_checked_out=False
        )
        self.db.add(new_cart)
        await self.db.commit()
        await self.db.refresh(new_cart)

        stmt = select(Cart).where(Cart.id == new_cart.id).options(
            selectinload(Cart.items).selectinload(CartItem.product)
        )
        result = await self.db.execute(stmt)
        db_cart = result.scalar_one()

        return CartRead.model_validate(db_cart)
    
    async def get_cart_by_user_id(self, user_id: UUID) -> Optional[CartRead]:
        cart = await self.cart_repository.get_cart_by_user_id(user_id)

        if not cart:
            return HTTPException(
                status_code=404,
                detail=f"Cart for user {user_id} not found."
            )
        return CartRead.model_validate(cart)
    
    async def list_carts(self) -> List[CartRead]:
        carts = await self.cart_repository.list_carts()
        return [CartRead.model_validate(cart) for cart in carts]
    
    async def delete_cart(self, cart_id: UUID) -> None:
        stmt = select(Cart).where(Cart.id == cart_id)
        result = await self.db.execute(stmt)
        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(
                status_code=404,
                detail=f"Cart with ID {cart_id} not found."
            )

        await self.cart_repository.delete_cart(cart)