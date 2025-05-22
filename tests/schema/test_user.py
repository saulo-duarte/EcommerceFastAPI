from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.models.value_objects import Password
from app.schema.user import UserCreate, UserRead, UserUpdate


def test_user_create_valid():
    password = Password(raw="Valid1@Password")
    user = UserCreate(
        email="user@example.com",
        full_name=" John Doe ",
        password=password
    )
    assert user.email == "user@example.com"
    assert user.full_name == "John Doe"  # deve remover espaços
    assert isinstance(user.password, Password)


def test_user_create_invalid_full_name():
    password = Password(raw="Valid1@Password")
    with pytest.raises(ValueError, match="Full name must contain only letters and spaces"):
        UserCreate(
            email="user@example.com",
            full_name="John123",
            password=password
        )


def test_user_update_partial():
    update = UserUpdate(
        full_name="  Jane Smith  ",
        is_active=False
    )
    assert update.full_name == "Jane Smith"
    assert update.is_active is False


def test_user_update_invalid_full_name():
    with pytest.raises(ValueError, match="Full name must contain only letters and spaces"):
        UserUpdate(full_name="Invalid123!")


def test_user_read_model():
    user_read = UserRead(
        id=uuid4(),
        email="read@example.com",
        full_name="Read User",
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        addresses=[]
    )
    assert user_read.full_name == "Read User"
    assert user_read.is_active is True
    assert isinstance(user_read.created_at, datetime)
    assert isinstance(user_read.addresses, list)
