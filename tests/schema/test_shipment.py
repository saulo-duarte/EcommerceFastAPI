import uuid
from datetime import datetime, timezone

import pytest
from app.schema.shipment import ShipmentCreate, ShipmentUpdate, ShipmentRead
from app.schema.address import AddressRead
from app.schema.order import OrderRead
from app.models import ShipmentStatus


def test_shipment_create_valid():
    data = {
        "order_id": uuid.uuid4(),
        "tracking_number": "TRACK12345",
        "status": ShipmentStatus.SHIPPED,
        "shipping_address_id": uuid.uuid4(),
        "billing_address_id": uuid.uuid4()
    }
    shipment = ShipmentCreate(**data)
    assert shipment.tracking_number == "TRACK12345"
    assert shipment.status == ShipmentStatus.SHIPPED


def test_shipment_create_invalid_tracking_number_blank():
    data = {
        "order_id": uuid.uuid4(),
        "tracking_number": "   ",
        "status": ShipmentStatus.PENDING,
        "shipping_address_id": uuid.uuid4()
    }
    with pytest.raises(ValueError) as exc_info:
        ShipmentCreate(**data)
    assert "Tracking number is required" in str(exc_info.value)


def test_shipment_update_valid():
    data = {
        "tracking_number": "UPDATED123",
        "status": ShipmentStatus.DELIVERED,
        "shipping_address_id": uuid.uuid4(),
        "billing_address_id": uuid.uuid4()
    }
    shipment = ShipmentUpdate(**data)
    assert shipment.tracking_number == "UPDATED123"
    assert shipment.status == ShipmentStatus.DELIVERED


def test_shipment_update_empty_tracking_number():
    data = {
        "tracking_number": "  "
    }
    with pytest.raises(ValueError) as exc_info:
        ShipmentUpdate(**data)
    assert "Tracking number cannot be empty" in str(exc_info.value)


def test_shipment_read_model():
    shipment_id = uuid.uuid4()
    order_id = uuid.uuid4()
    shipping_address_id = uuid.uuid4()
    billing_address_id = uuid.uuid4()

    address = AddressRead(
        id=shipping_address_id,
        street="Rua A",
        city="São Paulo",
        state="SP",
        zip_code="12345-678",
        country="Brasil",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    order = OrderRead(
        id=order_id,
        user_id=uuid.uuid4(),
        status="processing",
        total=199.99,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    shipment = ShipmentRead(
        id=shipment_id,
        order_id=order_id,
        tracking_number="ABC123",
        status=ShipmentStatus.PENDING,
        shipping_address_id=shipping_address_id,
        billing_address_id=billing_address_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        shipping_address=address,
        billing_address=address,
        order=order
    )

    assert shipment.tracking_number == "ABC123"
    assert shipment.status == ShipmentStatus.PENDING
    assert shipment.shipping_address.city == "São Paulo"
    assert shipment.order.total == 199.99
