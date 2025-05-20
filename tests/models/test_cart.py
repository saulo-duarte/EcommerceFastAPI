from app.models.cart import Cart
from tests.models_factory import CartFactory, set_factories_session


def test_cart_creation(session):
    set_factories_session(session)

    cart = CartFactory()
    session.add(cart)
    session.commit()

    assert cart.id is not None
    assert cart.user is not None
    assert cart.is_active is True
    assert cart.is_checked_out is False

    db_cart = session.query(Cart).filter_by(id=cart.id).first()
    assert db_cart is not None
    assert db_cart.user_id == cart.user.id


def test_cart_is_active_and_checked_out_flags(session):
    set_factories_session(session)

    cart = CartFactory(is_active=False, is_checked_out=True)
    session.add(cart)
    session.commit()

    assert cart.is_active is False
    assert cart.is_checked_out is True
