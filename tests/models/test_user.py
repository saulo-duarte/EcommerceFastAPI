from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import User
from tests.models_factory import UserFactory


def test_user_creation(session):
    UserFactory._meta.sqlalchemy_session = session
    user = UserFactory(full_name="Test User")
    db_user = session.query(User).filter_by(email=user.email).first()

    assert db_user is not None
    assert db_user.email == user.email
    assert db_user.full_name == "Test User"
    assert db_user.is_active is True
    assert db_user.is_superuser is False


def test_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email address"):
        User(email="invalid-email", hashed_password="StrongP@ssw0rd!")


def test_user_password_strength():
    weak_passwords = [
        "short",
        "alllowercase1!",
        "ALLUPPERCASE1!",
        "NoDigits!",
        "NoSpecial123",
    ]
    for pwd in weak_passwords:
        with pytest.raises(
            ValueError,
            match=(
                "Password must be at least 8 characters long and "
                "include at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character."
            ),
        ):
            User(email="user@example.com", hashed_password=pwd)


def test_user_missing_required_fields(session):
    incomplete_user = User(hashed_password="StrongP@ssw0rd!")
    session.add(incomplete_user)

    with pytest.raises(
        IntegrityError, match=r"null value in column .* violates not-null constraint"
    ):
        session.commit()


def test_user_duplicate_email(session):
    UserFactory._meta.sqlalchemy_session = session
    user = UserFactory()
    duplicate = User(
        email=user.email,
        hashed_password="StrongP@ssw0rd!",
        full_name="Duplicate",
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(duplicate)
    with pytest.raises(
        IntegrityError, match="duplicate key value violates unique constraint"
    ):
        session.commit()
