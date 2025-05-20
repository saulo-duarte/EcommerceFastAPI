from datetime import datetime
from decimal import Decimal

from app.models import OrderStatus
from tests.models_factory import OrderFactory, set_factories_session


def test_order_creation(session):
    set_factories_session(session)

    order = OrderFactory()
    session.add(order)
    session.commit()

    assert order.id is not None
    assert order.status in {OrderStatus.PENDING, "pending"}
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)
    assert order.total_price == Decimal("0.00")
    assert order.shipping_address is not None
    assert order.billing_address is not None
    assert order.user is not None
