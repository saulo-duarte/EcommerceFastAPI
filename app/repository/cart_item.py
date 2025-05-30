from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import CartItem, Product
from app.schema.cart_item import CartItemCreate, CartItemRead

class CartItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart_item(self, cart_item_data: CartItemCreate) -> CartItem:
        stmt = select(Product).where(Product.id == cart_item_data.product_id)
        result = await self.db.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        db_cart_item = CartItem(
            cart_id=cart_item_data.cart_id,
            product_id=cart_item_data.product_id,
            quantity=cart_item_data.quantity,
            price_snapshot=product.price
        )

        self.db.add(db_cart_item)
        await self.db.commit()
        await self.db.refresh(db_cart_item)

        return db_cart_item