import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.models.payment import Payment, PaymentMethod, PaymentStatus
from tests.models_factory import PaymentFactory, set_factories_session

AMOUNT_IN_CENTS = 10000

def test_payment_creation(session):
    set_factories_session(session)

    payment = PaymentFactory()
    session.add(payment)
    session.commit()

    assert payment.id is not None
    assert payment.amount == Decimal("100.00")
    assert payment.currency == "brl"
    assert payment.status == PaymentStatus.PENDING
    assert payment.method == PaymentMethod.CREDIT_CARD
    assert isinstance(payment.created_at, datetime)
    assert isinstance(payment.updated_at, datetime)
    assert payment.amount_in_cents == AMOUNT_IN_CENTS


@pytest.mark.parametrize("invalid_amount", [Decimal("0"), Decimal("-10")])
def test_payment_invalid_amount_raises(invalid_amount):
    with pytest.raises(ValueError, match="amount must be positive"):
        Payment(
            order_id=uuid.uuid4(),
            amount=invalid_amount,
            currency="brl",
            status=PaymentStatus.PENDING,
            method=PaymentMethod.CREDIT_CARD,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )


@pytest.mark.parametrize("invalid_status", ["invalid", None])
def test_payment_invalid_status_raises(invalid_status):
    with pytest.raises(ValueError, match=r"Invalid payment status: .*"):
        Payment(
            order_id=uuid.uuid4(),
            amount=Decimal("100.00"),
            currency="brl",
            status=invalid_status,
            method="credit_card",
        )


@pytest.mark.parametrize("invalid_method", ["invalid", None])
def test_payment_invalid_method_raises(invalid_method):
    with pytest.raises(ValueError, match=r"Invalid payment method: .*"):
        Payment(
            order_id=uuid.uuid4(),
            amount=Decimal("50.00"),
            status=PaymentStatus.PENDING,
            method=invalid_method,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
