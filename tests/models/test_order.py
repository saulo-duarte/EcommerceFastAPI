import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.models import Order, Address, User
from sqlalchemy.exc import IntegrityError

def test_order_creation(session):
    now = datetime.now(timezone.utc)

    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        hashed_password="hash",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        created_at=now,
        updated_at=now,
    )
    session.add(user)

    address = Address(
        id=uuid.uuid4(),
        user_id=user.id,
        street="Rua A",
        city="Cidade B",
        postal_code="12345-678",
        state="Estado C",
        country="Brasil",
        created_at=now,
        updated_at=now,
    )
    session.add(address)

    session.commit()
    
    order = Order(
        id=uuid.uuid4(),
        user_id=user.id,
        total_price=Decimal("100.00"),
        status="pending",
        shipping_address_id=address.id,
        billing_address_id=address.id,
        created_at=now,
        updated_at=now,
    )
    session.add(order)
    session.commit()

    assert order.id is not None
    assert order.user_id == user.id
    assert order.shipping_address_id == address.id
    assert order.billing_address_id == address.id
    assert order.total_price == Decimal("100.00")
    assert order.status == "pending"
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)


def test_order_total_price_negative_raises(session):
    now = datetime.now(timezone.utc)

    user = User(
        id=uuid.uuid4(),
        email="test2@example.com",
        hashed_password="hash2",
        full_name="Test User 2",
        is_active=True,
        is_superuser=False,
        created_at=now,
        updated_at=now,
    )
    session.add(user)

    address = Address(
        id=uuid.uuid4(),
        user_id=user.id,
        street="Rua X",
        city="Cidade Y",
        postal_code="98765-432",
        state="Estado Z",
        country="Brasil",
        created_at=now,
        updated_at=now,
    )
    session.add(address)
    session.commit()

    with pytest.raises(ValueError):
        order = Order(
            id=uuid.uuid4(),
            user_id=user.id,
            total_price=Decimal("-10.00"),
            status="pending",
            shipping_address_id=address.id,
            billing_address_id=address.id,
            created_at=now,
            updated_at=now,
        )
        session.add(order)
        session.commit()
