from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import CartItem, Product, Cart
from app.repository.cart_item import CartItemRepository
from app.schema.cart_item import CartItemCreate, CartItemRead

class CartItemService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.cart_item_repository = CartItemRepository(db)

    async def create_cart_item(self, cart_item_data: CartItemCreate) -> CartItemRead:
        # First get the cart to check user_id
        cart_stmt = select(Cart).where(Cart.id == cart_item_data.cart_id)
        cart_result = await self.db.execute(cart_stmt)
        cart = cart_result.scalar_one_or_none()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        stmt = select(CartItem).where(
            CartItem.cart_id == cart_item_data.cart_id,
            CartItem.product_id == cart_item_data.product_id
        ).options(
            selectinload(CartItem.product).selectinload(Product.category)
        )

        result = await self.db.execute(stmt)
        existing_item = result.scalar_one_or_none()

        if existing_item:
            existing_item.quantity += cart_item_data.quantity
            await self.db.commit()
            await self.db.refresh(existing_item)
            cart_item_read = CartItemRead.model_validate(existing_item, from_attributes=True)
            cart_item_read.user_id = cart.user_id
            return cart_item_read
        
        new_cart_item = CartItem(
            cart_id=cart_item_data.cart_id,
            product_id=cart_item_data.product_id,
            quantity=cart_item_data.quantity,
            price_snapshot=cart_item_data.price_snapshot,
        )

        self.db.add(new_cart_item)
        await self.db.commit()
        await self.db.refresh(new_cart_item)
        cart_item_read = CartItemRead.model_validate(new_cart_item, from_attributes=True)
        cart_item_read.user_id = cart.user_id
        return cart_item_read
