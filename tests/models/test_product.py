import uuid

import pytest

from app.models import Product
from tests.models_factory import ProductFactory, set_factories_session

TEST_PRODUCT_PRICE = 2499.90


def test_product_creation(session):
    set_factories_session(session)

    product = ProductFactory(
        name="Smartphone X",
        description="High-end smartphone with 128GB storage",
        price=TEST_PRODUCT_PRICE,
        stock=0,
        is_active=True,
    )
    session.add(product)
    session.commit()

    assert product.id is not None
    assert product.name == "Smartphone X"
    assert product.price == TEST_PRODUCT_PRICE
    assert product.stock == 0
    assert product.is_active is True

    db_product = session.query(Product).filter_by(name="Smartphone X").first()
    assert db_product is not None
    assert db_product.price == TEST_PRODUCT_PRICE


def test_product_name_too_short_raises():
    with pytest.raises(ValueError, match="Name must be between"):
        Product(name="A", price=10.0, stock=1, category_id=uuid.uuid4())


def test_product_name_too_long_raises():
    long_name = "A" * 300
    with pytest.raises(ValueError, match="Name must be between"):
        Product(name=long_name, price=10.0, stock=1, category_id=uuid.uuid4())


def test_product_price_must_be_positive():
    with pytest.raises(ValueError, match="Price must be positive"):
        Product(name="Valid Name", price=0, stock=1, category_id=uuid.uuid4())
    with pytest.raises(ValueError, match="Price must be positive"):
        Product(name="Valid Name", price=-5, stock=1, category_id=uuid.uuid4())


def test_product_stock_cannot_be_negative():
    with pytest.raises(ValueError, match="Stock must be non-negative"):
        Product(name="Valid Name", price=10.0, stock=-1, category_id=uuid.uuid4())
