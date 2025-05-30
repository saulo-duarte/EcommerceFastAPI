import uuid
from datetime import datetime, timezone

import pytest

from app.schema.product import ProductRead
from app.schema.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.schema.user import UserRead


def test_review_create_valid():
    data = {
        "rating": 4.5,
        "comment": "Ótimo produto!",
        "product_id": uuid.uuid4(),
        "user_id": uuid.uuid4(),
    }
    review = ReviewCreate(**data)
    assert review.rating == 4.5
    assert review.comment == "Ótimo produto!"


def test_review_create_invalid_rating_low():
    data = {
        "rating": 0.5,
        "comment": "Ruim",
        "product_id": uuid.uuid4(),
        "user_id": uuid.uuid4(),
    }
    with pytest.raises(ValueError) as exc_info:
        ReviewCreate(**data)
    assert "greater than or equal" in str(exc_info.value)


def test_review_create_invalid_rating_high():
    data = {
        "rating": 6.0,
        "comment": "Excelente demais",
        "product_id": uuid.uuid4(),
        "user_id": uuid.uuid4(),
    }
    with pytest.raises(ValueError) as exc_info:
        ReviewCreate(**data)
    assert "less than or equal" in str(exc_info.value)


def test_review_create_comment_too_long():
    data = {
        "rating": 4.0,
        "comment": "A" * 1001,
        "product_id": uuid.uuid4(),
        "user_id": uuid.uuid4(),
    }
    with pytest.raises(ValueError) as exc_info:
        ReviewCreate(**data)
    assert "1000" in str(exc_info.value)


def test_review_update_partial_valid():
    update = ReviewUpdate(rating=3.5, comment="Bom")
    assert update.rating == 3.5
    assert update.comment == "Bom"


def test_review_update_invalid_rating():
    with pytest.raises(ValueError) as exc_info:
        ReviewUpdate(rating=10)
    assert "less than or equal" in str(exc_info.value)


def test_review_read_model():
    product = ProductRead(
        id=uuid.uuid4(),
        name="Notebook",
        description="Bom para estudar",
        stock=10,
        price=1500.0,
        is_active=True,
        category={
            "id": uuid.uuid4(),
            "name": "Eletrônicos",
            "description": "Produtos eletrônicos",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    user = UserRead(
        id=uuid.uuid4(),
        email="user@example.com",
        full_name="João da Silva",
        is_active=True,
        is_superuser=False,
        addresses=[],
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    review = ReviewRead(
        id=uuid.uuid4(),
        product_id=product.id,
        user_id=user.id,
        rating=5.0,
        comment="Excelente!",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        product=product,
        user=user,
    )

    assert review.rating == 5.0
    assert review.comment == "Excelente!"
    assert review.product.name == "Notebook"
    assert review.user.full_name == "João da Silva"
