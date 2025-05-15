from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Category


def test_category_creation(session):
    category = Category(
        name="Eletrônicos",
        description="Produtos eletrônicos em geral",
        created_at=datetime.now(timezone.utc),
    )

    session.add(category)
    session.commit()

    assert category.id is not None
    assert category.name == "Eletrônicos"
    assert category.description == "Produtos eletrônicos em geral"

    db_category = session.query(Category).filter_by(name="Eletrônicos").first()
    assert db_category is not None
    assert db_category.name == "Eletrônicos"


def test_category_name_is_required(session):
    category = Category(
        name=None,
        description="Categoria sem nome",
        created_at=datetime.now(timezone.utc),
    )

    session.add(category)
    with pytest.raises(IntegrityError):
        session.commit()


def test_category_name_is_unique(session):
    category1 = Category(
        name="Livros",
        description="Categoria de livros",
        created_at=datetime.now(timezone.utc),
    )
    category2 = Category(
        name="Livros",
        description="Outro nome duplicado",
        created_at=datetime.now(timezone.utc),
    )

    session.add(category1)
    session.commit()

    session.add(category2)
    with pytest.raises(IntegrityError):
        session.commit()
