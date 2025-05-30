from datetime import timedelta

import pytest
from faker import Faker
from fastapi import HTTPException

from app.security.security import create_access_token, verify_access_token

fake = Faker()

TEST_SECRET = "testsecretkey123"


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", TEST_SECRET)
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")


def test_should_return_jwt_token_when_valid_payload_is_provided():
    user_id = fake.uuid4()
    payload = {"sub": user_id}

    token = create_access_token(payload)

    assert isinstance(token, str)
    assert token.count(".") == 2


def test_should_extract_user_id_from_valid_token():
    user_id = fake.uuid4()
    token = create_access_token({"sub": user_id})

    extracted_id = verify_access_token(token)

    assert extracted_id == user_id


def test_should_raise_exception_when_token_is_malformed():
    malformed_token = "abc.def.ghi"

    with pytest.raises(HTTPException) as error:
        verify_access_token(malformed_token)

    assert error.value.status_code == 401
    assert "Invalid credentials" in error.value.detail


def test_should_raise_exception_when_token_is_expired():
    user_id = fake.uuid4()
    token = create_access_token({"sub": user_id}, expires_delta=timedelta(seconds=-10))

    with pytest.raises(HTTPException) as error:
        verify_access_token(token)

    assert error.value.status_code == 401


def test_should_generate_unique_tokens_for_different_users():
    user_1 = fake.uuid4()
    user_2 = fake.uuid4()

    token_1 = create_access_token({"sub": user_1})
    token_2 = create_access_token({"sub": user_2})

    assert token_1 != token_2
