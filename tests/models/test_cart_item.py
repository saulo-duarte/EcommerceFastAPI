import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.models.cart_item import CartItem
from tests.models_factory import CartItemFactory, set_factories_session

TEST_QUANTITY = 3


def test_cart_item_creation(session):
    set_factories_session(session)

    cart_item = CartItemFactory(quantity=3)
    session.add(cart_item)
    session.commit()

    assert cart_item.id is not None
    assert cart_item.quantity == TEST_QUANTITY
    assert cart_item.price_snapshot == pytest.approx(
        Decimal(str(cart_item.product.price))
    )
    assert cart_item.cart is not None
    assert cart_item.product is not None

    db_cart_item = session.query(CartItem).filter_by(id=cart_item.id).first()
    assert db_cart_item is not None
    assert db_cart_item.quantity == TEST_QUANTITY


@pytest.mark.parametrize("invalid_quantity", [0, -1])
def test_cart_item_invalid_quantity_raises(invalid_quantity):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        CartItem(
            cart_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            quantity=invalid_quantity,
            price_snapshot=10.0,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
