import pytest

from app.models import Address
from tests.models_factory import AddressFactory, UserFactory

EXPECTED_ADDRESS_COUNT = 2


def test_multiple_addresses_for_same_user(session):
    UserFactory._meta.sqlalchemy_session = session
    AddressFactory._meta.sqlalchemy_session = session

    user = UserFactory()

    address1 = AddressFactory(
        user=user,
        street="Rua 1",
        city="Cidade 1",
        state="Estado 1",
        country="País 1",
        postal_code="00000-000",
        is_default_shipping=True,
        is_default_billing=False,
    )
    address2 = AddressFactory(
        user=user,
        street="Rua 2",
        city="Cidade 2",
        state="Estado 2",
        country="País 2",
        postal_code="11111-111",
        is_default_shipping=False,
        is_default_billing=True,
    )

    assert address1.user_id == address2.user_id
    addresses = session.query(Address).filter_by(user_id=user.id).all()
    assert len(addresses) == EXPECTED_ADDRESS_COUNT


@pytest.mark.parametrize(
    "missing_field", ["street", "city", "state", "country", "postal_code"]
)
def test_missing_required_fields_raises_error(session, missing_field):
    UserFactory._meta.sqlalchemy_session = session
    AddressFactory._meta.sqlalchemy_session = session

    user = UserFactory()

    base_data = {
        "user": user,
        "street": "Rua A",
        "city": "Cidade A",
        "state": "Estado A",
        "country": "País A",
        "postal_code": "00000-000",
    }

    base_data[missing_field] = None

    with pytest.raises(ValueError, match=f"{missing_field} is required"):
        AddressFactory(**base_data)
