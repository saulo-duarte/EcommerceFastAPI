import uuid
from datetime import datetime, timezone

from app.models import Address, User


def test_address_creation(session):
    user = User(
        email="testuser@example.com",
        hashed_password="hashedpassword123",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(user)
    session.commit()

    address = Address(
        id=uuid.uuid4(),
        user_id=user.id,
        street="123 Main St",
        city="Anytown",
        state="CA",
        country="USA",
        postal_code="12345",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(address)
    session.commit()

    assert address.id is not None
    assert address.street == "123 Main St"
    assert address.city == "Anytown"
    assert address.state == "CA"
    assert address.country == "USA"
    assert address.postal_code == "12345"
    assert address.user_id == user.id
    assert address.created_at is not None
    assert address.updated_at is not None
    assert address.created_at <= address.updated_at
    assert address.user_id == user.id

    db_address = session.query(Address).filter_by(street="123 Main St").first()
    assert db_address is not None
