import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Category
from tests.models_factory import CategoryFactory


def test_category_creation(session):
    CategoryFactory._meta.sqlalchemy_session = session
    category = CategoryFactory(name="Vestuário", description="Produtos eletrônicos")
    session.add(category)
    session.commit()

    assert category.id is not None
    assert category.name == "Vestuário"
    assert category.description == "Produtos eletrônicos"

    db_category = session.query(Category).filter_by(name="Vestuário").first()
    assert db_category is not None
    assert db_category.name == "Vestuário"


def test_category_name_unique_constraint(session):
    CategoryFactory._meta.sqlalchemy_session = session

    category1 = CategoryFactory(name="Eletrônicos")
    session.add(category1)
    session.commit()

    duplicate = Category(name="Eletrônicos", description="Outro desc")
    session.add(duplicate)

    with pytest.raises(
        IntegrityError, match="duplicate key value violates unique constraint"
    ):
        session.commit()

    session.rollback()


def test_category_name_too_short():
    with pytest.raises(ValueError, match="Name must be between"):
        Category(name="A", description="Curta demais")


def test_category_description_too_long():
    long_description = "A" * 300
    with pytest.raises(ValueError, match="Description must be at most"):
        Category(name="Descrição Teste", description=long_description)


@pytest.mark.parametrize("valid_name", ["AB", "A" * 255])
def test_category_name_length_limits(session, valid_name):
    CategoryFactory._meta.sqlalchemy_session = session
    category = CategoryFactory(name=valid_name)
    session.commit()

    assert category.name == valid_name


def test_category_description_optional(session):
    CategoryFactory._meta.sqlalchemy_session = session
    category = CategoryFactory(description=None)
    session.commit()

    assert category.description is None
