def test_order_creation(session):
    from app.models import Order, Address, User
    import uuid
    from datetime import datetime, timezone
    from decimal import Decimal

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
    assert order.shipping_address_id == address.id
