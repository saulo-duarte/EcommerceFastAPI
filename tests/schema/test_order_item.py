from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schema.category import CategoryRead
from app.schema.order_item import OrderItemCreate
from app.schema.product import ProductRead


@pytest.fixture()
def sample_category():
    return CategoryRead(
        id=uuid4(),
        name="Electronics",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture()
def sample_product(sample_category):
    return ProductRead(
        id=uuid4(),
        name="Smartphone",
        price=Decimal("999.99"),
        stock=50,
        category=sample_category,
        is_available=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def test_order_item_create_valid():
    item = OrderItemCreate(
        order_id=uuid4(),
        product_id=uuid4(),
        quantity=2,
        price_snapshot=Decimal("49.99"),
    )
    assert item.quantity == 2
    assert item.price_snapshot == Decimal("49.99")


def test_order_item_create_invalid_quantity():
    with pytest.raises(ValidationError) as exc_info:
        OrderItemCreate(
            order_id=uuid4(),
            product_id=uuid4(),
            quantity=0,
            price_snapshot=Decimal("10.00"),
        )
    assert "greater than or equal to 1" in str(exc_info.value)


def test_order_item_create_invalid_price():
    with pytest.raises(ValidationError) as exc_info:
        OrderItemCreate(
            order_id=uuid4(),
            product_id=uuid4(),
            quantity=1,
            price_snapshot=Decimal("-5.00"),
        )
    assert "greater than or equal to 0" in str(exc_info.value)
