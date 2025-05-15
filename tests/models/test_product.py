import uuid
from datetime import datetime, timezone

from app.models import Category, Product

TEST_PRODUCT_PRICE = 2499.90
TEST_PRODUCT_STOCK = 10


def test_product_creation(session):
    category = Category(
        id=uuid.uuid4(),
        name="Smartphones",
        description="Categoria para celulares",
        created_at=datetime.now(timezone.utc),
    )
    session.add(category)
    session.commit()

    product = Product(
        name="Smartphone X",
        description="High-end smartphone with 128GB storage",
        price=TEST_PRODUCT_PRICE,
        stock=10,
        is_active=True,
        category_id=category.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(product)
    session.commit()

    assert product.id is not None
    assert product.name == "Smartphone X"
    assert product.price == TEST_PRODUCT_PRICE
    assert product.stock == TEST_PRODUCT_STOCK
    assert product.is_active is True

    db_product = session.query(Product).filter_by(name="Smartphone X").first()
    assert db_product is not None
    assert db_product.price == TEST_PRODUCT_PRICE
