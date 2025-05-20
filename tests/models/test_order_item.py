import uuid
from decimal import Decimal

import pytest

from app.models.order_item import OrderItem
from tests.models_factory import OrderFactory, OrderItemFactory, set_factories_session

POSITIVE_QUANTITY = 2
ANOTHER_POSITIVE_QUANTITY = 3
EXPECTED_ITEMS_COUNT = 2


def test_orderitem_creation_and_total_price_update(session):
    set_factories_session(session)

    order = OrderFactory()
    item1 = OrderItemFactory(order=order, quantity=POSITIVE_QUANTITY)
    item2 = OrderItemFactory(order=order, quantity=ANOTHER_POSITIVE_QUANTITY)
    session.add(order)
    session.commit()

    order.update_total_price()
    session.commit()

    expected_total = sum(
        (item.quantity * Decimal(item.price_snapshot) for item in order.items),
        start=Decimal("0.00"),
    )

    assert order.id is not None
    assert len(order.items) == EXPECTED_ITEMS_COUNT
    assert order.total_price == expected_total
    assert item1.order_id == order.id
    assert item2.order_id == order.id
    assert item1.quantity > 0
    assert item2.quantity > 0


@pytest.mark.parametrize("invalid_quantity", [0, -1])
def test_orderitem_invalid_quantity_raises(invalid_quantity):
    with pytest.raises(ValueError, match="quantity must be positive"):
        OrderItem(
            order_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            quantity=invalid_quantity,
            price_snapshot=Decimal("10.00"),
        )


@pytest.mark.parametrize("invalid_price", [-1, Decimal("-0.01")])
def test_orderitem_invalid_price_snapshot_raises(invalid_price):
    with pytest.raises(ValueError, match="price_snapshot must be non-negative"):
        OrderItem(
            order_id=uuid.uuid4(),
            product_id=uuid.uuid4(),
            quantity=1,
            price_snapshot=invalid_price,
        )
