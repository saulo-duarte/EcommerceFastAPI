import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schema.cart import CartCreate, CartRead, CartUpdate
from app.schema.cart_item import CartItemRead
from app.schema.category import CategoryRead
from app.schema.product import ProductRead

CART_ITEM_QUANTITY = 2


def test_cart_create_valid():
    cart = CartCreate(user_id=uuid.uuid4())
    assert cart.is_active is True
    assert cart.is_checked_out is False
    assert isinstance(cart.user_id, uuid.UUID)


def test_cart_create_missing_user_id():
    with pytest.raises(ValidationError) as exc_info:
        CartCreate()
    assert "user_id" in str(exc_info.value)


def test_cart_update_partial():
    update = CartUpdate(is_checked_out=True)
    assert update.is_checked_out is True
    assert update.is_active is None


def test_cart_update_invalid_type():
    update = CartUpdate(is_active="yes")
    assert update.is_active is True


def test_cart_read_valid():
    cart_read = CartRead(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        is_active=True,
        is_checked_out=False,
        items=[],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    assert isinstance(cart_read.id, uuid.UUID)
    assert isinstance(cart_read.user_id, uuid.UUID)
    assert isinstance(cart_read.created_at, datetime)
    assert isinstance(cart_read.items, list)
    assert cart_read.is_checked_out is False


def test_cart_read_with_items():
    category = CategoryRead(
        id=uuid.uuid4(),
        name="Books",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    product = ProductRead(
        id=uuid.uuid4(),
        name="Test Product",
        price=Decimal("19.99"),
        stock=100,
        category=category,
        is_available=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    item = CartItemRead(
        id=uuid.uuid4(),
        cart_id=uuid.uuid4(),
        product=product,
        quantity=2,
        price_snapshot=Decimal("19.99"),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    cart = CartRead(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        is_active=True,
        is_checked_out=False,
        items=[item],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    assert len(cart.items) == 1
    assert isinstance(cart.items[0], CartItemRead)
    assert isinstance(cart.items[0].product.category, CategoryRead)
    assert cart.items[0].quantity == CART_ITEM_QUANTITY
