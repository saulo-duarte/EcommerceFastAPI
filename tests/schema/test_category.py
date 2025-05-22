import uuid
from datetime import datetime, timezone

import pytest

from app.schema.category import CategoryCreate, CategoryRead, CategoryUpdate


def test_category_create_valid():
    data = {
        "name": " Electronics ",
        "description": " Devices and gadgets "
    }
    category = CategoryCreate(**data)
    assert category.name == "Electronics"
    assert category.description == "Devices and gadgets"


def test_category_create_invalid_empty_name():
    data = {
        "name": "   ",
        "description": "Some description"
    }
    with pytest.raises(ValueError, match="Field cannot be empty or whitespace only."):
        CategoryCreate(**data)


def test_category_create_invalid_empty_description():
    data = {
        "name": "Books",
        "description": "  "
    }
    with pytest.raises(ValueError, match="Field cannot be empty or whitespace only."):
        CategoryCreate(**data)


def test_category_update_valid():
    data = {
        "name": " Updated Name ",
        "description": " Updated Description "
    }
    update = CategoryUpdate(**data)
    assert update.name == "Updated Name"
    assert update.description == "Updated Description"


def test_category_update_partial_none():
    update = CategoryUpdate()
    assert update.name is None
    assert update.description is None


def test_category_update_invalid_empty_name():
    data = {"name": " "}
    with pytest.raises(ValueError, match="Field cannot be empty or whitespace only."):
        CategoryUpdate(**data)


def test_category_update_invalid_empty_description():
    data = {"description": " "}
    with pytest.raises(ValueError, match="Field cannot be empty or whitespace only."):
        CategoryUpdate(**data)


def test_category_read_model():
    category = CategoryRead(
        id=uuid.uuid4(),
        name="Books",
        description="All kinds of books",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    assert category.name == "Books"
    assert isinstance(category.created_at, datetime)
    assert isinstance(category.updated_at, datetime)
