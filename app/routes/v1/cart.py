from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.schema.cart import CartCreate, CartRead, CartUpdate
from app.schema.cart_item import CartItemCreate
from app.services.cart import CartService
from app.services.cart_item import CartItemService

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/", response_model=CartRead)
async def create_cart(
    cart_data: CartCreate,
    db: AsyncSession = Depends(get_async_db),
): 
    try:
        cart_service = CartService(db)
        cart = await cart_service.create_cart(cart_data)
        return cart
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.get("/{user_id}", response_model=CartRead)
async def get_cart_by_user_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        cart_service = CartService(db)
        cart = await cart_service.get_cart_by_user_id(user_id)
        return cart
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=List[CartRead])
async def list_carts(
    db: AsyncSession = Depends(get_async_db),
):
    try:
        cart_service = CartService(db)
        carts = await cart_service.list_carts()
        return carts
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.delete("/{cart_id}", response_model=None)
async def delete_cart(
    cart_id: UUID,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        cart_service = CartService(db)
        await cart_service.delete_cart(cart_id)
        return {"detail": "Cart deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.post("/{cart_id}/items", response_model=CartRead)
async def add_item_to_cart(
    cart_item_data: CartItemCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        cart_item_service = CartItemService(db)
        cart = await cart_item_service.create_cart_item(cart_item_data)
        return cart
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)