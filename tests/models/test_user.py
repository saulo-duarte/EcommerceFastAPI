import pytest
from app.models import User
from datetime import datetime, timezone

def test_user_creation(session):
    user = User(
        email="testuser@example.com",
        hashed_password="hashedpassword123",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    session.add(user)
    session.commit()

    assert user.id is not None
    assert user.email == "testuser@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
    assert user.is_superuser is False

    db_user = session.query(User).filter_by(email="testuser@example.com").first()
    assert db_user is not None
    assert db_user.email == "testuser@example.com"
    assert db_user.full_name == "Test User"


def test_user_email_uniqueness(session):
    user1 = User(
        email="duplicate@example.com",
        hashed_password="password1",
        full_name="User One"
    )
    user2 = User(
        email="duplicate@example.com",
        hashed_password="password2",
        full_name="User Two"
    )

    session.add(user1)
    session.commit()

    with pytest.raises(Exception):
        session.add(user2)
        session.commit()
