import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.schema.cart_item import (
    CartItemCreate,
    CartItemRead,
    CartItemUpdate,
)
from app.schema.category import CategoryRead
from app.schema.product import ProductRead

PRICE_SNAPSHOT = Decimal("19.99")
ITEM_QUANTITY = 3


def test_cart_item_create_valid():
    item = CartItemCreate(
        cart_id=uuid.uuid4(),
        product_id=uuid.uuid4(),
        quantity=ITEM_QUANTITY,
        price_snapshot=PRICE_SNAPSHOT,
    )
    assert item.quantity == ITEM_QUANTITY
    assert item.price_snapshot == PRICE_SNAPSHOT


def test_cart_item_create_invalid_quantity():
    with pytest.raises(ValueError):
        CartItemCreate(
            cart_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            quantity=0,
            price_snapshot=Decimal("10.00"),
        )


def test_cart_item_create_invalid_price():
    with pytest.raises(ValueError):
        CartItemCreate(
            cart_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            quantity=1,
            price_snapshot=Decimal("-1.00"),
        )


def test_cart_item_update_valid():
    update = CartItemUpdate(quantity=5)
    assert update.quantity == 5


def test_cart_item_update_invalid_quantity():
    with pytest.raises(ValueError):
        CartItemUpdate(quantity=0)


def test_cart_item_read_valid():
    category = CategoryRead(
        id=uuid.uuid4(),
        name="Books",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    product = ProductRead(
        id=uuid.uuid4(),
        name="Test Product",
        price=Decimal("49.99"),
        stock=10,
        category=category,
        is_available=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    item = CartItemRead(
        id=uuid.uuid4(),
        cart_id=uuid.uuid4(),
        product=product,
        quantity=3,
        price_snapshot=Decimal("39.99"),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    assert isinstance(item.product, ProductRead)
    assert isinstance(item.created_at, datetime)
    assert item.quantity == 3
    assert item.price_snapshot == Decimal("39.99")
