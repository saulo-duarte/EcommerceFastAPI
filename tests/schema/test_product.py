import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.schema.category import CategoryRead
from app.schema.product import ProductCreate, ProductRead, ProductUpdate


def test_product_create_valid():
    data = {
        "name": " Smartphone ",
        "description": " A cool device ",
        "stock": 10,
        "price": 999.99,
        "category_id": uuid.uuid4(),
        "is_active": True
    }
    product = ProductCreate(**data)
    assert product.name == "Smartphone"
    assert product.description == "A cool device"
    assert product.stock == 10
    assert product.price == 999.99
    assert product.is_active is True


def test_product_create_invalid_name_too_short():
    data = {
        "name": "A",
        "stock": 5,
        "price": 100,
        "category_id": uuid.uuid4()
    }
    with pytest.raises(ValueError):
        ProductCreate(**data)


def test_product_create_invalid_description_too_short():
    data = {
        "name": "Valid Name",
        "description": "A",
        "stock": 5,
        "price": 100,
        "category_id": uuid.uuid4()
    }
    with pytest.raises(ValueError, match="Description must be at least 2 characters"):
        ProductCreate(**data)


def test_product_create_negative_stock():
    data = {
        "name": "Valid Name",
        "stock": -1,
        "price": 100,
        "category_id": uuid.uuid4()
    }
    with pytest.raises(ValueError):
        ProductCreate(**data)


def test_product_create_negative_price():
    data = {
        "name": "Valid Name",
        "stock": 10,
        "price": -10.5,
        "category_id": uuid.uuid4()
    }
    with pytest.raises(ValueError):
        ProductCreate(**data)


def test_product_update_partial():
    data = {
        "name": " New Name ",
        "description": " New Description ",
        "stock": 20,
        "price": 150.0,
        "is_active": False
    }
    update = ProductUpdate(**data)
    assert update.name == "New Name"
    assert update.description == "New Description"
    assert update.stock == 20
    assert update.price == 150.0
    assert update.is_active is False


def test_product_update_invalid_description_too_short():
    data = {"description": "A"}
    with pytest.raises(ValidationError) as exc_info:
        ProductUpdate(**data)
    assert "String should have at least 2 characters" in str(exc_info.value)


def test_product_update_negative_price():
    data = {"price": -1}
    with pytest.raises(ValueError):
        ProductUpdate(**data)


def test_product_read_model():
    category = CategoryRead(
        id=uuid.uuid4(),
        name="Electronics",
        description="Devices",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    product = ProductRead(
        id=uuid.uuid4(),
        name="Laptop",
        description="Gaming laptop",
        stock=5,
        price=2000.00,
        is_active=True,
        category=category,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    assert product.name == "Laptop"
    assert product.category.name == "Electronics"
    assert isinstance(product.created_at, datetime)
