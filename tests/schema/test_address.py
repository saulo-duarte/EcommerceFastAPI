from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.schema.address import AddressCreate, AddressRead, AddressUpdate


def test_address_create_valid():
    data = {
        "street": "Rua Exemplo",
        "city": "São Paulo",
        "state": "SP",
        "country": "Brasil",
        "postal_code": "12345-678",
        "is_default_shipping": True,
        "is_default_billing": False,
    }

    address = AddressCreate(**data)
    assert address.street == "Rua Exemplo"
    assert address.postal_code == "12345-678".upper()

def test_address_create_invalid_postal_code():
    data = {
        "street": "Rua X",
        "city": "Rio",
        "state": "RJ",
        "country": "Brasil",
        "postal_code": "12345@#",
    }

    with pytest.raises(ValueError, match="Postal code must contain only"):
        AddressCreate(**data)

def test_address_update_partial():
    update = AddressUpdate(
        street="   Rua Nova   ",
        postal_code=" 54321-000 "
    )

    assert update.street == "Rua Nova"
    assert update.postal_code == "54321-000"

def test_address_read_model():
    address = AddressRead(
        id=uuid4(),
        user_id=uuid4(),
        street="Rua ABC",
        city="Fortaleza",
        state="CE",
        country="Brasil",
        postal_code="60600-000",
        is_default_shipping=False,
        is_default_billing=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    assert address.street == "Rua ABC"
    assert isinstance(address.created_at, datetime)
