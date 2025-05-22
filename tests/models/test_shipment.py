from datetime import datetime, timezone

import pytest

from app.models.shipment import ShipmentStatus
from tests.models_factory import ShipmentFactory, set_factories_session


def test_shipment_creation(session):
    set_factories_session(session)

    shipment = ShipmentFactory()
    session.add(shipment)
    session.commit()

    assert shipment.id is not None
    assert shipment.status == ShipmentStatus.PENDING
    assert isinstance(shipment.tracking_number, str)
    assert shipment.order is not None
    assert shipment.shipping_address is not None
    assert shipment.billing_address is not None
    assert isinstance(shipment.created_at, datetime)
    assert isinstance(shipment.updated_at, datetime)


def test_shipment_status_enum(session):
    set_factories_session(session)

    for status in ShipmentStatus:
        shipment = ShipmentFactory(status=status)
        session.add(shipment)
        session.commit()
        assert shipment.status == status


def test_shipment_timestamps(session):
    set_factories_session(session)

    shipment = ShipmentFactory()
    session.add(shipment)
    session.commit()

    assert shipment.created_at <= datetime.now(timezone.utc)
    assert shipment.updated_at <= datetime.now(timezone.utc)


@pytest.mark.parametrize("invalid_status", ["invalid", None])
def test_shipment_invalid_status_raises(session, invalid_status):
    set_factories_session(session)

    with pytest.raises(ValueError):
        ShipmentFactory(status=invalid_status)


def test_shipment_tracking_number_required(session):
    set_factories_session(session)

    with pytest.raises(Exception):
        ShipmentFactory(tracking_number=None)
